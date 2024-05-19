from typing import List, Dict

from rich.style import Style
from rich.text import Text
from textual import on
from textual.coordinate import Coordinate
from textual.message import Message
from textual.widgets import DataTable

from context.datatablecursorlock import DataTableCursorLock


class ObjectTable[T](DataTable):
    class ObjectSelected[T](Message):
        def __init__(self, object_value: T, trigger: DataTable.CellSelected):
            self.object_value: T = object_value
            self.trigger: DataTable.CellSelected = trigger
            super().__init__()

    def __init__(self, objects: List[T]):
        super().__init__()
        self.objects: List[T] = objects.copy()
        self.filters: Dict[str, str] = {}

    def _fields(self):
        return list(vars(self.objects[0]).keys())

    def _matches_filter(self, object_element: T) -> bool:
        return all(getattr(object_element, field) == value for field, value in self.filters.items())

    def _reload(self):
        columns = self._fields()
        for column in columns:
            style = Style(underline=True) if column in self.filters else None
            self.add_column(Text(column, style=style), key=str(column))
        for index, candidate in enumerate(self.objects):
            if self._matches_filter(candidate):
                self.add_row(*[getattr(candidate, field) for field in columns], key=str(index))

    def on_mount(self):
        self._reload()

    def coordinate_to_object(self, coord_row: int) -> T:
        (row_key, _) = self.coordinate_to_cell_key(Coordinate(coord_row, 0))
        return self.objects[int(row_key.value)]

    def refresh_object(self, object_value: T):
        """
        Refreshes the cells representing the given object.

        Note that this does not apply filters to the object.
        :param object_value:
        :return:
        """
        object_index = self.objects.index(object_value)
        if object_index is None:
            return
        row_key = str(object_index)
        for column in self._fields():
            self.update_cell(row_key, column, getattr(object_value, column), update_width=True)

    def add_object(self, new_object: T):
        """
        Adds an object to the end of the table.

        Note that this does not apply filters to the object.
        :param new_object:
        :return:
        """
        self.objects.append(new_object)
        columns = self._fields()
        row_key = str(len(self.objects) - 1)
        self.add_row(*[getattr(new_object, field) for field in columns], key=row_key)
        row_index = self.get_row_index(row_key)
        self.move_cursor(row=row_index)
        # this is a fix for new rows causing the scrollbar to appear during screen callback
        self.call_after_refresh(self.move_cursor, row=row_index)

    def toggle_filter_column(self):
        """
        For the cell at the cursor, toggles the filter for the column with the value of the cell.
        """
        with DataTableCursorLock(self):
            coord = Coordinate(self.cursor_row, self.cursor_column)
            cell = self.get_cell_at(coord)
            column = self._fields()[self.cursor_column]
            if column in self.filters:
                if self.filters[column] == cell:
                    del self.filters[column]
                else:
                    self.filters[column] = cell
            else:
                self.filters[column] = cell
            self.clear(columns=True)
            self._reload()

    @on(DataTable.CellSelected)
    def on_cell_selected(self, event: DataTable.CellSelected):
        object_at_row = self.coordinate_to_object(event.coordinate.row)
        self.post_message(
            ObjectTable.ObjectSelected(
                object_at_row,
                trigger=event
            )
        )

    def __contains__(self, *args, **kwargs):
        return self.objects.__contains__(*args, **kwargs)
