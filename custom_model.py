from typing import Any, Dict, Optional, List
import requests
import json
from pydantic import BaseModel
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk


class hyperclovax(LLM):
    """
    Custom LLM class for using the hyperclovax API.
    """
    host: str
    api_key: str
    api_key_primary_val: str
    request_id: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.host = host
        # self.api_key = api_key
        # self.api_key_primary_val = api_key_primary_val
        # self.request_id = request_id

    @property
    def _llm_type(self) -> str:
        return "hyperclovax"

    def _call(
        self,
        prompt: Dict[str, Any],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:

        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self.api_key,
            'X-NCP-APIGW-API-KEY': self.api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self.request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }
        
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        response = requests.post(
            f"{self.host}/testapp/v1/chat-completions/HCX-DASH-001",
            headers=headers,
            json=prompt,
        )

        response.raise_for_status()  # Raises an error for bad status codes

        for line in response.iter_lines():
            if line:
                res = line.decode("utf-8")
                res = json.loads(res)
                res = res['result']['message']

        return res

# # Example usage
# hyperclovax_instance = hyperclovax(
#     host='https://clovastudio.stream.ntruss.com',
#     api_key='NTA0MjU2MWZlZTcxNDJiYxrm80PYC0F2nPTOcfcl6q+St7u/ykmVS25U0nuONAIC',
#     api_key_primary_val='fb8TL0kwYo5Mz8XWy0jwNuIpHmEiAqIjxkesYjnU',
#     request_id='8507dde5-9fff-45d6-ac49-3a8364f69291'
# )
# response = hyperclovax_instance._call(payload={"prompt": "Hello, how are you?"})
# print(response)


# Example usage
# hyperclovax_instance = hyperclovax(host="https://api.hyperclovax.com", api_key="your_api_key", api_key_primary_val="your_api_key_primary_val", request_id="your_request_id")
# response = hyperclovax_instance._call(payload={"prompt": "Hello, how are you?"})



    # def _stream(
    #     self,
    #     prompt: str,
    #     stop: Optional[List[str]] = None,
    #     run_manager: Optional[CallbackManagerForLLMRun] = None,
    #     **kwargs: Any,
    # ) -> Iterator[GenerationChunk]:
    #     for char in prompt[: self.n]:
    #         chunk = GenerationChunk(text=char)
    #         if run_manager:
    #             run_manager.on_llm_new_token(chunk.text, chunk=chunk)

    #         yield chunk

    # @property
    # def _identifying_params(self) -> Dict[str, Any]:
    #     """Return a dictionary of identifying parameters."""
    #     return {
    #         # The model name allows users to specify custom token counting
    #         # rules in LLM monitoring applications (e.g., in LangSmith users
    #         # can provide per token pricing for their model and monitor
    #         # costs for the given LLM.)
    #         "model_name": "CustomChatModel",
    #     }

    # @property
    # def _llm_type(self) -> str:
    #     """Get the type of language model used by this chat model. Used for logging purposes only."""
    #     return "custom"