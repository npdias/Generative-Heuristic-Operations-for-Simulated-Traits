import asyncio

if __name__ == "__main__":
    # Setup basic logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    async def main():
        orchestrator = Orchestrator()

        # Start a new session
        await orchestrator.start_session()

        # Handle user input
        user_input = "Explain the concept of gravity."
        print("\nNon-Streaming Response:")
        response = await orchestrator.handle_user_input(user_input)
        print(response)

        # Handle user input with streaming
        print("\nStreaming Response:")
        async for chunk in orchestrator.handle_user_input("Describe the water cycle.", stream=True):
            print(chunk, end="", flush=True)

        # End the session
        await orchestrator.end_session()

    asyncio.run(main())
