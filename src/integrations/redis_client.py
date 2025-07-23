# Клиент для работы с Redis сервером(пока оффлайн)

import redis
import base64

# MAIN CONNECT
r = redis.Redis(host='tcp.cloudpub.ru', port=35559, decode_responses=False)  # binary mode

"""
    Создание таблицы erida-re(тестовая)
    
"""
#
# key = "erida-re"
# fields = {
#     "Name": "Тестовая сущность",
#     "Info": "Просто описание для демонстрации",
#     "Source": "Автотест, Python-скрипт"
# }
#
# with open("privet.txt", "w", encoding="utf-8") as f:
#     f.write("Привет, Redis!")
#
# with open("privet.txt", "rb") as file:
#     file_data = base64.b64encode(file.read()).decode('utf-8')
#
# fields["Files"] = file_data
#
# r.hset(key, mapping=fields)
#
# print("✅✅✅✅✅✅✅✅.")
#

"""
    Чтение таблицы erida-re
"""


result = r.hgetall("erida-re")
for key, val in result.items():
    try:
        decoded = val.decode("utf-8")
        print(f"{key.decode('utf-8')}: {decoded}")
    except:
        pass

