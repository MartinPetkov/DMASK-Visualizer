import json

class Table:

    """
    Create a Table object.

    :param t_name: this table's string name
    :param step: the step on which this table was created
    :param col_names: a list of the column names; the indexes match the order of values in the value tuples
    :param tuples: a list of string lists, one for each tuple of values in the table
    """
    def __init__(self, t_name, step, col_names, tuples=[]):
        self.t_name = t_name
        self.step = step
        self.col_names = col_names
        self.tuples = tuples

    def to_json(self):
        json_dict = {
            "t_name": self.t_name,
            "step": self.step,
            "col_names": self.col_names,
            "tuples": self.tuples
        }

        return json.dumps(json_dict)


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
