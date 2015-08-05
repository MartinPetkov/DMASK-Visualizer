from sql_parser import *
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
    "Student": ['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
    "Course": ['Course.dept', 'Course.cNum', 'Course.name'],
    "Offering": ['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
    "Took": ['Took.sid', 'Took.ofid', 'Took.grade'],
}


if __name__ == '__main__':
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
    #from_test_case = ['FROM',[[[[ 'SELECT', [['oid'], ['dept']] ],[ 'FROM', [['Offering']] ]], 'AS', 'LimitedCols']]]


    # Run just the FROM test case and print results; __repr__ will ensure they print out in a readable way
    #from_steps = parse_from(from_test_case)
    #pprint(from_steps)

    reorder_test =  [
                        [
                            [
                                [
                                    ['select', ['sid']],
                                    ['from', 'Took']
                                ],
                                'union',

                                [
                                    ['select', ['sid']],
                                    ['from', ['Student']]
                                ]
                            ],

                            'union',

                            [
                                ['select', ['*']],
                                ['from', ['Course']]
                            ]
                        ],
                        ['ORDER BY', ['sid']],
                        ['LIMIT', '100']
                    ]
    pprint(reorder_sql_statements(reorder_test))
