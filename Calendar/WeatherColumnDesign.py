from DesignEntity import DesignEntity
from TextDesign import TextDesign
from TableTextDesign import TableTextDesign
from Assets import wpath, weathericons, tempicon, humicon, windicon, no_response
from PIL import Image
from settings import hours

icon_xpos = 0.1
icon_x_ypos = -0.1
icon_width = 1 - 2 * icon_xpos
info_x_height = icon_width * 0.3
info_x_ypos = icon_x_ypos + icon_width
fontsize_y = 0.1
numbers_x_ypos = icon_x_ypos + icon_width + info_x_height + 0.1
numbers_x_ypadding = 0.05
max_symbol_y_width = 0.15

general_text_color = "black"
background_color = "white"

class WeatherColumnDesign (DesignEntity):
    """Displays weather information in a column"""
    def __init__ (self, size, forecast):
        super().__init__(size)
        self.forecast = forecast

    def __finish_image__ (self):
        if self.forecast is None:
            self.__draw_no_response__()
            return

        self.__draw_icon__(self.forecast.icon)
        self.__draw_info__(self.forecast.short_description)
        #self.__draw_number_symbols__()
        #self.__draw_numbers__(self.forecast)
        self.__draw_numbers_text__(self.forecast)

    def __draw_info__ (self, info):
        height = info_x_height * self.size[0]
        ypos = info_x_ypos * self.size[0]
        size = (self.size[0], height)
        pos = (0, ypos)

        txt = TextDesign(size, text=info, fontsize=height, horizontalalignment="center")
        txt.pos = pos
        self.draw_design(txt)

    def __draw_number_symbols__ (self):
        symbols = [ tempicon,
                   humicon,
                   windicon ]

        ypos = numbers_x_ypos * self.size[0]
        fontsize = fontsize_y * self.size[1]
        line_spacing = (self.size[1] - ypos - len(symbols) * fontsize) / len(symbols)
        line_height = fontsize + line_spacing
        
        width = line_height
        max_width = max_symbol_y_width * self.size[1]
        if width > max_width:
            width = max_width
        size = (width, width)
        pos = (0, ypos)

        for index, symbol in enumerate(symbols):
            sym_ypos = pos[1] + line_height * index
            self.__draw_resized_image_at__(symbol, (0, sym_ypos), size)

    def __draw_numbers__ (self, forecast):
        temperature = forecast.air_temperature + " " + self.__get_unit__(("°C", "°F"))
        humidity = forecast.air_humidity + "%"
        windspeed = forecast.wind_speed + " " + self.__get_unit__(("km/h", "mph"))

        numbers_list = [ [ temperature ],
                        [ humidity ],
                        [ windspeed ] ]

        fontsize = fontsize_y * self.size[1]
        ypadding = numbers_x_ypadding * self.size[0]
        ypos = numbers_x_ypos * self.size[0]
        line_spacing = (self.size[1] - ypos - len(numbers_list) * fontsize) / len(numbers_list)
        symbol_width = fontsize + line_spacing
        max_symbol_width = max_symbol_y_width * self.size[1]
        if symbol_width > max_symbol_width:
            symbol_width = max_symbol_width
        xpos = symbol_width
        pos = (xpos, ypos + ypadding)
        size = (self.size[0] - pos[0], self.size[1] - pos[1])

        table = TableTextDesign(size, numbers_list, fontsize=fontsize, line_spacing=line_spacing)
        table.pos = pos
        self.draw_design(table)

    def __draw_numbers_text__ (self, forecast):
        temperature = forecast.air_temperature + " " + self.__get_unit__(("°C", "°F"))
        humidity = forecast.air_humidity + "%"
        windspeed = forecast.wind_speed + " " + self.__get_unit__(("km/h", "mph"))
        sunrise = self.__get_time__(forecast.sunrise)
        sunset = self.__get_time__(forecast.sunset)

        numbers_list = [ [ temperature ],
                        [ humidity ],
                        [ windspeed ] ]

        fontsize = fontsize_y * self.size[1]
        ypos = numbers_x_ypos * self.size[0]
        line_spacing = (self.size[1] - ypos - len(numbers_list) * fontsize) / len(numbers_list)
        pos = (0, ypos)
        size = (self.size[0], self.size[1] - pos[1])

        table = TableTextDesign(size, numbers_list, fontsize=fontsize, line_spacing=line_spacing, column_horizontal_alignments=[ "center" ], max_col_size=[ size[0] ])
        table.pos = pos
        self.draw_design(table)

    def __draw_icon__ (self, icon_id):
        width = int(icon_width * self.size[0])
        size = (width, width)
        xpos = icon_xpos * self.size[0]
        ypos = icon_x_ypos * self.size[0]
        pos = (xpos, ypos)

        self.__draw_resized_path_at__(wpath + weathericons[icon_id] + ".jpeg", pos, size)

    def __draw_no_response__ (self):
        width = int(icon_width * self.size[0])
        size = (width, width)
        xpos = icon_xpos * self.size[0]
        ypos = icon_x_ypos * self.size[0]
        pos = (xpos, ypos)

        self.__draw_resized_image_at__(no_response, pos, size)

    def __draw_resized_path_at__ (self, path, pos, size):
        img = Image.open(path)
        self.__draw_resized_image_at__(img, pos, size)

    def __draw_resized_image_at__ (self, img, pos, size):
        size = (int(size[0]), int(size[1]))
        resized_img = img.resize(size, resample=Image.LANCZOS)
        self.draw(resized_img, pos)


    def __get_unit__ (self, tuple):
        if self.forecast.units == "metric":
            return tuple[0]
        else:
            return tuple[1]

    def __abs_co__ (self, coordinates):
        return (coordinates[0] * self.size[0], coordinates[1] * self.size[1])

    def __get_time__ (self, time):
        if hours == "24":
            return time.strftime('%H:%M')
        else:
            return time.strftime('%I:%M')