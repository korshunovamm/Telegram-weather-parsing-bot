import peewee

db = peewee.SqliteDatabase('weather_last_week.db')  # БД для сайта

"""
Файл иницализирует базы данных сайта 
"""


class WeekWeather(peewee.Model):
    date = peewee.CharField()
    day_temperature = peewee.CharField()
    night_feeled_temperature = peewee.CharField()
    wind = peewee.CharField()

    class Meta:
        database = db


db.create_tables([WeekWeather])
db.close()
