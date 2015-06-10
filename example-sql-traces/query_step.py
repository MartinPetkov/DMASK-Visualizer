import json

class QueryStep:

    """
    Create a ParsedQuery object.

    :param step_number: a string representing which step this is (i.e. 1.1 or 1.3.4)
    :param sql_chunk: the string of the SQL chunk this steps represents
    :param input_tables: a list of the string IDs of all input tables
    :param result_table: a string ID of the output table
    :param namespace: a list of IDs of the tables in the namespace before executing this step
    :param res_table_name: the optional name of this resulting table
    :param reasons: a map of row numbers (counting from 1) to Reason objects, saying why they were kept; for WHERE and JOIN queries, this will be the actual row number but for NATUAL JOIN queries and queries with only one condition, there will only be an entry for row 0 which is true for all rows
    """
    def __init__(self, step_number, sql_chunk, input_tables, result_table, namespace=[], reasons={}):
        self.step_number = step_number
        self.sql_chunk = sql_chunk
        self.input_tables = input_tables
        self.result_table = result_table
        self.namespace = namespace
        self.reasons = reasons

    def to_json(self):
        json_dict = {
            "step_number": self.step_number,
            "sql_chunk": self.sql_chunk,
            "input_tables": self.input_tables,
            "result_table": self.result_table,
            "namespace": self.namespace,
            "reasons": [{"row": row, "conditions_matched": reason.to_json()} for row,reason in self.reasons.items()]
        }

        return json.dumps(json_dict)


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
