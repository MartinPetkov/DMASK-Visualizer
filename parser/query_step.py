import json

class QueryStep:

    """
    Create a QueryStep object.

    :param step_number: a string representing which step this is (i.e. 1.1 or 1.3.4)
    :param sql_chunk: the string of the SQL chunk this steps represents
    :param input_tables: a list of the string IDs of all input tables
    :param result_table: a string ID of the output table
    :param namespace: a list of strings of the tables in the namespace before executing this step
    :param executable_sql: the string of executable SQL that will execute this step
    :param res_table_name: the optional name of this resulting table
    """
    def __init__(self, step_number, sql_chunk, input_tables, result_table, executable_sql="", namespace=[]):
        self.step_number = step_number
        self.sql_chunk = sql_chunk
        self.input_tables = input_tables
        self.result_table = result_table
        self.executable_sql = executable_sql + ';'
        self.namespace = namespace

    def __repr__(self):
        return "[step_number: {0}\nsql_chunk: {1}\ninput_tables: {2}\nresult_table: {3}\nexecutable_sql: {4}\nnamespace: {5}]\n".format(self.step_number, self.sql_chunk, self.input_tables, self.result_table, self.executable_sql, self.namespace)

    def to_json(self):
        json_dict = {
            "step_number": self.step_number,
            "sql_chunk": self.sql_chunk,
            "input_tables": self.input_tables,
            "result_table": self.result_table,
            "executable_sql": self.executable_sql,
            "namespace": self.namespace
        }

        return json.dumps(json_dict)
