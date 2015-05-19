class Table:

    """
    Create a Table object.

    :param table_id: a string representing this table's id
    :param col_names: a list of the column names; the indexes match the order of values in the value tuples
    :param tuples: a list of string lists, one for each tuple of values in the table
    """
    def __init__(self, table_id, col_names, tuples=[]):
        self.table_id = table_id
        self.col_names = col_names
        self.tuples = tuples


    def get_col_name(self, col_idx):
        return self.col_names(col_idx)

    def get_cell_value(self, row, col):
        return self.tuples[row][col]

    def get_row(self, row):
        return self.tuples[row]

    def get_col(self, col):
        return [r[col] for r in self.tuples]

    def add_tuple(self, tup):
        self.tuples.append(tup)

    def add_tuples(self, tuples):
        for tup in tuples:
            self.add_tuple(tup)

