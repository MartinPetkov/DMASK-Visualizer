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
import copy


# TODO: Figure out how to handle the database connection
""" A class to handle the conversion functions and the database connection """
class DMASK:

    """
    Create a DMASK object.

    :param conn_params: The database connection parameters
    """
    def __init__(self, conn_params, base_tables):
        # TODO: Implement the database connection parameters
        self.conn_params = conn_params
        self.base_tables = base_tables

    def set_connection(self, schema=""):
        # TODO: Implement connecting to a database
        self.connection = psycopg2.connect(self.conn_params)
        self.cursor = self.connection.cursor()

        #TODO: Remove the below (which sets the schema)
        if schema:
            self.cursor.execute("SET search_path TO "+schema)

    def set_base_tables(self, base_tables):
        # TODO: Implement
        self.base_tables = base_tables


    """
    Convert a set of sql queries to JSON output suitable for the visualizer frontend
    Requires the connection parameters and base tables to be set
    """
    def sql_to_json(self, sql_queries):
        # TODO: Implement

        json_queries = []

        queries = sql_parser.split_sql_queries(sql_queries)
        
        for query in queries:
            ast = sql_parser.sql_to_ast(query)
            base_tables = self.base_tables.copy()
            # ERROR IN SQL_PARSER: steps can included a nested list -- temporary fix: Flatten list
            steps = flatten_list(sql_parser.sql_ast_to_steps(ast, self.base_tables))
            tables = self.steps_to_tables(steps)
            parsed_query = ParsedQuery(steps, tables, query, base_tables)
            json_queries.append(parsed_query.to_json())

        return json_queries



    """ Convert a set of relational algebra queries to JSON output suitable for the visualizer frontend """
    def ra_to_json(self, ra_queries):
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


    def steps_to_tables(self, steps):
        # Turns the QuerySteps given into Table objects by executing their queries on the database given by
        # self.conn_params and with the base tables given by self.base_tables
        tables = {}

        # Create a connection and cursor (PSQL)
        connection = self.connection;
        cursor = self.cursor;
        
        view_made = False
        # ERROR IN SQL_PARSER: steps can included a nested list -- temporary fix: Flatten list
        steps = flatten_list(steps)
        
        for step in steps:
            if str(step.result_table) not in tables:
                # Get the table name (table name matches FROM statement of the executable)
                name = get_table_name(step.executable_sql)

                # Do not generate tables for a create view step
                if (step.executable_sql.lower().find("create view") == 0):
                    if not view_made:
                        cursor.execute(step.executable_sql)
                        view_made = True
                    if (step.input_tables):
                        name = str(step.result_table)
                        input_table = tables[step.input_tables[0]]
                        tables[name] = Table(name, step.step_number, input_table.col_names, input_table.tuples, {})
                        self.base_tables[name] = input_table.col_names
                        
                else:
                    # Execute the query
                    cursor.execute(step.executable_sql)
    
                    # Get the columns
                    columns = [desc[0] for desc in cursor.description]
    
                    # Get the tuples
                    tuples = []
                    for row in cursor:
                        tuples.append(row)
    
                    # If the sql chunk is a where clause, get the reasons
                    # TODO: Adjust this to work for RA as well
                    if (step.sql_chunk.split()[0].lower() == "where"):
                        # Get all of the conditions (and the ASTs of their corresponding subqueries)
                        (conditions, subqueries) = get_all_conditions(step.executable_sql)
    
                        # Add the reasons for the input table
                        input_step = None
                        for s in steps:
                            if s.step_number == tables[step.input_tables[0]].step:
                                input_step = s
                        tables[str(input_step.result_table)].reasons = get_reasons(conditions, subqueries, input_step, tables, self)
                        set_passed(tables[str(input_step.result_table)].reasons, tables[input_step.result_table].tuples, tuples)
                        
                    # Prefix duplicate columns
                    duplicates = []
                    for i in range(len(columns)):
                        if columns.count(columns[i]) > 1:
                            duplicates.append(i)
                    namespace = get_namespace(sql_parser.sql_to_ast(step.executable_sql).asList(), self)
                    
                    for index in duplicates:
                        for alias_set in namespace:
                            if alias_set[0].lower() == columns[index].lower() and len(alias_set) > 1:
                                columns[index] = alias_set[1]
                                alias_set.pop(1)
                    
                    t = Table(name, step.step_number, columns, tuples, {})
                    tables[str(step.result_table)] = t
                    
        return tables
    
def set_passed(reasons, input_tuples, results):
    for i in range(1, len(input_tuples) + 1):
        if i in reasons and input_tuples[i - 1] not in results:
            reasons[i].passed = False

def get_all_conditions(sql_chunk):
    # Get the AST for the WHERE clause
    ast = sql_parser.sql_to_ast(sql_chunk).asList()

    for node in ast:
        if node[0].lower() == "where":
            return conditions_helper(node[1])

    return ([], {})

    # Given an AST for the WHERE clause, return a tuple containing 2 items:
    # The first is a list of all the conditions in the where clause (ex. ["grade >= 80", "cnum in SELECT ..."])
    # The second is a dictionary mapping a condition to its AST {"condition": [AST]}


def conditions_helper(ast):
    # If the first item in a list is a string, then that list contains a
    # condition -- Traverse the AST and return all conditions
    conditions = []
    subqueries = {}
    for item in ast:
        if isinstance(item, list):
            if isinstance(item[0], str):
                (key, sq) = flatten_ast_to_string(item)

                conditions.append(key)

                if sq:
                    subqueries[key] = sq[0]
                
            else:
                results = conditions_helper(item)
                conditions.extend(results[0])
                subqueries.update(results[1])

    return (conditions, subqueries)

def flatten_ast_to_string(item):
    # Given part of an AST, search for subqueries and return the flattened
    # expression with appropriate bracketing (as well as the ASTs of the subqueries)
    
    sq = find_subqueries(item)
    for s in sq:
        if (sq.count(s) > 1):
            sq.remove(s)
    
    key = " ".join(flatten_list(item))
    for subquery in sq:
        subquery_string = " ".join(flatten_list(subquery))
        key = key.replace(subquery_string, "("+subquery_string+")")    
    return (key, sq)

def find_subqueries(ast):
    # Given a list, return all subqueries found in the AST
    subqueries = []
    
    # Given an AST, locates every subquery
    if (isinstance(ast[0], list) and ast[0][0] == "SELECT"):
        subqueries.append(ast)
    
    for item in ast:
        if isinstance(item, list): # Possible the AST [["SELECT", [...]], ...]
            first_child = item[0]   # Possibly the list ["SELECT", [...]]
            if isinstance(first_child, list):
                maybe_select = first_child[0]
                if maybe_select == "SELECT":
                    subqueries.append(item)
            subqueries.extend(find_subqueries(item))
    return subqueries

def get_reasons(conditions, subqueries, input_step, tables, dmask):
    # Given a list of conditions, subqueries, the input step and dmask object,
    # return the Reasons
    input_query = input_step.executable_sql
    input_table = tables[input_step.result_table]
    input_tuples = input_table.tuples
    reasons = {0:Reason([], {}, [])}
    
    # Get the namespace of the entire query (only really need the FROM clause
    # of the original query)
    ast = sql_parser.sql_to_ast(input_query).asList()
    namespace = get_namespace(ast, dmask)

    connection = dmask.connection
    cursor = dmask.cursor

    # Execute all of the conditions
    for condition in conditions:
        reasons[0].conditions_matched.append(condition)
    
        condition_sql = input_query.strip(';') + " WHERE " + condition

        # Execute the query
        cursor.execute(condition_sql)

        # Get the columns
        columns = [desc[0] for desc in cursor.description]

        # Get the tuples
        tuples = []
        for row in cursor:
            tuples.append(row)

        correlated = []

        # Execute the corresponding subquery, getting its steps and tables
        if condition in subqueries:
            subquery = subqueries[condition]

            # Check if the subquery is correlated
            correlated = get_correlated_elements(subquery, dmask)

            if correlated:
                # If it is, prepare it for substitution for execution at each row
                pq = PreparedQuery(subquery, correlated)
            else:
                # If it's not, execute the subquery and store it in the reasons[0]
                steps = sql_parser.sql_ast_to_steps(subquery, dmask.base_tables)
                tables = dmask.steps_to_tables(steps)
                name = flatten_ast_to_string(subquery)[0]
                if name[0] == "(":
                    name = name[1:-1]
                name += ";"
                parsed_query = ParsedQuery(steps, tables, name, base_tables = dmask.base_tables)
                reasons[0].subqueries[condition] = parsed_query

        # Go through each row and add a reason
        for i in range(0, len(input_tuples)):
            # Substitute and execute the correlated subquery
            if correlated:
                # Get the items to substitute
                substitutes = {}

                for item in correlated:
                    for j in range(len(columns)):
                        if matches_alias(namespace, columns[j], item):
                            substitutes[item] = input_tuples[i][j]
                            break
                    # TODO:
                    # If substitutes[item] does not exist at this point, then
                    # it might be an aggregate function, in which case
                    # you will want to do "SELECT item FROM <from clause>"
                    # which may or may not fail


                # Substitute them in the query
                substituted_subquery = pq.substitute(substitutes)
                parsed_query = None
                if substituted_subquery:
                    # Create the parsed query
                    steps = sql_parser.sql_ast_to_steps(substituted_subquery, dmask.base_tables)
                    tables = dmask.steps_to_tables(steps)
                    parsed_query = ParsedQuery(steps, tables, " ".join(flatten_list(substituted_subquery)), base_tables = dmask.base_tables)

            # If the input tuple is in the returned list of tuples, it passed the condition
            kept = input_tuples[i] in tuples

            # If the tuple was kept or if there was a correlated subquery, add it as a reason
            if kept or correlated:
                if i+1 in reasons:
                    reasons[i+1].conditions_matched.append(condition)
                else:
                    reasons[i+1] = Reason([condition], {}, [])
                    
                # If there was a correlated subquery, add the parsed query and, if the condition
                # passed, add it to the list of passed subqueries
                if correlated:
                    if parsed_query:
                        reasons[i+1].subqueries[condition] = parsed_query
                    if kept:
                        reasons[i+1].passed_subqueries.append(condition)
    return reasons

def get_correlated_elements(query, dmask):
    # Given an AST representing a query, return a list of elements that do not
    # appear in the namespace of the (isolated) query.

    # get the namespace of the subquery
    namespace = [i.lower() for i in flatten_list(get_namespace(query, dmask))]

    # get the attributes called in the subquery
    attributes = find_attributes(query)

    # for each attribute, if it appears somewhere in the namespace, remove it
    i = 0
    while (i < len(attributes)):
        if attributes[i].lower() in namespace:
            attributes.pop(i)
        else:
            i += 1

    # return the list of remaining attributes (which did not appear in the namespace)
    return attributes

def find_attributes(query):
    # Given an AST representing a query, return a list of the attributes that appear
    # in the query (anything that is not a keyword or table name is an attribute)

    # DOES NOT HANDLE SUBQUERIES -- Subqueries would need to be handled recursively
    query = query[:]
    # Remove the FROM clause
    for i in range(len(query)):
        if query[i][0].lower() == "from":
            query.pop(i)
            break
    
    attributes = remove_keywords(flatten_list(query))
    return attributes

def remove_keywords(query):
    # Goes through a list and removes any keywords
    i = 0
    while i < len(query):
        if (is_keyword(query[i])):
            query.pop(i)
        else:
            i += 1
    return query

def is_keyword(string):
    punctuation = "~!@#$%^&*()-_=+[]\\|/.,<> \n"
    # At the moment, this list is nonexhaustive (see
    # http://www.postgresql.org/docs/9.3/static/sql-keywords-appendix.html
    # for full list of keywords)
    KEYWORDS = ["CREATE VIEW", "FROM", "WHERE", "HAVING", "GROUP BY", "SELECT",
                "DISTINCT", "UNION", "ORDER BY", "LIMIT", "OFFSET", "OR", "AND",
                "ANY", "ALL", "AS", "ASC", "DESC", "AVG", "BOTH", "ALWAYS",
                "BETWEEN", "JOIN", "NATURAL JOIN", ",", "EXCEPT", "EQUALS",
                "IN", "MIN", "MAX", "COUNT", "LEFT JOIN", "RIGHT JOIN",
                "LEFT INNER JOIN", "LEFT OUTER JOIN", "RIGHT INNER JOIN",
                "RIGHT OUTER JOIN", "EXISTS", "*"]

    # If subqueries are handled recursively, then none of the 'from clause' keywords
    # has to be mentioned

    string = string.upper().strip(punctuation)
    if not string or string.isnumeric() or string[0] == '"' or string[0] == "'":
        return True
    return (string in KEYWORDS)

def get_namespace(subquery, dmask):
    # Given an AST, return the namespace of the table in the form:
    # [[column, prefix.column, ...], [column, prefix.column, ...]]

    from_clause = []

    for node in subquery:
        if node[0].lower() == "from":
            from_clause = node[1]
            break

    on_using = False

    # tables is a list of (name, alias) tuples
    tables = []

    # Get all of the tables brought in (ex. FROM Took t, Student -> [(Took, t), (Student, Student)])
    for item in from_clause:
        if isinstance(item, list):
            if 'ON' in item or 'USING' in item:
                item = item[0]
            name = item[0]
            alias = item[-1]
            # If there's a subquery, bracket the name and add the alis
            if isinstance(name, list):
                name = flatten_ast_to_string(name)[0] + " " + alias
            tables.append((name, alias))
    
    main_table = flatten_ast_to_string(from_clause)[0]
    namespace = [[column] for column in get_columns("SELECT * FROM " + main_table, dmask)]
    
    # Traverse the list of tables, adding all of the columns to the namespace
    for table in tables:
        columns = get_columns("SELECT * FROM " + table[0], dmask)
        prefix = table[1]
        for column in columns:
            for name in namespace:
                if column == name[0]:
                    name.append(prefix + "." + column)
                    break

    return namespace

def get_columns(query, dmask):
    cursor = dmask.cursor

    # Execute the query
    cursor.execute(query + " LIMIT 0")

    # Get the columns
    return [desc[0] for desc in cursor.description]

def matches_alias(namespace, attribute, to_match):
    # Given a namespace, attribute (ex. "sid") and someting to match (ex. "Took.sid")
    # Returns true whether the attribute matches to_match
    to_match = to_match.lower()
    
    if attribute.lower() == to_match:
        return True

    for item in namespace:
        if to_match in [i.lower() for i in item]:
            return True

    return False



def get_table_name(exsqltable):
    # Given an executable SQL statement, return the table's name
    # TODO: This would be very weird for RA statements (even though it would work). Make an RA equivalent?

    # Get the AST so we can identify the FROM clause
    if (exsqltable.find("UNION") > -1):
        split = exsqltable.split("UNION")
        name = []
        for item in split:
            name.append(get_table_name(item))
        return " UNION ".join(name)
    
    ast = find_query(sql_parser.sql_to_ast(exsqltable).asList())

    # Traverse the AST until the FROM clause is found
    for node in ast:
        if node[0].lower() == "from":
            # The second element in the node [FROM, [...]] holds the table's name
            from_ast = node[1]
            name = []

            # Traverse each token in the FROM query
            for token in from_ast:
                # If it's a string, then it's either a keyword or table name, unless it follows the ON or USING keywords
                if isinstance(token, str):
                    # If the token is a "," (JOIN) add it to the previous token
                    if token.strip() == ",":
                        name[-1] = str(name[-1]) + ","
                    else:
                        name.append(token)
                elif isinstance(token, list):
                    if 'ON' in token or 'USING' in token:
                        # For the elements following ON/USING keywords, flatten them and add it to name
                        flattened = flatten_list(token)
                        name.extend(flattened)
                    else:
                        name.append(token[-1])

            # Return a string joined by whitespace
            return " ".join(str(item) for item in name)

def find_query(ast):
    if (isinstance(ast[0], list) and ast[0][0] == "SELECT"):
        return ast
    
    for item in ast:
        if isinstance(item, list):
            if isinstance(item[0], list):
                if item[0][0] == "SELECT":
                    return item
                elif isinstance(item[0][0], list):
                    search = find_query(item[0])
                    if search:
                        return search

def flatten_list(l):
    # Given a list of string or lists, flatten them into one list
    ret_val = []
    for item in l:
        if not isinstance(item, list):
            ret_val.append(item)
        else:
            ret_val.extend(flatten_list(item))
    return ret_val


class PreparedQuery:
    def __init__(self, query, substitutable):
        self.query = query
        self.substitutable = {}

        for item in substitutable:
            self.substitutable[item] = item

    def substitute(self, substitutes):
        # check to make sure everything that needs to be substituted is present
        for key in self.substitutable:
            if key not in substitutes:
                return

        # make a deep copy of the AST
        query_copy = copy.deepcopy(self.query)

        def replace(query, substitutes):
            for i in range(len(query)):
                element = query[i]

                if isinstance(element, list):
                    replace(element, substitutes)
                elif element in substitutes:
                    query[i] = str(substitutes[element])

        replace(query_copy, substitutes)
        return query_copy

# TODO: REMOVE -- this function is for sophia's testing purposes and is here because
# she doesn't want to rewrite this every single time
import psycopg2

def visualize_query(sql):
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    schema = {"Student" : ["sid", "firstName", "email", "cgpa"],
              "Course": ["dept", "cNum", "name"],
              "Offering": ["oid" ,"dept", "cNum", "instructor"],
              "Took": ["sid", "ofid", "grade"]
             }
    dmask = DMASK(conn_string, schema)
    dmask.set_connection("sophiadmask")

    # get_namespace works
    json = ""
    json = dmask.sql_to_json(sql)
    
    # nothing gets commited -- closing the connection will prevent hanging
    dmask.connection.close()
    
    import os.path
    f = open("front-end-code/template.html")
    copy = f.readlines()
    for i in range(len(copy)):
        if copy[i].strip() == "<!-- INSERT TEST BELOW -->":
            copy[i] = "<script>var pq = " + str(json) +";</script>"
        
    # MODIFY THIS PATH -- Need to get the current directory to append front-end-code/results.html
    output = open("C:/Users/School/Documents/DeMASK/git/front-end-code/results.html", "w")
    for line in copy:
        output.write(line)
    f.close()
    output.close()
    
print("File is located in front-end-code/results.html")
print("To run: visualize_query('QUERY')")