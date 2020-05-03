'''
Program that solves sudoku. It can solve any solvable sudoku, but it has
only one to show for it.
App uses Kivy GUI libraries for graphics.

Krzysztof Kaźmierczuk
'''

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from functools import partial


# Find empty cells on the sudoku board
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

# Solve the board by guessing the nr and checking if threre's no conflicts
# e.g. 2 ssame nr in a row or column
# Using backtracking
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False

# Function checs if same nr in a row or column
def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

# Window class containing all GUI
class Sudoku(App):

    WINDOW_SIZE = 400 # Size in pixels
    # example board
    board = [
                [7,8,0,4,0,0,1,2,0],
                [6,0,0,0,7,5,0,0,9],
                [0,0,0,6,0,1,0,7,8],
                [0,0,7,0,4,0,2,6,0],
                [0,0,1,0,5,0,9,3,0],
                [9,0,4,0,6,0,0,0,5],
                [0,7,0,3,0,0,0,1,2],
                [1,2,0,0,0,7,4,0,0],
                [0,4,9,2,0,6,0,0,7]
            ]

    # Show all numbers in the window
    def show_nums(self, canv):
        cell_size = self.WINDOW_SIZE//9

        for y in range(9):
            for x in range(9):
                num = str(self.board[8-y][x])
                if num == '0':
                    num = ' '
                canv.add_widget(Label(text=num, markup=True, font_size='36', color=[.7,.7,.8], pos=(cell_size*x-26, cell_size*y-26)))

    # Draw a grid
    def show_grid(self, canv):
        with canv.canvas:
            # define color
            Color(.7, .7, .9)
            # Add a rectangle
            for i in range(1, 9):
                if i == 3 or i == 6:
                    bar_size = 4
                else:
                    bar_size = 2

                Rectangle(pos=(self.WINDOW_SIZE//9 * i, 0), size=(bar_size, self.WINDOW_SIZE))
                Rectangle(pos=(0, self.WINDOW_SIZE//9 * i), size=(self.WINDOW_SIZE, bar_size))

    # What happens after pressing the (only) button
    def solve_sudoku(self, canv, *args):
        solve(self.board)
        canv.canvas.clear()
        self.show_grid(canv)
        self.show_nums(canv)

    # Neccessary function for kivy. Start the windaw and attach widgets
    def build(self):
        # Set size of the window
        Config.set('graphics', 'width', self.WINDOW_SIZE)
        Config.set('graphics', 'height', self.WINDOW_SIZE)
        root = BoxLayout(orientation='vertical')
        canv = Widget()
        btn = Button(text='solve',
                            on_press=partial(self.solve_sudoku, canv))
        # Next lines are responsible for attaching all the gfx to the window
        canv.add_widget(btn)
        self.show_nums(canv)
        self.show_grid(root)
        root.add_widget(canv)


        return root # Return the window content


if __name__ == '__main__':
    Sudoku().run() # Runs Kivy GUI
