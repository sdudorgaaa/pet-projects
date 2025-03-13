from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text, Command
from aiogram.types.input_media import InputMediaPhoto
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.middlewares import BaseMiddleware


from States import Main, Station, Number, is_real_station # Импортим Основную машину состояний
from Classes import Station_obj, Trolleybus # Импортим объект Троллейбус
from keyboards import keyboard_trolleybus, keyboard_mode, keyboard_bus, keyboard_transport, keyboard_wrong_station, keyboard_find_station, keyboard_personal_area # Импортируем клавиатуры
from keyboards import create_nearest_keyboard 
from databases import db_users 
from config import mode_list, TOKEN
from messages import hello_msg, choose_trolleybus_msg, choose_station_msg, choose_station_nearest_msg, format_schedule


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Обрабатывем комманду старт
@dp.message_handler(Command('start'))
async def start(message: types.Message):

    # Функция для добавления юзера в БД
    db_users(message.from_user.id, message.from_user.first_name) 

    # Отправляем сообщение с клавиатурой юзеру
    await bot.send_message(message.from_user.id, hello_msg.format(first_name = message.from_user.first_name), reply_markup=keyboard_mode, parse_mode="HTML")
    await Main.start.set()


#Обраатываем режим работы по станции или по номеру 
@dp.message_handler(
    state= Main.start
)
async def choosing_mode(message: types.Message, state: FSMContext):
    await state.finish()

    if message.text == mode_list[0]:
        await Number.choosing_number.set()
        await bot.send_message(message.from_user.id, choose_trolleybus_msg, reply_markup=keyboard_trolleybus)

    if message.text == mode_list[1]: # По станции 
        await bot.send_message(message.from_user.id, choose_station_msg, reply_markup=keyboard_find_station, parse_mode="HTML") #Отпраляем сообщение предлагая ввести станцию или определить местоположение
        Real_station = Station_obj() #Создаём объект станции
        await Station.in_progress.set() #Первое состояние для Station для сохранения объекта в FSM
        await state.update_data(my_object = Real_station)
        await Station.choosing_station.set() #След. состояние для выбора станции


# Хэндлер которорый ловит геолокацию если пользователь её отправил во время выбора остановки 
@dp.message_handler(
    content_types=types.ContentType.LOCATION,
    state= [Station.choosing_station, Station.wrong_station]
)
async def handle_location(message: types.Message, state: FSMContext):
    longitude = message.location.longitude # Получаем из сообщения широту и долготу
    latitude = message.location.latitude
    state_data = await state.get_data()
    Real_station = state_data.get("my_object") # Достаём экземпляр из FSM

    Real_station.find_nearest_station(latitude, longitude) # Юхаем метод который добавляет атрибуты ближайшей ст. списка бл. ст. и расстояние до ближайшей
    await message.answer("Геолокация определена упешно", reply_markup=keyboard_personal_area) 
    await message.answer(format_schedule(Real_station.get_first_schedule_by_station(), Real_station.station, Real_station.distance_to), reply_markup=keyboard_wrong_station, parse_mode='HTML')
    await state.update_data(my_object = Real_station) # Сохраняем обновленный объект
    await Station.pre.set()


# Инлайн кнопка для случая если станция геолокацией определена не верно 
@dp.callback_query_handler(lambda query: query.data == 'wrong_station', state=Station.pre)
async def wrong_station(query: types.CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    Real_station = state_data.get("my_object")

    nearest_keyboard = create_nearest_keyboard(Real_station.coming[0][0], Real_station.coming[1][0], Real_station.coming[2][0])

    await bot.send_message(query.from_user.id, choose_station_nearest_msg, reply_markup=nearest_keyboard, parse_mode="HTML")
    await state.update_data(my_object = Real_station) 
    await Station.wrong_station.set()

#Обнов станция по ГП
@dp.callback_query_handler(state= Station.wrong_station)
async def nearest_station(query: types.CallbackQuery, state:FSMContext):
    state_data = await state.get_data()
    Real_station = state_data.get("my_object")

    correct_station = query.data

    Real_station.update_attributes_by_name(correct_station)

    await bot.send_message(query.from_user.id, format_schedule(Real_station.get_first_schedule_by_station(), Real_station.station, Real_station.distance_to), reply_markup=keyboard_personal_area, parse_mode='HTML')
    await state.update_data(my_object = Real_station) 
    await Station.end.set()


@dp.message_handler(
    state=[Station.end, Station.pre],
    text="Назад"
)
async def back(message: types.Message, state:FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Выбирай падла не можешь с первого раза определиться урод", reply_markup=keyboard_mode, parse_mode="HTML")
    await Main.start.set()

@dp.message_handler(
    state=[Station.wrong_station, Station.end, Station.pre],
    text="Обновить"
)
async def update(message: types.Message, state:FSMContext):
    state_data = await state.get_data()
    Real_station = state_data.get("my_object")

    await bot.send_message(message.from_user.id, format_schedule(Real_station.get_first_schedule_by_station(), Real_station.station, Real_station.distance_to), reply_markup=keyboard_personal_area, parse_mode='HTML')


@dp.message_handler(
    state=[Station.choosing_station, Station.wrong_station]
)
async def choosing_station(message: types.Message, state:FSMContext):
    state_data = await state.get_data()
    Real_station = state_data.get("my_object")

    Real_station.find_station_reduction(message.text)

    await message.answer(format_schedule(Real_station.get_first_schedule_by_station(), Real_station.station, Real_station.distance_to, 2), reply_markup=keyboard_personal_area, parse_mode='HTML')

    await state.update_data(my_object = Real_station) 

if __name__ == '__main__':
    executor.start_polling(dp)
