from parser.query_step import QueryStep
from parser.table import Table

import json

class ParsedQuery:

    """
    Create a ParsedQuery object.

    :param steps: a list of QueryStep objects
    :param tables: a map of table ids (strings) to Table objects
    :param query_text: the full text of the query
    """
    def __init__(self, steps=[], tables={}, query_text="", base_tables = {}):
        self.steps = sorted(steps, key=self.levels_compare_sort)
        self.tables = tables
        self.query_text = query_text
        self.base_tables = base_tables

    def __repr__(self):
        return "[steps: {0}\ntables: {1}\nquery_text: {2}]\n".format(self.steps, self.tables, self.query_text)

    def to_json(self):
        json_dict = {
            "query_text": self.query_text,
            "steps": [step.to_json() for step in self.steps],
            "tables": {t_id: table.to_json() for t_id,table in self.tables.items()},
            "base_tables": self.base_tables
        }

        return json.dumps(json_dict)


    ''' Sort the list of steps in table-of-contents order '''
    def levels_compare_sort(self, item):
        """
        Sort in deepening levels, where a level is separated by a period
        Example:
        ['1.1.2', '1.1', '1.3', '1.2', '1.2.34', '1.2.3.4']
        -> ['1.1', '1.1.2', '1.2', '1.2.3.4', '1.2.34', '1.3']
        """

        item = item.step_number
        return (item, len(item[item.rfind('.')+1:]), item.count('.'))

    def get_table(self, table_id):
        return self.tables.get(table_id);

    def add_step(self, query_step):
        self.steps.append(query_step)

    def add_steps(self, query_steps):
        for step in query_step:
            self.add_step(step)
