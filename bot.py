import telebot
from telebot import types
from web_request import Parser

bot = telebot.TeleBot('1800951201:AAGQhthVpv5UBnQzlyqiu59zCDlFmAf3IQA')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "week":  # call.data это callback_data, которую мы указали при объявлении кнопки
        try:
            week = Parser('https://www.meteoservice.ru/weather/week/moskva').find_weather_week()
            str_week = ''
            for key, value in week.items():
                str_week += key + "\n" + value + "\n\n"
        except Exception as e:
            str_week = e
        bot.send_message(call.message.chat.id, str_week)
    else:
        number_day = int(call.data)
        str_day = f'{day[1][number_day]},{day[2][number_day]},{day[3][number_day]}'
        str_format = str_day.replace("'", '').replace(',', '\n').replace(']', '\n').replace('[', '\n')
        bot.send_message(call.message.chat.id,
                         f'{day[0][number_day]}\n{str_format}')


def parser_days_of_week():
    try:
        list_of_days = Parser('https://www.meteoservice.ru/weather/week/moskva').find_weather_day()
    except Exception as e:
        list_of_days = e
    return list_of_days


day = parser_days_of_week()


@bot.message_handler(commands=['weather'])
def keyboard_get_weather_of_day(message):
    keyboard = types.InlineKeyboardMarkup()
    key_week_weather = types.InlineKeyboardButton(text='Погода на неделю', callback_data='week')
    key_day_0 = types.InlineKeyboardButton(text='Погода на сегодня', callback_data="0")
    key_day_1 = types.InlineKeyboardButton(text='Погода на завтра', callback_data="1")
    keyboard.add(key_day_0)

    keyboard.add(key_day_1)

    for i in range(2, 6):
        key_day = types.InlineKeyboardButton(text=day[0][i], callback_data=f"{i}")
        keyboard.add(key_day)
    keyboard.add(key_week_weather)

    bot.send_message(chat_id=message.chat.id, text='Выбрать период', reply_markup=keyboard)


@bot.message_handler(commands=['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Наш сайт',
                                             url='https://www.meteoservice.ru/weather/week/moskva',
                                             callback_data='url')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                          f'Вот некоторые команды для работы с ботом:\n'
                                          f'/url - сайт погоды\n'
                                          f'/weather - узнать погоду\n')
    elif message.text.lower() == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                          f'Вот некоторые команды для работы с ботом:\n'
                                          f'/url - сайт погоды\n'
                                          f'/weather - узнать погоду\n')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        pass
