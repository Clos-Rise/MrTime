import redis
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(title="гойда")
r = redis.Redis(host='tcp.cloudpub.ru', port=35559, decode_responses=True)

class ProjectCreate(BaseModel):
    proekt_id: str
    name: str
    description: str
    stack: str
    links: str

class Plan(BaseModel):
    week1: str
    week2: str
    week3: str

class Task(BaseModel):
    task: str
    description: str

class Worker(BaseModel):
    name: str
    skills: List[str]
    load: float

class Assignment(BaseModel):
    task: str
    timeline: str
    worker: str

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
    plan = json.loads(r.hget(f"{proekt_id}:plan", "plan") or "{}")
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
    tasks = json.loads(r.hget(f"{proekt_id}:tasks", "tasks") or "[]")
    return shablon(
        status="success",
        action="get_tasks",
        parameters={"proekt_id": proekt_id, "tasks": tasks},
        message="Задачи получены"
    )

def save_workers(workers_data):
    workers_json = {key: json.dumps(value, ensure_ascii=False) for key, value in workers_data.items()}
    r.hset("workers", mapping=workers_json)
    return shablon(
        status="success",
        action="save_workers",
        parameters={"workers": workers_data},
        message="Данные о работниках сохранены"
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
    assignments = json.loads(r.hget(f"{proekt_id}:assignments", "assignments") or "[]")
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

@app.post("/projects", response_model=dict)
async def api_create_project(project: ProjectCreate):
    try:
        result = create_project(
            project.proekt_id,
            project.name,
            project.description,
            project.stack,
            project.links
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании проекта: {str(e)}")

@app.post("/projects/{proekt_id}/plan", response_model=dict)
async def api_save_plan(proekt_id: str, plan: Plan):
    try:
        result = save_plan(proekt_id, plan.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении плана: {str(e)}")

@app.get("/projects/{proekt_id}/plan", response_model=dict)
async def api_get_plan(proekt_id: str):
    try:
        result = get_plan(proekt_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении плана: {str(e)}")

@app.post("/projects/{proekt_id}/tasks", response_model=dict)
async def api_save_tasks(proekt_id: str, tasks: List[Task]):
    try:
        result = save_tasks(proekt_id, [task.dict() for task in tasks])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении задач: {str(e)}")

@app.get("/projects/{proekt_id}/tasks", response_model=dict)
async def api_get_tasks(proekt_id: str):
    try:
        result = get_tasks(proekt_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении задач: {str(e)}")

@app.post("/workers", response_model=dict)
async def api_save_workers(workers: Dict[str, Worker]):
    try:
        workers_data = {key: worker.dict() for key, worker in workers.items()}
        result = save_workers(workers_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении работников: {str(e)}")

@app.get("/workers", response_model=dict)
async def api_get_workers():
    try:
        result = get_workers()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении работников: {str(e)}")

@app.post("/projects/{proekt_id}/assignments", response_model=dict)
async def api_save_assignments(proekt_id: str, assignments: List[Assignment]):
    try:
        result = save_assignments(proekt_id, [assignment.dict() for assignment in assignments])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении назначений: {str(e)}")

@app.get("/projects/{proekt_id}/assignments", response_model=dict)
async def api_get_assignments(proekt_id: str):
    try:
        result = get_assignments(proekt_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении назначений: {str(e)}")

@app.post("/backup", response_model=dict)
async def api_backup_db():
    try:
        result = backup_db()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при резервном копировании: {str(e)}")

@app.post("/clear", response_model=dict)
async def api_clear_db():
    try:
        result = clear_db()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при очистке базы данных: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)