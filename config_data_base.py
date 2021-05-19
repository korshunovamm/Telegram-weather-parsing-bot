from data_base import db, WeekWeather
from web_request import Parser


def fill_db():
    db.connect()
    try:
        parser = Parser('https://www.meteoservice.ru/weather/week/moskva')
        new_weather = parser.find_weather_day()
        for i in range(7):
            WeekWeather.create(date=new_weather[0][i],
                               day_temperature=new_weather[1][i][0],
                               night_feeled_temperature=new_weather[2][i][0],
                               wind=new_weather[3][i][0])
    except Exception as e:
        print("SITE DROPPED : ", e)

    db.close()


def update_db():
    """
    Обновление базы данных сайта
    """
    print("update started")
    db.connect()

    try:
        parser = Parser('https://www.meteoservice.ru/weather/week/moskva')
        new_weather = parser.find_weather_day()
        selected_day = WeekWeather.select().limit(1)

        if selected_day:
            selected_day = selected_day[0]
            selected_day.delete_instance()

        WeekWeather.create(date=new_weather[0][6],
                           day_temperature=new_weather[1][6][0],
                           night_feeled_temperature=new_weather[2][6][0],
                           wind=new_weather[3][6][0])

    except Exception as e:
        print("ERROR : ", e)

    db.close()


# fill_db()
