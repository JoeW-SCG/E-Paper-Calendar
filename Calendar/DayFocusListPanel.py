from datetime import date, datetime, timedelta, timezone
from settings import line_thickness, general_settings
from DayHeaderDesign import DayHeaderDesign
from HourListDesign import HourListDesign
from DayRowDesign import DayRowDesign
from PanelDesign import PanelDesign
from Assets import colors
from PIL import ImageDraw

HEADER_SIZE = (1, 0.2)
HOURLIST_HEIGHT = 0.3
HOURLIST_SIZE = (1, HOURLIST_HEIGHT)
DAYLIST_YPOS = HEADER_SIZE[1] + HOURLIST_SIZE[1]
DAYLIST_HEIGHT = 1 - HEADER_SIZE[1] - HOURLIST_SIZE[1]
DAYLIST_SIZE = (1, DAYLIST_HEIGHT)
HOURS_COUNT = 6
DAYROW_MIN_FORMAT = 40 / 384
DAYROW_MAX_FORMAT = 60 / 384
PANEL_LINE_THICKNESS = line_thickness


class DayFocusListPanel (PanelDesign):
    """Shows Day-View for today and a short Day-List for
    the upcoming days."""

    def __init__(self, size):
        super(DayFocusListPanel, self).__init__(size)
        self.hours_count = HOURS_COUNT
        self.__init_modules__()

    def __abs_co__(self, coordinates):
        return (int(coordinates[0] * self.size[0]), int(coordinates[1] * self.size[1]))

    def __init_modules__(self):
        self.__init_header__()
        self.__init_hourlist__()
        self.__init_daylist__()

    def __init_header__(self):
        self.__header__ = DayHeaderDesign(
            self.__abs_co__(HEADER_SIZE), date.today())
        self.__header__.pos = (0, 0)

    def __init_hourlist__(self):
        start, end = self.__get_current_hour_range__()
        size = self.__abs_co__(HOURLIST_SIZE)

        self.__hourlist__ = HourListDesign(size, start, end)
        self.__hourlist__.pos = (0, self.__header__.size[1])

    def __init_daylist__(self):
        self.__daylist_rows__ = []
        self.__calc_dayrow_size__()
        self.__create_day_rows__()

    def __calc_dayrow_size__(self):
        max_area_height = DAYLIST_HEIGHT * self.size[1]
        max_row_number = max_area_height / (DAYROW_MIN_FORMAT * self.size[0])
        min_row_number = max_area_height / (DAYROW_MAX_FORMAT * self.size[0])
        average_row_number = (max_row_number + min_row_number) / 2
        self.dayrow_count = round(average_row_number)
        row_height = max_area_height / self.dayrow_count
        self.dayrow_size = (1, row_height / self.size[1])

    def __create_day_rows__(self):
        following_days = self.__get_following_days__()
        for i, date in enumerate(following_days):
            row = DayRowDesign(self.__abs_co__(self.dayrow_size), date)
            row.pos = self.__get_day_row_pos__(i)
            self.__daylist_rows__.append(row)

    def __get_following_days__(self):
        following_days = []
        for i in range(self.dayrow_count):
            following_days.append(date.today() + timedelta(days=i + 1))
        return following_days

    def __get_day_row_pos__(self, i):
        ypos = self.size[1] * DAYLIST_YPOS
        down_shift = i * self.dayrow_size[1] * self.size[1]
        return (0, int(ypos + down_shift))

    def __finish_panel__(self):
        self.draw_design(self.__header__)
        self.draw_design(self.__hourlist__)

        for row in self.__daylist_rows__:
            self.draw_design(row)
        self.__draw_daylist_lines__()

    def __draw_daylist_lines__(self):
        positions = []
        for i in range(len(self.__daylist_rows__)):
            positions.append(self.__get_day_row_pos__(i)[1])
        for ypos in positions:
            line_start = (0, ypos)
            line_end = (self.size[0], ypos)
            ImageDraw.Draw(self.__image__).line(
                [line_start, line_end], fill=colors["fg"], width=PANEL_LINE_THICKNESS)

    def __get_current_hour_range__(self):
        start_hour = datetime.now().hour
        additional_hours = self.hours_count - 1

        if start_hour + additional_hours > 23:
            start_hour = 23 - additional_hours

        return start_hour, start_hour + additional_hours

    def add_weather(self, weather):
        self.__header__.add_weather(weather)

    def add_calendar(self, calendar):
        allday_ev, timed_ev = self.__split_events__(
            calendar.get_today_events())
        self.__header__.add_events(allday_ev)
        self.__hourlist__.add_events(timed_ev)

        self.__add_calendar_daylist__(calendar)

    def __split_events__(self, events):
        allday_ev = []
        timed_ev = []

        for event in events:
            if event.allday:
                allday_ev.append(event)
            elif event.multiday:
                if self.__is_today__(event.begin_datetime):
                    timed_ev.append(event)
                elif self.__is_today__(event.end_datetime):
                    timed_ev.append(event)
                else:
                    allday_ev.append(event)
            else:
                timed_ev.append(event)
        return allday_ev, timed_ev

    def __is_today__(self, dt):
        today = date.today()
        return dt.day == today.day and \
            dt.month == today.month and \
            dt.year == today.year

    def __add_calendar_daylist__(self, calendar):
        calendar.exclude_calendars(general_settings["extra-excluded-urls"])

        for row in self.__daylist_rows__:
            row.add_calendar(calendar)

        calendar.exclude_calendars()
