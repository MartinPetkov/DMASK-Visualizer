class QueryStep:

    """
    Create a ParsedQuery object.

    :param step_number: a string representing which step this is (i.e. 1.1 or 1.3.4)
    :param sql_chunk: the string of the SQL chunk this steps represents
    :param input_tables: a list of the string IDs of all input tables
    :param result_table: a string ID of the output table
    :param res_table_name: the optional name of this resulting table
    """
    def __init__(self, step_number, sql_chunk, input_tables, result_table, res_table_name=""):
        self.step_number = step_number
        self.sql_chunk = sql_chunk
        self.input_tables = input_tables
        self.result_table = result_table
        self.res_table_name = res_table_name
