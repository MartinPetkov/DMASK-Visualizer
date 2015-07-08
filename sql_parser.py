# All the functions for parsing and converting sql reside here

from parsed_query import *
from query_step import *
from table import *

import re

# Used for a custom sorting function
SQL_EXEC_ORDER = {
    "CREATE VIEW": 0,
    "FROM": 1,
    "WHERE": 2,
    "GROUP BY": 3,
    "HAVING": 4,
    "SELECT": 5,
    "DISTINCT": 6,
    "UNION": 7,
    "ORDER BY": 8,
}


""" Split a string containing multiple SQL queries into a list of single SQL queries """
def remove_sql_comments(sql_queries):
    # This matches either a single-line -- comment, or a multi-line /**/ comment
    comments_regex = re.compile(r"((/\*.*\*/)|(--[^\n]*\n))+", re.DOTALL | re.MULTILINE);
    clean_sql = comments_regex.sub("", sql_queries)

    return clean_sql

def split_sql_queries(sql_queries):
    # Assuming semicolons are enforced
    return list(map(
                lambda x: str.strip(x) + ";", # or just str.strip if not adding a ;
                filter(None,
                        remove_sql_comments(sql_queries).split(";"))))


""" Convert a single SQL query into an AST """
def sql_to_ast(query):
    # TODO: Implement
    pass


def reorder_sql_statements(sql_statements):
    return sorted(sql_statements, key=lambda statement: SQL_EXEC_ORDER[statement[0]])

""" Convert a single SQL AST into a list of QueryStep objects """
def sql_ast_to_steps(ast, schema):
    # TODO: Implement
    steps = []

    # Reorder the statements in the correct order, then parse beginning to end
    ast = reorder_sql_statements(ast)


def parse_create_view(ast_node):
    # TODO: Implement
    pass

def parse_from(ast_node):
    # TODO: Implement
    pass

def parse_where(ast_node):
    # TODO: Implement
    pass

def parse_group_by(ast_node):
    # TODO: Implement
    pass

def parse_having(ast_node):
    # TODO: Implement
    pass

def parse_select(ast_node):
    # TODO: Implement
    pass

def parse_distinct(ast_node):
    # TODO: Implement
    pass

def parse_union(ast_node):
    # TODO: Implement
    pass

def parse_order_by(ast_node):
    # TODO: Implement
    pass
