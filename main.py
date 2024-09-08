from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Center

from art import text2art

from widgets import CenteredButton, DigitalClock
from containers import MidCenter


class Main(App[None]):
    CSS_PATH = "test.tcss"

    def load_choose_difficulty_screen(self) -> None:
        ...

    def compose(self) -> ComposeResult:
        self.mid_center = MidCenter()
        with self.mid_center:
            yield Static(text2art("PySudoku", font='tarty-1'), id='title')
            yield CenteredButton('New Game')
            yield CenteredButton('Leader Board')
            yield CenteredButton("Quit")
            yield DigitalClock()
        
    
    def on_custom_button_clicked(self):
        self.app.notify('Hello')

if __name__ == "__main__":
    Main().run()

