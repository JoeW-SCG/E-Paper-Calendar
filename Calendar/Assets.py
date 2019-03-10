#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageFont
from settings import *
im_open = Image.open

path =      ''
wpath =     path+'weather-icons/'
opath =     path+'other/'
fpath =     path+'fonts/'

tempicon =      im_open(opath+'temperature.jpeg')
humicon =       im_open(opath+'humidity.jpeg')
no_response=    im_open(opath+'cloud-no-response.jpeg')
sunriseicon =   im_open(opath+'wi-sunrise.jpeg')
sunseticon =    im_open(opath+'wi-sunset.jpeg')
windicon =      im_open(opath+'wi-strong-wind.jpeg')

fonts = {
    "extralight" : "Assistant-ExtraLight.otf",
    "light" : "Assistant-Light.otf",
    "regular" : "Assistant-Regular.otf",
    "semibold" : "Assistant-SemiBold.otf",
    "bold" : "Assistant-Bold.otf",
    "extrabold" : "Assistant-ExtraBold.otf"
}

defaultfont = fpath + fonts[font_boldness]

datetime_locals = {
    "de" : "de_DE.UTF-8",
    "en" : "en_US.UTF-8",
    "zh_TW" : "zh_TW.UTF-8"
}

weathericons = {
'01d': 'wi-day-sunny', '02d':'wi-day-cloudy', '03d': 'wi-cloudy',
'04d': 'wi-cloudy-windy', '09d': 'wi-showers', '10d':'wi-rain',
'11d':'wi-thunderstorm', '13d':'wi-snow', '50d': 'wi-fog',
'01n': 'wi-night-clear', '02n':'wi-night-cloudy',
'03n': 'wi-night-cloudy', '04n': 'wi-night-cloudy',
'09n': 'wi-night-showers', '10n':'wi-night-rain',
'11n':'wi-night-thunderstorm', '13n':'wi-night-snow',
'50n': 'wi-night-alt-cloudy-windy'}