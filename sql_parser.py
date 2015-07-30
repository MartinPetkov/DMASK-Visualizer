# All the functions for parsing and converting sql reside here

from parsed_query import *
from query_step import *
from table import *
from to_ast import ast

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
    "LIMIT": 9,
    "OFFSET": 10
}

import collections
basestring = (str, bytes)
def flatten(lst):
    result = []
    for elem in lst:
        if hasattr(elem, "__iter__") and not isinstance(elem, basestring):
            result.extend(flatten(elem))
        else:
            result.append(elem)
    return result


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
    return ast(query) 


def reorder_sql_statements(sql_statements):
    return sorted(sql_statements, key=lambda statement: SQL_EXEC_ORDER[statement[0]])



last_table = '';
last_executable_sql = '';
""" Convert a single SQL AST into a list of QueryStep objects """
# TODO: Implement
def sql_ast_to_steps(ast, schema):
    STATEMENT_HANDLERS = {
        "CREATE VIEW": parse_create_view,
        "FROM": parse_from,
        "WHERE": parse_where,
        "GROUP BY": parse_group_by,
        "HAVING": parse_having,
        "SELECT": parse_select,
        "DISTINCT": parse_distinct,
        "UNION": parse_union,
        "ORDER BY": parse_order_by,
        "LIMIT": parse_limit,
        "OFFSET": parse_offset
    }

    steps = []
    # Reorder the statements in the correct order, then parse beginning to end
    ast = reorder_sql_statements(ast)
    if len(ast) < 1:
        print("No ast nodes found")
        return

    first_ast_node = ast[0]
    first_statement = first_ast_node[0].upper()
    if first_statement == 'CREATE VIEW':
        steps = parse_create_view(first_ast_node)
    else:
        steps = parse_sql_query(ast)

    return steps


def parse_sql_query(ast, step_number=''):
    # A list of steps for just this sql query, would be appended to a bigger list if we're many levels deep
    steps = []

    local_step_number = 1;
    while local_step_number <= len(ast):
        ast_node = ast[local_step_number-1]
        statement = ast_node[0] # Statement name has to be the first element in this list

        # Each statement has a handler that will generate its own steps and substeps, and those get appended to the overall list of steps
        steps += STATEMENT_HANDLERS[statement](ast_node, str(local_step_number))
        local_step_number += 1


def parse_from(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []
    if step_number:
        step_number += '.'

    args = ast_node[1]

    if len(args) < 1:
        print("No arguments to FROM statement")
        return

    # Create the first step
    local_step_number = 1
    current_step_number = step_number + str(local_step_number)
    sql_chunk = ' '.join(flatten(ast_node))
    input_tables = []
    # Either going to be a combined intermediate table, or just the one table being selected if there is only one
    result_table = args[0][0] if (len(args) == 1 and len(args[0]) == 1 ) else current_step_number
    executable_sql = "SELECT * " + sql_chunk
    last_executable_sql = executable_sql
    namespace = '' # TODO

    # Create and add the first step
    first_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(first_step)

    # TODO: Create and add the remaining substeps, if any
    for arg in args:
        pass


def parse_where(ast_node, step_number=''):
    # TODO: 
    # - check for subquery and create ParsedQuery from this

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    # If there is a WHERE clause, must be at least three elements
    if len(ast_node) <= 2:
        print("No WHERE clause")
        return

    # If at least three elements, check that the third element is WHERE clause
    clause_number = 2
    args = ast_node[clause_number]

    if len(args) < 1 or args[0] != 'WHERE':
        print("No WHERE clause")
        return


    # Create the first step
    local_step_number = clause_number
    current_step_number = step_number + "." + str(local_step_number)
    sql_chunk = ' '.join(flatten(args))
    executable_sql = "SELECT * " + ' '.join(flatten(ast_node[1: clause_number + 1]))

    # Input tables: comes from previous clause number
    prev_step = current_step_number[:-1] + str(int(current_step_number[-1]) - 1)
    input_tables = [prev_step]

    result_table = [current_step_number]
    where_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(where_step)

    return steps


def parse_group_by(ast_node, step_number=''):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    # If there is a GROUP BY clause, must be at least three elements
    if len(ast_node) <= 2:
        print("No GROUP BY clause")
        return

    #If at least three elements, check which element is GROUP BY clause
    for clause_number in range(2, SQL_EXEC_ORDER['GROUP BY'] + 1): # 'GROUP BY': 3
        found = False
        if len(ast_node) > clause_number:
            args = ast_node[clause_number]
            if len(args) < 1:
                print("No GROUP BY clause")
            elif args[0] == "GROUP BY":
                found = True
                break

    if found: # ast_node[clause_number] is the GROUP BY clause 

        # Create first step
        local_step_number = clause_number
        current_step_number = step_number + "." + str(local_step_number)
        sql_chunk = ' '.join(flatten(args))
        executable_sql = "SELECT * " + ' '.join(flatten(ast_node[1: clause_number + 1]))

        # Input tables: comes from previous clause number
        prev_step = current_step_number[:-1] + str(int(current_step_number[-1]) - 1)
        input_tables = [prev_step]

        result_table = [current_step_number]
        groupby_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
        steps.append(groupby_step)

    else:
        print("No GROUP BY clause")

    return steps


def parse_having(ast_node, step_number=''):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    # If there is a HAVING clause, must be at least three elements
    if len(ast_node) <= 2:
        print("No HAVING clause")
        return

    #If at least three elements, check which element is HAVING clause
    for clause_number in range(2, SQL_EXEC_ORDER['HAVING'] + 1): # HAVING: 4
        found = False
        if len(ast_node) > clause_number:
            args = ast_node[clause_number]
            if len(args) < 1:
                print("No HAVING clause")
            elif args[0] == "HAVING":
                found = True
                break

    if found: # ast_node[clause_number] is the GROUP BY clause 

        # Create first step
        local_step_number = clause_number
        current_step_number = step_number + "." + str(local_step_number)
        sql_chunk = ' '.join(flatten(args))        
        executable_sql = "SELECT * " + ' '.join(flatten(ast_node[1: clause_number + 1]))

        
        # Input tables: comes from previous clause number
        prev_step = current_step_number[:-1] + str(int(current_step_number[-1]) - 1)
        input_tables = [prev_step]

        result_table = [current_step_number]
        having_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
        steps.append(having_step)

    else:
        print("No HAVING clause")

    return steps

def parse_select(ast_node, step_number=''):
    # TODO: 
    # - ignore DISTINCT
    # - namespace

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    args = ast_node[0]
    if len(args) < 1:
        print("No arguments to SELECT clause")
        return

    clause_number = len(ast_node)

    # Create first step
    local_step_number = clause_number
    current_step_number = step_number + "." + str(local_step_number)
    
    # Selected columns are found in last entry of SELECT clause
    sql_chunk = 'SELECT ' + ', '.join(flatten(args[-1]))
    executable_sql = sql_chunk + " " + ' '.join(flatten(ast_node[1: clause_number + 1]))

    # Input tables: comes from previous clause number
    prev_step = current_step_number[:-1] + str(int(current_step_number[-1]) - 1)
    input_tables = [prev_step]

    result_table = [current_step_number]

    namespace = ''

    select_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(select_step)

    return steps

def parse_distinct(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    args = ast_node[0]
    if len(args) < 3:
        print("Query does not select DISTINCT entries")
        return

    clause_number = len(ast_node) + 1

    # Create first step
    local_step_number = clause_number
    current_step_number = step_number + "." + str(local_step_number)
    sql_chunk = ' '.join(flatten(args))
    executable_sql = ' '.join(flatten(ast_node[0: clause_number + 1]))

    # Input tables: comes from previous clause number
    prev_step = current_step_number[:-1] + str(int(current_step_number[-1]) - 1)
    input_tables = [prev_step]

    result_table = [current_step_number]

    distinct_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(distinct_step)

    return steps

def parse_union(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    pass

def parse_order_by(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    # If there is a HAVING clause, must be at least three elements
    if len(ast_node) <= 2:
        print("No ORDER BY clause")
        return

    #If at least three elements, check which element is HAVING clause
    for clause_number in range(2, SQL_EXEC_ORDER['ORDER BY'] + 1): # ORDER BY: 8
        found = False
        if len(ast_node) > clause_number:
            args = ast_node[clause_number]
            if len(args) < 1:
                print("No HAVING clause")
            elif args[0] == "HAVING":
                found = True
                break

    if found: # ast_node[clause_number] is the GROUP BY clause 

        # Create first step
        local_step_number = clause_number
        current_step_number = step_number + "." + str(local_step_number)
        sql_chunk = ' '.join(flatten(args))        
        executable_sql = "SELECT * " + ' '.join(flatten(ast_node[1: clause_number + 1]))

        
        # Input tables: comes from previous clause number
        prev_step = current_step_number[:-1] + str(int(current_step_number[-1]) - 1)
        input_tables = [prev_step]

        result_table = [current_step_number]
        having_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
        steps.append(having_step)

    else:
        print("No HAVING clause")

    return steps

def parse_limit(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    pass

def parse_offset(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    pass

def parse_create_view(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    pass
