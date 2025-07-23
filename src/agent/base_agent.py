# Базовый класс для агентов

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAgent(ABC):
    """Базовый класс для всех агентов"""

    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name

    @abstractmethod
    def decide(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Главный метод - отправляет запрос к модели и возвращает ответ

        Args:
            messages: История сообщений в формате OpenAI
            tools: Список доступных инструментов

        Returns:
            Ответ от модели (текст или вызов функции)
        """
        pass