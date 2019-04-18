from DataSourceInterface import DataSourceInterface
from datetime import datetime, timezone, timedelta

class RssInterface(DataSourceInterface):
    """Interface for fetching and processing rss post information."""
    def __init__(self):
        self.loaded_posts = []
        self.reload()

    def reload(self):
        if self.is_available() == False:
            return
        self.loaded_posts = self.__get_posts__()
        self.__sort_posts__()

    def __get_posts__(self):
        raise NotImplementedError("Functions needs to be implemented")

    def get_latest_posts(self, count=10):
        return self.loaded_posts[0:count]

    def get_today_posts(self):
        return self.get_day_posts(datetime.now())

    def get_day_posts(self, day):
        return self.__get_posts_to_filter__(lambda x : x.datetime.strftime('%d-%m-%y') == day.strftime('%d-%m-%y'))

    def __get_posts_to_filter__(self, post_filter):
        if self.loaded_posts is None:
            return []
        return [post for post in self.loaded_posts if post_filter(post)]

    def __sort_posts__(self):
        self.loaded_posts.sort(key=lambda x : x.datetime, reverse=True)