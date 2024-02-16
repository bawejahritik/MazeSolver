import time
import random
from cell import Cell

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        self._cells = [[Cell(self._win) for _ in range(self._num_rows)] for _ in range(self._num_cols)]

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i*self._cell_size_x
        x2 = x1 + self._cell_size_x
        y1 = self._y1 + j*self._cell_size_y
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return

        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            to_visit = []
            
            if i > 0 and not self._cells[i-1][j]._visited:
                to_visit.append((i-1, j))
            if i < self._num_cols-1 and not self._cells[i+1][j]._visited:
                to_visit.append((i+1, j))
            if j > 0 and not self._cells[i][j-1]._visited:
                to_visit.append((i, j-1))
            if j < self._num_rows-1 and not self._cells[i][j+1]._visited:
                to_visit.append((i, j+1))
            
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            next_index = random.randrange(len(to_visit))
            next_i = to_visit[next_index][0]
            next_j = to_visit[next_index][1]

            if next_i == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][j].has_left_wall = False
            
            if next_i == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][j].has_right_wall = False
            
            if next_j == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][next_j].has_top_wall = False
            
            if next_j == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][next_j].has_bottom_wall = False

            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._cells[i][j]._visited = False
    
    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        curr_cell = self._cells[i][j]
        curr_cell._visited = True
        if i == self._num_cols-1 and j == self._num_rows-1:
            return True

        if i > 0 and not self._cells[i-1][j]._visited and not curr_cell.has_left_wall:
            curr_cell.draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            curr_cell.draw_move(self._cells[i-1][j], undo=True)
        if i < self._num_cols-1 and not self._cells[i+1][j]._visited and not curr_cell.has_right_wall:
            curr_cell.draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            curr_cell.draw_move(self._cells[i+1][j], undo=True)
        if j > 0 and not self._cells[i][j-1]._visited and not curr_cell.has_top_wall:
            curr_cell.draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            curr_cell.draw_move(self._cells[i][j-1], undo=True)
        if j < self._num_rows-1 and not self._cells[i][j+1]._visited and not curr_cell.has_bottom_wall:
            curr_cell.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            curr_cell.draw_move(self._cells[i][j+1], undo=True)   
        return False          

