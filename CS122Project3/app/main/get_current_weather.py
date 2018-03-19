import os
import sys

import requests
# get current weather of the required city


def get_current_weather(city):
    api_key = os.environ['openweatherapi']
    default_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
                    'q': city,
                    'APPID': api_key
             }

    res = requests.get(default_url, params=params).json()
    weather_description = res['weather'][0]['description']
    temp = res['main']['temp']
    icon_tag = res['weather'][0]['icon']
    # img_tag_url = "http://openweathermap.org/img/w/"+icon_tag+".png"
    # r = requests.get(img_tag_url, allow_redirects=True)
    # path =  sys.path[1] + "/app/static/img.png"
    # open(path, 'wb').write(r.content)
    tup = (temp, weather_description, icon_tag)
    return tup

