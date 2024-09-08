from __future__ import annotations

from textual.containers import Center
from textual.widgets import Static, Digits
from textual.message import Message
from textual.reactive import var
from textual.timer import Timer
from textual.app import ComposeResult, App

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

class Cell(Static):

    selected = var(False)

    DEFAULT_CSS = """
        Cell {
            height: 1;
            width: 3;
            text-align: center;
            background: $success-lighten-3 25%;
        }

        Cell.-selected {
            background: blue; 
        }
    """

    def on_click(self) -> None:
        self.post_message(self.Clicked(self))

    class Clicked(Message):
        def __init__(self, cell):
            self.cell = cell
            super().__init__()

    

class MyApp(App):

    CSS_PATH = "test.tcss"

    def compose(self):
        yield Cell('1')

if __name__ == "__main__": MyApp().run()

