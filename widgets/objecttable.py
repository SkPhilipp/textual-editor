from typing import List, Any, Dict

from rich.style import Style
from rich.text import Text
from textual.coordinate import Coordinate
from textual.widgets import DataTable

from context.datatablecursorlock import DataTableCursorLock


class ObjectTable(DataTable):
    def __init__(self, objects: List[Any]):
        super().__init__()
        self.objects: List[Any] = objects
        self.objects_displayed: List[Any] = objects
        self.filters: Dict[str, str] = {}

    def get_objects_fields(self):
        return list(vars(self.objects[0]).keys())

    def _reload(self):
        columns = self.get_objects_fields()
        for index, column in enumerate(columns):
            if column in self.filters:
                self.add_column(Text(column, style=Style(underline=True)), key=str(index))
            else:
                self.add_column(column, key=str(index))

        for index, candidate in enumerate(self.objects):
            if self._object_matches_filters(candidate):
                self.add_row(*[getattr(candidate, field) for field in columns], key=str(index))

    def on_mount(self):
        self._reload()

    def coordinate_to_object(self, coord_row: int) -> str:
        (row_key, _) = self.coordinate_to_cell_key(Coordinate(coord_row, 0))
        return self.objects[int(row_key.value)]

    def update_object_at(self, coord_row: int):
        """
        Updates the row at the given coordinate with the object's values.

        Note that this does not apply filters to the object.
        :param coord_row:
        :return:
        """
        object_at_coord = self.coordinate_to_object(coord_row)
        for index, field in enumerate(self.get_objects_fields()):
            self.update_cell_at(Coordinate(coord_row, index), getattr(object_at_coord, field), update_width=True)

    def _object_matches_filters(self, object_element: Any) -> bool:
        return all(getattr(object_element, field) == value for field, value in self.filters.items())

    def toggle_filter_column(self):
        """
        Toggles the filter for the selected column, assigning it the value of the selected cell.
        """
        with DataTableCursorLock(self):
            coord = Coordinate(self.cursor_row, self.cursor_column)
            cell = self.get_cell_at(coord)
            column = self.get_objects_fields()[self.cursor_column]
            if column in self.filters:
                if self.filters[column] == cell:
                    del self.filters[column]
                else:
                    self.filters[column] = cell
            else:
                self.filters[column] = cell
            self.clear(columns=True)
            self._reload()
