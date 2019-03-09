#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
E-Paper Software (main script) for the 3-colour and 2-Colour E-Paper display
A full and detailed breakdown for this code can be found in the wiki.
If you have any questions, feel free to open an issue at Github.

Copyright by aceisace
"""
from datetime import datetime
from time import sleep
from Assets import datetime_locals
import locale
from DebugConsole import DebugConsole
from settings import *
from MonthOvPanel import MonthOvPanel
from DayListPanel import DayListPanel
import OwmForecasts
import IcalEvents
import RssParserPosts

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

available_panels = {
    "day-list" : DayListPanel,
    "month-overview" : MonthOvPanel
}

"""Main loop starts from here"""
def main ():
    while True:

        time = datetime.now()
        hour = int(time.strftime("%H"))
        month = int(time.now().strftime('%m'))
        year = int(time.now().strftime('%Y'))

        for i in range(1):
            debug.print_line('_________Starting new loop___________')
            debug.print_line('Date: '+ time.strftime('%a %d %b %y') + ', time: ' + time.strftime('%H:%M') + '\n')

            if hour in calibrate_hours:
                for output in output_adapters:
                    output.calibrate()

            if choosen_design in available_panels.keys():            
                design = available_panels[choosen_design]((epd.width, epd.height))
            else:
                raise ImportError("choosen_design must be valid (" + choosen_design + ")")

            debug.print_line("Fetching weather information from open weather map")
            owm = OwmForecasts.OwmForecasts(location, api_key)
            design.add_weather(owm)

            debug.print_line('Fetching events from your calendar')
            events_cal = IcalEvents.IcalEvents(ical_urls)
            design.add_calendar(events_cal)

            debug.print_line('Fetching posts from your rss-feeds')
            rss = RssParserPosts.RssParserPosts(rss_feeds)
            design.add_rssfeed(rss)

            for output in output_adapters:
                output.render(design)

            debug.print_line("=> Finished rendering" + "\n")

            for i in range(1):
                nexthour = ((60 - int(time.strftime("%M"))) * 60) - (int(time.strftime("%S")))
                sleep(nexthour)

if __name__ == '__main__':
    main()
