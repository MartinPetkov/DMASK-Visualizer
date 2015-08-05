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

    # If selected columns DISTINCT
    if len(sql_statements[0]) > 2:
        sql_statements.append(['DISTINCT'])

    return sorted(sql_statements, key=lambda statement: SQL_EXEC_ORDER[statement[0]])



last_table = '';
last_executable_sql = '';
namespace = '';
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

    last_table = '';
    last_executable_sql = '';
    namespace = '';

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
    elif second_statement == 'UNION':
        steps = parse_union(first_ast_node)
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
        new_step = STATEMENT_HANDLERS[statement](ast_node, str(local_step_number), steps)
        if new_step not None:
            steps += new_step
            local_step_number += 1

    return steps

def parse_clause(ast_node, step_number, prev_steps):

    current_step_number = step_number
    prev_step_number = int(current_step_number - 1)

    sql_chunk = ' '.join(flatten(ast_node))
    prev_chunk = prev_steps[prev_step_number].executable_sql
    executable_sql = prev_chunk + " " + sql_chunk

    input_tables = [str(prev_step_number)]
    result_table = [current_step_number]

    step = QueryStep(current_step_number, sql_chunk, input_tables, result_tables, executable_sql)

    return step


def parse_from(ast_node, step_number='', prev_steps):
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
    result_table = args[0][0] if (len(args) == 1 and len(args[0]) == 1) else current_step_number
    executable_sql = "SELECT * " + sql_chunk
    last_executable_sql = executable_sql
    namespace = '' # TODO

    # Create and add the first step
    first_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(first_step)

    if (len(args) == 1 and len(args[0]) == 1):
        return

    # TODO: Create and add the remaining substeps, if any
    i = 1
    while i+1 < len(args):
        from_connector = args[i]
        from_arg = args[i+1]
        local_step_number += 1
        current_step_number = step_number + str(local_step_number)

        if len(from_arg) == 1:
            # Simple table select
            # TODO: Handle case
            pass

        else:
            from_arg_connector = from_arg[1]
            if from_arg_connector == "ON":
                # TODO: Handle case
                reason = from_arg[2]

                pass
            elif from_arg_connector == "AS" or from_arg_connector == "":
                # TODO: Handle case
                new_name = from_arg[2]

                pass

        i += 2 # Going by twos, collecting the connector and the next table


def parse_where(ast_node, step_number='', prev_steps):
    # TODO:
    # - check for subquery and create ParsedQuery from this

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'WHERE':
        print("No WHERE clause")
        return

    # === QueryStep attributes ===
    where_step = parse_clause(ast_node, step_number, prev_steps)
    steps.append(where_step)

    return steps


def parse_group_by(ast_node, step_number='', prev_steps):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'GROUP BY':
        print("No GROUP BY clause")
        return

    groupby_step = parseclause(ast_node, step_number, prev_steps)
    steps.append(groupby_step)

    return steps


def parse_having(ast_node, step_number='', prev_steps):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'HAVING':
        print("No HAVING clause")
        return

    having_step = parse_clause(ast_node, step_number, prev_steps)
    steps.append(having_step)

    return steps

def parse_select(ast_node, step_number='', prev_steps):
    # TODO:
    # - ignore DISTINCT
    # - namespace

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1:
        print("No arguments to SELECT clause")
        return

    # Create first step
    current_step_number = step_number
    prev_step_number = int(current_step_number - 1)
    input_tables = [str(prev_step_number)]
    result_table = [current_step_number]
    namespace = ''

    # Check if selecting DISTINCT
    if len(ast_node) > 2:
        select_node = ast_node[0] + ast_node[-1]
        sql_chunk = ' '.join(flatten(select_node))
        executable_sql = sql_chunk + " " + prev_chunk[9:]
    else:

        sql_chunk = ' '.join(flatten(ast_node))
        executable_sql = sql_chunk + " " + prev_chunk[9:]

    select_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(select_step)

    return steps

def parse_distinct(ast_node, step_number='', prev_steps):
    # TODO: Implement

    steps = []

    if len(ast_node) < 1:
        print("Query does not select DISTINCT entries")
        return

    current_step_number = step_number
    prev_step_number = int(step_number) - 1
    input_tables = [prev_step_number]
    result_table = [current_step_number]

    prev_step = prev_steps[prev_step_number]
    sql_chunk = 'SELECT DISTINCT ' + prev_step.sql_chunk[7:]
    executable_sql = "SELECT DISTINCT " + prev_step.executable_sql[7:]

    distinct_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(distinct_step)

    return steps

def parse_union(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    pass

def parse_order_by(ast_node, step_number='', prev_steps):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'ORDER BY':
        print("No ORDER BY clause")
        return

        orderby_step = parse_clause(ast_node, step_number, prev_steps)
    steps.append(orderby_step)

    return steps

def parse_limit(ast_node, step_number='', prev_steps):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'LIMIT':
        print("No LIMIT clause")
        return

    limit_step = parse_clause(ast_node, step_number, prev_steps)
    steps.append(limit_step)

    return steps

def parse_offset(ast_node, step_number='', prev_steps):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'OFFSET':
        print("No OFFSET clause")
        return

    offset_step = parse_clause(ast_node, step_number, prev_steps)
    steps.append(offset_step)

    return steps

def parse_create_view(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    # Create the first step
    current_step_number = step_number + "1"
    sql_chunk = ' '.join(flatten(ast_node))
    input_tables = []
    result_table = ast_node[1]
    executable_sql = sql_chunk # In the case of CREATE VIEW, it is its own executable SQL
    namespace = '' # TODO

    # Create and add the first step
    first_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(first_step)

    sql_query_node = ast_node[len(ast_node)-1]
    steps += parse_sql_query(sql_query_node)

    return steps
