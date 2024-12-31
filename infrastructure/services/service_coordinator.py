import json
import logging
import asyncio
import time
from infrastructure.models import Conversation
from infrastructure.repositories.chat_manager import ChatManager
from infrastructure.repositories.memory_manager import MemoryManager
from infrastructure.services.llm_api.llm_api import LLMService
from config import DEFAULT_MEM_PROMPT, INITIAL_PROMPT, DEFAULT_CONVO_SUM_PROMPT

class Coordinator:
    def __init__(self):
        self.llm_service = LLMService()
        self.chat_manager = ChatManager()
        self.mem_manager = MemoryManager()
        self.last_activity_time = time.time()
        self.activity_lock = asyncio.Lock()
        self.cur_user =""
        self.last_response = None
        logging.info('Coordinator Initialized')

    async def set_user(self,name:str=None):
        self.cur_user=name
        self.chat_manager.add_message(role='system',content=f"Current User: {self.cur_user}")

    async def update_last_activity(self):
        """Update the last activity timestamp in a thread-safe manner."""
        async with self.activity_lock:
            logging.info('updating last activity')
            self.last_activity_time = time.time()

    async def monitor_inactivity(self, inactivity_limit_minutes: int = 5):
        """Continuously monitor for inactivity and trigger an action upon timeout."""
        inactivity_limit_seconds = inactivity_limit_minutes * 60
        logging.debug("Starting inactivity monitor...")
        while True:
            async with self.activity_lock:
                elapsed_time = time.time() - self.last_activity_time
            if elapsed_time >= inactivity_limit_seconds:
                logging.info(f"Inactivity for {elapsed_time / 60:.2f} minutes detected. Triggering save_current_start_new.")
                await self.save_current_start_new()
                # Reset last activity to avoid immediate re-trigger
                await self.update_last_activity()
            await asyncio.sleep(15)

    async def _summarize_memories(self, prompt: str = DEFAULT_MEM_PROMPT, content: str = ""):
        if content.strip() == "":
            content = str(await self.mem_manager.get_all_memories())
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
        async for response in self.llm_service.send_completion(messages=messages, stream=False):
            return response

    async def build_system_instructions(self, refresh:bool = False):
        if refresh:
            self.mem_manager.load_memories()
        recap = await self._summarize_memories()
        identity = self.mem_manager.get_identity()
        self.chat_manager.add_message(
            role='system',
            content=f"Your name is {identity['name']} {INITIAL_PROMPT} {recap} {identity}"
        )
        self.chat_manager.add_message(
            role='system',
            content=f"{self.mem_manager.misc_details_collection}"
        )
        return self.chat_manager.get_transcript()

    async def user_to_completion(self, message: str, role: str ='user'):
        """Process a user message and yield the assistant's streamed response."""
        if role == 'user':
            self.chat_manager.add_message(
                role='system',
                content=f"Current time:{time.strftime('%a, %d %b %Y %I:%M:%S %p', time.localtime())} CST Location:Montgomery, TX 77356"
            )
        self.chat_manager.add_message(role=role, content=message)
        logging.debug("User prompt stored in chat log.")
        async for chunk in self._stream_completion():
            yield chunk
        if LLMService.last_response.get('tool_call_id'):
            async for chunk in self._tool_completion(LLMService.last_response):
                yield chunk

    async def _stream_completion(self):
        response = None
        async for chunk in self.llm_service.send_completion(messages=self.chat_manager.get_transcript(), stream=True):
            response = chunk['message']
            yield str(chunk['chunk'])
        LLMService.last_response = json.loads(response)
        logging.debug(f"Response ~ {LLMService.last_response}")
        self.chat_manager.add_response(LLMService.last_response)
        logging.debug("Assistant response stored in chat log.")

    async def _tool_completion(self,tool_response):
        content = dict(type='text', text='{"status\":"success\"}')
        self.chat_manager.add_response(dict(role='tool', tool_call_id=tool_response.get('tool_call_id'), content=[content]))
        async for chunk in self._stream_completion():
            yield chunk


    async def create_conversation(self):
        self.chat_manager.load_transcript()
        transcript = str(self.chat_manager.get_transcript(trimmed=True))
        if transcript != "[]":
            response = await self._summarize_memories(prompt=DEFAULT_CONVO_SUM_PROMPT, content=transcript)
            convo = Conversation(transcript=transcript, summary=response)
            self.mem_manager.add_memory(convo)
            return convo
        else:
            return

    async def save_current_start_new(self):
        logging.info('auto save started')
        logging.info("attempting Storing current conversation into memory and starting a new one.")
        conversation = await self.create_conversation()
        if conversation:
            self.chat_manager.clear_transcript()
            await self.build_system_instructions(refresh=True)
            logging.info("save_current_start_new complete")
        else:
            logging.info("no conversation to clear")
        logging.info('\rauto save complete')

    async def save_current(self):
        print('Saving', end='', flush=True)
        logging.info("attempting Storing current conversation into memory")
        await self.create_conversation()
        print('\rSession SAVED')


    async def system_start_up(self):
        logging.info("Running system startup...")
        await self.build_system_instructions()
        logging.info('initial payload complete')
        logging.info("System instructions built.")

        # Start background inactivity monitoring
        asyncio.create_task(self.monitor_inactivity(inactivity_limit_minutes=3))
        logging.info("Inactivity monitoring task started.")
