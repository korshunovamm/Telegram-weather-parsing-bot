import telebot
from telebot import types
from web_request import Parser

bot = telebot.TeleBot('1878148758:AAF23aybi5Ss0eUR4etsvI6ttFVq1ptAL04')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "week":  # call.data это callback_data, которую мы указали при объявлении кнопки
        parser = Parser('https://www.meteoservice.ru/weather/week/moskva').find_weather_week()
        bot.send_message(call.message.chat.id, parser)
    elif call.data == "day":
        parser = Parser('https://www.meteoservice.ru/weather/week/moskva').find_weather_day(1, 2)
        bot.send_message(call.message.chat.id, parser)


def keyboard_get_weather(message):
    keyboard = types.InlineKeyboardMarkup()

    key_week_weather = types.InlineKeyboardButton(text='Погода на неделю', callback_data='week')
    keyboard.add(key_week_weather)  # добавляем кнопку в клавиатуру

    key_day_weather = types.InlineKeyboardButton(text='Погода на день', callback_data="day")
    keyboard.add(key_day_weather)

    bot.send_message(message.from_user.id, text='Выб', reply_markup=keyboard)

def keyboard_get_weather_of_day(message):
    keyboard = types.InlineKeyboardMarkup()

    key_day_1 = types.InlineKeyboardButton(text='Погода на сегодня', callback_data="day1")
    keyboard.add(key_day_1)

    key_day_2 = types.InlineKeyboardButton(text='Погода на завтра', callback_data="day2")
    keyboard.add(key_day_2)

    key_day_3 = types.InlineKeyboardButton(text='Погода на день', callback_data="day3")
    keyboard.add(key_day_3)

    key_day_4 = types.InlineKeyboardButton(text='Погода на день', callback_data="day4")
    keyboard.add(key_day_4)

    key_day_5 = types.InlineKeyboardButton(text='Погода на день', callback_data="day5")
    keyboard.add(key_day_5)

    key_day_6 = types.InlineKeyboardButton(text='Погода на день', callback_data="day"6)
    keyboard.add(key_day_6)

    key_day_7 = types.InlineKeyboardButton(text='Погода на день', callback_data="day7")
    keyboard.add(key_day_7)

    bot.send_message(message.from_user.id, text='Выб', reply_markup=keyboard)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        pass
