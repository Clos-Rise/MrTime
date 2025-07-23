# agent/devstral_agent.py
from typing import List, Dict, Any
from openai import OpenAI
from .base_agent import BaseAgent


class DevstralAgent(BaseAgent):
    """
        Агент Devstral
    """

    def __init__(self, model_name: str = "mistralai/devstral-small-2505:free", api_key: str = "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"):
        """
            Клиент OpenAI.
        """
        super().__init__(model_name)

        self.api_key = api_key

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def decide(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Отправляет запрос.
        """
        try:
            # Параметры
            request_params = {
                "model": self.model_name,
                "messages": messages,
            }
            if tools:
                request_params["tools"] = tools
                request_params["tool_choice"] = "auto"


            completion = self.client.chat.completions.create(**request_params)
            return completion.choices[0].message

        except Exception as e:
            print(e)