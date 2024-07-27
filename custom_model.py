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