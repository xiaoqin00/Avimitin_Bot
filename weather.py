# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/12 16:53
import pyweathercn


class City:
    place = ''

    def __init__(self, city):
        self.place = city

    def get_city(self):
        return self.place


class Weather:
    data = ''
    today = ''
    tips = ''
    tomorrow = ''

    @staticmethod
    def get_weather(place):
        c = City(place)
        w = pyweathercn.Weather(c.get_city())

        Weather.data = w.data
        Weather.today = w.today()
        Weather.tips = w.tip()
        Weather.tomorrow = w.tomorrow()
