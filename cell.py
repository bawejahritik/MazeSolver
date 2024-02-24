from graphics import Window, Line, Point

class Cell():
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self._visited = False
    
    def draw(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        if self._win is None:
            return
        self._x1 = top_left_x
        self._x2 = bottom_right_x
        self._y1 = top_left_y
        self._y2 = bottom_right_y

        # draw left line
        left_line = Line(Point(top_left_x, top_left_y), Point(top_left_x, bottom_right_y))
        if self.has_left_wall:
            self._win.draw_line(left_line)
        else:
            self._win.draw_line(left_line, 'white')

        # draw right line
        right_line = Line(Point(bottom_right_x, top_left_y), Point(bottom_right_x, bottom_right_y))
        if self.has_right_wall:
            self._win.draw_line(right_line)
        else:
            self._win.draw_line(right_line, 'white')
        
        # draw top line
        top_line = Line(Point(top_left_x, top_left_y), Point(bottom_right_x, top_left_y))
        if self.has_top_wall:
            self._win.draw_line(top_line)
        else:
            self._win.draw_line(top_line, 'white')

        # draw bottom line
        bottom_line = Line(Point(top_left_x, bottom_right_y), Point(bottom_right_x, bottom_right_y))
        if self.has_bottom_wall:
            self._win.draw_line(bottom_line)
        else:
            self._win.draw_line(bottom_line, 'white')
        
    def draw_move(self, to_cell, undo=False, fill_color="red"):
        if self._win is None:
            return 
        x_mid = (self._x1 + self._x2)/2
        y_mid = (self._y1 + self._y2)/2
        
        to_x_mid = (to_cell._x1 + to_cell._x2)/2
        to_y_mid = (to_cell._y1 + to_cell._y2)/2

        fill_color = fill_color
        
        if undo:
            fill_color = "gray"
        
        # move left
        if x_mid > to_x_mid:
            line = Line(Point(to_x_mid, to_y_mid), Point(x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)
        # move right
        if x_mid < to_x_mid:
            line = Line(Point(x_mid, to_y_mid), Point(to_x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)
        # move up
        if y_mid > to_y_mid:
            line = Line(Point(x_mid, to_y_mid) ,Point(x_mid, y_mid))
            self._win.draw_line(line, fill_color)
        # move down
        if y_mid < to_y_mid:
            line = Line(Point(x_mid, y_mid), Point(x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)