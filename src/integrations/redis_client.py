import redis

r = redis.Redis(host='tcp.cloudpub.ru', port=35559, decode_responses=True)

def write_to_db(key, mapping):
    r.hset(key, mapping=mapping)

def read_from_db(key):
    return r.hgetall(key)

def delete_field(key, field):
    r.hdel(key, field)

def list_keys(pattern="*"):
    return r.keys(pattern)

def available_key(key):
    return r.exists(key)

def available_field(key, field):
    return r.hexists(key, field)

def update_field(key, field, value):
    r.hset(key, field, value)

def backup_db():
    try:
        r.save()
        return True
    except Exception as e:
        print(f"Ошибка резервного копирования: {e}")
        return False

def clear_db():
    try:
        r.flushdb()
        return True
    except Exception as e:
        print(f"Ошибка очистки базы: {e}")
        return False

if __name__ == "__main__":
    key = "erida-re"
    field = "Name"
    data = {
        "Name": "Тестовая сущность",
        "Info": "Просто описание для демонстрации",
        "Source": "Автотест, Python-скрипт"
    }

    write_to_db(key, data)
    print(read_from_db(key))

    update_field(key, "Info", "описание намбер два")
    print(read_from_db(key))

    delete_field(key, "Source")
    print(read_from_db(key))

    print(available_field(key, field))

    if backup_db():
        print("Резервное копирование выполнено успешно.")
    else:
        print("Резервное копирование не удалось.")

    # это бдшку под ноль снести
    if clear_db():
        print("База данных очищена.")
