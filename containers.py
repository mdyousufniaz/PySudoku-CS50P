from textual.containers import Vertical

class MidCenter(Vertical):

    DEFAULT_CSS = """
        MidCenter {
            align: center middle;
            background: $success-lighten-3 5%;
            border: round #0F0;
        }
    """
    BORDER_TITLE = "PySudoku"