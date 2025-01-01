import os
from infrastructure.services.llm_api.llm_tools_config import tools
import logging
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv
from dataclasses import dataclass, field

from infrastructure.models.message import Content, Message, ToolCall, ToolFunction


# Load environment variables
load_dotenv()


@dataclass
class LLMService:

    model: str = os.getenv("GPT_MODEL")
    client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    last_response: any = field(kw_only=True, default=None)

    @staticmethod
    async def send_completion(messages: List[Dict[str, str]], stream: bool = False):
        try:
            logging.info("Preparing to send completion request to LLM.")
            logging.debug("Model: %s, Streaming: %s", LLMService.model, stream)
            logging.debug("Messages: %s", messages)
            logging.info(f"Sending request {'in streaming mode.' if stream else '.'}")
            response = LLMService.client.chat.completions.create(
                model=LLMService.model,
                messages=messages,
                stream=stream,
                tools=tools
            )
            if stream:
                resp_content = Content(type='text', text='')
                resp_toolcall = ToolCall(id='', type='function')
                resp_function = ToolFunction(name='',arguments='')
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        logging.debug("Received stream chunk: %s", delta.content)
                        resp_content.text += delta.content
                        yield {'chunk':delta.content,'message':None}
                    if delta.tool_calls:
                        logging.debug("Received stream chunk: %s", delta.content)
                        resp_toolcall.id += delta.tool_calls[0].id if delta.tool_calls[0].id else ""
                        resp_function.name += delta.tool_calls[0].function.name if delta.tool_calls[0].function.name else ""
                        resp_function.arguments += delta.tool_calls[0].function.arguments if delta.tool_calls[0].function.arguments else ""
                if resp_toolcall.id != '':
                    resp_toolcall.function = resp_function
                    LLMService.last_response = Message(role='assistant', tool_calls=[resp_toolcall], tool_call_id=resp_toolcall.id)
                else:
                    LLMService.last_response = Message(role='assistant', content=[resp_content])
                # send collected chunks as complete response to handler for storage
                logging.debug(f"Collected Chunks: {LLMService.last_response.model_dump_json(exclude_none=True)}")
                yield {'chunk':'', 'message':LLMService.last_response.model_dump_json(exclude_none=True)}


            else:
                content = response.choices[0].message.content
                logging.debug("Received response: %s", content)
                yield content

            logging.info("Completion request processed successfully.")
        except Exception as e:
            logging.error("Error in send_completion: %s", e, exc_info=True)
            yield {'flag': 'error', 'content': f"Error: Unable to process the request. Details: {str(e)}"}
