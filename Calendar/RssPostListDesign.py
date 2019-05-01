from DesignEntity import DesignEntity
from TableDesign import TableDesign
from Assets import defaultfontsize

class RssPostListDesign (DesignEntity):
    """Creates a TableDesign filled with rss post
    date and title"""
    def __init__ (self, size, rssfeed, text_size = defaultfontsize):
        super(RssPostListDesign, self).__init__(size)
        self.rssfeed = rssfeed
        self.__post_matrix__ = []
        self.text_size = text_size

    def __finish_image__ (self):
        self.__fill_post_matrix__()

        table_design = TableDesign(self.size, line_spacing=5, col_spacing=3, text_matrix=self.__post_matrix__, fontsize = self.text_size, mask=False, truncate_cols=False, wrap=True)
        self.draw_design(table_design)
    
    def __get_formatted_post__ (self, post):
        date = post.datetime.strftime('%d %b')
        date = self.__remove_leading_zero__(date)
        return [ '', '•', post.title ]

    def __remove_leading_zero__(self, text):
        while text[0] is '0':
            text = text[1:]
        return text
    
    def __fill_post_matrix__ (self):
        for post in self.rssfeed.get_latest_posts():
            row = self.__get_formatted_post__(post)
            self.__post_matrix__.append(row)