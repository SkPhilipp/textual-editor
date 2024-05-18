#!/usr/bin/env python
import json
from datetime import datetime

from textual import on
from textual.app import App, ComposeResult

from screens.textareascreen import TextAreaScreen
from widgets.footerwidget import CustomFooter
from widgets.objecttable import ObjectTable


class Row:
    def __init__(self, time, channel, sender, receiver, status, message):
        self.time = time
        self.channel = channel
        self.sender = sender
        self.receiver = receiver
        self.status = status
        self.message = message


INITIAL_ROWS = [
    Row(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 1"),
    Row(datetime.now().isoformat(), "alice--bob", "alice", "bob", "sent", "message 2"),
    Row(datetime.now().isoformat(), "#team", "eve", "#team", "sent", "message 3"),
    Row(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 4"),
    Row(datetime.now().isoformat(), "#team", "bob", "#team", "sent", "message 5"),
    Row(datetime.now().isoformat(), "alice--eve", "eve", "alice", "sent", "message 6"),
    Row(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 7"),
    Row(datetime.now().isoformat(), "#team", "eve", "#team", "sent", "message 8"),
    Row(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 9"),
    Row(datetime.now().isoformat(), "#team", "bob", "#team", "sent", "message 10"),
    Row(datetime.now().isoformat(), "alice--eve", "alice", "eve", "sent", "message 11"),
    Row(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 12"),
    Row(datetime.now().isoformat(), "#team", "eve", "#team", "sent", "message 13"),
    Row(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 14"),
    Row(datetime.now().isoformat(), "#team", "bob", "#team", "sent", "message 15"),
]


class TableApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "duplicate", "Duplicate"),
        ("f", "filter", "Filter"),
    ]

    def __init__(self):
        super().__init__()
        self.object_editing = None

    def compose(self) -> ComposeResult:
        yield ObjectTable[Row](INITIAL_ROWS)
        yield CustomFooter(self.BINDINGS)

    def action_filter(self):
        table = self.query_one(ObjectTable)
        table.toggle_filter_column()

    def action_duplicate(self):
        table: ObjectTable[Row] = self.query_one(ObjectTable)
        object_at_row = table.coordinate_to_object(table.cursor_row)
        table.add_object(Row(datetime.now().isoformat(),
                             object_at_row.channel,
                             object_at_row.sender,
                             object_at_row.receiver,
                             object_at_row.status,
                             object_at_row.message))

    @on(ObjectTable.CellSelected)
    def on_cell_selected(self, event: ObjectTable.CellSelected):
        table = self.query_one(ObjectTable)
        object_at_row = table.coordinate_to_object(event.coordinate.row)
        object_dict = {field: getattr(object_at_row, field) for field in table.get_objects_fields()}
        self.push_screen(TextAreaScreen(json.dumps(object_dict, indent=2)), self.callback_edit_row)

    def callback_edit_row(self, result: str):
        table = self.query_one(ObjectTable)
        try:
            object_dict = json.loads(result)
            row = table.coordinate_to_object(table.cursor_row)
            for field, value in object_dict.items():
                setattr(row, field, value)
            table.update_object_at(table.cursor_row)
        except json.JSONDecodeError:
            return


if __name__ == "__main__":
    app = TableApp()
    app.run()
