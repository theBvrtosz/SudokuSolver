import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.config import Config
from kivy.metrics import sp

from time import sleep
import threading

Config.set('graphics','resizable', False)
Config.set('graphics', 'width', 540)
Config.set('graphics', 'height', 610)


class SudokuWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # getting the ids from the .kv file
        self.resolve_button = self.ids.resolve_button
        self.reset_button = self.ids.reset_button
        self.previous_grid_button = self.ids.previous_grid_button
        self.next_grid_button = self.ids.next_grid_button
        
        
        # reading grids from .txt
        self.grids = self._read_grids()
        self.current_grid = 1
        self.sudoku_table = self.grids[self.current_grid]

        # setting up the layout 
        self.sudoku_grid = GridLayout(cols=9, row_force_default=True, row_default_height= sp(60))

        # inntitializing the label grid with default first grid
        self.label_table = []
        self._init_grid(self.sudoku_grid ,self.sudoku_table, self.label_table)
        self.add_widget(self.sudoku_grid)

        self._disable_button(self.reset_button)
        self._disable_button(self.previous_grid_button)

    def _init_grid(self, grid, sudoku_grid, label_grid):
        """
        Method to initialize the sudoku grid to the GridLabel in the Window.
        Should be called only when initializing the Window
        
        Args:
            grid (GridLayout): GridLayout inside which the grid will be initialized
            sudoku_grid ([int]): list of int lists; imitation of the sudoku grid. 
                                 Contains that are to be respresented in with Labels inside grid
            label_grid (list): empty list. used to store the Labels that are the representations of the sudoku_grid
        """
        for row in range(9):
            label_grid.append([])
            for col in range(9):
                nbr = sudoku_grid[row][col]
                label = Label(font_size= sp(25), bold=True, color=[0,0,0,1])
                if nbr != 0:
                    label.text = str(nbr)
                else:
                    label.text = " "
                label_grid[row].append(label)
                grid.add_widget(label)

    # ---------- SUDOKU RESOLVING METHODS ----------
    
    def _is_empty(self):
        """method to seek for empty position inside the sudoku gid
        
        Returns:
            [(int, int)]: tuple representing the row and column(position) of the empty box.
                          if empty position not found returns None
        """
        for row in range(9):
            for col in range(9):
                if self.label_table[row][col].text == ' ':
                    return (row, col)
        return None

    def _is_available(self, row, col, nbr):
        """method to check if the nbr can be inserted in the row, col with respect to sudoku rules
        
        Args:
            row (int): numeric representation of the row of the sudoku gird
            col (int): numeric representation of the column of the sudoku gird
            nbr (int): number in range(1,10) to be in row, col in the sudoku grid
        
        Returns:
            boolean: return True if the number can placed in the row, col position. Returns False otherwise.
        """

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
        """
        Method to resolve the displayed sudoku gird and visualize the resolving proccess.
        Using recursive backtracking logic. 
        
        Returns:
            boolean: returns True if the grid is resolved. 
            Returns false if the value inserted in current call is making the grid unresolvable, 
            forces the algorithm to backtrack the changes
        """

        self._disable_button(self.resolve_button)
        self._disable_button(self.reset_button)
        self._disable_pick_grid_buttons()

        position = self._is_empty()
        if not position:
            self._enable_button(self.reset_button)
            self._enable_pick_grid_buttons()
            return True
        
        row, col = position

        for num in range(1,10):
            if self._is_available(row, col, str(num)):
                self.label_table[row][col].text = str(num)
                # sleep(0.025)
                if self._resolve():
                    return True

                self.label_table[row][col].text = " "
                # sleep(0.025)
        return False

    def btn_resolve(self):
        """method to run the _resolve method using threading
        """
        threading.Thread(target=self._resolve).start()

    def btn_reset(self):
        """method to run the _reset_grid method using threading
        """
        threading.Thread(target=self._reset_grid).start()

    # ---------- GUI MANAGEMENT METHODS ----------

    def _set_grid(self, grid_nbr):
        for row in range(9):
            for col in range(9):
                nbr = str(self.grids[grid_nbr][row][col])
                if nbr == "0":
                    self.label_table[row][col].text = ' '
                else:
                    self.label_table[row][col].text = nbr

    def _next_grid(self):
        self.current_grid += 1
        if self.current_grid == max(self.grids.keys()):
            self._disable_button(self.next_grid_button)

        if self.current_grid == min(self.grids.keys()) + 1:
            self._enable_button(self.previous_grid_button)

        if self.reset_button.state != 'disabled':
            self._disable_button(self.reset_button)
            self._enable_button(self.resolve_button)

        self._set_grid(self.current_grid)

    def _previous_grid(self):
        self.current_grid -= 1
        
        if self.current_grid == min(self.grids.keys()):
            self._disable_button(self.previous_grid_button)
        
        if self.current_grid == max(self.grids.keys()) - 1:
            self._enable_button(self.next_grid_button)
        
        if self.reset_button.state != 'disabled':
            self._disable_button(self.reset_button)
            self._enable_button(self.resolve_button)

        self._set_grid(self.current_grid)

    def _reset_grid(self):
        """Method to reset the resolved sudoku grid to the unresolved state
        """
        self._disable_button(self.reset_button)
        self._set_grid(self.current_grid)
        self._enable_button(self.resolve_button)
    
    @staticmethod
    def _disable_button(button):
        """method to handle all the actions while disabling button provided as an argument
        
        Args:
            button (Buton): Button to be disabled
        """
        button.background_color = (0, .3137, .0888, 0.5)
        button.disabled = True
    
    @staticmethod
    def _enable_button(button):
        """method to handle all the actions while enabling button provided as an argument
        
        Args:
            button (Buton): Button to be enabled
        """
        button.background_color = (0, .3137, .0888, 1)
        button.disabled = False

    def _disable_pick_grid_buttons(self):
        if self.next_grid_button.state != 'disabled':
            self._disable_button(self.next_grid_button)

        if self.previous_grid_button.state != 'disabled':
            self._disable_button(self.previous_grid_button)

    def _enable_pick_grid_buttons(self):
        if self.current_grid == min(self.grids.keys()):
            self._enable_button(self.next_grid_button)

        elif self.current_grid == max(self.grids.keys()):
            self._enable_button(self.previous_grid_button)

        else:
            self._enable_button(self.next_grid_button)
            self._enable_button(self.previous_grid_button)

    @staticmethod
    def _read_grids():
        grids = ''
        with open("sudoku_grids.txt") as grids_txt:
            for line in grids_txt:
                grids += line
        
        return eval(grids)

        
class SudokuApp(App):
    def build(self):
        self.root = SudokuWindow()
        return self.root

if __name__ == "__main__":
    SudokuApp().run()