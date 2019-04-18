from RssInterface import RssInterface
from datetime import datetime, timedelta, date
import feedparser
import RssPost
from urllib.request import urlopen

max_range_days = 14

class RssParserPosts (RssInterface):
    """Fetches posts from url-addresses via rss parser."""
    def __init__(self, urls):
        self.urls = urls
        super(RssParserPosts, self).__init__()

    def is_available(self):
        try:
            urlopen("https://google.com", timeout=2)
            return True
        except:
            return False

    def __get_posts__(self):
        posts = []

        today = date.today()
        time_span = today - timedelta(days=max_range_days)

        for feeds in self.urls:
            parse = feedparser.parse(feeds)
            for post in parse.entries:
                parsed_post = self.__parse_post__(post)
                if parsed_post.datetime.date() >= time_span:
                    posts.append(parsed_post)
        return posts

    def __parse_post__(self, post):
        parsed_post = RssPost.RssPost()
        parsed_post.fetch_datetime = datetime.now()

        parsed_post.title = post.title
        parsed_post.description = post.description
        parsed_post.source = self.__get_webpage__(post.link)
        parsed_post.datetime = datetime(*post.published_parsed[:6])

        return parsed_post

    def __get_webpage__(self, link):
        start_index = link.find('://') + 3
        end_index = link[start_index:].find('/') + start_index
        return link[start_index : end_index]
        