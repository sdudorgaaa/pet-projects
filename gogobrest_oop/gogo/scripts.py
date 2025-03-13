from datetime import datetime, timedelta

def time_sort(data):
    now = datetime.now()
    current_time_str = now.strftime("%H:%M")

    # Функция для вычисления времени до события
    def time_until_event(event_time_str):
        event_time = datetime.strptime(event_time_str, "%H:%M")
        # Если событие уже прошло, прибавляем 24 часа
        if event_time < now:
            event_time += timedelta(days=1)  
        return (event_time - now).total_seconds()

    # Сортировка по времени до ближайшего события
    sorted_data = sorted(data, key=lambda x: time_until_event(x[0]))
    return sorted_data