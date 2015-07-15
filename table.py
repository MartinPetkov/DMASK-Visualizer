import json

class Table:

    """
    Create a Table object.

    :param t_name: this table's string name
    :param step: the step on which this table was created
    :param col_names: a list of the column names; the indexes match the order of values in the value tuples
    :param tuples: a list of string lists, one for each tuple of values in the table
    """
    def __init__(self, t_name, step, col_names, tuples=[], reasons={}):
        self.t_name = t_name
        self.step = step
        self.col_names = col_names
        self.tuples = tuples
        self.reasons = reasons

    def to_json(self):
        json_dict = {
            "t_name": self.t_name,
            "step": self.step,
            "col_names": self.col_names,
            "tuples": self.tuples,
            "reasons": [{"row": row, "conditions_matched": reason.to_json()} for row,reason in self.reasons.items()]
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

class Reason:
    """
    A Reason is a list of conditions of the string parts of the WHERE clause that matched, and potentially a ParsedQuery object matching that particular part of the conditions. The idea is that if many conditions matched together, they can be highlighted separately instead of sent over as one big string.
    """


    """
    Create a Reason object

    :param conditions_matched: a list of strings of conditions that matched; each one has an entry in the map
    :param subqueries: a map of string conditions to their corresponding subqueries (will be empty usually)
    """
    def __init__(self, conditions_matched, subqueries={}):
        self.conditions_matched = conditions_matched
        self.subqueries = subqueries;

    def to_json(self):
        json_dict = {
            "conditions_matched": self.conditions_matched,
            "subqueries": {condition: subquery.to_json() for condition,subquery in self.subqueries.items()}
        }

        return json.dumps(json_dict)


    def get_reasons_only(self):
        return list(self.conditions_matched.keys())

    def get_subquery(self, condition):
        return self.conditions_matched.get(condition)

