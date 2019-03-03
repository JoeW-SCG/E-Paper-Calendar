from TextDesign import TextDesign

class TableTextDesign (TextDesign):
    """Gets a matrix with text that is than
    displayed in a table without borders."""
    def __init__ (self, size, text_matrix, max_col_size = None, font = None, fontsize = 12, column_horizontal_alignments=[], mask = True, line_spacing = 0, col_spacing = 0, truncate_rows = True, truncate_cols = True):
        super(TableTextDesign, self).__init__(size, font=font, fontsize=fontsize, mask=mask)
        self.matrix = text_matrix
        self.max_col_size = max_col_size
        self.line_spacing = line_spacing
        self.col_spacing = col_spacing
        self.truncate_rows = truncate_rows
        self.truncate_cols = truncate_cols
        self.max_row = None
        self.max_col = None
        self.column_horizontal_alignments = column_horizontal_alignments

    def __finish_image__ (self):
        self.__reform_col_size__()
        self.cell_sizes = self.__get_cell_sizes__()
        self.max_col, self.max_row = self.__get_truncated_counts__()
        self.__print_table__(self.matrix)


    def __reform_col_size__ (self):
        if self.max_col_size is not None:
            return
        
        partial_col_spacing = int(self.col_spacing * (len(self.matrix[0]) - 1) / len(self.matrix[0]) - 1)
        font = self.__get_font__()
        col_sizes = []
        for c in range(len(self.matrix[0])):    #amout of columns
            for r in range(len(self.matrix)):
                row_col_size = font.getsize(self.matrix[r][c])[0]    #get width of text in that row/col
                if len(col_sizes) - 1 < c:
                    col_sizes.append(row_col_size)
                elif row_col_size > col_sizes[c]:
                    col_sizes[c] = row_col_size
        
        self.max_col_size = [size - partial_col_spacing for size in col_sizes]

    def __get_truncated_counts__ (self):
        max_col = 0
        if self.truncate_cols:
            while max_col < len(self.matrix[0]) and self.__get_cell_pos__(0, max_col + 1)[0] <= self.size[0]:
                max_col += 1
        else:
            max_col = len(self.matrix[0])

        max_row = 0
        if self.truncate_rows:
            while max_row < len(self.matrix) and self.__get_cell_pos__(max_row + 1,0)[1] <= self.size[1]:
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
        design = TextDesign(size, text=self.matrix[row][col], font=self.font_family, fontsize=self.font_size, horizontalalignment=self.__get_col_hori_alignment__(col))
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
        partial_col_spacing = int(self.col_spacing * (len(self.matrix[0]) - 1) / len(self.matrix[0]) - 1)
        size_matrix = []
        for r in range(len(self.matrix)):
            size_matrix.append([])
            for c in range(len(self.matrix[0])):
                size = (self.max_col_size[c] - partial_col_spacing, int(self.font_size * 1.1))
                size_matrix[r].append(size)
        return size_matrix

    def __get_col_hori_alignment__ (self, c):
        if len(self.column_horizontal_alignments) <= c:
            return "left"
        return self.column_horizontal_alignments[c]