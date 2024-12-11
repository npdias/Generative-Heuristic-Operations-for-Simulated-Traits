## This needs to be collapsed into Memory

class MemoryHandler:

    def __init__(self):
        self.memory_repository = Memory()
        self.llm_service = LLMService()

    async def load_memories(self):
        await self.memory_repository.load_memories()

    async def summarize_all_memories(self):
        # Query LLM for summary
        messages = [
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": f"Summarize the following memories and conversation:\n\n{Memory.all_memories}"}
        ]
        summary = ""
        async for chunk in self.llm_service.send_completion(messages, stream=False):
            summary += chunk
        return summary


    async def summarize_chat(self, transcript):
        # Query LLM for summary
        messages = [
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": f"Summarize this conversation:\n\n{transcript}"}
        ]
        summary = ""
        async for chunk in self.llm_service.send_completion(messages, stream=False):
            summary += chunk
        # Return the summary and transcript
        Conversation(**{"summary": summary, "transcript": transcript})
        await self.memory_repository.save_memories()
        print(Memory.all_memories)

    @staticmethod
    def update_self(**kwargs):
        cur_self = Memory.identity
        for key, value in kwargs.items():
            if key not in ['relation', 'isSelf']:
                # Log the change as an event and update the memory
                Event(note=f'My {key} changed from "{getattr(cur_self, key)}" to "{value}"')
                setattr(cur_self, key, value)

    async def get_self(self):
        if Memory.identity is None:
            cur_self = Person(name='', relation='self')
            self.update_self(alive=True)
        else:
            pass
        print(Memory.identity.__str__)