from infrastructure.services.llm_service import LLMService
import logging

llm_service = LLMService()


if __name__ == "__main__":
    # Setup basic logging for demonstration
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Initialize the LLMService
    llm_service = LLMService()

    # Example 1: Non-Streaming Response
    messages_non_streaming = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    print("\nNon-Streaming Response:")
    non_streaming_response = llm_service.send_completion(messages_non_streaming)
    print(non_streaming_response)

    # Example 2: Streaming Response
    messages_streaming = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain how photosynthesis works in simple terms."}
    ]
    print("\nStreaming Response:")
    for chunk in llm_service.send_completion(messages_streaming, stream=True):
        print(chunk, end="", flush=True)
