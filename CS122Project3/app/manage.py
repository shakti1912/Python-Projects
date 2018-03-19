import StringIO
import base64
import os
from threading import Thread
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import requests
from flask import Flask, request
from flask import render_template
from werkzeug.utils import redirect

from app.main.get_current_weather import get_current_weather
from app.main.five_day_forcast import *
from time import sleep

app = Flask(__name__)

# Please put your api key here
os.environ["openweatherapi"] = "put your api key here"
# please put your absolute path to static folder here
os.environ["path_to_static_folder"] = "/Users/shakti/PycharmProjects/CS122Project3/app/static/" # this is my abs path to static folder

print os.environ

@app.route('/')
def main():
    return redirect('/index/')


@app.route('/index/')
def index():
    return render_template('getCity.html')


@app.route('/dashboard', methods=['POST'])
def get_city():
    info = request.form.to_dict()
    city_raw = info['Name']
    city_name = city_raw[0].upper() + city_raw[1:]


    #cur_weather = get_current_weather(city_name)  # returns tuple with values (temp, description, img url) also saves img file

    #res = get_five_day_forecast(city_name)  # saves weather_map file

    cur_weather = get_current_weather(city_name)
    img_url = save_icon_image(cur_weather[2], city_name)
    info['img_url'] = img_url
    info['current_data'] = cur_weather
    info['city'] = city_name

    forecast_dict = get_five_day_forecast(city_name)
    plot_url = plot_map(forecast_dict, city_name)
    info['plot_url'] = plot_url
    #return render_template('info.html',plot_url=plot_url)
    return render_template('dashboard.html', info=info)


def plot_map(forecast, city):
    list_of_temps = forecast.values()
    list_of_dates = forecast.keys()
    # img = StringIO.StringIO()
    plt.xlabel("Dates")
    plt.ylabel("Temperature")
    plt.title("Five Day Weather Forecast for " + city)
    plt.plot(list_of_dates, list_of_temps)
    #file_name = sys.path[1] + "/app/static/weather_map.png"
    file_name = os.environ['path_to_static_folder'] + "weather_" + city.replace(" ", "") + ".png"
    plt.savefig(file_name)
    plt.close()
    plot_url = "../static/weather_" + city.replace(" ", "") + ".png"
    return plot_url


def save_icon_image(icon_tag, city):
    img_tag_url = "http://openweathermap.org/img/w/" + icon_tag + ".png"
    r = requests.get(img_tag_url, allow_redirects=True)
    #path = sys.path[1] + "/app/static/img.png"
    path = os.environ['path_to_static_folder'] + "img_" + city.replace(" ", "") + ".png"
    img_url = "../static/img_" + city.replace(" ", "") + ".png"
    open(path, 'wb').write(r.content)
    return img_url


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.debug = False
    app.run(port = 35408)
