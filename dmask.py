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

        queries = sql_parser.split_sql_queries(sql_queries)
        for query in queries:
            ast = sql_parser.sql_to_ast(query)
            steps = sql_parser.sql_ast_to_steps(ast, base_tables)
            tables = self.steps_to_tables(steps)

            parsed_query = ParsedQuery(steps, tables, query)
            json_queries.append(parsed_query.to_json())
            # TODO: If the query was a CREATE VIEW, add that table to the base tables for all subsequent steps

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
            # TODO: If the query was an assignment (:= or whatever), add that table to the base tables for all
            # subsequent steps

        return json_queries


    def steps_to_tables(steps):
        # TODO: Implement
        # Turns the QuerySteps given into Table objects by executing their queries on the database given by
        # self.conn_params and with the base tables given by self.base_tables
        tables = {}
        
        # TODO: Import psycopg2? Modify this so we can get the connection
        # Create a connection and cursor (PSQL)
        connection = psycopg2.connect(this.conn_params)
        cursor = connection.cursor()
        
        for step in steps:
            if str(step.result_table) not in tables:
                # Get the table name (table name matches FROM statement of the executable)
                name = get_table_name(step.executable_sql)
                
                # Execute the query
                cursor.execute(step.executeable_sql)
                
                # Get the columns
                columns = [desc[0] for desc in cursor.description]
                
                # Get the tuples
                tuples = []
                for row in cursor:
                    tuples.append(row)
                
                # Get the reasons
                reasons = {}
                
                t = Table(name, step.step_number, columns, tuples, reasons)
                tables[str(step.result_table)] = t
        return tables

def get_table_name(exsqltable):
    # Given an executable SQL statement, return the table's name
    # TODO: This would be very weird for RA statements (even though it would work). Make an RA equivalent?
    
    # Get the AST so we can identify the FROM clause
    ast = sql_parser.sql_to_ast(exsqltable)
    
    # Traverse the AST until the FROM clause is found
    for node in ast:
        if node[0] == "FROM":
            # The second element in the node [FROM, [...]] holds the table's name
            from_ast = node[1]
            name = []
            on_using = False
            
            # Traverse each token in the FROM query
            for token in from_ast:
                # If it's a string, then it's either a keyword or table name, unless it follows the ON or USING keywords
                if isinstance(token, str) and not on_using:
                    # If the token is a "," (JOIN) add it to the previous token
                    if token.strip() == ",":
                        name[-1] = str(name[-1]) + ","
                    else:
                        name.append(token)
                    if token.lower() in ["on", "using"]:
                        on_using = True
                elif not on_using:
                    # If it's an array, then the last token in it is the name (as in the case of ["Student", "AS", "s1"])
                    name.append(token[-1])
                else:
                    # For the elements following ON/USING keywords, flatten them and add it to name
                    if isinstance(token, list):
                        flattened = flatten_list(token)
                        name.extend(flattened)
                    else:
                        name.append(token)
                    on_using = False
            
            # Return a string joined by whitespace
            return " ".join(str(item) for item in name)

def flatten_list(l):
    # Given a list of string or lists, flatten them into one list
    ret_val = []
    for item in l:
        if not isinstance(item, list):
            ret_val.append(item)
        else:
            ret_val.extend(flatten_list(item))
    return ret_val