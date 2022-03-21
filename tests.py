import unittest
from web_request import Parser


class CommandTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser('https://www.meteoservice.ru/weather/week/moskva')

    def test_find_weather_day_temperature(self):
        self.assertEqual(self.parser.find_weather_day()[1][0][0][0:27], "Температура воздуха ночью: ")

    def test_find_weather_day_wind(self):
        self.assertEqual(self.parser.find_weather_day()[3][0][3][0:15], "Ветер вечером: ")


if __name__ == "__main__":
    unittest.main()
