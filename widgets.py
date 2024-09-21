from __future__ import annotations

from textual.containers import Center, Grid
from textual.widgets import Static, Digits
from textual.message import Message
from textual.reactive import var
from textual.timer import Timer
from textual.app import ComposeResult, App
from textual import work
from textual.events import Key

from datetime import datetime

from typing import Optional

from time import monotonic

from sudoku import Sudoku

class CenteredButton(Center):

    DEFAULT_CSS = """
        CenteredButton {
            margin: 1;
        }
    """

    def __init__(self, btn_name: str, btn_id: str | None = None) -> None:
        self.btn_name = btn_name
        self.btn_id = btn_id
        super().__init__()

    def compose(self):
        yield CustomButton(self.btn_name, id=self.btn_id)

class CustomButton(Static):
    
    DEFAULT_CSS = """
    CustomButton {
        background: $success-lighten-3 5%;
        border: round #0F0;
        color: #0A0;
        padding: 0 1;
        width: auto;
    }

    CustomButton:hover {
        color: #0F0;
    }

    """

    class Clicked(Message):
        def __init__(self, custom_button: CustomButton) -> None:
            self.custom_button = custom_button
            super().__init__()
              # Reference to the button instance (control)

        @property
        def control(self) -> CustomButton:
            return self.custom_button

    def on_click(self) -> None:
        # Post the Clicked message with the current instance (`self`) as control
        self.post_message(self.Clicked(self))


class DigitalClock(Static):
    DEFAULT_CSS = """
    DigitalClock {
        color: #0F0;
        text-style: bold;
        dock: bottom;
        text-align: right;
    }
    """

    def update_time(self) -> None:
        self.update(datetime.now().strftime("%H:%M:%S"))

    def on_mount(self) -> None:
        self.update_time()
        self.set_interval(1, self.update_time)

class CustomTimer(Digits):

    DEFAULT_CSS = """
        CustomTimer {
            width: auto;
            padding: 1;
            border: hkey #0F0;
            border-title-align: center;
            border-title-style: bold italic;
        }
    """
  
    BORDER_TITLE = "TIMER"

    start_time: Optional[float] = None
    total_time: float = 0.0
    pause: var[bool] = var(True, init=False)

    def spended_time(self) -> float:
        if self.start_time is None:
            return 0.0
        return self.total_time + monotonic() - self.start_time
    
    def update_display(self) -> None:
        minutes, seconds = divmod(self.spended_time(), 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")


    def on_mount(self) -> None:
        self.update_display()
        self.timer: Timer = self.set_interval(1, self.update_display, pause=self.pause)

    def watch_pause(self) -> None:
        #self.app.notify("Inside Watch")
        if self.pause:
            self.timer.pause()
        else:
            self.timer.resume()
        

    def start_timer(self) -> None:
        if self.pause:
            self.start_time = monotonic()
            self.pause = False
        else:
            self.app.notify("Timer is already Running!")

    def stop_timer(self) -> None:
        if self.pause:
            self.app.notify("Timer is already Stopped!")
        else:
            self.pause = True
            self.total_time = self.spended_time()
            
    def reset_timer(self) -> None:
        self.pause = True
        self.start_time = None
        self.total_time = 0.0
        self.update_display()

class SimpleCounter(Static):

    DEFAULT_CSS = """
       SimpleCounter {
            width: 15;
            height: 7;
            align: center middle;
            border: hkey #0F0;
            border-title-align: center;
            border-title-style: bold italic;
        
            Digits {
                width: auto;
            }
        }
    """

    BORDER_TITLE = "MOVES"

    value = 0

    def compose(self) -> ComposeResult:
        self.counter_display = Digits(str(self.value))
        yield self.counter_display

    def increment(self) -> None:
        self.value += 1
        self.counter_display.update(str(self.value))

class Cell(Static):

    DEFAULT_CSS = """
        Cell {
            height: 1;
            width: 3;
            text-align: center;
            color: #0F0;

            &.selected {
                background: $surface-lighten-3; 
            }

            &.neighbour {
                background: $success-lighten-3 10%; 
            }

            &.built-in {
                color: white 50%;
                text-style: italic;
            }
            &.error {
                color: red;
            }
        }

    """

    class Clicked(Message):
        def __init__(self, cell):
            self.cell = cell
            super().__init__()

    selected: var[bool] = var(False, init=False)
    digit: var[int] = var(0, init=False)

    def __init__(self, digit: int | None, row_index: int, col_index: int) -> None:
        super().__init__()
        self.row: int = row_index
        self.col: int = col_index
        self.digit = digit
        if self.digit:
            self.add_class('built-in')

    def on_click(self) -> None:
        self.post_message(self.Clicked(self))

    def watch_digit(self):
        if self.digit:
            self.update(str(self.digit))
        else:
            self.update('')

    def watch_selected(self):
        # self.app.notify(str(self.selected))
        if self.selected and not self.has_class('selected'):
            self.add_class('selected')
        else:
            if self.has_class('selected'):
                self.remove_class('selected')

    def __str__(self):
        return f"({self.row}, {self.col})"

class SudokuGrid3X3(Grid, can_focus=True):

    DEFAULT_CSS = """
        SudokuGrid3X3 {
            box-sizing: content-box;
            grid-size: 9;
            width: 40;
            height: 23;
            padding-top: 2;
            padding-left: 1;
            keyline: thin $success-darken-3;
            background: $success-lighten-3 15%;
            grid-gutter: 0 1;
        }

        SudokuGrid3X3:focus {
            border: vkey green;
        }

    """

    def __init__(self) -> None:
        self.puzzle = Sudoku(3).difficulty(0.5).board
        super().__init__()

    def compose(self) -> ComposeResult:
        self.cells = [
            [Cell(digit, row_in, col_in) for col_in, digit in enumerate(row)]
            for row_in, row in enumerate(self.puzzle)
            # [Cell(str((row * 9 + col) % 10), row, col) for col in range(9)]
            # for row in range(9)
        ]
        for row in self.cells:
            yield from row

    # def on_blur(self) -> None:
    #     if self.selected_cell:
    #         self.selected_cell.selected = False
    #         self.selected_cell = None

    def on_mount(self) -> None:
        # To track the currently selected cell
        self.selected_cell = None

    def select_cell(self, cell) -> None:
        cell.selected = True
        self.selected_cell = cell

    def select_neighbours(self):
        prev_neighbour_cells = set(self.query_children('.neighbour'))
        curr_neighbour_cells = set(self.neighbour_cells())
        
        # Remove the class from cells that are no longer neighbors
        for cell in (prev_neighbour_cells - curr_neighbour_cells):
            cell.remove_class('neighbour')

        # Add the class to new neighbor cells
        for cell in (curr_neighbour_cells - prev_neighbour_cells):
            cell.add_class('neighbour')


    def neighbour_cells(self, cell: Cell = None):
        if cell is None:
            cell = self.selected_cell

        row = cell.row // 3 * 3
        col = cell.col // 3 * 3
        return [
                self.cells[i][j]
                for i in range(row, row + 3)
                for j in range(col, col + 3)
                if (i , j) != (cell.row, cell.col)
            ] + [
                self.cells[cell.row][j]
                for j in range(9)
                if j // 3 * 3 != col
            ] + [
                self.cells[i][cell.col]
                for i in range(9)
                if i // 3 * 3 != row
            ]
    def has_conflict_cells(self, Cell):
        for cell in self.neighbour_cells(Cell):
            if Cell.digit == cell.digit:
                return True
        
        return False
    	
    def check_neighbours(self):
        if self.selected_cell.digit:
            for cell in self.neighbour_cells():
                if self.selected_cell.digit == cell.digit:
                    if not cell.has_class('error'):
                        cell.add_class('error')
                    if not self.selected_cell.has_class('error'):
                        self.selected_cell.add_class('error')
                else:
                    if cell.has_class('error') and not self.has_conflict_cells(cell):
                        cell.remove_class('error')
        else:
            ... 

    def on_cell_clicked(self, event: Cell.Clicked) -> None:
        clicked_cell = event.cell

        # Reset the previous selected cell's background if any
        if self.selected_cell and self.selected_cell != clicked_cell:
            self.selected_cell.selected = False

        # Set the new selected cell's background
        self.select_cell(clicked_cell)
        self.select_neighbours()
            
                
    async def on_key(self, event: Key) -> None:
        if self.selected_cell:
            if event.key.isdecimal() or event.key == 'backspace':
                if self.selected_cell.has_class('built-in'):
                    self.app.notify("This Cell Can not be Modified!")
                else:
                    match event.key:
                        case '0':
                            self.app.notify('0 is not a valid input!')
                        case 'backspace':
                            self.selected_cell.digit = None
                        case _:
                            self.selected_cell.digit = int(event.key)
                            self.check_neighbours()
            else:
                new_row, new_col = self.selected_cell.row, self.selected_cell.col
                match event.key:
                    case "up":
                        new_row -= 1
                    case "down":
                        new_row += 1
                    case "left":
                        new_col -= 1
                    case "right":
                        new_col += 1
                    case _:
                        pass
                
                self.move_selection(new_row, new_col) 
               
            

    @work(exclusive=True)
    async def move_selection(self, row: int, col: int) -> None:
        # Deselect the current cell
        if self.selected_cell:
            self.selected_cell.selected = False

        # Update the selected cell coordinates
        row, col = row % 9, col % 9
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True
        self.select_neighbours()

class MyApp(App):

    CSS_PATH = "test.tcss"

    def compose(self):
        yield SudokuGrid3X3()

if __name__ == "__main__": MyApp().run()

