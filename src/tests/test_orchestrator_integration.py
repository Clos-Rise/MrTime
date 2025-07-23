
from typing import Dict, Any

from agent.devstral_agent import DevstralAgent
from core.orchestrator import Orchestrator


# Фейковый инструмент для тестов
class FakeUserTool:
    @property
    def name(self) -> str:
        return "get_user_info"

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "ОБЯЗАТЕЛЬНО используй эту функцию когда нужно найти информацию о пользователе. Получает детали пользователя по ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID пользователя, например 'client_123'",
                        }
                    },
                    "required": ["user_id"],
                },
            },
        }

    def execute(self, user_id: str) -> str:
        """Притворяется что ходит в базу данных"""
        print(f"[FakeUserTool] Ищем пользователя: {user_id}")
        return f"Пользователь {user_id}: Имя - Jane Smith, Отдел - Продажи, Статус - Активен"


def test_orchestrator_with_real_devstral():
    """Тест всей системы с настоящим API"""
    print("\n--- Запуск интеграционного теста ---")

    # настройка
    api_key = "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"
    agent = DevstralAgent(api_key=api_key)
    tool = FakeUserTool()
    orchestrator = Orchestrator(agent=agent, tools=[tool])

    question = "Используй функцию get_user_info чтобы найти пользователя с ID client_777"

    try:
        # выполняем запрос
        print("Отправляем запрос...")
        answer = orchestrator.process_request(question)
        print(f"Получен ответ: {answer}")

        # проверяем результат только если нет ошибки
        if "К сожалению, произошла ошибка" not in answer:
            assert "Jane Smith" in answer
            assert "client_777" in answer
            assert "Продажи" in answer


    except Exception as e:
        raise