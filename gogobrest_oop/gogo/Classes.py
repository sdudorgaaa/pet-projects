import json
from databases import db_nearest_station, get_stations_by_location, get_nearest_times, get_two_sides_station
from scripts import time_sort

class Trolleybus(object): # Создаем объект троллейбус
    number = None 
    direction = None # Все аттрибуты Троллейбуса по умлочанию в Nonew
    station = None

    def __init__(self, x_number, y_directoin, z_station): # Инициализируем конструктор с параметрами
        number = x_number
        directioin = y_directoin
        station = z_station

    def method1(self, x):
        return 2*x
    

class Station_obj(object):

    def __init__(self, station = None, distance_to = None, coming = None, coming_to_this_station = None, dict_time = None):
        self.station = station
        self.distance_to = distance_to
        self.coming = coming
        self.coming_to_this_station = coming_to_this_station
        self.dict_time = dict_time
    
    def find_station_reduction(self, input_str):

        # Чтение JSON файла
        with open('reduction.json', 'r', encoding='utf-8') as file:
            stations = json.load(file)['stations']

        for key, abbreviations in stations.items():
            if input_str.lower() in abbreviations:
                self.station = key
        return "Остановка не найдена"

    def find_nearest_station(self, latitude, longitude):
        row = db_nearest_station(latitude, longitude)
        if row:
            self.station = row[0][0]
            self.coming = []
            self.coming.append(row[0])
            self.coming.append(row[1])
            self.coming.append(row[2])
            distance = int(row[0][5]*1000)
            self.distance_to = distance
            print(row[0])
            print(row[1])
            print(row[2])
        else:
            return None  # Если нет данных, возвращаем None
        
    def update_attributes_by_name(self, target_name):
        # Поиск кортежа по имени
        for tup in self.coming:
            if tup[0] == target_name:
                # Обновление атрибутов объекта
                self.station = tup[0]  # Название из кортежа
                self.distance_to = int(tup[5]*1000)  # Расстояние из кортежа
                # Если кортеж содержит дополнительные данные, например, третий элемент,
                # то можно его обработать или использовать по необходимости
                print(f"Обновлено: {self.station}, {self.distance_to}")
                return  # Завершение, если нашли нужное значение
        
        print("Кортеж с таким именем не найден.")
    
    def get_schedule_by_station(self):
        return f"Расписание {self.station}\nПримерно {self.distance_to}м. от вас"
    
    
    
    def schedule_by_station(self, num):
        # Пример использования
        tuples_from_db = get_stations_by_location(self.station)

        # Загрузка данных из файла code.json
        with open("code.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Обработка кортежей и сопоставление с JSON
        result = {}

        # Проход по кортежам
        for tup in tuples_from_db:
            # Извлекаем значения из кортежа
            id_value = tup[0]               # Значение id
            name_value = tup[1]             # Значение из tupes_from_db[1]
            location_name = tup[3]          # Значение из tupes_from_db[3]

            # Ищем соответствие в JSON
            for key, value in json_data.items():
                # Проверяем наличие обоих значений
                if name_value in value and location_name in value:
                    if key not in result:
                        result[key] = []  # Инициализация списка, если ключа еще нет
                    result[key].append(tup)  # Сохраняем кортеж с найденным ключом

        # Проверяем результат
        self.coming_to_this_station = result
        time_data = get_nearest_times(self.coming_to_this_station, num)
        result_dict = {}

        # Проходим по каждому элементу в списке
        for key, time_value in time_data:
            if key in self.coming_to_this_station:
                # Преобразуем значение времени в строку формата "HH:MM"
                total_seconds = int(time_value.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                time_str = f"{hours:02}:{minutes:02}"

                # Добавляем кортеж времени и значения из my_dict
                if key not in result_dict:
                    result_dict[key] = []  # Инициализируем список, если ключ еще не был добавлен
                result_dict[key].append((time_str, *self.coming_to_this_station[key][0]))  # Делаем кортеж с временем изначениями из my_dict

        result_dict = [item for sublist in result_dict.values() for item in sublist]
        result_dict = [(item[0], item[4], item[5]) for item in result_dict]
        result_dict = time_sort(result_dict)

        self.dict_time=result_dict

        return self.dict_time

    def get_first_schedule_by_station(self):
        stat = get_two_sides_station(self.station)
        
        if stat == 1:
            time_data = self.schedule_by_station(5)
        if stat == 0:
            time_data = self.schedule_by_station(3)

        return time_data

        