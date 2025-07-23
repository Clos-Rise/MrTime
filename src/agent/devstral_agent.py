# agent/devstral_agent.py

from typing import List, Dict, Any
from openai import OpenAI, APIError
from .base_agent import BaseAgent


class DevstralAgent(BaseAgent):
    """Агент для работы с Devstral через OpenRouter"""

    def __init__(self, model_name: str = "mistralai/devstral-small-2505:free", api_key: str = None):
        super().__init__(model_name)
        self.api_key = api_key
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def decide(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> Any:
        """Отправляет запрос к модели и получает ответ"""
        max_retries = 2 # разводка на дауна

        for attempt in range(max_retries):
            try:
                params = {
                    "model": self.model_name,
                    "messages": messages,
                }
                if tools:
                    params["tools"] = tools
                    params["tool_choice"] = "auto"

                response = self.client.chat.completions.create(**params)

                if not response or not response.choices:
                    error_msg = f"API вернул пустой ответ (попытка {attempt + 1}/{max_retries})"
                    print(error_msg)
                    if attempt == max_retries - 1:  # последняя попытка
                        raise Exception("API возвращает пустые ответы")
                    continue

                message = response.choices[0].message
                if not message:
                    error_msg = f"Сообщение пустое (попытка {attempt + 1}/{max_retries})"
                    print(error_msg)
                    if attempt == max_retries - 1:
                        raise Exception("Пустое сообщение в ответе")
                    continue

                return message

            except APIError as e:
                print(f"Ошибка API (попытка {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise e
                import time
                time.sleep(1)

            except Exception as e:
                print(f"Что-то пошло не так (попытка {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise e
                import time
                time.sleep(1)