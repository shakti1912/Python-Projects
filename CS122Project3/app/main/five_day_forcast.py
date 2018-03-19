import os

import requests
# get five day weather forecast of the required city
import sys


def get_five_day_forecast(city):
    api_key = os.environ['openweatherapi']
    default_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city,
        'APPID': api_key
    }

    res = requests.get(default_url, params=params)
    r = res.json()

    weather_list =  r['list']
    #print r['list'][len(r['list'])-1]
    forecast_dict = dict()
    for item in weather_list:
        forecast_dict[item['dt_txt'].split(" ")[0]] = item['main']['temp']
    return forecast_dict
