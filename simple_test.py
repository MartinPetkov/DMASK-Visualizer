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

    from_test = [ 'FROM', [
                            ['Student'],
                            'NATURAL JOIN', ['Took'],
                            'NATURAL JOIN', ['Course']
                          ]
                ]
    from_steps = parse_from(from_test)
    pprint(from_steps)
