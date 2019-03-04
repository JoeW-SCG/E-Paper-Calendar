from DesignEntity import DesignEntity
from TableTextDesign import TableTextDesign

col_sizes = [0.15, 0.85]

class RssPostListDesign (DesignEntity):
    """Creates a TableTextDesign filled with rss post
    date and title"""
    def __init__ (self, size, rssfeed, text_size = 16):
        super(RssPostListDesign, self).__init__(size)
        self.rssfeed = rssfeed
        self.__post_matrix__ = []
        self.text_size = text_size

    def __finish_image__ (self):
        self.__fill_post_matrix__()
        
        max_col_size = [int(col_sizes[0] * self.size[0]), int(col_sizes[1] * self.size[0])]
        col_hori_alignment = ['right', 'left']

        table_design = TableTextDesign(self.size, line_spacing=3, col_spacing=10, text_matrix=self.__post_matrix__, fontsize = self.text_size, column_horizontal_alignments=col_hori_alignment, mask=False, max_col_size = max_col_size, truncate_cols=False)
        self.draw_design(table_design)
    
    def __get_formatted_post__ (self, post):
        date = post.datetime.strftime('%d %b')
        date = self.__remove_leading_zero__(date)
        return [ date, post.title ]

    def __remove_leading_zero__(self, text):
        while text[0] is '0':
            text = text[1:]
        return text
    
    def __fill_post_matrix__ (self):
        for post in self.rssfeed.get_latest_posts():
            row = self.__get_formatted_post__(post)
            self.__post_matrix__.append(row)