from data_base import db, WeekWeather
from web_request import Parser


def fill_db():
    """
    new_weather - список с описанием погоды на неделю,
        в котором каждый элемент также является списком,
        первый элемент - список из дат на неделю,
        второй элемент - список из температур на неделю,
        третий элемент - список из ощущений по температуре на неделю,
        четвертый элемент - список из скоростей ветра на неделю
    
    new_weather[0] - список дат на неделю
    new_weather[0][day_of_week] - дата в день номер day_of_week
    
    new_weather[1] - список из списков температур каждого дня на неделю
    new_weather[1][day_of_week] - список, характеризующий температуру дня на day_of_week день,
        где первый элемент этого списка описывает температуру ночью,
        второй элемент описывает температуру утром,
        третий элемент описывает температуру днем,
        четвертый элемент описывает температуру вечером
    
    new_weather[2] - полностью аналогичный список предыдущему,
    только описание идет как ощущается погода
    
    new_weather[3] - полностью аналогичный список предыдущим двум,
    только описание идет скорости ветра
    """
    db.connect()

    try:
        site_of_weather = Parser('https://www.meteoservice.ru/weather/week/moskva')
        new_weather = site_of_weather.find_weather_day()
        for day_of_week in range(7):
            WeekWeather.create(date=new_weather[0][day_of_week],
                               day_temperature=new_weather[1][day_of_week][0],
                               night_feeled_temperature=new_weather[2][day_of_week][0],
                               wind=new_weather[3][day_of_week][0])
    except Exception as e:
        print("SITE DROPPED : ", e)

    db.close()


def update_db():
    """
    Обновление базы данных сайта
    """

    print("update started")
    db.connect()

    """
    описание new_weather представлено в вышестоящей функции
    """

    try:
        site_of_weather = Parser('https://www.meteoservice.ru/weather/week/moskva')
        new_weather = site_of_weather.find_weather_day()
        # Выбираю самую врехнюю одну строчку из таблицы
        selected_day = WeekWeather.select().limit(1)

        # если есть верхняя строка
        if selected_day:
            selected_day = selected_day[0]
            selected_day.delete_instance()

        # создаю новую строку, то есть записываю данные вчеращнего дняеоторый будет
        # последним в неделе и 6 по счету в списках, которые являются элементами
        # в списке new_weather
        WeekWeather.create(date=new_weather[0][6],
                           day_temperature=new_weather[1][6][0],
                           night_feeled_temperature=new_weather[2][6][0],
                           wind=new_weather[3][6][0])

    except Exception as e:
        print("ERROR : ", e)

    db.close()


# fill_db()
