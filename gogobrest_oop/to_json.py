import mysql.connector
import json

# Установите соответствующие значения для вашей базы данных
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'trolleybus'
}

# Создаем подключение к базе данных
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Выбираем данные из таблицы
cursor.execute("SELECT StationName, Direction FROM `102`")
rows = cursor.fetchall()

# Загружаем существующие данные из файла JSON, если таковые имеются
existing_data = {}
try:
    with open('code.json', 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    pass

# Создаем новый JSON объект и записываем его в файл, обновляя существующие значения
current_index = len(existing_data) + 1
for row in rows:
    stop_name = row[0]
    direction = row[1]
    key = 'T' + str(current_index)
    if key in existing_data:
        existing_data[key].append(stop_name)
    else:
        existing_data[key] = [stop_name, direction]
        current_index += 1

with open('code.json', 'w', encoding='utf-8') as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=4)

# Закрываем соединение
conn.close()
