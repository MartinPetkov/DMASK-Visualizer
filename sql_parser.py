# All the functions for parsing and converting sql reside here
from parsed_query import *
from query_step import *
from table import *
from to_ast import ast, KEYWORDS

import re
import collections

import pdb
from pprint import pprint
import pyparsing

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
    "INTERSECT": 7,
    "EXCEPT": 7,
    "ORDER BY": 8,
    "LIMIT": 9,
    "OFFSET": 10
}

SET_OPERATIONS = ['UNION', 'INTERSECT', 'EXCEPT']
CONDITIONS = ['WHERE', 'HAVING']
BRACKETS = ['(', ')']

basestring = (str, bytes)

last_table = ''
last_executable_sql = ''
schema = {}
namespace = []

def flatten(lst):
    result = []

    if lst[0] in CONDITIONS:
        return flatten_where(lst)

    for elem in lst:
        if hasattr(elem, "__iter__") and not isinstance(elem, basestring):
            if (elem[0][0] == 'SELECT'):
                result.append('(')
                result.extend(flatten(elem))
                result.append(')')
            elif (elem[0] == 'SELECT'):
                result.append('SELECT ' + make_column(elem[1]))
            elif (elem[0] in CONDITIONS):
                result.append(elem[0] + ' ')
                result.extend(flatten_where(elem[1]))
                print(result)
            else:
                result.extend(flatten(elem))
        else:
            result.append(elem)
    return result


def flatten_where(lst):
    result = []
    for elem in lst:
        if hasattr(elem, "__iter__") and not isinstance(elem, basestring):

            if (elem[0][0] == 'SELECT'):
                result.append('(')
                result.extend(flatten(elem))
                result.append(')')
            else:
                if len(elem) == 1:
                    result.extend(flatten_where(elem))
                else:
                    result.append('(')
                    result.extend(flatten_where(elem))
                    result.append(')')
        else:
            result.append(elem)

    return result


''' Return a string of the columns provided in column_list, separated by a comma. '''
def make_column(column_list):
    if column_list == ["*"]:
        return "*"

    columns = ''
    for item in column_list:
        columns += ' '.join(flatten(item)) + ', '

    return columns[:-2]


''' Returns a string representation of the flatten list lst. '''
def lst_to_str(lst):
    if isinstance(lst, basestring):
        return lst

    return ' '.join(clean_lst(flatten(lst)))


def clean_lst(lst):
    query = []

    for i in range(len(lst)):
        if lst[i] in BRACKETS:
            if query[-1] in KEYWORDS:
                query[-1] = query[-1] + ' ' + lst[i]
            else:
                query[-1] = query[-1] + lst[i]
        elif lst[i] != '':
            query.append(lst[i]) # Remove nonexistence elements

    return query

def get_namespace(steps, step_number='', table_name=''):
    for step in steps:
        if step_number:
            if step.step_number == step_number:
                return step.namespace
        elif table_name:
            if step.result_table == table_name:
                return step.namespace

def get_all_cols(namespace):

    cols = []
    for table in namespace:
        cols.extend(table[1])
    return cols


""" Split a string containing multiple SQL queries into a list of single SQL queries """
def remove_sql_comments(sql_queries):
    # This matches either a single-line -- comment, or a multi-line /**/ comment
    comments_regex = re.compile(r"((/\*.*\*/)|(--[^\n]*\n))+", re.DOTALL | re.MULTILINE)
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
    global namespace
    namespace = []
    return ast(query)


def reorder_sql_statements(sql_statements):

    # If there are set operations, all of them will be contained in the first element, followed by things like 'LIMIT'
    # and 'ORDER BY'. Successive set operations are nested deeper instead of being serialized in sequence.
    if len(sql_statements[0]) == 3 and isinstance(sql_statements[0][1], basestring) and sql_statements[0][1].upper() in SET_OPERATIONS:
        # Handle set operation reordering
        set_operation = sql_statements[0]
        first_sql_query = set_operation[0]
        operator = set_operation[1]
        second_sql_query = set_operation[2]

        final_statements = [
                            [
                                operator,
                                first_sql_query,
                                second_sql_query
                            ]
                           ]
        final_statements += sql_statements[1:]
        return final_statements
    
    # For inner set operations, do different things
    if len(sql_statements) == 3 and isinstance(sql_statements[1],basestring) and sql_statements[1].upper() in SET_OPERATIONS:
        # Handle set operation reordering
        first_sql_query = sql_statements[0]
        operator = sql_statements[1]
        second_sql_query = sql_statements[2]

        final_statements = [
                            [
                            operator, first_sql_query, second_sql_query
                            ]
                            ]
        return final_statements

    # If selected columns DISTINCT
    if len(sql_statements[0]) > 2 and sql_statements[1] == 'DISTINCT':
        sql_statements[0].pop(1)
        sql_statements.append(['DISTINCT'])

    # TODO: handle union and create view
    return sorted(sql_statements, key=lambda statement: SQL_EXEC_ORDER[statement[0].upper()])



""" Convert a single SQL AST into a list of QueryStep objects """
def sql_ast_to_steps(ast, current_schema={}):

    global schema
    schema = current_schema

    steps = []

    if len(ast) < 1:
        print("No ast nodes found")
        return

    first_ast_node = ast[0]
    if isinstance(first_ast_node, str) and first_ast_node.upper() == 'CREATE VIEW':
        steps = parse_create_view(ast)

    else:
        steps = parse_sql_query(ast)

    return steps


def parse_sql_query(ast, parent_number=''):

    global namespace

    STATEMENT_HANDLERS = {
        "CREATE VIEW": parse_create_view,
        "FROM": parse_from,
        "WHERE": parse_where,
        "GROUP BY": parse_group_by,
        "HAVING": parse_having,
        "SELECT": parse_select,
        "DISTINCT": parse_distinct,
        "UNION": parse_set,
        "INTERSECT": parse_set,
        "EXCEPT": parse_set,
        "ORDER BY": parse_order_by,
        "LIMIT": parse_limit,
        "OFFSET": parse_offset
    }

    last_table = ''
    last_executable_sql = ''
    # A list of steps for just this sql query, would be appended to a bigger list if we're many levels deep
    steps = []

    local_step_number = 1
    current_step_number = str(local_step_number)

    if parent_number:
        current_step_number = parent_number

    sql_chunk = lst_to_str(ast)
    input_tables = []
    result_table = current_step_number
    executable_sql = sql_chunk

    query = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    if parent_number:
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
    executable_sql = prev_chunk[:-1] + " " + sql_chunk
    input_tables = [prev_steps[-1].result_table]
    result_table = current_step_number

    step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)

    return step


def parse_from(ast_node, step_number='', parent_number='', prev_steps=[]):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []
    if parent_number:
        parent_number += '.'

    args = ast_node[1]

    if len(args) < 1:
        print("No arguments to FROM statement")
        return

    collapse_step = ( len(args) == 1 and (len(args[0]) == 1 or isinstance(args[0][0], basestring)) )

    # Create the first step
    current_step_number = parent_number + '1'
    sql_chunk = lst_to_str(ast_node)
    input_tables = []

    # Either going to be a combined intermediate table, or just the one table being selected if there is only one
    result_table = extract_from_arg_table_name(args[0]) if collapse_step else current_step_number

    executable_sql = "SELECT * " + sql_chunk
    last_executable_sql = executable_sql
    current_namespace = []

    this_namespace = get_namespace_from_args(args)
    # Create and add the first step
    first_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, this_namespace[:])
    steps.append(first_step)

    # Exit early if we are collapsing the steps into only one step
    if collapse_step:
        return steps

    local_step_number = 1
    substep_number = current_step_number + '.' + str(local_step_number)

    # Create the first substep
    sql_chunk = extract_from_arg_table_name(args[0])
    combine_sql_chunk = sql_chunk
    executable_sql = "SELECT * FROM " + sql_chunk
    combine_executable_sql = executable_sql

    full_table_name = extract_from_arg_table_name(args[0])
    original_table_name = full_table_name.split(' ')[0]
    output_table_name = full_table_name.split(' ')[-1]

    last_from_table = output_table_name

    # The first step is a rename of a subquery
    if(len(args[0]) == 3 and args[0][2] != "ON" and not isinstance(args[0][0], basestring)):
        subquery = args[0][0]
        local_step_number += 1
        steps += parse_sql_query(subquery, substep_number)

        # Add the separate rename step
        index_of_new_tables = len(current_namespace)
        prev_step = steps[-1]
        prev_step_number = prev_step.result_table
        rename_number = current_step_number + '.' + str(local_step_number)
        rename_sql_chunk = ' '.join(args[0][1:])
        rename_new_name = args[0][2]
        rename_executable_sql = "SELECT * FROM (" + prev_step.executable_sql[:-1] + ') ' + rename_sql_chunk
        subquery_namespace = steps[-1].namespace
        # Get the namespace after the subquery
        # Go through all the new namespace tables and collect all of their columns into one
        subquery_cols = [ c for t in subquery_namespace for c in t[1] ]
        this_namespace = [(rename_new_name, subquery_cols)]
        
        for item in this_namespace:
            if item not in current_namespace:
                current_namespace.append(item)

        substep = QueryStep(rename_number, rename_sql_chunk, [prev_step_number], rename_new_name, rename_executable_sql, this_namespace[:])
        steps.append(substep)
        last_from_table = rename_new_name


    # No subquery in the first step
    else:
        this_namespace = [(output_table_name, schema[original_table_name])]
        for item in this_namespace:
            if item not in current_namespace:
                current_namespace.append(item)
        substep = QueryStep(substep_number, sql_chunk, [], output_table_name, executable_sql, this_namespace[:])
        steps.append(substep)
    # Create and add the remaining substeps
    i = 1
    while i+1 < len(args):
        from_connector = args[i]
        from_arg = args[i+1]
        local_step_number += 1
        substep_number = current_step_number + '.' + str(local_step_number)

        # Case of a subquery being renamed
        if len(from_arg) > 1 and (from_arg[1] == "AS" or from_arg[1] == "") and not isinstance(from_arg[0], basestring):
            subquery = from_arg[0]

            local_step_number += 1
            steps += parse_sql_query(subquery, substep_number)

            # Add the separate rename step
            index_of_new_tables = len(current_namespace)
            prev_step = steps[-1]
            prev_step_number = prev_step.result_table
            rename_number = current_step_number + '.' + str(local_step_number)
            rename_sql_chunk = ' '.join(from_arg[1:])
            rename_new_name = from_arg[2]
            rename_executable_sql = "SELECT * FROM (" + prev_step.executable_sql[:-1] + ') ' + rename_sql_chunk
            subquery_namespace = steps[-1].namespace
            
            # Get the namespace after the subquery
            subquery_cols = [c for t in subquery_namespace for c in t[1]]
            this_namespace = [(rename_new_name, subquery_cols)]

            for item in this_namespace:
                if item not in current_namespace:
                    current_namespace.append(item)

            substep = QueryStep(rename_number, rename_sql_chunk, [prev_step_number], rename_new_name, rename_executable_sql, this_namespace[:])
            steps.append(substep)

            last_from_table = rename_new_name
            local_step_number += 1
            substep_number = current_step_number + '.' + str(local_step_number)

        # Case of simple table select
        else:
            # Step for collecting the new table
            sql_chunk = extract_from_arg_table_name(from_arg)
            executable_sql = "SELECT * FROM " + sql_chunk

            full_table_name = extract_from_arg_table_name(from_arg)
            original_table_name = full_table_name.split(' ')[0]
            output_table_name = full_table_name.split(' ')[-1]

            this_namespace = [(output_table_name, schema[original_table_name])]
            
            for item in this_namespace:
                if item not in current_namespace:
                    current_namespace.append(item)

            substep = QueryStep(substep_number, sql_chunk, [], output_table_name, executable_sql, this_namespace[:])
            steps.append(substep)
            local_step_number += 1
            substep_number = current_step_number + '.' + str(local_step_number)

        # Step for joining everything up to this point and this table
        combine_sql_chunk += ' ' + from_connector + ' ' + lst_to_str(from_arg)
        combine_executable_sql += ' ' + from_connector + ' ' + lst_to_str(from_arg)
        new_joined_table = output_table_name
        output_table_name = substep_number if (i+2) != len(args) else current_step_number
        this_namespace = get_namespace(steps, table_name=last_from_table)
        this_namespace = this_namespace[:] + (get_namespace(steps, table_name=new_joined_table))
        #     for j in range(len(this_namespace)):
        #         table = this_namespace[j][0]
        #         cols = this_namespace[j][1]

        #         this_namespace[j] = (this_namespace[j][0], [c for c in cols if c in keep_cols])

        substep = QueryStep(substep_number, combine_sql_chunk, [last_from_table, new_joined_table], output_table_name, combine_executable_sql, this_namespace[:])
        steps.append(substep)

        last_from_table = output_table_name

        i += 2 # Going by twos, collecting the connector and the next table

    return steps


def extract_from_arg_table_name(from_arg):
    if len(from_arg) == 1:
        return from_arg[0]
    elif len(from_arg) == 3:
        if from_arg[1] == 'ON':
            if len(from_arg[0]) == 3:
                return from_arg[0][0] + ' ' + from_arg[0][2]
            else:
                return from_arg[0][0]
        else:
            # If it's a renamed query or table
            if not isinstance(from_arg[0], basestring):
                return from_arg[2]
            else:
                return lst_to_str(from_arg[0]) + ' ' + lst_to_str(from_arg[2])

    # Not correctly parsable
    return ''


def get_namespace_from_args(from_args):
    i = 0
    extracted_namespace = []
    while i < len(from_args):
        from_arg = from_args[i]
        table_names = extract_from_arg_table_name(from_arg)
        new_name = table_names.split(' ')[-1]
        schema_table = table_names.split(' ')[0]

        if schema_table in schema:
            extracted_namespace.append((new_name, schema[schema_table]))
        else:
            # Subquery in from clause
            if not isinstance(from_args[i][0], basestring):
                subquery_namespace = sql_ast_to_steps(from_args[i][0], schema)[-1].namespace
                keep_cols = []
                for table in subquery_namespace:
                    keep_cols += table[1]
                extracted_namespace.append((new_name, keep_cols))
        i += 2
    return extracted_namespace


def parse_where(ast_node, step_number='', parent_number='', prev_steps=[]):

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
    
    input_tables = [prev_steps[-1].result_table]
    result_table = current_step_number

    prev_step = prev_steps[-1]

    # Check if selecting DISTINCT
    column_list = ast_node[-1]
    column_string = make_column(column_list)
    sql_chunk = 'SELECT ' + column_string 
    executable_sql = sql_chunk + " " + prev_step.executable_sql[9:-1]
    # Go through existing tables and do three things:
    #   1. Modify names of existing columns if renamed 
    #   2. Remove columns that weren't selected
    #       a. If table matches, remove columns not selected
    #       b. If table not matched, remove all columns
    #   3. Add new columns (i.e. static ones, combined ones, col ops)

    # Create copy of namespace
    
    from_step_number = parent_number + str(1)
    from_namespace = get_namespace(prev_steps, step_number=from_step_number)

    current_namespace = from_namespace[:]
    all_cols = get_all_cols(current_namespace)
    if column_list[0] != "*":
        current_namespace.append(('', [])) # Empty tuple for collecting columns not associated with any table
        final_cols = {} # Used to remove any columns that were not selected

        for col in column_list:
            equation_or_old_col = col[0]
            start_name = equation_or_old_col
            final_col_name = ''
            table_name = None

            if len(col) == 3:
                final_col_name = col[-1]

            if not final_col_name:
                if isinstance(start_name, basestring):
                    start_name = lst_to_str(start_name)
                final_col_name = start_name
            
            if '.' in start_name:
                table_name = start_name.split('.')[0]
                final_col_name = start_name.split('.')[1]

            # If table name is prefixed add to final_cols
            if table_name:
                if table_name in final_cols:
                    final_cols[table_name].append(final_col_name)
                else:
                    final_cols[table_name] = [final_col_name]

            # Go through existing namespace and perform steps 1 and 3
            for i in range(len(current_namespace)):
                table = current_namespace[i][0]
                cols = current_namespace[i][1]

                if table_name == '':
                    cols.append(final_col_name)

                # Either match the table name or look for the column in the table name
                # This works because ambiguous column names must be differentiated using the table name
                if (not table_name or table == table_name) and (final_col_name in cols):
                    # Replace the old column name with the new column name, if there is a new column name
                    current_namespace[i][1][cols.index(final_col_name)] = final_col_name
                    final_cols[table] = final_cols[table] + [final_col_name] if table in final_cols else [final_col_name]
                elif (not table_name and final_col_name not in all_cols):
                    current_namespace[i][1].append(final_col_name)

        for i in range(len(current_namespace)):
            table = current_namespace[i][0]
            cols = current_namespace[i][1] # Remove the table prefixes

            if table in final_cols:
                keep_cols = final_cols[table]
                current_namespace[i] = (current_namespace[i][0], [c for c in cols if c in keep_cols])

        # Remove the independent columns if there are none
        if current_namespace:
            current_namespace = [x for x in current_namespace if x[1] != [] and (x[0] == '' or x[0] in final_cols)]

    select_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, current_namespace)
    steps.append(select_step)

    global namespace
    namespace = current_namespace

    return steps


def parse_distinct(ast_node, step_number='', parent_number='', prev_steps=[]):

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
    executable_sql = "SELECT DISTINCT " + prev_step.executable_sql[7:-1]

    distinct_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql)
    steps.append(distinct_step)

    return steps


def parse_set(ast_node, step_number='', parent_number='', prev_steps=[]):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 3:
        print("Not enough arguments for UNION clause: <query1> UNION <query2>")
        return

    if parent_number and parent_number[-1] != '.':
        parent_number += '.'

    # UNION step
    current_step_number = parent_number + step_number
    sql_reorder = [ast_node[1], ast_node[0], ast_node[2]]
    sql_chunk = lst_to_str(sql_reorder)
    input_tables = []
    result_table = current_step_number
    executable_sql = sql_chunk
    namespace = []

    union_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(union_step)
    
    input_num1 = current_step_number + '.1'
    input_num2 = current_step_number + '.2'
    query1 = parse_sql_query(ast_node[1], input_num1)
    query2 = parse_sql_query(ast_node[2], input_num2)

    steps += query1
    steps += query2

    #WLOG, namespace is same as query 1's namespace

    cols = query2[-1].namespace[0][1]
    namespace.append(('', cols))
    namespace = [x for x in namespace if x[1] != [] and (x[0] == '')]
    
    prev_step_number = query2[-1].step_number
    current_step_number += '.3'
    input_tables = [input_num1, input_num2]
    union_sub_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)

    steps.append(union_sub_step)

    return steps


def parse_order_by(ast_node, step_number='', parent_number='', prev_steps=[]):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'ORDER BY':
        print("No ORDER BY clause")
        return

    orderby_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(orderby_step)

    return steps


def parse_limit(ast_node, step_number='', parent_number='', prev_steps=[]):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'LIMIT':
        print("No LIMIT clause")
        return

    limit_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(limit_step)

    return steps


def parse_offset(ast_node, step_number='', parent_number='', prev_steps=[]):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 1 or ast_node[0] != 'OFFSET':
        print("No OFFSET clause")
        return

    offset_step = parse_clause(ast_node, step_number, parent_number, prev_steps)
    steps.append(offset_step)

    return steps


def parse_create_view(ast_node, step_number=''):

    # Generate a list of steps just for this statement, they should get merged by previous calls
    steps = []

    if len(ast_node) < 2:
        print("Not enough arguments for CREATE VIEW clause: CREATE VIEW AS? <query>")
        return

    current_step_number = '1'
    sql_chunk = lst_to_str(ast_node)
    input_tables = []
    result_table = ast_node[1]
    executable_sql = sql_chunk
    namespace = [(result_table, [])]
    
    create_view_step = QueryStep(current_step_number, sql_chunk, input_tables, result_table, executable_sql, namespace)
    steps.append(create_view_step)

    query = parse_sql_query(ast_node[-1], current_step_number + '.1')
    steps += query

    current_step_number += '.2'
    last_query_step_number = [query[-1].result_table]

    # Replace namespace table with view name
    last_query_namespace = query[-1].namespace
    for name in last_query_namespace:
        namespace[0][1].extend(name[1])

    create_view_sub_step = QueryStep(current_step_number, sql_chunk, last_query_step_number, result_table, executable_sql, namespace)
    steps.append(create_view_sub_step)

    return steps
