import json
from openai import OpenAI


# MAIN CONNECT
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
# тулы
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
                        "description": "Уникальный идентификатор пользователя",
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

    response_message = completion.choices[0].message

    if response_message.tool_calls:
        print("Func calling found")
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"Имя функции: {function_name}")
            print(f"Аргументы: {arguments}")


            if function_name == "get_user_details":
                print(f"user_id: {arguments.get('user_id')}")
    else:
        pass

except Exception as e:
    print(f"Произошла ошибка: {e}")