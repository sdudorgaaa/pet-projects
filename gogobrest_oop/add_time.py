import mysql.connector
from time import sleep

# Подключение к базе данных
conn = mysql.connector.connect(
    host='localhost',
    user='root',  # Замените на ваше имя пользователя
    password='root',  # Замените на ваш пароль
    database='trolleybus'  # Замените на вашу базу данных
)

cursor = conn.cursor()

# Строка со значениями времени
time_string = input("Временная строка: ")

time_string = ' '.join(time_string[i:i+5] for i in range(0, len(time_string), 5))

# Разделяем строку по пробелам и убираем лишние пробелы
time_values = [time.strip() for time in time_string.split()]

column_name = input("Номер столбца:")

# Проверяем наличие столбца и создаем его, если его нет
cursor.execute("DESCRIBE `times`")
existing_columns = [column[0] for column in cursor.fetchall()]
if column_name not in existing_columns:
    cursor.execute(f"ALTER TABLE `times` ADD COLUMN `{column_name}` TIME")

# Вставляем значения в таблицу в формате HH:MM:00
for index, time_value in enumerate(time_values, start=1):
    formatted_time = time_value.replace('.', ':') + ":00"
    cursor.execute(f"INSERT INTO `trolleybus`.`times` (`num`, `{column_name}`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `{column_name}` = %s", (index, formatted_time, formatted_time))

conn.commit()

cursor.close()
conn.close()

print("Временные значения успешно добавлены в базу данных.")
sleep(3)








































