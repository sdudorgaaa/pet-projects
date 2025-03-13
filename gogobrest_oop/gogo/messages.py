hello_msg = "👋 <b> Здравствуй {first_name}!👋\n Я бот, который облегчает твою жизнь в общественном транспорте потому что я:</b>\n\n\
✨<b>Прост и удобен</b>✨\n\
    <i><s>Никаких</s> поисков и <s>лишних</s> подписок — просто чат !</i>\n\n\
🚀<b>Не предлагаю рекламы</b>🚀\n\
    <i>Чистый интерфейс, только полезная информация !</i>\n\n\
💡<b>Меня <s>не нужно</s> скачивать</b>💡\n\
    <i>Забудь о лишних приложениях и сложной регистрации!</i>\n\n\
<b>Просто выбери режим работы и давай сэкономим твое время!</b>"

choose_trolleybus_msg = "Выберите номер троллейбуса"
choose_station_msg = "✏️<b>Напишите название остановки</b>✏️"
choose_station_nearest_msg = '🗺️<b>Выбери свою остановку из списка самых близких</b>🗺️'

from collections import defaultdict

def format_distance(distance):
    if distance > 1000:
        # Преобразуем в километры и округляем до двух знаков после запятой
        km = distance / 1000
        return f"Примерно {km:.0f} <i>км. от вас</i>"
    else:
        return f"Примерно {distance} <i>м. от вас</i>"

def format_schedule(schedule, station_name, distance, mode = 1):

    grouped_schedule = defaultdict(lambda: defaultdict(list))

    for time, direction, number in schedule:
        # Используем number как ключ для группировки
        grouped_schedule[number][direction].append(time)

    # Шаг 2: Формируем сообщение
    messages = ""

    for number, directions in grouped_schedule.items():
        for direction, times in directions.items():
            # Соединяем времена в строку, разделенную запятыми
            time_str = ", ".join(times)
            # Формируем строку для каждого направления и времени
            message = f"<b>🚎{number}🚎</b>\n<b>{direction}:</b>\n <i>🕒 {time_str}</i>\n\n"
            messages += message

    # Формируем финальное сообщение
    if mode == 1:
        msg = f"<b>Ближайшие рейсы на остановке \n🚏<i>{station_name}</i></b>🚏\n{format_distance(distance)}\n\n{messages}"
    elif mode == 2:
        msg = f"<b>Ближайшие рейсы на остановке \n🚏<i>{station_name}</i></b>🚏\n\n{messages}"

    return msg
