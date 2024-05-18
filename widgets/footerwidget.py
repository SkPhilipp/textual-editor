from textual.widget import Widget


class CustomFooter(Widget):
    """
    Simplified variant of Footer, without inheritance of bindings between screens.
    """

    DEFAULT_CSS = """
    CustomFooter {
        background: $accent;
        color: $text;
        dock: bottom;
        height: 1;
        text-style: bold;
    }
    """

    def __init__(self, bindings: list[tuple[str, str, str]]):
        super().__init__()
        self.bindings = bindings

    def render(self) -> str:
        return ''.join(f"[on dark_blue] {key.upper()} [/on dark_blue] {description} " for key, action, description in self.bindings)
