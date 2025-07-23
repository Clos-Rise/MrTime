import json
from openai import OpenAI

# подключение к OpenRouter
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

# функция для получения инфы о пользователе
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_user_details",
            "description": "Получить информацию о пользователе по его ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID пользователя",
                    }
                },
                "required": ["user_id"],
            },
        },
    }
]

try:
    completion = client.chat.completions.create(
      model="mistralai/devstral-small-2505:free",
      messages=[
        {
          "role": "user",
          "content": "Расскажи мне о пользователе с ID 42"
        }
      ],
      tools=tools,
      tool_choice="auto",
    )

    message = completion.choices[0].message

    if message.tool_calls:
        print("Модель вызвала функцию!")
        for call in message.tool_calls:
            func_name = call.function.name
            args = json.loads(call.function.arguments)

            print(f"Функция: {func_name}")
            print(f"Аргументы: {args}")

            if func_name == "get_user_details":
                print(f"Ищем пользователя: {args.get('user_id')}")
    else:
        print("Обычный ответ без вызова функций")

except Exception as e:
    print(f"Ошибка: {e}")