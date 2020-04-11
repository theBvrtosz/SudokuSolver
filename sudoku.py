import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.button import Button

from time import sleep
import threading

Config.set('graphics','resizable', False)
Config.set('graphics', 'width', 630)
Config.set('graphics', 'height', 700)


class SudokuWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # base grid 
        self.cols=1
        
        # sudoku grid
        self.sudoku_grid = GridLayout(cols=9, row_force_default=True, row_default_height=70)
        self.label_table = []
        self.sudoku_table = [
            [0,4,0,5,0,0,0,1,0],
            [0,6,0,8,4,0,0,0,0],
            [0,0,1,0,0,0,0,9,0],
            [5,0,0,0,0,0,4,0,1],
            [0,0,2,0,0,5,0,0,0],
            [1,0,0,0,0,3,0,0,7],
            [0,0,0,7,9,0,1,0,5],
            [0,0,0,0,0,2,0,4,0],
            [0,0,0,1,3,0,9,0,6]
            ]

        self._init_grid(self.sudoku_grid ,self.sudoku_table, self.label_table)


        # adding new grid layout to the 10th row of the self grid for button management
        self.button_grid = GridLayout(cols=2, pos_hint={'y':0,}, size_hint=(1,.1), padding=[10, 10], spacing=[10])

        self.resolve_button = Button()
        self.resolve_button.text = "resolve"
        self.resolve_button.bind(on_release=self.btn_resolve)
        self.button_grid.add_widget(self.resolve_button)

        self.reset_button = Button()
        self.reset_button.text = "reset"
        self.reset_button.bind(on_release=self.btn_reset)
        self.reset_button.disabled = True
        self.button_grid.add_widget(self.reset_button)

        # adding two grids to the self grid
        self.add_widget(self.sudoku_grid)
        self.add_widget(self.button_grid)

    @staticmethod
    def _init_grid(grid, sudoku_grid, label_grid):
        for row in range(9):
            label_grid.append([])
            for col in range(9):
                nbr = sudoku_grid[row][col]
                label = Label()
                label.font_size = 25
                label.bold = True
                if nbr != 0:
                    label.text = str(nbr)
                else:
                    label.text = "0"
                label_grid[row].append(label)
                grid.add_widget(label)
    
    def _is_empty(self):
        for row in range(9):
            for col in range(9):
                if self.label_table[row][col].text == '0':
                    return (row, col)
        return None

    def _is_available(self, row, col, nbr):

        for c in range(9):
            if self.label_table[row][c].text == nbr:
                return False
        
        for r in range(9):
            if self.label_table[r][col].text == nbr:
                return False

        base_row = row // 3 * 3
        base_col = col // 3 * 3

        for r in range(3):
            for c in range(3):
                if self.label_table[base_row + r][base_col + c].text == nbr:
                    return False
        return True

    def _resolve(self):
        self.resolve_button.disabled = True
        self.reset_button.disabled = True

        position = self._is_empty()
        if not position:
            self.reset_button.disabled = False
            return True
        
        row, col = position

        for num in range(1,10):
            if self._is_available(row, col, str(num)):
                self.label_table[row][col].text = str(num)
                sleep(0.00025)
                if self._resolve():
                    return True

                self.label_table[row][col].text = "0"
                sleep(0.00025)
        return False

    def _reset_grid(self):
        self.reset_button.disabled = True
        for row in range(9):
            for col in range(9):
                nbr = self.sudoku_table[row][col]
                if nbr != 0:
                    self.label_table[row][col].text = str(nbr)
                else:
                    self.label_table[row][col].text = "0"
                sleep(0.05)    
        self.resolve_button.disabled = False

    def btn_resolve(self, instance):
        threading.Thread(target=self._resolve).start()

    def btn_reset(self, instance):
        threading.Thread(target=self._reset_grid).start()
        
class SudokuApp(App):
    def build(self):
        return SudokuWindow()

if __name__ == "__main__":
    SudokuApp().run()