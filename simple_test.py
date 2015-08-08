from sql_parser import *
import sql_parser
import pdb
from pprint import pprint
from traces import DESIRED_ASTS

# Test SQL
sql =\
"SELECT * FROM MY_TABLE; -- This is a standard SQL comment;\n\
UPDATE MY_TABLE SET A = 5;\n\
/* multiline comment\n\
 * with nesting:\n\
    /* nested block comment */\n\
*/\n\
INSERT INTO MY_TABLE VALUES (3, 'hi there');"

schema = {
    "Student": ['sid', 'firstName', 'email', 'cgpa'],
    "Course": ['dept', 'cNum', 'name'],
    "Offering": ['oid', 'dept', 'cNum', 'instructor'],
    "Took": ['sid', 'ofid', 'grade'],
}


if __name__ == '__main__':
    sql_parser.schema = schema

    #print(sql)
    #print("----------------------------------------------")
    #pprint(split_sql_queries(sql))
    #print("----------------------------------------------")

    #ast = DESIRED_ASTS['simple_query']
    #pprint(sql_ast_to_steps(ast, schema))


    # The simple_natural_join_query test case
    #from_test_case = [ 'FROM', [['Student'], 'NATURAL JOIN', ['Took'], 'NATURAL JOIN', ['Course']]]

    # The simple_query test case
    #from_test_case = [ 'FROM', [['Student']] ]

    # A simple rename test case
    #from_test_case = [ 'FROM', [['Student','AS','Gooby']] ]

    # The simple_subquery test case
    from_test_case = ['FROM',[[[[ 'SELECT', [['oid'], ['dept']] ],[ 'FROM', [['Offering']] ]], 'AS', 'LimitedCols']]]

    # The simple_natural_join_query test case
    #from_test_case = [ 'FROM', [['Offering', '', 'o1'], 'JOIN', [['Offering', '', 'o2'], 'ON', ['Took.ofid','=','Offering.ofid']]]]

    # Attempting to translate a query, gives really weird results back
    #query_text =\
    #' SELECT * '\
    #' FROM Offering o1 JOIN Offering o2 ON o1.oid = o2.oid '
    #from_test_case = sql_to_ast(query_text).asList()


    # Run just the FROM test case and print results; __repr__ will ensure they print out in a readable way
    from_steps = parse_from(from_test_case)
    pprint(from_steps)

    #reorder_test =  [[[[['select', ['sid']],['from', 'Took']],'union',[['select', ['sid']],['from', ['Student']]]],'union',[['select', ['*']],['from', ['Course']]]],['ORDER BY', ['sid']],['LIMIT', '100']]
    #pprint(reorder_sql_statements(reorder_test))
