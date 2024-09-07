from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Center

from art import text2art

from widgets import CenteredButton
from containers import MidCenter





class Main(App[None]):
    CSS_PATH = "test.tcss"

    def compose(self) -> ComposeResult:
        with MidCenter():
            yield Static(text2art("PySudoku", font='tarty-1'), id='title')
            yield CenteredButton('New Game')
            yield CenteredButton('Leader Board')
            yield CenteredButton("Quit")
        
    
    def on_custom_button_clicked(self):
        self.app.notify('Hello')

if __name__ == "__main__":
    Main().run()

