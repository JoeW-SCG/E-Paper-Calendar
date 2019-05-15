from DesignEntity import DesignEntity
from Assets import no_response, windicon, tempicon, sunseticon, sunriseicon, wpath, weathericons, humicon
from TextDesign import TextDesign
from settings import units, hours

wiconplace = (0, 0)
tempplace = (0.779, 0)
humplace = (0.779, 0.486)
windiconspace = (0.206, 0)
sunriseplace = (0.55, 0)
sunsetplace = (0.55, 0.486)

class WeatherHeaderDesign (DesignEntity):
    """Defines a top area that displays basic weather information"""
    def __init__ (self, size, weather):
        super(WeatherHeaderDesign, self).__init__(size)
        self.__weather__ = weather
        self.__first_render__()

    def __first_render__ (self):
        if self.__weather__.is_available() is False:
            self.__render_missing_connection__()
            return

        cur_weather = self.__weather__.get_today_forecast()

        if cur_weather == None:
            self.__render_missing_connection__()
            return

        temperature = cur_weather.air_temperature + " " + self.__get_unit__(("°C", "°F"))
        if units== "aviation": #pick up aviation
            if int(cur_weather.wind_speed)<10:
                windspeed = cur_weather.wind_deg + "@" + "0" + cur_weather.wind_speed  + self.__get_unit__(("", "")) #added degrees, if wind<10 add a 0 to make two digit
            else:
                windspeed = cur_weather.wind_deg + "@" + cur_weather.wind_speed  + self.__get_unit__(("", "")) #added degrees
        else:
            windspeed = cur_weather.wind_speed + " " + self.__get_unit__(("km/h", "mph"))

        self.__draw_text__(temperature, self.__abs_pos__((0.87, 0)), (50,35))
        self.__draw_text__(windspeed, self.__abs_pos__((0.297, 0.05)), (100,35))
        self.__draw_text__(self.__get_time__(cur_weather.sunrise), self.__abs_pos__((0.64,0)), (50,35))
        self.__draw_text__(self.__get_time__(cur_weather.sunset), self.__abs_pos__((0.64,0.486)), (50,35))
        self.__draw_text__(cur_weather.air_humidity + " %", self.__abs_pos__((0.87,0.486)), (50,35))
        self.__draw_text__(cur_weather.short_description, self.__abs_pos__((0.182,0.486)), (144,35))

        self.draw(windicon, self.__abs_pos__(windiconspace))
        self.draw(sunseticon, self.__abs_pos__(sunsetplace))
        self.draw(sunriseicon, self.__abs_pos__(sunriseplace))
        self.draw(humicon, self.__abs_pos__(humplace))
        self.draw(tempicon, self.__abs_pos__(tempplace))
        self.draw_image(wpath + weathericons[cur_weather.icon] + '.jpeg', self.__abs_pos__(wiconplace))

    def __render_missing_connection__ (self):
        self.draw(no_response, self.__abs_pos__(wiconplace))

    def __abs_pos__ (self, pos):
        return (int(pos[0] * self.size[0]), int(pos[1] * self.size[1]))

    def __draw_text__ (self, text, pos, size):
        txt = TextDesign(size, fontsize=18, text=text, verticalalignment="center", horizontalalignment="center")
        txt.pos = pos
        self.draw_design(txt)

    def __get_unit__ (self, tuple):
        if units == "metric" or units == "aviation":
            return tuple[0]
        else:
            return tuple[1]

    def __get_time__ (self, time):
        if hours == "24":
            return time.strftime('%H:%M')
        else:
            return time.strftime('%I:%M')
