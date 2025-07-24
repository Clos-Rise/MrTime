import redis
import json
from datetime import datetime

r = redis.Redis(host='tcp.cloudpub.ru', port=35559, decode_responses=True)

def shablon(status, action, parameters, message):
    return {
        "status": status,
        "tool": "Редиска",
        "action": action,
        "parameters": parameters,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def create_project(proekt_id, name, description, stack, links):
    project_data = {
        "name": name,
        "description": description,
        "stack": stack,
        "links": links
    }
    r.hset(proekt_id, mapping=project_data)
    return shablon(
        status="success",
        action="create_project",
        parameters={"proekt_id": proekt_id, "data": project_data},
        message="Проект создан"
    )

def save_plan(proekt_id, plan):
    r.hset(f"{proekt_id}:plan", "plan", json.dumps(plan, ensure_ascii=False))
    return shablon(
        status="success",
        action="save_plan",
        parameters={"proekt_id": proekt_id, "plan": plan},
        message="План сохранен"
    )

def get_plan(proekt_id):
    plan = json.loads(r.hget(f"{proekt_id}:plan", "plan"))
    return shablon(
        status="success",
        action="get_plan",
        parameters={"proekt_id": proekt_id, "plan": plan},
        message="План получен"
    )

def save_tasks(proekt_id, tasks):
    r.hset(f"{proekt_id}:tasks", "tasks", json.dumps(tasks, ensure_ascii=False))
    return shablon(
        status="success",
        action="save_tasks",
        parameters={"proekt_id": proekt_id, "tasks": tasks},
        message="Задачи сохранены"
    )

def get_tasks(proekt_id):
    tasks = json.loads(r.hget(f"{proekt_id}:tasks", "tasks"))
    return shablon(
        status="success",
        action="get_tasks",
        parameters={"proekt_id": proekt_id, "tasks": tasks},
        message="Задачи успешно получены"
    )

def save_workers(workers_data):
    workers_json = {key: json.dumps(value, ensure_ascii=False) for key, value in workers_data.items()}
    r.hset("workers", mapping=workers_json)
    return shablon(
        status="success",
        action="save_workers",
        parameters={"workers": workers_data},
        message="Данные о работниках успешно сохранены"
    )

def get_workers():
    workers_raw = r.hgetall("workers")
    workers = {key: json.loads(value) for key, value in workers_raw.items()}
    return shablon(
        status="success",
        action="get_workers",
        parameters={"workers": workers},
        message="Данные о работниках получены"
    )

def save_assignments(proekt_id, assignments):
    r.hset(f"{proekt_id}:assignments", "assignments", json.dumps(assignments, ensure_ascii=False))
    return shablon(
        status="success",
        action="save_assignments",
        parameters={"proekt_id": proekt_id, "assignments": assignments},
        message="Распределение задач сохранено"
    )

def get_assignments(proekt_id):
    assignments = json.loads(r.hget(f"{proekt_id}:assignments", "assignments"))
    return shablon(
        status="success",
        action="get_assignments",
        parameters={"proekt_id": proekt_id, "assignments": assignments},
        message="Распределение задач получено"
    )

def backup_db():
    r.save()
    return shablon(
        status="success",
        action="backup_db",
        parameters={},
        message="Резервное копирование выполнено"
    )

def clear_db():
    r.flushdb()
    return shablon(
        status="success",
        action="clear_db",
        parameters={},
        message="База данных очищена"
    )

if __name__ == "__main__":
    proekt_id = "project:test"
    result = create_project(
        proekt_id=proekt_id,
        name="Project",
        description="Разработка оружия",
        stack="Принглс, Губка, Перчатки, Смазка",
        links="https://penis.com"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))

    plan = {
        "week1": "Разработка чего-нибудь",
        "week2": "Настройка чего-нибудь",
        "week3": "Тестирование чего-нибудь"
    }
    result = save_plan(proekt_id, plan)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    result = get_plan(proekt_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    tasks = [
        {"task": "Настройка редиски", "description": "Настроить редиску"},
    ]
    result = save_tasks(proekt_id, tasks)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    workers = {
        "worker1": {"name": "Хесус", "skills": ["Политика", "Стримы"], "load": 0.5},
    }
    result = save_workers(workers)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    assignments = [
        {"task": "Разработка чего-нибудь", "timeline": "2 недели", "worker": "worker1"}
    ]
    result = save_assignments(proekt_id, assignments)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    result = get_assignments(proekt_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))