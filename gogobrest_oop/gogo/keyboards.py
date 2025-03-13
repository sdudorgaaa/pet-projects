from aiogram import types

# Клавиатура выбора транспорта(choosing_transport)
keyboard_transport_list = [
		[types.KeyboardButton(text="Автобус"),
		types.KeyboardButton(text="Троллейбус")]
	]
keyboard_transport= types.ReplyKeyboardMarkup(keyboard=keyboard_transport_list, resize_keyboard=True, input_field_placeholder="Выберите режим работы")


# Клавиатура выбора режима (choosing_mode)
keyboard_mode_list = [
		[types.KeyboardButton(text="По номеру"),
		types.KeyboardButton(text="По станции")]
	]
keyboard_mode= types.ReplyKeyboardMarkup(keyboard=keyboard_mode_list, resize_keyboard=True,  input_field_placeholder="Отправьте режим работы")


# Клавиатура с номерами троллейбусов
keyboard_trolleybus_list = [
     [types.KeyboardButton(text="100"),
	types.KeyboardButton(text="101"),
    types.KeyboardButton(text="102")],
     [types.KeyboardButton(text="103"),
	types.KeyboardButton(text="104"),
    types.KeyboardButton(text="105")],
     [types.KeyboardButton(text="106"),
	types.KeyboardButton(text="107"),
    types.KeyboardButton(text="108")],
     [types.KeyboardButton(text="109"),
	types.KeyboardButton(text="110")]
]
keyboard_trolleybus= types.ReplyKeyboardMarkup(keyboard=keyboard_trolleybus_list, resize_keyboard=True, input_field_placeholder="Выберите режим работы")


# Клавиатура с номерами автобусов
keyboard_bus_list=[
    [types.KeyboardButton(text='номера автобусов')]
]
keyboard_bus= types.ReplyKeyboardMarkup(keyboard=keyboard_bus_list, resize_keyboard=True, input_field_placeholder="Выберите режим работы")

#Клавиатура если станция определена неверно
keyboard_wrong_station_list=[
    [types.InlineKeyboardButton(text='Не твоя остановка ?', callback_data='wrong_station')]
]
keyboard_wrong_station = types.InlineKeyboardMarkup(inline_keyboard=keyboard_wrong_station_list, resize_keyboard=True)

#поиск ближайшей остановки с геолокацтей
keyboard_find_station_list = [
    [types.KeyboardButton(text="Найти ближайшую остановку", request_location=True)]
]
keyboard_find_station = types.ReplyKeyboardMarkup(keyboard=keyboard_find_station_list, resize_keyboard=True, input_field_placeholder="Отправьте остановку")

#создание клавиатуры ближайших станций с геолакацией
def create_nearest_keyboard(one, two, three):
	keyboard_nearest_station_list = [
		[types.InlineKeyboardButton(text= one, callback_data=one),
		types.InlineKeyboardButton(text= two, callback_data=two),
		types.InlineKeyboardButton(text= three, callback_data=three)]
	]
	nearest_keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_nearest_station_list, resize_keyboard=True, input_field_placeholder="Выберите ближайшую")

	return nearest_keyboard

keyboard_personal_area_list = [
	[types.KeyboardButton(text='В избранное'),
	types.KeyboardButton(text="Обновить"),
	types.KeyboardButton(text="Назад")],
	[types.KeyboardButton(text="Найти ближайшую остановку", request_location=True)]	
]
keyboard_personal_area= types.ReplyKeyboardMarkup(keyboard=keyboard_personal_area_list, resize_keyboard=True)



    

