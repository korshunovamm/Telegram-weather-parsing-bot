import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url):
        self.url = url
        headers = [
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:45.0) Gecko/20100101 Firefox/45.0'},
            {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                              ' (KHTML, like Gecko) Chrome/88.0.4324.111 YaBrowser/21.2.1.94 (beta)'
                              ' Yowser/2.5 Safari/537.36'},
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/88.0.4324.146 Safari/537.36'},
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'},
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/87.0.4280.141 Safari/537.36'},
            {
                'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        ]

        response = requests.get(self.url, headers=headers[3])
        response.encoding = "utf-8"
        self.html = response.text
        self.soup = BeautifulSoup(self.html, "lxml")
        with open("media/file.html", "w") as file:
            file.write(self.html)

    def find_weather_week(self):

        weather_week = {}
        describe_date = self.soup.find_all("span", class_="show-for-medium")
        describe_day = self.soup.find_all("table")

        for date, day in zip(describe_date, describe_day):
            if date and day:
                weather_week[date.text] = day["summary"]
        return weather_week

    def find_weather_day(self):
        weather_day_date = []
        weather_day_temperature = []
        weather_day_feeled_temperature = []
        weather_day_wind = []

        describe_day = self.soup.find_all(["span"], {"class": ["show-for-medium"]})
        for item in describe_day:
            if item:
                weather_day_date.append(item.text)
                # print(item.text)

        describe_temperature = self.soup.find_all(["tr"], {"class": ["temperature"]})
        for item in describe_temperature:
            list_temperature = item.text.replace("\n", '').replace("  ", '').split('\t')
            list_temperature_describe = ["Температура воздуха ночью: ", "Температура воздуха утром: ",
                                         "Температура воздуха днем: ", "Температура воздуха вечером: "]
            list_day_temperature = [list_temperature[i]
                                    for i in range(len(list_temperature))
                                    if list_temperature[i] != '' and i % 4 == 0 and i]
            weather_day_temperature.append(
                [list_temperature_describe[i] + list_day_temperature[i] for i in range(4)])

        describe_feeled_temperature = self.soup.find_all(["tr"], {"class": ["feeled-temperature"]})
        for item in describe_feeled_temperature:
            list_feeled_temperature = item.text.replace("\n", '').replace("  ", '').replace("Ощущается", "").split("°")
            list_feeled_temperature_describe = ["Ощущается ночью: ", "Ощущается утром: ",
                                                "Ощущается днем: ", "Ощущается вечером: "]
            if len(list_feeled_temperature) != 1:
                list_day_feeled_temperature = [list_feeled_temperature[i] + "°"
                                               for i in range(len(list_feeled_temperature))
                                               if list_feeled_temperature[i] != '' and i % 2 != 0]
                weather_day_feeled_temperature.append(
                    [list_feeled_temperature_describe[i] + list_day_feeled_temperature[i] for i in range(4)])

        describe_wind = self.soup.find_all(["tr"], {"class": ["wind"]}, {"title": [True]})
        for item in describe_wind:
            list_wind = item.text.replace("  ", '').replace("\n", '').replace("Ветер", '').split("м/с")
            list_wind_describe = ["Ветер ночью: ", "Ветер утром: ",
                                  "Ветер днем: ", "Ветер вечером: "]
            list_day_wind = [list_wind[i] + "м/с"
                             for i in range(len(list_wind))
                             if list_wind[i] != '' and i % 2 != 0]
            weather_day_wind.append([list_wind_describe[i] + list_day_wind[i] for i in range(4)])

        return [weather_day_date, weather_day_temperature, weather_day_feeled_temperature, weather_day_wind]

#
# try:
#     list_of_dayss = Parser('https://www.meteoservice.ru/weather/week/moskva').find_weather_day()
# except Exception as e:
#     list_of_dayss = e
# print(list_of_dayss)
