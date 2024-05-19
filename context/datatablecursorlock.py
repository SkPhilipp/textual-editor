from textual.widgets import DataTable


class DataTableCursorLock:
    """
    A context manager that restores the cursor position of a DataTable after the block is executed.

    Note that the cell key must be remain valid .after the block is executed.
    """

    def __init__(self, table: DataTable):
        self.table: DataTable = table

    def __enter__(self):
        self.cursor_coordinate = self.table.cursor_coordinate
        self.cell_key = self.table.coordinate_to_cell_key(self.cursor_coordinate)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cursor_coordinate = self.table.get_cell_coordinate(self.cell_key.row_key, self.cell_key.column_key)
        self.table.cursor_coordinate = cursor_coordinate
