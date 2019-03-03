from TextDesign import TextDesign

class TableTextDesign(TextDesign):
    """Gets a matrix with text that is than
    displayed in a table without borders."""
    def __init__(self, size, text_matrix, max_col_size=None, font = None, fontsize = 12, horizontalalignment = "left", verticalalignment = "top", mask = True):
        super(TableTextDesign, self).__init__(size, font=font, fontsize=fontsize, horizontalalignment=horizontalalignment, verticalalignment=verticalalignment, mask=mask)
        self.matrix = text_matrix
        self.max_col_size = max_col_size

    def __finish_image__(self):
        self.__reform_col_size__()
        self.cell_sizes = self.__get_cell_sizes__()
        self.__print_table__(self.matrix)


    def __reform_col_size__(self):
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

        self.max_col_size = col_sizes

    def __print_table__(self, matrix):
        for r, row in enumerate(matrix):
            for c, cell in enumerate(row):
                size = self.cell_sizes[r][c]
                pos = self.__get_cell_pos__(r,c)
                self.__draw_text__(pos, size, self.matrix[r][c])
                
    def __draw_text__(self, pos, size, text):
        design = TextDesign(size, text=text, font=self.font_family, fontsize=self.font_size, horizontalalignment=self.horizontal_alignment, verticalalignment=self.vertical_alignment)
        design.pos = pos
        self.draw_design(design)
        
    def __get_cell_pos__(self, row, col):
        xpos, ypos = (0, 0)
        for c in range(col):
            xpos += self.cell_sizes[row][c][0]
        for r in range(row):
            ypos += self.cell_sizes[r][col][1]
        return (xpos, ypos)

    def __get_cell_sizes__(self):
        size_matrix = []
        for r in range(len(self.matrix)):
            size_matrix.append([])
            for c in range(len(self.matrix[0])):
                size = (self.max_col_size[c], self.font_size)
                size_matrix[r].append(size)
        return size_matrix