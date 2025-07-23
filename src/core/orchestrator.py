import json
from typing import List, Dict, Any
from agent.base_agent import BaseAgent


class Orchestrator:
    """
    Весь цикл здесь: пользователь -> агент -> инструменты -> агент -> пользователь.
    """

    def __init__(self, agent: BaseAgent, tools: List[Any]):
        self.agent = agent
        self.tools = {tool.name: tool for tool in tools}
        self.tool_schemas = [tool.get_schema() for tool in tools]

    def process_request(self, user_prompt: str, conversation_history: List[Dict] = None) -> str:
        
        if conversation_history is None:
            conversation_history = []

        conversation_history.append({"role": "user", "content": user_prompt})

        max_turns = 5  

        for _ in range(max_turns):
            try:
                # 1. Получаем решение от агента (это объект Pydantic)
                assistant_response_obj = self.agent.decide(conversation_history, self.tool_schemas)
            except Exception as e:
                print(f"[Оркестратор] поймал исключение от агента: {e}")
                return f"К сожалению, произошла [Ошибка] при обращении к AI-модели. (Детали: {e})"

            # Проверяем, есть ли запрос на вызов инструментов
            if not assistant_response_obj.tool_calls:
                # Если нет, значит это финальный ответ
                final_answer = assistant_response_obj.content
                print(f"[Оркестратор]: Финальный ответ получен: {final_answer}")
                return final_answer

            # 2. Если есть tool_calls, добавляем сообщение ассистента в историю в правильном формате
            # Создаем словарь вручную для полной уверенности в формате
            assistant_message_dict = {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    } for call in assistant_response_obj.tool_calls
                ]
            }
            conversation_history.append(assistant_message_dict)

            print(f"[Оркестратор]: Агент запросил вызов инструментов: {assistant_response_obj.tool_calls}")

            for tool_call in assistant_response_obj.tool_calls:
                tool_name = tool_call.function.name

                if tool_name in self.tools:
                    tool_to_run = self.tools[tool_name]
                    try:
                        tool_args = json.loads(tool_call.function.arguments)
                        result = tool_to_run.execute(**tool_args)
                        print(f"[Оркестратор]: Инструмент '{tool_name}' вернул результат.")
                    except Exception as e:
                        result = f"[Ошибка] при выполнении инструмента {tool_name}: {e}"
                        print(f"[Оркестратор]: {result}")

                    
                    conversation_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": str(result),
                    })
                else:
                    print(f"[Оркестратор]: Модель запросила несуществующий инструмент '{tool_name}'.")
                    conversation_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": f"[Ошибка]: инструмент '{tool_name}' не найден.",
                    })

        return "err"