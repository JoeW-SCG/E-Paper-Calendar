from DesignEntity import DesignEntity
from TextDesign import TextDesign
from TableDesign import TableDesign
from Assets import wpath, weathericons, tempicon, humicon, windicon, no_response, colors, defaultfontsize
from PIL import Image
from settings import hours

icon_xpos = 0.1
icon_x_ypos = 0
icon_width = 1 - 2 * icon_xpos
info_x_ypos = icon_x_ypos + icon_width
info_yresize = -0.05
fontsize_static = defaultfontsize
max_symbol_y_width = 0.15


class WeatherColumnDesign (DesignEntity):
    """Displays weather information in a column"""

    def __init__(self, size, forecast):
        super().__init__(size)
        self.forecast = forecast

    def __finish_image__(self):
        if self.forecast is None:
            self.__draw_no_response__()
            return

        self.__draw_icon__(self.forecast.icon)
        self.__draw_infos__(self.forecast)

    def __draw_infos__(self, forecast):
        temperature = forecast.air_temperature + \
            " " + self.__get_unit__(("°C", "°F"))
        humidity = forecast.air_humidity + "%"
        if forecast.units == "aviation":
            if forecast.wind_deg == None:
                forecast.wind_deg = ""
            elif len(forecast.wind_deg) == 1:
                forecast.wind_deg = "00" + forecast.wind_deg
            elif len(forecast.wind_deg) == 2:
                forecast.wind_deg = "0" + forecast.wind_deg
            if int(forecast.wind_speed) < 10:
                windspeed = forecast.wind_deg + "@" + "0" + forecast.wind_speed + \
                    self.__get_unit__(
                        ("", ""))  # added degrees, if wind<10 add a 0 to make two digit
            else:
                windspeed = forecast.wind_deg + "@" + forecast.wind_speed + \
                    self.__get_unit__(("", ""))  # added degrees
        else:
            windspeed = forecast.wind_speed + " " + \
                self.__get_unit__(("km/h", "mph"))

        numbers_list = [[forecast.short_description],
                        [temperature],
                        [humidity],
                        [windspeed]]

        ypos = info_x_ypos * self.size[0]
        pos = (0, ypos)
        size = (self.size[0], self.size[1] +
                info_yresize * self.size[1] - pos[1])
        line_spacing = (size[1] - len(numbers_list) *
                        fontsize_static) / (len(numbers_list) + 1)

        table = TableDesign(size, numbers_list, fontsize=fontsize_static, line_spacing=line_spacing, column_horizontal_alignments=[
                            "center"], max_col_size=[size[0]], truncate_text=False, truncate_rows=False)
        table.pos = pos
        self.draw_design(table)

    def __draw_icon__(self, icon_id):
        width = int(icon_width * self.size[0])
        size = (width, width)
        xpos = icon_xpos * self.size[0]
        ypos = icon_x_ypos * self.size[0]
        pos = (xpos, ypos)

        self.__draw_resized_path_at__(
            wpath + weathericons[icon_id] + ".jpeg", pos, size)

    def __draw_no_response__(self):
        width = int(icon_width * self.size[0])
        size = (width, width)
        xpos = icon_xpos * self.size[0]
        ypos = icon_x_ypos * self.size[0]
        pos = (xpos, ypos)

        self.__draw_resized_image_at__(no_response, pos, size)

    def __draw_resized_path_at__(self, path, pos, size):
        img = Image.open(path)
        self.__draw_resized_image_at__(img, pos, size)

    def __draw_resized_image_at__(self, img, pos, size):
        size = (int(size[0]), int(size[1]))
        resized_img = img.resize(size, resample=Image.LANCZOS)
        self.draw(resized_img, pos)

    def __get_unit__(self, tuple):
        if self.forecast.units == "metric" or self.forecast.units == "aviation":
            return tuple[0]
        else:
            return tuple[1]

    def __abs_co__(self, coordinates):
        return (coordinates[0] * self.size[0], coordinates[1] * self.size[1])

    def __get_time__(self, time):
        if hours == "24":
            return time.strftime('%H:%M')
        else:
            return time.strftime('%I:%M')
