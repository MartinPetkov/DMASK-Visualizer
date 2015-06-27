# Kathy: Sorry if this file is confusing,  I needed it to write dmask.py
# All the functiosn for parsing and converting sql reside here

from parsed_query import *
from query_step import *
from table import *


""" Split a string containing multiple SQL queries into a list of single SQL queries """
def split_sql_queries(sql_queries):
    # TODO: Implement
    pass

""" Convert a single SQL query into an AST """
def sql_to_ast(query):
    pass

""" Convert a single SQL AST into a list of QueryStep objects """
def sql_ast_to_steps(ast):
    pass
