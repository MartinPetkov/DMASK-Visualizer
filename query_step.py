import json

class QueryStep:

    """
    Create a ParsedQuery object.

    :param step_number: a string representing which step this is (i.e. 1.1 or 1.3.4)
    :param sql_chunk: the string of the SQL chunk this steps represents
    :param input_tables: a list of the string IDs of all input tables
    :param result_table: a string ID of the output table
    :param namespace: a list of strings of the tables in the namespace before executing this step
    :param res_table_name: the optional name of this resulting table
    :param reasons: a map of row numbers (counting from 1) to Reason objects, saying why they were kept; for WHERE and JOIN queries, this will be the actual row number but for NATUAL JOIN queries and queries with only one condition, there will only be an entry for row 0 which is true for all rows
    """
    def __init__(self, step_number, sql_chunk, input_tables, result_table, namespace=[]):
        self.step_number = step_number
        self.sql_chunk = sql_chunk
        self.input_tables = input_tables
        self.result_table = result_table
        self.namespace = namespace

    def to_json(self):
        json_dict = {
            "step_number": self.step_number,
            "sql_chunk": self.sql_chunk,
            "input_tables": self.input_tables,
            "result_table": self.result_table,
            "namespace": self.namespace
        }

        return json.dumps(json_dict)