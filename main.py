from textual.app import App, ComposeResult
from textual.widgets import Static, Select
from textual.containers import Center
from textual import on

from art import text2art

from widgets import CenteredButton, DigitalClock, CustomButton
from containers import MidCenter


class Main(App[None]):
    CSS_PATH = "test.tcss"

    def load_choose_difficulty_screen(self) -> None:
        self.inner_center.query(CenteredButton).remove()
        self.inner_center.mount(
            Center(
                Select.from_values(
                    ("Easy", "Medium", "Hard"),
                    prompt= "Choose a difficulty"
                )
            ),
            CenteredButton('Start Game', btn_id='start-game'),
            CenteredButton('Back to Home', btn_id='back-to-home')
        )

    def load_home_screen(self) -> None:
        self.inner_center.query().remove()
        self.inner_center.mount(
            CenteredButton('New Game', btn_id='new-game'),
            CenteredButton('Leader Board', btn_id='leader-board'),
            CenteredButton('Quit', btn_id='quit')
        )

    def compose(self) -> ComposeResult:
        with MidCenter():
            yield Static(text2art("PySudoku", font='tarty-1'), id='title')
            self.inner_center = Center()
            yield self.inner_center
            yield DigitalClock()

    def on_mount(self) -> None:
        self.load_home_screen()
        
    @on(CustomButton.Clicked, '#new-game')
    def handle_new_game(self) -> None:
        self.load_choose_difficulty_screen()

    @on(CustomButton.Clicked, '#back-to-home')
    def handle_back_to_home(self) -> None:
        self.load_home_screen()

    @on(CustomButton.Clicked, '#quit')
    def handle_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    Main().run()

