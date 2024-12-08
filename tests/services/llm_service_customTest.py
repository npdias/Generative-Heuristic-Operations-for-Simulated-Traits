import pytest
from infrastructure.services.llm_service import LLMService

#The tests are totally borked up the ass on this one.. Not only is pytest being a bitch but walking through this recfactor with GPt is hellscape.. they memory holed the api in its head so it keeps using the deprecated methods.

# @pytest.mark.asyncio
# async def test_llm_service_example():
#     """
#     Example test function for the LLMService in a production-like scenario.
#     """
#     # Initialize the service with a test API key
#     llm_service = LLMService()
#
#     # Define a chat log as input
#     chat_log = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "What is the capital of France?"}
#     ]
#
#     # Call the service to get a response
#     response = await llm_service.generate_chat_response(chat_log)
#
#     # Assertions
#     assert response is not None
#     assert isinstance(response, str)
#     print("Assistant Response:", response)
