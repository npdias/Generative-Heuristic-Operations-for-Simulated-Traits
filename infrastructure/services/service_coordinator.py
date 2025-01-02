import json
import asyncio
import time
from infrastructure.services.agent_functions.agentic_memory_management import function_router
from infrastructure.models import Conversation
from infrastructure.repositories.chat_manager import ChatManager
from infrastructure.repositories.memory_manager import MemoryManager
from infrastructure.services.llm_api.llm_api import LLMService
from config import DEFAULT_MEM_PROMPT, INITIAL_PROMPT, DEFAULT_CONVO_SUM_PROMPT
from infrastructure.services.logging_service import coordinator_logger

class Coordinator:
    def __init__(self):
        self.logger = coordinator_logger
        self.logger.info('Coordinator Initialization Start')
        self.llm_service = LLMService()
        self.chat_manager = ChatManager()
        self.mem_manager = MemoryManager()
        self.current_bot = self.mem_manager.get_identity()
        self.last_activity_time = time.time()
        self.activity_lock = asyncio.Lock()
        self.cur_user =""
        self.last_response = None
        self.logger.info('Coordinator Initialized')

    async def set_user(self,name:str=None):
        self.cur_user=name
        self.chat_manager.add_message(role='system',content=f"Current User: {self.cur_user}")

    async def update_last_activity(self):
        """Update the last activity timestamp in a thread-safe manner."""
        async with self.activity_lock:
            self.logger.info('updating last activity')
            self.last_activity_time = time.time()

    async def monitor_inactivity(self, inactivity_limit_minutes: int = 5):
        """Continuously monitor for inactivity and trigger an action upon timeout."""
        inactivity_limit_seconds = inactivity_limit_minutes * 60
        self.logger.debug("Starting inactivity monitor...")
        while True:
            async with self.activity_lock:
                elapsed_time = time.time() - self.last_activity_time
            if elapsed_time >= inactivity_limit_seconds:
                self.logger.info(f"Inactivity for {elapsed_time / 60:.2f} minutes detected. Triggering save_current_start_new.")
                await self.save_current_start_new()
                # Reset last activity to avoid immediate re-trigger
                await self.update_last_activity()
            await asyncio.sleep(15)

    async def _summarize_memories(self, prompt: str = DEFAULT_MEM_PROMPT, content: str = ""):
        self.logger.debug(f'summarize memories: {content}')
        if content.strip() == "":
            content = str(await self.mem_manager.get_all_memories())
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
        async for response in self.llm_service.send_completion(messages=messages, stream=False, use_tools=False):
            return response

    async def build_system_instructions(self, refresh:bool = False):
        if refresh:
            self.mem_manager.load_memories()
        recap = await self._summarize_memories()
        self.chat_manager.add_message(
            role='system',
            content=f"Your name is {self.current_bot.name} {INITIAL_PROMPT} {recap} {self.current_bot.__dict__}"
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
        self.logger.debug("User prompt stored in chat log.")
        async for chunk in self._stream_completion():
            yield chunk
        if LLMService.last_response.get('tool_call_id'):
            async for chunk in self._tool_completion(LLMService.last_response):
                yield chunk

    async def _stream_completion(self):
        response = None
        async for chunk in self.llm_service.send_completion(messages=self.chat_manager.get_transcript(), stream=True):
            response = chunk.get('message')
            yield chunk.get('chunk')
        LLMService.last_response = json.loads(response)
        self.logger.debug(f"Response ~ {LLMService.last_response}")
        self.chat_manager.add_response(LLMService.last_response)
        self.logger.debug("Assistant response stored in chat log.")

    async def _tool_completion(self,tool_response):
        tool_resp_msg =await function_router(name=tool_response['tool_calls'][0]['function']['name'],arguments= json.loads(str(tool_response['tool_calls'][0]['function']['arguments'])))
        content = dict(type='text', text=str({"response":f'{tool_resp_msg}'}))
        self.chat_manager.add_response(dict(role='tool', tool_call_id=tool_response.get('tool_call_id'), content=[content]))
        async for chunk in self._stream_completion():
            yield chunk


    async def create_conversation(self):
        self.logger.info("Attempting to create 'conversation memory")
        self.chat_manager.load_transcript()
        transcript = str(self.chat_manager.get_transcript(trimmed=True))
        self.logger.debug(f"Chat Transcript: {transcript}")
        if transcript != "[]":
            response = await self._summarize_memories(prompt=DEFAULT_CONVO_SUM_PROMPT, content=transcript)
            convo = Conversation(transcript=transcript, summary=response)
            self.mem_manager.add_memory(convo)
            self.logger.info('Conversation Summarized')
            return convo
        else:
            self.logger.warning("No transcript")
            return

    async def save_current_start_new(self):
        self.logger.info('auto save started')
        self.logger.info("attempting Storing current conversation into memory and starting a new one.")
        conversation = await self.create_conversation()
        if conversation:
            self.chat_manager.clear_transcript()
            await self.build_system_instructions(refresh=True)
            self.logger.info("save_current_start_new complete")
        else:
            self.logger.info("no conversation to clear")
        self.logger.info('\rauto save complete')

    async def save_current(self):
        print('Saving', end='', flush=True)
        self.logger.info("attempting Storing current conversation into memory")
        await self.create_conversation()
        print('\rSession SAVED')


    async def system_start_up(self):
        self.logger.info("Running system startup...")
        await self.build_system_instructions()
        self.logger.info('initial payload complete')
        self.logger.info("System instructions built.")
        self.logger.info(f"Bot Name: {self.current_bot.name}")

        # Start background inactivity monitoring
        asyncio.create_task(self.monitor_inactivity(inactivity_limit_minutes=3))
        self.logger.info("Inactivity monitoring task started.")

        return dict(status='success', bot_name=self.current_bot.name)
