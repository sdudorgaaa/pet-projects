import mysql.connector

# Установите соответствующие значения для вашей базы данных
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'trolleybus'
}

# Открываем текстовый файл и считываем его содержимое
with open('stations.txt', 'r', encoding='utf-8') as file:
    stops = file.read().splitlines()

# Создаем подключение к базе данных
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

direction = "Дворец спорта «Виктория» - Свердлова"

for stop in stops:
    cursor.execute("INSERT INTO `102` (StationName, Direction) VALUES (%s, %s)", (stop, direction))

# Коммитим изменения и закрываем соединение
conn.commit()
conn.close()
