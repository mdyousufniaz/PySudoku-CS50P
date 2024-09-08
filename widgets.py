from textual.containers import Center
from textual.widgets import Static, Digits
from textual.message import Message
from datetime import datetime

class CenteredButton(Center):
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
        def __init__(self, custom_button) -> None:
            self.custom_button = custom_button
            super().__init__()
              # Reference to the button instance (control)

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