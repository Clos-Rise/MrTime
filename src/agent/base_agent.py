# Базовый класс для агента

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAgent(ABC):
    """
    базовый класс для всех агентов.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        просто базовые кварги

        """
        self.model_name = model_name
    @abstractmethod
    def decide(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Основной метод
        Он обращается к LLM и возвращает ее ответ.

        :param messages: История сообщений в формате OpenAI.
        :param tools: Список инструментовб доступных модели.
        :return: Ответ от модели. Может содержать:
                 - текстовый ответ
                 - вызов инструмента (tool_calls).
        """
        pass