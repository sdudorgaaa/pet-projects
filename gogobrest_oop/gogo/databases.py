import sqlite3
import mysql.connector
from config import host, user, password, database

#Функция для заполнения базы данных юзеров
def db_users(id, name):
    db_users = sqlite3.connect('gogo\\database\\USERS.db') # Подключаемся к БД
    cursor_users = db_users.cursor() # Создаём курсор

    cursor_users.execute(f"SELECT user_id FROM users WHERE user_id = '{id}'") #Делаем запрос на id в БД
    
    # Если пользователя нету в БД то добавляем его туда
    if cursor_users.fetchone() is None: 
        cursor_users.execute(f"INSERT INTO users VALUES (?, ?)", (id, name))
        
        db_users.commit() # Сохраняем
        db_users.close() # Закрываем БД
"""
def db_nearest_station(latitude, longitude):
    # Подключение к базе данных
    conn = sqlite3.connect('gogo\\database\\STATIONS.db')  # Замените на имя вашей базы данных
    cursor = conn.cursor()
    select_query = "SELECT station_name, latitude, longitude, ((latitude - ?) * (latitude - ?)) + ((longitude - ?) * (longitude - ?)) AS distance FROM stations ORDER BY distance ASC LIMIT 3"
    cursor.execute(select_query, (latitude, latitude, longitude, longitude))
    rows = cursor.fetchall()
    conn.close()
    print(rows)
    return rows
"""

def db_nearest_station(target_latitude, target_longitude):
    conn = mysql.connector.connect(
        host=host,
        user=user,  
        password=password, 
        database=database 
    )

    cursor = conn.cursor()

    try:
        cursor = conn.cursor()

        # SQL-запрос с параметрами
        sql_query = """
        SELECT StationName, 
            Latitude AS lat1, 
            Longitude AS lon1, 
            Latitudetwo AS lat2, 
            Longitudetwo AS lon2,
            (6371 *
            acos(cos(radians(%s)) * cos(radians(Latitude)) *
            cos(radians(Longitude) - radians(%s)) +
            sin(radians(%s)) *
            sin(radians(Latitude)))) AS distance
        FROM stations
        WHERE Latitude IS NOT NULL AND Longitude IS NOT NULL

        UNION ALL

        SELECT StationName, 
            LatitudeTwo AS lat1, 
            LongitudeTwo AS lon1, 
            Latitude AS lat2, 
            Longitude AS lon2,
            (6371 *
            acos(cos(radians(%s)) * cos(radians(LatitudeTwo)) *
            cos(radians(LongitudeTwo) - radians(%s)) + 
            sin(radians(%s)) * 
            sin(radians(LatitudeTwo)))) AS distance
        FROM stations
        WHERE LatitudeTwo IS NOT NULL AND LongitudeTwo IS NOT NULL

        ORDER BY distance
        LIMIT 3;

        """

        # Выполнение запроса с передачей параметров
        cursor.execute(sql_query, (target_latitude, target_longitude, target_latitude, target_latitude, target_longitude, target_latitude))

        # Получение результата
        result = cursor.fetchall()
        if result:
            return result
        else:
            print("Станция не найдена.")
            return "kakito huita"

    finally:
        # Закрытие курсора и соединения
        cursor.close()
        conn.close()

def get_stations_by_location(search_station_name):
        # Настройка подключения к базе данных
        conn = mysql.connector.connect(
            host='localhost',       # замените на ваш хост
            user='root',   # замените на ваше имя пользователя
            password='root',  # замените на ваш пароль
            database='trolleybus'  # замените на имя вашей базы данных
        )
        
        cursor = conn.cursor()

        # Получаем имена всех таблиц, состоящих только из чисел
        cursor.execute("SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = %s AND table_name REGEXP '^[0-9]+$'", 
                    (conn.database,))
        
        # Получаем названия таблиц
        tables = cursor.fetchall()

        # Подготовим запрос для объединения результатов
        union_queries = []
        for (table_name,) in tables:
            union_queries.append(f"SELECT *, '{table_name}' as table_name FROM `{table_name}` WHERE StationName = %s")

        if union_queries:
            final_query = " UNION ".join(union_queries)

            # Выполняем запрос для всех таблиц
            cursor.execute(final_query, (search_station_name,) * len(union_queries))
            
            results = cursor.fetchall()

            t_list = []
            
            for row in results:
                t_list.append(row)
            return t_list
        else:
            print("Нет таблиц с названиями, состоящими только из чисел.")

        # Закрываем курсор и соединение
        cursor.close()
        conn.close()
    
def get_nearest_times(key_dict, num_values):
        # Подключение к базе данных
        connection = mysql.connector.connect(
            host='localhost',        # Замените на ваш хост
            user='root',        # Замените на ваше имя пользователя
            password='root', # Замените на ваш пароль
            database='trolleybus'  # Замените на вашу базу данных
        )
        cursor = connection.cursor()

        columns = list(key_dict.keys())
        # Формируем запрос
        union_queries = []
        for col in columns:
            query = f"""
                SELECT '{col}' AS column_name, {col} AS value
                FROM times
                WHERE {col} >= CURTIME()
            """
            union_queries.append(query)

        # Объединяем все запросы с помощью UNION ALL
        final_query = "UNION ALL ".join(union_queries) + f" ORDER BY value ASC LIMIT {num_values};"

        
        cursor.execute(final_query )
        results = cursor.fetchall()

        # Закрытие соединения
        cursor.close()
        connection.close()


        print(results)
        return results

def get_two_sides_station(station_name):
    # Настройки подключения к базе данных
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'trolleybus'
    }

    # Подключение к базе данных
    connection = mysql.connector.connect(**db_config)

    try:
        cursor = connection.cursor()

        # Значение StationName, по которому нужно делать поиск

        # SQL-запрос
        query = "SELECT TwoSides FROM stations WHERE StationName = %s"
        
        # Выполнение запроса с параметром
        cursor.execute(query, (station_name,))
        
        # Получение результата
        result = cursor.fetchone()

        if result:
            print(f'TwoSides для {station_name}: {result[0]}')
            return result[0]
        else:
            print('Станция не найдена.')

    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()
