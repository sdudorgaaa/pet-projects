from aiogram.dispatcher.filters.state import State, StatesGroup
    
class Main(StatesGroup):
    start = State()

class Number(StatesGroup):   
    choosing_number = State() # Выбор номера
    choosin_direction = State() # Выбор направления
    choosing_station = State() # Выбор станции

class Station(StatesGroup):
    in_progress = State()
    choosing_station = State() # Выбор остановки
    pre = State()
    wrong_station = State()
    end = State() # Выбор стороны

async def is_real_station(query, state) -> bool:
    state_data = state.get_data()
    Real_station = state_data.get("my_object")

    if query.data in [Real_station['coming'][i][0] for i in range(3)]:
        return True
    else:
        return False



