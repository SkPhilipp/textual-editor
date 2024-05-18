from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import TextArea

from widgets.footerwidget import CustomFooter


class TextAreaScreen(ModalScreen):
    """
    TextArea as a modal screen.
    """

    CSS = """
    Container {
        margin: 1;
    }

    TextArea {
        padding: 0;
        border: none;
    }
    """

    BINDINGS = [
        ("escape", "modal_cancel", "Close"),
        ("ctrl+s", "save", "Save"),
    ]

    def __init__(self, initial_value: str):
        super().__init__()
        self.initial_value = initial_value

    def compose(self) -> ComposeResult:
        with Container():
            yield TextArea(text=self.initial_value)
            yield CustomFooter(self.BINDINGS)

    def action_save(self):
        result = self.query_one(TextArea).text
        self.dismiss(result)

    def action_modal_cancel(self):
        self.dismiss(self.initial_value)
