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
from LoopTimer import LoopTimer
import locale
from DebugConsole import DebugConsole
from settings import *
from MonthOvPanel import MonthOvPanel
from DayListPanel import DayListPanel
from DayViewPanel import DayViewPanel
from AgendaListPanel import AgendaListPanel
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
    "month-overview" : MonthOvPanel,
    "day-view" : DayViewPanel,
    "agenda-list" : AgendaListPanel
}

loop_timer = LoopTimer(update_interval, run_on_hour=True)

"""Main loop starts from here"""
def main():
    owm = OwmForecasts.OwmForecasts(location, api_key, paid_api=owm_paid_subscription)

    while True:
        loop_timer.begin_loop()
        start_time = loop_timer.get_current()[0]

        if start_time.hour in calibrate_hours and loop_timer.is_new_hour_loop():
            debug.print_line("Calibrating outputs")
            for output in output_adapters:
                output.calibrate()

        if choosen_design in available_panels.keys():            
            design = available_panels[choosen_design]((epd.width, epd.height))
        else:
            raise ImportError("choosen_design must be valid (" + choosen_design + ")")

        debug.print_line("Fetching weather information from open weather map")
        design.add_weather(owm)

        debug.print_line('Fetching events from your calendar')
        events_cal = IcalEvents.IcalEvents(ical_urls, highlighted_ical_urls)
        design.add_calendar(events_cal)

        debug.print_line('Fetching posts from your rss-feeds')
        rss = RssParserPosts.RssParserPosts(rss_feeds)
        design.add_rssfeed(rss)

        debug.print_line("\nStarting to render")
        for i, output in enumerate(output_adapters):
            output.render(design)
            debug.print_line(str(i + 1) + " of " + str(len(output_adapters)) + " rendered")

        debug.print_line("=> Finished rendering" + "\n")

        loop_timer.end_loop()
        sleep_time = loop_timer.time_until_next()

        debug.print_line("This loop took " + str(loop_timer.get_last_duration()) + " to execute.")
        debug.print_line("Sleeping " + str(sleep_time) + " until next loop.")
        sleep(sleep_time.total_seconds())

if __name__ == '__main__':
    main()
