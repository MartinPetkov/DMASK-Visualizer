from query_step import QueryStep
from table import Table

class ParsedQuery:

    """
    Create a ParsedQuery object.

    :param steps: a list of QueryStep objects
    :param table_map: a map of table ids (strings) to Table objects
    :param query_text: the full text of the query
    """
    def __init__(self, steps=[], table_map={}, query_text=""):
        self.steps = sorted(steps, key=self.levels_compare_sort)
        self.table_map = table_map
        self.query_text = query_text


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
        return self.table_map.get(table_id);

    def add_step(self, query_step):
        self.steps.append(query_step)

    def add_steps(self, query_steps):
        for step in query_step:
            self.add_step(step)
