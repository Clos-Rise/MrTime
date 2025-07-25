# Интеграционный тест 2, фулл работа редиса
import pytest
import json

from agent.devstral_agent import DevstralAgent
from core.orchestrator import Orchestrator
from integrations import redis_client


# для создания новых проектов
class CreateProjectTool:
    def __init__(self):
        self.name = "create_project"

    def get_schema(self):
        schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Создает новый проект в системе. Вызывай когда пользователь хочет начать новый проект!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "proekt_id": {"type": "string"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "stack": {"type": "string"},
                        "links": {"type": "string"}
                    },
                    "required": ["proekt_id", "name", "description", "stack", "links"]
                }
            }
        }
        return schema

    def execute(self, **params):
        print(f"Создаю проект с параметрами: {params}")
        redis_client.create_project(**params)
        project_id = params.get('proekt_id')
        return f"Ура! Проект '{project_id}' успешно создан в базе данных!" # явно не гпт коммент

# для сохранения планов проекта
class SavePlanTool:
    def __init__(self):
        self.name = "save_plan"

    def get_schema(self):
        schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Сохраняет план проекта в базу данных. Используй когда нужно записать план!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "proekt_id": {"type": "string"},
                        "plan": {"type": "object"}
                    },
                    "required": ["proekt_id", "plan"]
                }
            }
        }
        return schema

    def execute(self, **params):
        print(f"Сохраняю план: {params}")
        redis_client.save_plan(**params)
        project_id = params.get('proekt_id')
        return f"Отлично! План для проекта '{project_id}' сохранен!"


# для сохранения списка задач
class SaveTasksTool:
    def __init__(self):
        self.name = "save_tasks"

    def get_schema(self):
        schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Сохраняет список задач для проекта. Вызывай когда нужно записать задачи!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "proekt_id": {"type": "string"},
                        "tasks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "task": {"type": "string"},
                                    "description": {"type": "string"}
                                }
                            }
                        }
                    },
                    "required": ["proekt_id", "tasks"]
                }
            }
        }
        return schema

    def execute(self, **params):
        print(f"Сохраняю задачи: {params}")
        redis_client.save_tasks(**params)
        project_id = params.get('proekt_id')
        return f"Круто! Задачи для проекта '{project_id}' записаны в базу!"


# для получения списка работников
class GetWorkersTool:
    def __init__(self):
        self.name = "get_workers"

    def get_schema(self):
        schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Получает список всех работников и их навыки. Обязательно вызывай перед распределением задач!",
                "parameters": {"type": "object", "properties": {}}
            }
        }
        return schema

    def execute(self, **params):
        print("Получаю список работников из базы...")
        workers_data = redis_client.get_workers()
        workers_list = workers_data['parameters']['workers']
        return f"Вот все наши работники: {json.dumps(workers_list, ensure_ascii=False)}"


# для распределения задач между работниками
class SaveAssignmentsTool:
    def __init__(self):
        self.name = "save_assignments"

    def get_schema(self):
        schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Сохраняет распределение задач по работникам. Используй чтобы назначить кому что делать!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "proekt_id": {"type": "string"},
                        "assignments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "task": {"type": "string"},
                                    "timeline": {"type": "string"},
                                    "worker": {"type": "string"}
                                }
                            }
                        }
                    },
                    "required": ["proekt_id", "assignments"]
                }
            }
        }
        return schema

    def execute(self, **params):
        print(f"Сохраняю распределение задач: {params}")
        redis_client.save_assignments(**params)
        project_id = params.get('proekt_id')
        return f"Супер! Распределение задач для проекта '{project_id}' готово!"


"""
Настройка тестов

"""
@pytest.fixture(scope="module")
def setup_orchestrator():

    my_api_key = "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"

    # агент
    agent = DevstralAgent(api_key=my_api_key)

    # собираем все наши инструменты
    all_tools = [
        CreateProjectTool(),
        SavePlanTool(),
        SaveTasksTool(),
        GetWorkersTool(),
        SaveAssignmentsTool()
    ]

    system_message = (
        "Привет! Ты MrTime - помощник для управления проектами. "
        "Твоя работа - быстро и точно выполнять то что просит пользователь. "
        "Используй инструменты когда пользователь что-то хочет создать или сохранить. "
        "Не болтай лишнего, делай что просят!"
    )

    # оркестратор
    orchestrator = Orchestrator(
        agent=agent,
        tools=all_tools,
        system_prompt=system_message
    )

    print("Подготавливаю базу данных для тестов...")
    redis_client.clear_db()

    test_workers = {
        "worker_andrey": {
            "name": "Андрей",
            "skills": ["Python", "Redis", "AI"],
            "load": 0
        },
        "worker_anna": {
            "name": "Анна",
            "skills": ["Frontend", "UX/UI", "Дизайн"],
            "load": 1
        }
    }
    redis_client.save_workers(test_workers)

    yield orchestrator

    print("Очищаю базу данных после тестов...")
    redis_client.clear_db()


def test_complete_project_workflow(setup_orchestrator):
    """Тестируем полный цикл создания проекта"""

    orchestrator = setup_orchestrator
    test_project_id = "project:llm-chat-app"

    # === ШАГ 1: Создаем новый проект ===
    step1_message = (
        f"Привет! Давай создадим проект LLM Чат-помощник с ID {test_project_id}. "
        f"Стек: Python, Redis. Описание: Управление задачами через чат."
    )

    print(f"\n=== ШАГ 1: Создание проекта ===")
    print(f"Отправляю сообщение: {step1_message}")

    response1 = orchestrator.process_request(step1_message)
    print(f"Получил ответ: {response1}")

    assert "успешно создан" in response1.lower() or "создан" in response1.lower()
    project_data = redis_client.r.hgetall(test_project_id)
    assert project_data is not None and len(project_data) > 0

    # === ШАГ 2: Сохраняем план проекта ===
    step2_message = (
        f"Отлично! Для проекта `{test_project_id}` план такой: "
        f"на неделе 1 делаем API, на неделе 2 - логику."
    )

    print(f"\n=== ШАГ 2: Сохранение плана ===")
    print(f"Отправляю сообщение: {step2_message}")

    response2 = orchestrator.process_request(step2_message)
    print(f"Получил ответ: {response2}")

    assert "план" in response2.lower() and "сохран" in response2.lower()
    plan_data = redis_client.get_plan(test_project_id)
    assert len(plan_data['parameters']['plan']) == 2

    # === ШАГ 3: Добавляем задачи ===
    step3_message = (
        f"Для проекта `{test_project_id}` запиши, пожалуйста, три задачи: "
        f"1. Настроить redis_client. 2. Написать схемы. 3. Создать тест."
    )

    print(f"\n=== ШАГ 3: Добавление задач ===")
    print(f"Отправляю сообщение: {step3_message}")

    response3 = orchestrator.process_request(step3_message)
    print(f"Получил ответ: {response3}")

    assert "задач" in response3.lower() and ("сохран" in response3.lower() or "записан" in response3.lower())
    tasks_data = redis_client.get_tasks(test_project_id)
    assert len(tasks_data['parameters']['tasks']) == 3

    # === ШАГ 4: Распределяем задачи между работниками ===
    step4_message = (
        f"Финальный шаг для проекта `{test_project_id}`. "
        f"Распредели, пожалуйста, созданные задачи между работниками, учитывая их навыки. "

    )

    print(f"\n=== ШАГ 4: Распределение задач ===")
    print(f"Отправляю сообщение: {step4_message}")

    response4 = orchestrator.process_request(step4_message)
    print(f"Получил ответ: {response4}")

    assignments_data = redis_client.get_assignments(test_project_id)
    assert assignments_data['status'] == 'success', "Ошибка! Распределение не сохранилось в Redis!"

    assignments_list = assignments_data['parameters']['assignments']
    print(f"\nПроверяю распределения в Redis: {json.dumps(assignments_list, ensure_ascii=False, indent=2)}")

    assert len(assignments_list) > 0, "Список распределений пустой!"

    redis_task_assigned_to_jesus = False
    for assignment in assignments_list:
        if "redis_client" in assignment['task'] and assignment['worker'] == 'worker_anna':
            redis_task_assigned_to_jesus = True
            break

    assert redis_task_assigned_to_jesus, "Задача про Redis не назначена Хесусу!"

