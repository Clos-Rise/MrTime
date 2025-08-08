# routes.py
# Описание эндпоинтов API

API_ROUTES = [
    {
        "method": "POST",
        "path": "/projects",
        "description": "Создает новый проект в Redis.",
        "parameters": {
            "proekt_id": "str - ID проекта",
            "name": "str - Название проекта",
            "description": "str - Описание проекта",
            "stack": "str - Стек проекта",
            "links": "str - Ссылки проекта"
        },
        "response": "JSON с информацией о созданном проекте"
    },
    {
        "method": "POST",
        "path": "/projects/{proekt_id}/plan",
        "description": "Сохраняет план проекта.",
        "parameters": {
            "proekt_id": "str - Идентификатор проекта",
            "plan": "dict - План проекта (week1, week2, week3)"
        },
        "response": "JSON с подтверждением сохранения плана"
    },
    {
        "method": "GET",
        "path": "/projects/{proekt_id}/plan",
        "description": "Получает план указанного проекта.",
        "parameters": {
            "proekt_id": "str - Идентификатор проекта"
        },
        "response": "JSON с планом проекта"
    },
    {
        "method": "POST",
        "path": "/projects/{proekt_id}/tasks",
        "description": "Сохраняет список задач для указанного проекта.",
        "parameters": {
            "proekt_id": "str - Идентификатор проекта",
            "tasks": "list[dict] - Список задач, каждая с полями task и description"
        },
        "response": "JSON с подтверждением сохранения задач"
    },
    {
        "method": "GET",
        "path": "/projects/{proekt_id}/tasks",
        "description": "Получает список задач указанного проекта.",
        "parameters": {
            "proekt_id": "str - Идентификатор проекта"
        },
        "response": "JSON со списком задач"
    },
    {
        "method": "POST",
        "path": "/workers",
        "description": "Сохраняет данные о работниках.",
        "parameters": {
            "workers": "dict - Словарь работников, где ключ - ID, значение - объект с полями name, skills, load"
        },
        "response": "JSON с подтверждением сохранения работников"
    },
    {
        "method": "GET",
        "path": "/workers",
        "description": "Получает данные всех работников.",
        "parameters": {},
        "response": "JSON со списком всех работников"
    },
    {
        "method": "POST",
        "path": "/projects/{proekt_id}/assignments",
        "description": "Сохраняет распределение задач для указанного проекта.",
        "parameters": {
            "proekt_id": "str - Идентификатор проекта",
            "assignments": "list[dict] - Список назначений, каждое с полями task, timeline, worker"
        },
        "response": "JSON с подтверждением сохранения назначений"
    },
    {
        "method": "GET",
        "path": "/projects/{proekt_id}/assignments",
        "description": "Получает распределение задач для указанного проекта.",
        "parameters": {
            "proekt_id": "str - Идентификатор проекта"
        },
        "response": "JSON со списком назначений"
    },
    {
        "method": "POST",
        "path": "/backup",
        "description": "Выполняет резервное копирование базы данных Redis.",
        "parameters": {},
        "response": "JSON с подтверждением выполнения резервного копирования"
    },
    {
        "method": "POST",
        "path": "/clear",
        "description": "Очищает всю бд Redis.",
        "parameters": {},
        "response": "JSON с подтверждением очистки бд"
    }
]