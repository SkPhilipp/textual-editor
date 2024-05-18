#!/usr/bin/env python
from typing import Tuple

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer


class EnumWidget[T](Widget):
    """
    A widget that allows cycling through as well as changing a tuple of allowed values.
    Implicitly allows None as a value.
    """
    value = reactive(default=None, layout=True)
    allowed_values = reactive(default=(), layout=True)

    def __init__(self, value: T, allowed_values: Tuple[T]):
        super().__init__()
        self.allowed_values = allowed_values
        self.value = value

    def get_previous(self) -> T:
        idx = self.allowed_values.index(self.value)
        idx = (idx - 1) % len(self.allowed_values)
        return self.allowed_values[idx]

    def get_next(self) -> T:
        idx = self.allowed_values.index(self.value)
        idx = (idx + 1) % len(self.allowed_values)
        return self.allowed_values[idx]

    def set_to_previous(self) -> T:
        self.value = self.get_previous()
        return self.value

    def set_to_next(self) -> T:
        self.value = self.get_next()
        return self.value

    def validate_value(self, value: T) -> T:
        if value not in self.allowed_values:
            raise ValueError(f"{value} not in {self.allowed_values}")
        return value

    def watch_value(self, _: T, _new: T):
        self._resize()

    def watch_allowed_values(self, _: tuple[T], new: tuple[T]):
        """
        Watch for changes in the allowed values and update the current value if it is no longer allowed.

        :param _:
        :param new:
        :return:
        """
        if self.value in new:
            return
        if len(new) == 0:
            return None
        self.value = new[0]

    def render(self) -> str:
        return f"{self.value}"

    def _resize(self):
        self.styles.width = len(self.render())
        self.styles.height = 1

    def on_mount(self):
        self._resize()


class EnumWidgetApp(App):
    """
    A simple app to demonstrate the EnumWidget.
    """
    BINDINGS = [
        ("w", "custom_toggle_value", "Toggle to next value"),
        ("e", "custom_toggle_allowed_values", "Toggle to next allowed values"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield EnumWidget[str]("Alice", ("Alice", "Bob"))
        yield EnumWidget[str]("Alice", ("Alice", "Bob"))
        yield EnumWidget[str]("Alice", ("Alice", "Bob"))
        yield EnumWidget[str]("Alice", ("Alice", "Bob"))
        yield Footer()

    def action_custom_toggle_value(self):
        widgets = self.query(EnumWidget)
        for widget in widgets:
            widget.set_to_next()

    def action_custom_toggle_allowed_values(self):
        widgets = self.query(EnumWidget)
        for widget in widgets:
            widget.allowed_values = ("Alice", "Bob") if "Eve" in widget.allowed_values else ("Alice", "Bob", "Eve")


if __name__ == "__main__":
    app = EnumWidgetApp()
    app.run()
