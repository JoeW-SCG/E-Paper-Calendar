from TextDesign import TextDesign
from TextWraper import wrap_text_with_font
from Assets import defaultfontsize, colors


default_props = {
    "color" : colors["fg"],
    "background_color" : colors["bg"]
}

class TableTextDesign (TextDesign):
    """Gets a matrix with text that is than
    displayed in a table without borders."""
    def __init__ (self, size, text_matrix, max_col_size = None, max_row_size = None, font = None, fontsize = defaultfontsize, column_horizontal_alignments = [], mask = True, line_spacing = 0, col_spacing = 0, truncate_rows = True, truncate_cols = True, wrap = False, truncate_text=True, truncate_suffix="...", cell_properties=None, background_color = colors["bg"]):
        super(TableTextDesign, self).__init__(size, font=font, fontsize=fontsize, mask=mask)
        self.__init_image__(background_color)
        self.matrix = text_matrix
        self.max_col_size = max_col_size
        self.max_row_size = max_row_size
        self.line_spacing = line_spacing
        self.col_spacing = col_spacing
        self.truncate_rows = truncate_rows
        self.truncate_cols = truncate_cols
        self.max_row = None
        self.max_col = None
        self.column_horizontal_alignments = column_horizontal_alignments
        self.wrap = wrap
        self.truncate_text = truncate_text
        self.truncate_suffix = truncate_suffix
        self.cell_properties = cell_properties

    def __finish_image__ (self):
        if len(self.matrix) is 0:
            return
        self.__reform_col_size__()
        self.__reform_row_size__()
        self.cell_sizes = self.__get_cell_sizes__()
        self.max_col, self.max_row = self.__get_truncated_counts__()
        self.__print_table__(self.matrix)

    def __reform_col_size__ (self):
        if self.max_col_size is not None:
            return
        
        font = self.__get_font__()
        col_sizes = []
        for c in range(len(self.matrix[0])):    #amout of columns
            for r in range(len(self.matrix)):
                row_col_size = font.getsize(self.matrix[r][c])[0]    #get width of text in that row/col
                if len(col_sizes) - 1 < c:
                    col_sizes.append(row_col_size)
                elif row_col_size > col_sizes[c]:
                    col_sizes[c] = row_col_size
        
        for index, size in enumerate(col_sizes):
            preceding_size = sum(col_sizes[:index])
            if preceding_size + size > self.size[0]:
                col_sizes[index] = self.size[0] - preceding_size
                break

        self.max_col_size = col_sizes

    def __reform_row_size__ (self):
        if self.max_row_size is not None:
            return
        
        font = self.__get_font__()
        row_sizes = []
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[0])):    #amout of columns
                cell_text = self.matrix[r][c]
                if self.wrap:
                    cell_text = wrap_text_with_font(cell_text, self.max_col_size[c], font)
                col_row_size = font.getsize_multiline(cell_text)[1]    #get height of text in that col/row
                if len(row_sizes) - 1 < r:
                    row_sizes.append(col_row_size)
                elif col_row_size > row_sizes[r]:
                    row_sizes[r] = col_row_size
        
        self.max_row_size = row_sizes

    def __get_truncated_counts__ (self):
        max_col = 0
        if self.truncate_cols:
            while max_col < len(self.matrix[0]) and self.__get_cell_pos__(0, max_col + 1)[0] - self.col_spacing <= self.size[0]:
                max_col += 1
        else:
            max_col = len(self.matrix[0])

        max_row = 0
        if self.truncate_rows:
            while max_row < len(self.matrix) and self.__get_cell_pos__(max_row + 1,0)[1] - self.line_spacing <= self.size[1]:
                max_row += 1
        else:
            max_row = len(self.matrix)

        return (max_col, max_row)

    def __print_table__ (self, matrix):
        for r in range(self.max_row):
            for c in range(self.max_col):
                size = self.cell_sizes[r][c]
                pos = self.__get_cell_pos__(r,c)
                self.__draw_text__(pos, size, r, c)
                
    def __draw_text__ (self, pos, size, row, col):
        color = self.__get_cell_prop__(row, col, "color")
        bg_color = self.__get_cell_prop__(row, col, "background_color")

        design = TextDesign(size, text=self.matrix[row][col], font=self.font_family, color=color, background_color=bg_color, fontsize=self.font_size, horizontalalignment=self.__get_col_hori_alignment__(col), wrap=self.wrap, truncate=self.truncate_text, truncate_suffix=self.truncate_suffix)
        design.pos = pos
        self.draw_design(design)
        
    def __get_cell_pos__ (self, row, col):
        xpos, ypos = (0, 0)
        for c in range(col):
            xpos += self.cell_sizes[row][c][0]
            xpos += self.col_spacing
        for r in range(row):
            ypos += self.cell_sizes[r][col][1]
            ypos += self.line_spacing
        return (xpos, ypos)

    def __get_cell_sizes__ (self):
        size_matrix = []
        for r in range(len(self.matrix)):
            size_matrix.append([])
            for c in range(len(self.matrix[0])):
                size = (self.max_col_size[c], int(self.max_row_size[r]))
                size_matrix[r].append(size)
        return size_matrix

    def __get_col_hori_alignment__ (self, c):
        if len(self.column_horizontal_alignments) <= c:
            return "left"
        return self.column_horizontal_alignments[c]

    def __get_cell_prop__(self, r, c, prop):
        if self.cell_properties is None:
            return default_props[prop]
        try:
            return self.cell_properties[r][c][prop]
        except:
            return default_props[prop]