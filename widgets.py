from __future__ import annotations

from textual.containers import Center, Grid
from textual.widgets import Static, Digits
from textual.message import Message
from textual.reactive import var
from textual.timer import Timer
from textual.app import ComposeResult, App
from textual import on
from textual.events import Key, DescendantFocus


from datetime import datetime

from typing import Optional

from time import monotonic

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

class Cell(Static, can_focus=True):

    selected = var(False)

    DEFAULT_CSS = """
        Cell {
            height: 1;
            width: 3;
            text-align: center;
            # background: $success-lighten-3 25%;
        }

        Cell:focus {
            background: blue; 
        }
    """

    def on_click(self) -> None:
        self.post_message(self.Clicked(self))

    class Clicked(Message):
        def __init__(self, cell):
            self.cell = cell
            super().__init__()

class SudokuGrid3X3(Grid, can_focus=True):

    DEFAULT_CSS = """
        SudokuGrid3X3 {
            box-sizing: content-box;
            grid-size: 9;
            width: 40;
            height: 23;
            padding-top: 2;
            padding-left: 1;
            keyline: thin $secondary;
            background: $background;
            grid-gutter: 0 1;
        }

        SudokuGrid3X3:focus {
            border: solid blue;
        }

    """

    def compose(self) -> ComposeResult:
        self.cells = [
            [Cell(str((row * 9 + col) % 10)) for col in range(9)]
            for row in range(9)
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
        self.selected_row = 0
        self.selected_col = 0

    def on_cell_clicked(self, event: Cell.Clicked) -> None:
        self.app.notify('Hello')
        clicked_cell = event.cell

        # Reset the previous selected cell's background if any
        if self.selected_cell and self.selected_cell != clicked_cell:
            self.selected_cell.selected = False

        # Set the new selected cell's background
        clicked_cell.selected = True
        self.selected_cell = clicked_cell

        for r in range(9):
            for c in range(9):
                if self.cells[r][c] == clicked_cell:
                    self.selected_row = r
                    self.selected_col = c
                    break
            
        # self.focus()

        @on(DescendantFocus)
        @on(Key)                
        def on_key(self, event: Key) -> None:
        # Handle arrow key navigation
            if event.key == "up" and self.selected_row > 0:
                self.move_selection(self.selected_row - 1, self.selected_col)
            elif event.key == "down" and self.selected_row < 8:
                self.move_selection(self.selected_row + 1, self.selected_col)
            elif event.key == "left" and self.selected_col > 0:
                self.move_selection(self.selected_row, self.selected_col - 1)
            elif event.key == "right" and self.selected_col < 8:
                self.move_selection(self.selected_row, self.selected_col + 1)

    def move_selection(self, new_row: int, new_col: int) -> None:
        # Deselect the current cell
        if self.selected_cell:
            self.selected_cell.selected = False

        # Update the selected cell coordinates
        self.selected_row, self.selected_col = new_row, new_col
        self.selected_cell = self.cells[new_row][new_col]
        self.selected_cell.selected = True

class MyApp(App):

    CSS_PATH = "test.tcss"

    def compose(self):
        yield SudokuGrid3X3()

if __name__ == "__main__": MyApp().run()

