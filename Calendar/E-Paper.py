#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
E-Paper Software (main script) for the 3-colour and 2-Colour E-Paper display
A full and detailed breakdown for this code can be found in the wiki.
If you have any questions, feel free to open an issue at Github.

Copyright by aceisace
"""
from __future__ import print_function
from datetime import datetime
from time import sleep
from Assets import datetime_locals
import locale
from DebugConsole import DebugConsole
from settings import *
from MonthOvPanel import MonthOvPanel
from WeatherHeaderDesign import WeatherHeaderDesign
import OwmForecasts
import IcalEvents

locale.setlocale(locale.LC_ALL, datetime_locals[language])
debug = DebugConsole()
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

"""Main loop starts from here"""
def main ():
    while True:

        time = datetime.now()
        hour = int(time.strftime("%H"))
        month = int(time.now().strftime('%m'))
        year = int(time.now().strftime('%Y'))

        for i in range(1):
            debug.print_line('_________Starting new loop___________' + '\n')
            debug.print_line('Date:'+ time.strftime('%a %d %b %y') + ', time: ' + time.strftime('%H:%M') + '\n')

            if hour in calibrate_hours:
                for output in output_adapters:
                    output.calibrate()

            design = MonthOvPanel((epd.width, epd.height))

            debug.print_line("Connecting to Openweathermap API servers...")
            owm = OwmForecasts.OwmForecasts(api_key)
            design.add_weather(OwmForecasts.OwmForecasts(api_key))
























            #"""Filter upcoming events from your iCalendar/s"""
            #debug.print_line('Fetching events from your calendar' + '\n')

            #events_cal = IcalEvents.IcalEvents(ical_urls)

            #for event in events_cal.get_month_events():
            #    debug.print_event(event)

            #upcoming = events_cal.get_upcoming_events()
            #events_this_month = events_cal.get_month_events()
            #events_this_month = [event.begin_datetime.day for event in events_this_month]

            #def takeDate (elem):
            #    return elem.begin_datetime

            #upcoming.sort(key=takeDate)

            #del upcoming[4:]
            ## uncomment the following 2 lines to display the fetched events
            ## from your iCalendar
            #debug.print_line('Upcoming events:')
            #debug.print_line(upcoming)
            #debug.print_line('Month events:')
            #debug.print_line(events_this_month)

            ##Credit to Hubert for suggesting truncating event names
            #def write_text_left (box_width, box_height, text, tuple):
            #    text_width, text_height = font.getsize(text)
            #    while (text_width, text_height) > (box_width, box_height):
            #        text=text[0:-1]
            #        text_width, text_height = font.getsize(text)
            #    y = int((box_height / 2) - (text_height / 2))
            #    space = Image.new('L', (box_width, box_height), color=255)
            #    ImageDraw.Draw(space).text((0, y), text, fill=0, font=font)
            #    image.paste(space, tuple)

            #"""Write event dates and names on the E-Paper"""
            #for dates in range(len(upcoming)):
            #    write_text(70, 25, (upcoming[dates].begin_datetime.strftime('%d %b')), date_positions['d' + str(dates + 1)])

            #for events in range(len(upcoming)):
            #    write_text_left(314, 25, (upcoming[events].title), event_positions['e' + str(events + 1)])

            #"""Draw smaller squares on days with events"""
            #for numbers in events_this_month:
            #    if numbers in cal[0]:
            #        draw(positions['a' + str(cal[0].index(numbers) + 1)], eventicon)
            #    if numbers in cal[1]:
            #        draw(positions['b' + str(cal[1].index(numbers) + 1)], eventicon)
            #    if numbers in cal[2]:
            #        draw(positions['c' + str(cal[2].index(numbers) + 1)], eventicon)
            #    if numbers in cal[3]:
            #        draw(positions['d' + str(cal[3].index(numbers) + 1)], eventicon)
            #    if numbers in cal[4]:
            #        draw(positions['e' + str(cal[4].index(numbers) + 1)], eventicon)
            #    try:
            #        if numbers in cal[5]:
            #            draw(positions['f' + str(cal[5].index(numbers) + 1)], eventicon)
            #    except IndexError:
            #        pass

            #"""Draw a larger square on today's date"""
            #today = time.day
            #if today in cal[0]:
            #    draw(positions['a' + str(cal[0].index(today) + 1)], dateicon)
            #if today in cal[1]:
            #    draw(positions['b' + str(cal[1].index(today) + 1)], dateicon)
            #if today in cal[2]:
            #    draw(positions['c' + str(cal[2].index(today) + 1)], dateicon)
            #if today in cal[3]:
            #    draw(positions['d' + str(cal[3].index(today) + 1)], dateicon)
            #if today in cal[4]:
            #    draw(positions['e' + str(cal[4].index(today) + 1)], dateicon)
            #try:
            #    if today in cal[5]:
            #        draw(positions['f' + str(cal[5].index(today) + 1)], dateicon)
            #except IndexError:
            #    pass

            for output in output_adapters:
                output.render(design)

            debug.print_line("Finished rendering")

            for i in range(1):
                nexthour = ((60 - int(time.strftime("%M"))) * 60) - (int(time.strftime("%S")))
                sleep(nexthour)

if __name__ == '__main__':
    main()
