"""
A class for parsing SQL or RA statements into visualizable QuerySteps
Would be used like so:
from dmask import DMASK
...
dmask = DMASK(database_connection_params)
json_output = dmask.sql_to_json()
# Send json_output to the visualizer to visualize
"""

from parsed_query import *
from query_step import *
from table import *

import sql_parser
import ra_parser


# TODO: Figure out how to handle the database connection
""" A class to handle the conversion functions and the database connection """
class DMASK:

    """
    Create a DMASK object.

    :param conn_params: The database connection parameters
    """
    def __init__(self, conn_params):
        # TODO: Implement the database connection parameters
        self.conn_params = conn_params
        self.base_tables = base_tables


    def set_connection(conn_params):
        # TODO: Implement connecting to a database
        self.conn_params = conn_params

    def set_base_tables(base_tables):
        # TODO: Implement
        self.base_tables = base_tables


    """
    Convert a set of sql queries to JSON output suitable for the visualizer frontend
    Requires the connection parameters and base tables to be set
    """
    def sql_to_json(sql_queries):
        # TODO: Implement

        json_queries = []

        queries = split_sql_queries(sql_queries)
        for query in queries:
            ast = sql_parser.sql_to_ast(query)
            steps = sql_parser.sql_ast_to_steps(ast)
            tables = self.steps_to_tables(steps)

            parsed_query = ParsedQuery(steps, tables, query)
            json_queries.append(parsed_query.to_json())

        return json_queries



    """ Convert a set of relational algebra queries to JSON output suitable for the visualizer frontend """
    def ra_to_json(ra_queries):
        json_queries = []

        queries = ra_parser.split_ra_queries(ra_queries)
        for query in queries:
            ast = ra_parser.ra_to_ast(query)
            steps = ra_parser.ra_ast_to_steps(ast)
            tables = self.steps_to_tables(steps)

            parsed_query = ParsedQuery(steps, tables, query)
            json_queries.append(parsed_query.to_json())

        return json_queries


    def steps_to_tables(steps):
        # TODO: Implement

        # Turns the QuerySteps given into Table objects by executing their queries on the database given by
        # self.conn_params and with the base tables given by self.base_tables
        pass
