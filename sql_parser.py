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
    "ORDER BY": 7,
    "LIMIT": 8,
    "OFFSET": 9
}

SET_OPERATIONS = ['UNION', 'INTERSECT', 'EXCEPT']

import collections
basestring = (str, bytes)
def flatten(lst):
    result = []
    for elem in lst:
        if hasattr(elem, "__iter__") and not isinstance(elem, basestring):
            if (elem[0][0] == 'SELECT'):
                result.append('(')
                result.extend(flatten(elem))
                result.append(')')
            else:
                result.extend(flatten(elem))
        else:
            result.append(elem)
    return result

def lst_to_str(lst):
    return ' '.join(flatten(lst))


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
        sql_statements[0].pop(1)
        sql_statements.append(['DISTINCT'])

    return sorted(sql_statements, key=lambda statement: SQL_EXEC_ORDER[statement[0]])

last_table = '';
last_executable_sql = '';
namespace = '';
""" Convert a single SQL AST into a list of QueryStep objects """
# TODO: Implement
def sql_ast_to_steps(ast, schema):

    steps = []

    if len(ast) < 1:
        print("No ast nodes found")
        return

    first_ast_node = ast[0]
    first_statement = first_ast_node[0].upper()
    second_statement = first_ast_node[1].upper()
    if first_statement == 'CREATE VIEW':
        steps = parse_create_view(ast)
    elif second_statement in SET_OPERATIONS:
        steps = parse_union(first_ast_node)
    else:
        steps = parse_sql_query(ast)

    return steps


def parse_sql_query(ast, parent_number=''):

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
    # A list of steps for just this sql query, would be appended to a bigger list if we're many levels deep
    steps = []

    local_step_number = 1

    # entire query

    current_step_number = local_step_number
    if parent_number:
        current_step_number = parent_number

    sql_chunk = lst_to_str(ast)
    input_tables = []
    result_table = current_step_number
    executable_sql = sql_chunk + ';'

    query = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(query)

    ast = reorder_sql_statements(ast)
    while local_step_number <= len(ast):
        ast_node = ast[local_step_number-1]
        statement = ast_node[0] # Statement name has to be the first element in this list

        # Each statement has a handler that will generate its own steps and substeps, and those get appended to the overall list of steps
        new_step = STATEMENT_HANDLERS[statement](ast_node, str(local_step_number), parent_number, steps)
        if new_step != []:
            steps += new_step
            local_step_number += 1

    return steps

def parse_clause(ast_node, step_number='', parent_number='', prev_steps=[]):

    if parent_number:
        parent_number += '.'

    current_step_number = parent_number + step_number
    prev_step_number = parent_number + str(int(step_number)- 1)

    sql_chunk = lst_to_str(ast_node)
    prev_chunk = prev_steps[-1].executable_sql
    executable_sql = prev_chunk[:-1] + " " + sql_chunk + ';'

    input_tables = [str(prev_step_number)]
    result_table = current_step_number

    step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)

    return step

def parse_from(ast_node, step_number='', parent_number='', prev_steps=[]):
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
    current_step_number = step_number + ('.' if step_number else '') + '1'
    sql_chunk = lst_to_str(ast_node)
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


    local_step_number = 1
    substep_number = current_step_number + '.' + str(local_step_number)

    # Create the first substep
    sql_chunk = lst_to_str(args[0]);
    combine_sql_chunk = sql_chunk
    executable_sql = "SELECT * FROM " + sql_chunk
    combine_executable_sql = executable_sql
    output_table_name = extract_from_arg_table_name(args[0])
    last_from_table = output_table_name

    if(len(args[0]) == 3 and args[0][2] != "ON" and isinstance(args[0][0], list)):
        # The first step is a rename of a subquery
        subquery = args[0][0]

        # Create the top step
        top_step_sql_chunk = '(' + lst_to_str(subquery) + ')'
        top_step_executable_sql = lst_to_str(subquery)
        substep = QueryStep(substep_number, top_step_sql_chunk, [], substep_number, top_step_executable_sql, namespace)
        steps.append(substep)
        last_from_table = substep_number

        # Gather the subquery steps
        steps.append(parse_sql_query(subquery, substep_number))

        # Advance to the next step on this level
        local_step_number += 1
        substep_number = current_step_number + '.' + str(local_step_number)

        # Add the separate rename step
        rename_sql_chunk = ' '.join(args[0][1:])
        rename_new_name = args[0][2] if len(args) > 1 else current_step_number
        rename_executable_sql = "SELECT * FROM " + top_step_sql_chunk + ' ' + rename_sql_chunk
        substep = QueryStep(substep_number, rename_sql_chunk, [last_from_table], rename_new_name, rename_executable_sql, namespace)
        steps.append(substep)

        last_from_table = rename_new_name

    else:
        substep = QueryStep(substep_number, sql_chunk, [], output_table_name, executable_sql, namespace)
        steps.append(substep)


    # Create and add the remaining substeps
    i = 1
    while i+1 < len(args):
        from_connector = args[i]
        from_arg = args[i+1]
        local_step_number += 1
        substep_number = current_step_number + '.' + str(local_step_number)

        if len(from_arg) > 1 and (from_arg[1] == "AS" or from_arg[1] == "") and isinstance(from_arg[0], list):
            # Case of a subquery being renamed
            subquery = from_arg[0]

            # Create the top step
            top_step_sql_chunk = '(' + lst_to_str(subquery) + ')'
            top_step_executable_sql = lst_to_str(subquery)
            substep = QueryStep(substep_number, top_step_sql_chunk, [], substep_number, top_step_executable_sql, namespace)
            steps.append(substep)
            last_from_table = substep_number

            # Gather the subquery steps
            steps.append(parse_sql_query(subquery, substep_number))

            # Advance to the next step on this level
            local_step_number += 1
            substep_number = current_step_number + '.' + str(local_step_number)

            # Add the separate rename step
            rename_sql_chunk = ' '.join(from_arg[1:])
            rename_new_name = from_arg[2]
            rename_executable_sql = "SELECT * FROM " + top_step_sql_chunk + ' ' + rename_sql_chunk
            substep = QueryStep(substep_number, rename_sql_chunk, [last_from_table], rename_new_name, rename_executable_sql, namespace)
            steps.append(substep)

            last_from_table = rename_new_name
            local_step_number += 1
            substep_number = current_step_number + '.' + str(local_step_number)

        else:
            # Simple table select

            # Step for collecting the new table
            sql_chunk = lst_to_str(from_arg);
            executable_sql = "SELECT * FROM " + sql_chunk
            output_table_name = extract_from_arg_table_name(from_arg)
            substep = QueryStep(substep_number, sql_chunk, [], output_table_name, executable_sql, namespace)
            steps.append(substep)

            local_step_number += 1
            substep_number = current_step_number + '.' + str(local_step_number)

        # Step for joining everything up to this point and this table
        combine_sql_chunk += ' ' + from_connector + ' ' + lst_to_str(from_arg);
        combine_executable_sql += ' ' + combine_sql_chunk
        new_joined_table = output_table_name
        output_table_name = substep_number if (i+2) != len(args) else current_step_number

        substep = QueryStep(substep_number, combine_sql_chunk, [last_from_table, new_joined_table], output_table_name, combine_executable_sql, namespace)
        steps.append(substep)

        last_from_table = output_table_name

        i += 2 # Going by twos, collecting the connector and the next table

    return steps

def extract_from_arg_table_name(from_arg):
    if len(from_arg) == 1:
        return from_arg[0]
    elif len(from_arg) == 3:
        if from_arg[1] == 'ON':
            return from_arg[0]
        else:
            # If it's a renamed query or table
            return from_arg[2]

    # Not correctly parsable
    return ''


def parse_where(ast_node, step_number='', parent_number='', prev_steps=[]):
    # TODO:
    # - check for subquery and create ParsedQuery from this

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'WHERE':
        print("No WHERE clause")
        return

    # === QueryStep attributes ===
    where_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(where_step)

    return steps


def parse_group_by(ast_node, step_number='', parent_number='', prev_steps=[]):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'GROUP BY':
        print("No GROUP BY clause")
        return

    groupby_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(groupby_step)

    return steps


def parse_having(ast_node, step_number='', parent_number='', prev_steps=[]):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'HAVING':
        print("No HAVING clause")
        return

    having_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(having_step)

    return steps

def parse_select(ast_node, step_number='', parent_number='', prev_steps=[]):
    # TODO:
    # - ignore DISTINCT
    # - namespace

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1:
        print("No arguments to SELECT clause")
        return

    if parent_number and parent_number[-1] != '.':
        parent_number += '.'

    current_step_number = parent_number + step_number
    prev_step_number = parent_number + str(int(step_number) - 1)
    input_tables = [str(prev_step_number)]
    result_table = current_step_number
    namespace = ''

    prev_step = prev_steps[-1]

    # Check if selecting DISTINCT
    if len(ast_node) > 2:
        sql_chunk = 'SELECT ' + lst_to_str(ast_node[-1])
        executable_sql = sql_chunk + " " + prev_step.executable_sql[9:-1] + ';'
    else:

        sql_chunk = lst_to_str(ast_node)
        executable_sql = sql_chunk + " " + prev_step.executable_sql[9:-1] + ';'

    select_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(select_step)

    return steps

def parse_distinct(ast_node, step_number='', parent_number='', prev_steps=[]):
    # TODO: Implement

    steps = []

    if len(ast_node) < 1:
        print("Query does not select DISTINCT entries")
        return

    if parent_number and parent_number[-1] != '.':
        parent_number += '.'

    current_step_number = parent_number + step_number
    prev_step_number = parent_number + str(int(step_number) - 1)
    input_tables = [str(prev_step_number)]
    result_table = current_step_number

    prev_step = prev_steps[-1]
    sql_chunk = 'SELECT DISTINCT ' + prev_step.sql_chunk[7:]
    executable_sql = "SELECT DISTINCT " + prev_step.executable_sql[7:-1] + ';'

    distinct_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(distinct_step)

    return steps

def parse_union(ast_node, step_number='', parent_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 3:
        print("Not enough arguments for UNION clause: <query1> UNION <query2>")
        return

    # UNION step
    current_step_number = step_number
    sql_chunk = lst_to_str(ast_node)

    input_num1 = parent_number + '.1'
    input_num2 = parent_number + '.2'
    input_tables = [input_num1, input_num2]
    result_table = current_step_number
    executable_sql = sql_chunk

    union_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(union_step)

    query1 = parse_sql_query(ast_node[0], input_num1)
    query2 = parse_sql_query(ast_node[2], input_num2)

    steps += query1
    steps += query2


    return steps

def parse_order_by(ast_node, step_number='', parent_number='', prev_steps=[]):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'ORDER BY':
        print("No ORDER BY clause")
        return

    orderby_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(orderby_step)
    print(orderby_step)

    return steps

def parse_limit(ast_node, step_number='', parent_number='', prev_steps=[]):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'LIMIT':
        print("No LIMIT clause")
        return

    limit_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(limit_step)

    return steps

def parse_offset(ast_node, step_number='', parent_number='', prev_steps=[]):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'OFFSET':
        print("No OFFSET clause")
        return

    offset_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(offset_step)

    return steps

def parse_create_view(ast_node, step_number=''):
    # TODO: Implement

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 2:
        print("Not enough arguments for CREATE VIEW clause: CREATE VIEW AS? <query>")
        return

    current_step_number = '1'
    sql_chunk = lst_to_str(ast_node)

    input_tables = []
    result_table = current_step_number
    executable_sql = sql_chunk

    create_view_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(create_view_step)

    query = parse_sql_query(ast_node[-1], current_step_number + '.1')

    steps += query

    return steps
