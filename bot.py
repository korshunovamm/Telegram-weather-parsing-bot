import os
import telebot
import threading
import time
import schedule
from config_data_base import update_db
from web_request import Parser

bot = telebot.TeleBot(os.environ["MY_TOKEN_BOT"])
url_site = 'https://www.meteoservice.ru/weather/week/moskva'


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    day = parser_days_of_week()
    if call.data == "week":  # call.data это callback_data, которую мы указали при объявлении кнопки
        try:
            week = Parser(url_site).find_weather_week()
            str_week = "".join([f'{key}\n{value}\n\n' for key, value in week.items()])
        except Exception as e:
            str_week = e
        bot.send_message(call.message.chat.id, str_week)
    else:
        number_day = int(call.data)
        if isinstance(day, list):
            str_day = f'{day[1][number_day]},{day[2][number_day]},{day[3][number_day]}'
            str_format = str_day.replace("'", '').replace(',', '\n').replace(']', '\n').replace('[', '\n')
            bot.send_message(call.message.chat.id,
                             f'{day[0][number_day]}\n{str_format}')
        else:
            str_format = 'сайт упал, подождите какое-то время'
            bot.send_message(call.message.chat.id, str_format)


def parser_days_of_week():
    try:
        list_of_days = Parser(url_site).find_weather_day()
        return list_of_days
    except Exception as e:
        print("ERROR: ", e)
        return 0


@bot.message_handler(commands=['weather'])
def keyboard_get_weather_of_day(message):
    day = parser_days_of_week()
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_week_weather = telebot.types.InlineKeyboardButton(text='Погода на неделю', callback_data='week')
    key_day_0 = telebot.types.InlineKeyboardButton(text='Погода на сегодня', callback_data="0")
    key_day_1 = telebot.types.InlineKeyboardButton(text='Погода на завтра', callback_data="1")
    keyboard.add(key_day_0, key_day_1)

    for number_of_day in range(2, 6):
        key_day = telebot.types.InlineKeyboardButton(text=day[0][number_of_day], callback_data=f"{number_of_day}")
        keyboard.add(key_day)

    keyboard.add(key_week_weather)

    bot.send_message(chat_id=message.chat.id, text='Выбрать период', reply_markup=keyboard)


@bot.message_handler(commands=['url'])
def url(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_my_site = telebot.types.InlineKeyboardButton(text='Наш сайт',
                                                     url=url_site,
                                                     callback_data='url')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n')
    elif message.text.lower() == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                          f'Вот некоторые команды для работы с ботом:\n'
                                          f'/url - сайт погоды\n'
                                          f'/weather - узнать погоду\n')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


def threaded_func(func, *args):
    """
    Загоняет функцию в поток.
    :param func: функция для исполнения в отдельном потоке
    :param args: аргументы функции
    """
    thread = threading.Thread(target=func, args=args)
    thread.start()  # выполняем функцию
    thread.join()  # закрываем поток


# запускаем бота в отдельном потоке
bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()
# каждый день обновляется бд в отдельном потоке
schedule.every().day.at("00:05").do(threaded_func, update_db)
# Многопоточность используется чтобы не останавливать
# бота для обновления бд погоды
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
