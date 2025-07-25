import json
from typing import List, Dict, Any
from agent.base_agent import BaseAgent


class Orchestrator:
    """
    Весь цикл здесь: пользователь -> агент -> инструменты -> агент -> пользователь.
    """

    def __init__(self, agent: BaseAgent, tools: List[Any], system_prompt: str = ""):
        self.agent = agent
        self.tools = {tool.name: tool for tool in tools}
        self.tool_schemas = [tool.get_schema() for tool in tools]
        self.system_prompt = system_prompt
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({"role": "system", "content": self.system_prompt})

    def process_request(self, user_prompt: str) -> str:

        self.conversation_history.append({"role": "user", "content": user_prompt})

        max_turns = 5
        for _ in range(max_turns):
            print(f"\n[Оркестратор] Итерация {_ + 1}. История содержит {len(self.conversation_history)} сообщений.")

            try:
                assistant_response_obj = self.agent.decide(self.conversation_history, self.tool_schemas)
            except Exception as e:
                self.conversation_history.pop()
                return f"К сожалению, произошла [Ошибка] при обращении к AI-модели: {e}"

            if not assistant_response_obj.tool_calls:
                final_answer = assistant_response_obj.content
                print(f"[Оркестратор]: Финальный ответ (без инструментов) получен: {final_answer}")
                self.conversation_history.append({"role": "assistant", "content": final_answer})
                return final_answer

            print(
                f"[Оркестратор]: Агент запросил вызов инструментов: {[call.function.name for call in assistant_response_obj.tool_calls]}")

            self.conversation_history.append(assistant_response_obj.model_dump())

            for tool_call in assistant_response_obj.tool_calls:
                tool_name = tool_call.function.name
                tool_to_run = self.tools[tool_name]
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                    result = tool_to_run.execute(**tool_args)
                    print(f"[Оркестратор]: Инструмент '{tool_name}' вернул результат.")
                    self.conversation_history.append({
                        "tool_call_id": tool_call.id, "role": "tool", "content": str(result),
                    })
                except Exception as e:
                    error_result = f"[Ошибка] при выполнении инструмента {tool_name}: {e}"
                    print(f"[Оркестратор]: {error_result}")
                    self.conversation_history.append({
                        "tool_call_id": tool_call.id, "role": "tool", "content": error_result,
                    })

        return "[Ошибка]"