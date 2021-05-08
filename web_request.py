import requests
from bs4 import BeautifulSoup
import time


class Parser:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url)
        response.encoding = "utf-8"
        self.html = response.text
        self.soup = BeautifulSoup(self.html, "lxml")
        with open("file.html", "w") as file:
            file.write(self.html)

    def find_weather_week(self):
        weather_week = {}
        describe_date = self.soup.find_all("span", class_="show-for-medium")
        describe_day = self.soup.find_all("table")

        for date, day in zip(describe_date, describe_day):
            if date and day:
                weather_week[date.text] = day["summary"]
        return weather_week

    def find_weather_day(self, number_day, number_daytime):
        weather_day = []
        number_day = f"div:nth-of-type({number_day})"
        describe_day = self.soup.select(number_day, class_="row collapse align-middle")
        print(describe_day)
        # for item in describe_day:
        #     if describe_day:
        #         describe_date = describe_day.find_all_previous("span", class_="show-for-medium")
        # describe_day = self.soup.select("div", class_="row collapse align-middle")
        # weather_day.append(describe_dat)
        return weather_day


# t1 = time.time()
# t2 = time.time()
# print("Time of execution: ", t2 - t1)
print(Parser('https://www.meteoservice.ru/weather/week/moskva').find_weather_week())
print(Parser('https://www.meteoservice.ru/weather/week/moskva').find_weather_day(1, 2))
