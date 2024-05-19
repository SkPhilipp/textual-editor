#!/usr/bin/env python
import json
from datetime import datetime
from typing import Tuple

from textual import on
from textual.app import App, ComposeResult

from screens.textareascreen import TextAreaScreen
from widgets.footerwidget import CustomFooter
from widgets.objecttable import ObjectTable


class Communication:
    def __init__(self, time=None, channel=None, sender=None, receiver=None, status=None, message=None):
        self.time = time
        self.channel = channel
        self.sender = sender
        self.receiver = receiver
        self.status = status
        self.message = message


INITIAL_ROWS = [
    Communication(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 1"),
    Communication(datetime.now().isoformat(), "alice--bob", "alice", "bob", "sent", "message 2"),
    Communication(datetime.now().isoformat(), "#team", "eve", "#team", "sent", "message 3"),
    Communication(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 4"),
    Communication(datetime.now().isoformat(), "#team", "bob", "#team", "sent", "message 5"),
    Communication(datetime.now().isoformat(), "alice--eve", "eve", "alice", "sent", "message 6"),
    Communication(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 7"),
    Communication(datetime.now().isoformat(), "#team", "eve", "#team", "sent", "message 8"),
    Communication(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 9"),
    Communication(datetime.now().isoformat(), "#team", "bob", "#team", "sent", "message 10"),
    Communication(datetime.now().isoformat(), "alice--eve", "alice", "eve", "sent", "message 11"),
    Communication(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 12"),
    Communication(datetime.now().isoformat(), "#team", "eve", "#team", "sent", "message 13"),
    Communication(datetime.now().isoformat(), "#team", "alice", "#team", "sent", "message 14"),
    Communication(datetime.now().isoformat(), "#team", "bob", "#team", "sent", "message 15"),
]


class TableApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "duplicate_from_row", "Duplicate row"),
        ("f", "filter", "Filter by value"),
    ]

    def __init__(self):
        super().__init__()
        self.object_editing = None

    def compose(self) -> ComposeResult:
        yield ObjectTable[Communication](INITIAL_ROWS)
        yield CustomFooter(self.BINDINGS)

    def action_filter(self):
        table = self.query_one(ObjectTable)
        table.toggle_filter_column()

    def action_duplicate_from_row(self):
        table = self.query_one(ObjectTable)
        communication = table.coordinate_to_object(table.cursor_row)
        communication_dict = {
            "time": None,
            "channel": communication.channel,
            "sender": communication.sender,
            "receiver": communication.receiver,
            "status": "paused",
            "message": "",
        }

        def callback(result: Tuple[str, bool]):
            result_json, confirmed = result
            if not confirmed:
                return
            try:
                result_dict = json.loads(result_json)
                table.add_object(Communication(
                    time=result_dict["time"],
                    channel=result_dict["channel"],
                    sender=result_dict["sender"],
                    receiver=result_dict["receiver"],
                    status=result_dict["status"],
                    message=result_dict["message"],
                ))
            except json.JSONDecodeError:
                return

        self.push_screen(TextAreaScreen(json.dumps(communication_dict, indent=2)), callback)

    @on(ObjectTable.ObjectSelected)
    def on_object_selected(self, event: ObjectTable.ObjectSelected):
        communication = event.object_value
        communication_dict = {
            "time": communication.time,
            "channel": communication.channel,
            "sender": communication.sender,
            "receiver": communication.receiver,
            "status": communication.status,
            "message": communication.message,
        }

        def callback(result: Tuple[str, bool]):
            result_json, confirmed = result
            if not confirmed:
                return
            try:
                result_dict = json.loads(result_json)
                communication.time = result_dict["time"]
                communication.channel = result_dict["channel"]
                communication.sender = result_dict["sender"]
                communication.receiver = result_dict["receiver"]
                communication.status = result_dict["status"]
                communication.message = result_dict["message"]
                table = self.query_one(ObjectTable)
                table.refresh_object(communication)
            except json.JSONDecodeError:
                return

        self.push_screen(TextAreaScreen(json.dumps(communication_dict, indent=2)), callback)


if __name__ == "__main__":
    app = TableApp()
    app.run()
