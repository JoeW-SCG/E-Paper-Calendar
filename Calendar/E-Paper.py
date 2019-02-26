#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
E-Paper Software (main script) for the 3-colour and 2-Colour E-Paper display
A full and detailed breakdown for this code can be found in the wiki.
If you have any questions, feel free to open an issue at Github.

Copyright by aceisace
"""
from __future__ import print_function
import calendar
from datetime import datetime
from time import sleep

from DebugConsole import DebugConsole

debug = DebugConsole()

from settings import *
from icon_positions_locations import *

from PIL import Image, ImageDraw, ImageFont, ImageOps
import OwmForecasts
import IcalEvents
try:
    from urllib.request import urlopen
except Exception as e:
    debug.print("Something didn't work right, maybe you're offline?" + e.reason)

output_adapters = []

if render_to_file:
    import ImageFileAdapter
    epd = ImageFileAdapter.ImageFileAdapter()
    output_adapters.append(epd)

if render_to_display:
    if display_colours == "bwr":
        import Epd7in5bAdapter
        epd = Epd7in5bAdapter.Epd7in5bAdapter()
        output_adapters.append(epd)
    elif display_colours == "bw":
        import Epd7in5Adapter
        epd = Epd7in5Adapter.Epd7in5Adapter()
        output_adapters.append(epd)

EPD_WIDTH = epd.width
EPD_HEIGHT = epd.height
font = ImageFont.truetype(path + 'Assistant-Regular.ttf', 18)
im_open = Image.open

"""Main loop starts from here"""
def main ():
    while True:

        time = datetime.now()
        hour = int(time.strftime("%H"))
        month = int(time.now().strftime('%m'))
        year = int(time.now().strftime('%Y'))

        for i in range(1):
            debug.print('_________Starting new loop___________' + '\n')
            """At the following hours (midnight, midday and 6 pm), perform
               a calibration of the display's colours"""

            if hour in calibrate_hours:
                for output in output_adapters:
                    output.calibrate()

            debug.print('Date:'+ time.strftime('%a %d %b %y') + ', time: ' + time.strftime('%H:%M') + '\n')

            """Create a blank white page, for debugging, change mode to
            to 'RGB' and and save the image by uncommenting the image.save
            line at the bottom"""
            image = Image.new('L', (EPD_HEIGHT, EPD_WIDTH), 'white')
            draw = (ImageDraw.Draw(image)).bitmap

            """Draw the icon with the current month's name"""
            image.paste(im_open(mpath + str(time.strftime("%B") + '.jpeg')), monthplace)

            """Draw a line seperating the weather and Calendar section"""
            image.paste(seperator, seperatorplace)

            """Draw the icons with the weekday-names (Mon, Tue...) and
               draw a circle  on the current weekday"""
            if (week_starts_on == "Monday"):
                calendar.setfirstweekday(calendar.MONDAY)
                image.paste(weekmon, weekplace)
                draw(weekdaysmon[(time.strftime("%a"))], weekday)

            if (week_starts_on == "Sunday"):
                calendar.setfirstweekday(calendar.SUNDAY)
                image.paste(weeksun, weekplace)
                draw(weekdayssun[(time.strftime("%a"))], weekday)

            """Using the built-in calendar function, draw icons for each
               number of the month (1,2,3,...28,29,30)"""
            cal = calendar.monthcalendar(time.year, time.month)
            #debug.print(cal) #-uncomment for debugging with incorrect dates

            for numbers in cal[0]:
                image.paste(im_open(dpath + str(numbers) + '.jpeg'), positions['a' + str(cal[0].index(numbers) + 1)])
            for numbers in cal[1]:
                image.paste(im_open(dpath + str(numbers) + '.jpeg'), positions['b' + str(cal[1].index(numbers) + 1)])
            for numbers in cal[2]:
                image.paste(im_open(dpath + str(numbers) + '.jpeg'), positions['c' + str(cal[2].index(numbers) + 1)])
            for numbers in cal[3]:
                image.paste(im_open(dpath + str(numbers) + '.jpeg'), positions['d' + str(cal[3].index(numbers) + 1)])
            for numbers in cal[4]:
                image.paste(im_open(dpath + str(numbers) + '.jpeg'), positions['e' + str(cal[4].index(numbers) + 1)])
            try:
                for numbers in cal[5]:
                    image.paste(im_open(dpath + str(numbers) + '.jpeg'), positions['f' + str(cal[5].index(numbers) + 1)])
            except IndexError:
                pass

            """Custom function to display text on the E-Paper.
            Tuple refers to the x and y coordinates of the E-Paper display,
            with (0, 0) being the top left corner of the display."""
            def write_text (box_width, box_height, text, tuple):
                text_width, text_height = font.getsize(text)
                if (text_width, text_height) > (box_width, box_height):
                    raise ValueError('Sorry, your text is too big for the box')
                else:
                    x = int((box_width / 2) - (text_width / 2))
                    y = int((box_height / 2) - (text_height / 2))
                    space = Image.new('L', (box_width, box_height), color=255)
                    ImageDraw.Draw(space).text((x, y), text, fill=0, font=font)
                    image.paste(space, tuple)

            """ Handling Openweathermap API"""
            debug.print("Connecting to Openweathermap API servers...")
            owm = OwmForecasts.OwmForecasts(api_key, units=units)
            if owm.is_available() is True:
                forecast = owm.get_today_forecast(location)
                debug.print_forecast(forecast)

                if forecast.units == "metric":
                    write_text(50, 35, forecast.air_temperature + " °C", (334, 0))
                    write_text(100, 35, forecast.wind_speed + " km/h", (114, 0))

                if forecast.units == "imperial":
                    write_text(50, 35, forecast.air_temperature + " °F", (334, 0))
                    write_text(100, 35, forecast.wind_speed + " mph", (114, 0))

                if hours == "24":
                    sunrisetime = str(forecast.sunrise.strftime('%H:%M'))
                    sunsettime = str(forecast.sunset.strftime('%H:%M'))

                if hours == "12":
                    sunrisetime = str(forecast.sunrise.strftime('%I:%M'))
                    sunsettime = str(forecast.sunset.strftime('%I:%M'))

                """Drawing the fetched weather icon"""
                image.paste(im_open(wpath + weathericons[forecast.icon] + '.jpeg'), wiconplace)

                """Drawing the fetched temperature"""
                image.paste(tempicon, tempplace)

                """Drawing the fetched humidity"""
                image.paste(humicon, humplace)
                write_text(50, 35, forecast.air_humidity + " %", (334, 35))

                """Drawing the fetched sunrise time"""
                image.paste(sunriseicon, sunriseplace)
                write_text(50, 35, sunrisetime, (249, 0))

                """Drawing the fetched sunset time"""
                image.paste(sunseticon, sunsetplace)
                write_text(50, 35, sunsettime, (249, 35))

                """Drawing the wind icon"""
                image.paste(windicon, windiconspace)

                """Write a short weather description"""
                write_text(144, 35, forecast.short_description, (70, 35))

            else:
                image.paste(no_response, wiconplace)

            """Filter upcoming events from your iCalendar/s"""
            debug.print('Fetching events from your calendar' + '\n')

            events_cal = IcalEvents.IcalEvents(ical_urls)

            for event in events_cal.get_month_events():
                debug.print_event(event)

            upcoming = events_cal.get_upcoming_events()
            events_this_month = events_cal.get_month_events()
            events_this_month = [event.begin_datetime.day for event in events_this_month]

            def takeDate (elem):
                return elem.begin_datetime

            upcoming.sort(key=takeDate)

            del upcoming[4:]
            # uncomment the following 2 lines to display the fetched events
            # from your iCalendar
            debug.print('Upcoming events:')
            debug.print(upcoming)
            debug.print('Month events:')
            debug.print(events_this_month)

            #Credit to Hubert for suggesting truncating event names
            def write_text_left (box_width, box_height, text, tuple):
                text_width, text_height = font.getsize(text)
                while (text_width, text_height) > (box_width, box_height):
                    text=text[0:-1]
                    text_width, text_height = font.getsize(text)
                y = int((box_height / 2) - (text_height / 2))
                space = Image.new('L', (box_width, box_height), color=255)
                ImageDraw.Draw(space).text((0, y), text, fill=0, font=font)
                image.paste(space, tuple)

            """Write event dates and names on the E-Paper"""
            for dates in range(len(upcoming)):
                write_text(70, 25, (upcoming[dates].begin_datetime.strftime('%d %b')), date_positions['d' + str(dates + 1)])

            for events in range(len(upcoming)):
                write_text_left(314, 25, (upcoming[events].title), event_positions['e' + str(events + 1)])

            """Draw smaller squares on days with events"""
            for numbers in events_this_month:
                if numbers in cal[0]:
                    draw(positions['a' + str(cal[0].index(numbers) + 1)], eventicon)
                if numbers in cal[1]:
                    draw(positions['b' + str(cal[1].index(numbers) + 1)], eventicon)
                if numbers in cal[2]:
                    draw(positions['c' + str(cal[2].index(numbers) + 1)], eventicon)
                if numbers in cal[3]:
                    draw(positions['d' + str(cal[3].index(numbers) + 1)], eventicon)
                if numbers in cal[4]:
                    draw(positions['e' + str(cal[4].index(numbers) + 1)], eventicon)
                try:
                    if numbers in cal[5]:
                        draw(positions['f' + str(cal[5].index(numbers) + 1)], eventicon)
                except IndexError:
                    pass

            """Draw a larger square on today's date"""
            today = time.day
            if today in cal[0]:
                draw(positions['a' + str(cal[0].index(today) + 1)], dateicon)
            if today in cal[1]:
                draw(positions['b' + str(cal[1].index(today) + 1)], dateicon)
            if today in cal[2]:
                draw(positions['c' + str(cal[2].index(today) + 1)], dateicon)
            if today in cal[3]:
                draw(positions['d' + str(cal[3].index(today) + 1)], dateicon)
            if today in cal[4]:
                draw(positions['e' + str(cal[4].index(today) + 1)], dateicon)
            try:
                if today in cal[5]:
                    draw(positions['f' + str(cal[5].index(today) + 1)], dateicon)
            except IndexError:
                pass

            for output in output_adapters:
                output.render(image)

            debug.print("Finished rendering")

            for i in range(1):
                nexthour = ((60 - int(time.strftime("%M"))) * 60) - (int(time.strftime("%S")))
                sleep(nexthour)

if __name__ == '__main__':
    main()
