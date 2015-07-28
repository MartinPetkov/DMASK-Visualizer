from parsed_query import *
from query_step import *
from table import *

from pprint import pprint

'''
The schema:
Student(_sid_, firstName, email, cgpa)
Course(_dept,cNum_, name)
Offering(_oid_, dept, cNum, instructor)
Took(_sid,ofid_, grade)
'''

# Starting Values:
Student_colnames = ['sid', 'firstName', 'email', 'cgpa']
Student_tuples=[
('1', 'Martin', 'martin@mail.com', '3.4'),
('2', 'Kathy', 'kathy@mail.com', '4.0'),
('3', 'Sophia', 'sophia@mail.com', '1.7'),
('4', 'James', 'james@mail.com', '2.8')]
Student_table = Table(t_name='Student', step = '0', col_names=Student_colnames, tuples=Student_tuples)

Course_colnames = ['dept', 'cNum', 'name']
Course_tuples=[
('csc', '148', 'Intro to Computer Science'),
('csc', '209', 'Systems Programming'),
('csc', '343', 'Intro to Databases'),
('mat', '137', 'Calculus'),
('ger', '100', 'Intro to German')]
Course_table = Table(t_name='Course', step = '0', col_names=Course_colnames, tuples=Course_tuples)

Offering_colnames = ['oid', 'dept', 'cNum', 'instructor']
Offering_tuples=[
('1', 'csc', '209', 'K. Reid'),
('2', 'csc', '343', 'D. Horton'),
('3', 'mat', '137', 'J. Kamnitzer'),
('4', 'ger', '100', 'E. Luzi'),]
Offering_table = Table(t_name='Offering', step = '0', col_names=Offering_colnames, tuples=Offering_tuples)

Took_colnames = ['sid', 'ofid', 'grade']
Took_tuples=[
('1', '2', '87'),
('1', '4', '73'),
('2', '2', '92'),
('3', '1', '80'),
('4', '1', '60')]
Took_table = Table(t_name='Took', step = '0', col_names=Took_colnames, tuples=Took_tuples)


global_tables = {
    'Student': Student_table,
    'Course': Course_table,
    'Offering': Offering_table,
    'Took': Took_table,
    }

DESIRED_ASTS = {}

# ============= FIXED ================
''' A simple SELECT-FROM-WHERE query '''
def generate_simple_query():
    query_text =\
    ' SELECT sid, cgpa' +\
    ' FROM Student' +\
    ' WHERE cgpa > 3'

    steps = [
        QueryStep('1', 'FROM Student', [], 'Student', 'SELECT * FROM Student',
            namespace=["Student: sid, firstName, email, cgpa "]),
        QueryStep('2', 'WHERE cgpa > 3', ['Student'], '2', 'SELECT * FROM Student WHERE cgpa > 3'),
        QueryStep('3', 'SELECT sid, cgpa', ['2'], '3', 'SELECT sid, cgpa FROM Student WHERE cgpa > 3'),
    ]

    tables = {
        '1': Table(t_name='Student',
                    step='1',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')],
                    reasons={
                        0: Reason(["cgpa > 3"]),
                        1: Reason(["cgpa > 3"]),
                        2: Reason(["cgpa > 3"])
                    }),
        '2': Table(t_name='Student',
                   step='2',
                   col_names=['sid', 'firstName', 'email', 'cgpa'],
                   tuples=[
                           ('1', 'Martin', 'martin@mail.com', '3.4'),
                           ('2', 'Kathy', 'kathy@mail.com', '4.0')]
                   ),
        '3': Table(t_name='Student',
                   step='3',
                   col_names=['sid', 'cgpa'],
                   tuples=[
                           ('1', '3.4'),
                           ('2', '4.0')]
                   )
    }


    # Strings if it is a simple column or table, list if it's a subquery or expression (i.e. "SELECT (a+b) AS col1")
    DESIRED_ASTS['simple_query'] =\
        [
            [ 'SELECT', [['sid'], ['cgpa']] ],
            [ 'FROM',   [ ['Student'] ] ],
            [ 'WHERE',  [ ['cgpa', '>', '3'] ] ],
        ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with a cross product in it '''
def generate_simple_cross_product_query():
    query_text =\
    ' SELECT Student.sid, Student.email, Took.grade' +\
    ' FROM Student, Took'

    steps = [
        QueryStep('1', 'FROM Student, Took', [], '1', 'SELECT * FROM Student, Took',
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade"]),
        QueryStep('1.1', 'Student', [], 'Student', 'SELECT * FROM Student',
            namespace=[ "Student: sid, firstName, email, cgpa"]),
        QueryStep('1.2', 'Took', [], 'Took', 'SELECT * FROM Took',
            namespace=[ "Took: sid, ofid, grade"]),
        QueryStep('1.3', 'Student, Took', ['Student', 'Took'], '1', 'SELECT * FROM Student, Took',
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade"]),
        QueryStep('2', 'SELECT Student.sid, Student.email, Took.grade', ['1'], '2', 'SELECT Student.sid, Student.email, Took.grade FROM Student, Took')
        ]

    tables = {
        '1': Table(t_name='Student, Took',
                    step='1',
                    col_names=['Student.sid', 'firstName', 'email', 'cgpa', 'Took.sid', 'ofid', 'grade'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '1', '2', '87'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '1', '2', '87'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '2', '87'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '2', '87'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '1', '4', '73'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '1', '4', '73'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '4', '73'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '4', '73'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '2', '92'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '2', '92'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '2', '2', '92'),
                            ('4', 'James', 'james@mail.com', '2.8',     '2', '2', '92'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '3', '1', '80'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '3', '1', '80'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '3', '1', '80'),
                            ('4', 'James', 'james@mail.com', '2.8',     '3', '1', '80'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '1', '60'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '4', '1', '60'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '4', '1', '60'),
                            ('4', 'James', 'james@mail.com', '2.8',     '4', '1', '60')]
                    ),

        '1.1': Table(t_name='Student',
                    step='1.1',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),

        '1.2': Table(t_name='Took',
                    step='1.2',
                    col_names=['sid', 'ofid', 'grade'],
                    tuples=[
                            ('1', '2', '87'),
                            ('1', '4', '73'),
                            ('2', '2', '92'),
                            ('3', '1', '80'),
                            ('4', '1', '60')]
                    ),

        '1.3': Table(t_name='Student, Took',
                    step='1.3',
                    col_names=['Student.sid', 'firstName', 'email', 'cgpa', 'Took.sid', 'ofid', 'grade'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '1', '2', '87'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '1', '2', '87'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '2', '87'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '2', '87'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '1', '4', '73'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '1', '4', '73'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '4', '73'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '4', '73'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '2', '92'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '2', '92'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '2', '2', '92'),
                            ('4', 'James', 'james@mail.com', '2.8',     '2', '2', '92'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '3', '1', '80'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '3', '1', '80'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '3', '1', '80'),
                            ('4', 'James', 'james@mail.com', '2.8',     '3', '1', '80'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '1', '60'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '4', '1', '60'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '4', '1', '60'),
                            ('4', 'James', 'james@mail.com', '2.8',     '4', '1', '60')]
                    ),

        '2': Table(t_name='Student, Took',
                    step='2',
                    col_names=['sid', 'email', 'grade'],
                    tuples=[
                            ('1', 'martin@mail.com', '87'),
                            ('2', 'kathy@mail.com', '87'),
                            ('3', 'sophia@mail.com', '87'),
                            ('4', 'james@mail.com', '87'),

                            ('1', 'martin@mail.com', '73'),
                            ('2', 'kathy@mail.com', '73'),
                            ('3', 'sophia@mail.com', '73'),
                            ('4', 'james@mail.com', '73'),

                            ('1', 'martin@mail.com', '92'),
                            ('2', 'kathy@mail.com', '92'),
                            ('3', 'sophia@mail.com', '92'),
                            ('4', 'james@mail.com', '92'),

                            ('1', 'martin@mail.com', '80'),
                            ('2', 'kathy@mail.com', '80'),
                            ('3', 'sophia@mail.com', '80'),
                            ('4', 'james@mail.com', '80'),

                            ('1', 'martin@mail.com', '60'),
                            ('2', 'kathy@mail.com', '60'),
                            ('3', 'sophia@mail.com', '60'),
                            ('4', 'james@mail.com', '60')]
                    ),
    }


    DESIRED_ASTS['simple_cross_product_query'] =\
        [
            [ 'SELECT', [['Student.sid'], ['Student.email'], ['Took.grade']] ],
            [ 'FROM',   [ ['Student'], ',', ['Took'] ] ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with two NATURAL JOINs in it '''
def generate_simple_natural_join_query():
    query_text =\
    ' SELECT sid, email, cgpa' +\
    ' FROM Student NATURAL JOIN Took NATURAL JOIN Course'

    steps = [
        QueryStep('1', 'FROM Student NATURAL JOIN Took NATURAL JOIN Course', [], '1',
            executable_sql="SELECT * FROM Student NATURAL JOIN Took NATURAL JOIN Course",
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade",
                        "Course: dept, cNum, name"]),

        QueryStep('1.1', 'Student NATURAL JOIN Took', [], '1.1',
            executable_sql="SELECT * FROM Student NATURAL JOIN Took",
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade"]),

        QueryStep('1.1.1', 'Student', [], 'Student',
            executable_sql="SELECT * FROM Student",
            namespace=[ "Student: sid, firstName, email, cgpa"]),

        QueryStep('1.1.2', 'Took', [], 'Took',
            executable_sql="SELECT * FROM Took",
            namespace=[ "Took: sid, ofid, grade"]),

        QueryStep('1.1.3', 'Student NATURAL JOIN Took', ['Student', 'Took'], '1.1',
            executable_sql="SELECT * FROM Student NATURAL JOIN Took",
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade"]),

        QueryStep('1.2', 'Course', [], 'Course',
            executable_sql="SELECT * FROM Course",
            namespace=[ "Course: dept, cNUm, name"]),

        QueryStep('1.3', 'Student NATURAL JOIN Took NATURAL JOIN Course', ['1.1', 'Course'], '1',
            executable_sql="SELECT * FROM Student NATURAL JOIN Took NATURAL JOIN Course",
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade",
                        "Course: dept, cNum, name"]),

        QueryStep('2', 'SELECT sid, email, cgpa', ['1'], '2',
            executable_sql="SELECT sid, email, cgpa FROM Student NATURAL JOIN Took NATURAL JOIN Course",
            namespace=['1: sid, email, cgpa'])
    ]

    tables = {
        '1': Table(t_name='Student NATURAL JOIN Took NATURAL JOIN Course',
                    step='1',
                    col_names=['sid', 'firstName', 'email', 'cgpa', 'ofid', 'grade', 'dept', 'cNum', 'name'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'csc', '148', 'Intro to Computer Science'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'csc', '148', 'Intro to Computer Science'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'csc', '148', 'Intro to Computer Science'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'csc', '148', 'Intro to Computer Science'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'csc', '148', 'Intro to Computer Science'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'csc', '209', 'Systems Programming'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'csc', '209', 'Systems Programming'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'csc', '209', 'Systems Programming'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'csc', '209', 'Systems Programming'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'csc', '209', 'Systems Programming'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'csc', '343', 'Intro to Databases'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'csc', '343', 'Intro to Databases'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'csc', '343', 'Intro to Databases'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'csc', '343', 'Intro to Databases'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'csc', '343', 'Intro to Databases'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'mat', '137', 'Calculus'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'mat', '137', 'Calculus'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'mat', '137', 'Calculus'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'mat', '137', 'Calculus'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'mat', '137', 'Calculus'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'ger', '100', 'Intro to German'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'ger', '100', 'Intro to German'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'ger', '100', 'Intro to German'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'ger', '100', 'Intro to German'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'ger', '100', 'Intro to German')]

                    ),

        '1.1': Table(t_name='Student NATURAL JOIN Took',
                    step='1.1',
                    col_names = ['sid', 'firstName', 'email', 'cgpa', 'ofid', 'grade'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4', '2', '87'),
                            ('1', 'Martin', 'martin@mail.com', '3.4', '4', '73'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',   '2', '92'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7', '1', '80'),
                            ('4', 'James', 'james@mail.com', '2.8',   '1', '60')]),

        '1.1.1': Table(t_name='Student',
                    step='1.1.1',
                    col_names = ['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]),

        '1.1.2': Table(t_name='Took',
                    step='1.1.2',
                    col_names = ['sid, ofid, grade'],
                    tuples=[
                            ('1', '2', '87'),
                            ('1', '4', '73'),
                            ('2', '2', '92'),
                            ('3', '1', '80'),
                            ('4', '1', '60')]),

        '1.1.3': Table(t_name='Student NATURAL JOIN Took',
                    step='1.1.3',
                    col_names = ['sid', 'firstName', 'email', 'cgpa', 'ofid', 'grade'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4', '2', '87'),
                            ('1', 'Martin', 'martin@mail.com', '3.4', '4', '73'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',   '2', '92'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7', '1', '80'),
                            ('4', 'James', 'james@mail.com', '2.8',   '1', '60')]),

        '1.2': Table(t_name='Course',
                    step='1.2',
                    col_names = ['dept', 'cNum', 'name'],
                    tuples=[
                            ('csc', '148', 'Intro to Computer Science'),
                            ('csc', '209', 'Systems Programming'),
                            ('csc', '343', 'Intro to Databases'),
                            ('mat', '137', 'Calculus'),
                            ('ger', '100', 'Intro to German')]),

        '1.3': Table(t_name='Student NATURAL JOIN Took NATURAL JOIN Course',
                    step='1.3',
                    col_names=['sid', 'firstName', 'email', 'cgpa', 'ofid', 'grade', 'dept', 'cNum', 'name'],
                    tuples = [
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'csc', '148', 'Intro to Computer Science'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'csc', '148', 'Intro to Computer Science'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'csc', '148', 'Intro to Computer Science'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'csc', '148', 'Intro to Computer Science'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'csc', '148', 'Intro to Computer Science'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'csc', '209', 'Systems Programming'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'csc', '209', 'Systems Programming'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'csc', '209', 'Systems Programming'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'csc', '209', 'Systems Programming'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'csc', '209', 'Systems Programming'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'csc', '343', 'Intro to Databases'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'csc', '343', 'Intro to Databases'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'csc', '343', 'Intro to Databases'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'csc', '343', 'Intro to Databases'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'csc', '343', 'Intro to Databases'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'mat', '137', 'Calculus'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'mat', '137', 'Calculus'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'mat', '137', 'Calculus'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'mat', '137', 'Calculus'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'mat', '137', 'Calculus'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87', 'ger', '100', 'Intro to German'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73', 'ger', '100', 'Intro to German'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92', 'ger', '100', 'Intro to German'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80', 'ger', '100', 'Intro to German')]),

        '2': Table(t_name='Student NATURAL JOIN Took NATURAL JOIN Course',
                    step='2',
                    col_names=['sid', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'martin@mail.com', '3.4'),
                            ('1', 'martin@mail.com', '3.4'),
                            ('2', 'kathy@mail.com', '4.0'),
                            ('3', 'sophia@mail.com', '1.7'),
                            ('4', 'james@mail.com', '2.8'),

                            ('1', 'martin@mail.com', '3.4'),
                            ('1', 'martin@mail.com', '3.4'),
                            ('2', 'kathy@mail.com', '4.0'),
                            ('3', 'sophia@mail.com', '1.7'),
                            ('4', 'james@mail.com', '2.8'),

                            ('1', 'martin@mail.com', '3.4'),
                            ('1', 'martin@mail.com', '3.4'),
                            ('2', 'kathy@mail.com', '4.0'),
                            ('3', 'sophia@mail.com', '1.7'),
                            ('4', 'james@mail.com', '2.8'),

                            ('1', 'martin@mail.com', '3.4'),
                            ('1', 'martin@mail.com', '3.4'),
                            ('2', 'kathy@mail.com', '4.0'),
                            ('3', 'sophia@mail.com', '1.7'),
                            ('4', 'james@mail.com', '2.8'),

                            ('1', 'martin@mail.com', '3.4'),
                            ('1', 'martin@mail.com', '3.4'),
                            ('2', 'kathy@mail.com', '4.0'),
                            ('3',  'sophia@mail.com', '1.7'),
                            ('4', 'james@mail.com', '2.8')]

                    )
    }


    DESIRED_ASTS['simple_natural_join_query'] =\
        [
            [ 'SELECT', [['sid'], ['email'], ['cgpa']] ],
            [ 'FROM',   [['Student'], 'NATURAL JOIN', ['Took'],
                            'NATURAL JOIN', ['Course']] ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with a LEFT JOIN on a condition in it '''
def generate_simple_condition_join_query():
    query_text =\
    ' SELECT sid, grade, instructor' +\
    ' FROM Took LEFT JOIN Offering ON Took.ofid=Offering.oid'

    steps = [
        QueryStep('1', 'FROM Took LEFT JOIN Offering ON Took.ofid=Offering.oid', ['Took', 'Offering'], '1',
                  executable_sql="SELECT * Took LEFT JOIN Offering ON Took.ofid=Offering.oid",  
                  namespace=["Took: sid, ofid, grade",
                             "Offering: oid, dept, cNum, instructor"]),
        QueryStep('1.1', 'Took', [], 'Took', 
                executable_sql="SELECT * FROM Took",
                namespace=["Took: sid, ofid, grade"]),
        QueryStep('1.2', 'Offering', [], 'Offering', 
                executable_sql="SELECT * FROM Offering",
                namespace=["Offering: oid, dept, cNum, instructor"]),
        QueryStep('1.3', 'Took LEFT JOIN Offering ON Took.ofid=Offering.oid', ['Took', 'Offering'], '1', 
                  executable_sql="SELECT * FROM Took LEFT JOIN Offering ON Took.ofid=Offering.oid",
                  namespace=["Took: sid, ofid, grade",
                             "Offering: oid, dept, cNum, instructor"]),
        QueryStep('2', 'SELECT sid, grade, instructor', ['1'], '2', 
                executable_sql="SELECT sid, grade, instructor FROM Took LEFT JOIN Offering ON Took.ofid=Offering.oid",
                namespace=["Took: sid, grade", "Offering: instructor"]),
    ]

    tables = {
        '1': Table(t_name='Took LEFT JOIN Offering ON Took.ofid = Offering.oid',
                    step='1',
                    col_names=['sid', 'ofid', 'grade', 'oid', 'dept', 'cNum', 'instructor'],
                    tuples=[
                            ('1', '2', '87', '1', 'csc', '209', 'K. Reid'),
                            ('1', '4', '73', '1', 'csc', '209', 'K. Reid'),
                            ('2', '2', '92', '2', 'csc', '343', 'D. Horton'),
                            ('3', '1', '80', '3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', '1', '60', '4', 'ger', '100', 'E. Luzi')],
                    reasons={
                        0: Reason(["Took.ofid=Offering.oid"]),
                        1: Reason(["Took.ofid=Offering.oid"]),
                        2: Reason(["Took.ofid=Offering.oid"]),
                        3: Reason(["Took.ofid=Offering.oid"]),
                        4: Reason(["Took.ofid=Offering.oid"]),
                        5: Reason(["Took.ofid=Offering.oid"])
                    }),

        '2': Table(t_name='Took LEFT JOIN Offering ON Took.ofid = Offering.oid',
                    step='2',
                    col_names=['Took.sid', 'Took.grade', 'Offering.instructor'],
                    tuples=[
                            ('1', '87', 'K. Reid'),
                            ('1', '73', 'K. Reid'),
                            ('2', '92', 'D. Horton'),
                            ('3', '80', 'J. Kamnitzer'),
                            ('4', '60', 'E. Luzi')]
                    ),
    }


    DESIRED_ASTS['simple_condition_join_query'] =\
        [
            [ 'SELECT', [['sid'], ['grade'], ['instructor']] ],
            [ 'FROM', [['Took'],
                        'LEFT JOIN', ['Offering'], 'ON', ['Took.ofid','=','Offering.ofid']]],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with one subquery in the FROM '''
def generate_simple_subquery():
    query_text =\
    ' SELECT LimitedCols.oid' +\
    ' FROM' +\
    '    (SELECT oid, dept' +\
    '     FROM Offering' +\
    '    ) AS LimitedCols'

    steps = [
        QueryStep('1', 'FROM (SELECT oid, dept FROM Offering) AS LimitedCols', ['Offering'], '1',
                
                executable_sql="SELECT * FROM (SELECT oid, dept FROM Offering) AS LimitedCols",
                namespace=["LimitedCols: oid, dept"]),

            QueryStep('1.1', '(SELECT oid, dept FROM Offering)', ['Offering'], '1.1',
                executable_sql="SELECT oid, dept FROM Offering",
                namespace=["Offering: oid, dept"]),

            QueryStep('1.1.1', 'FROM Offering', [], '1.1.1',
                executable_sql="SELECT * FROM Offering",
                namespace=["Offering: oid, dept, cNum, instructor"]),
            
            QueryStep('1.1.2', 'SELECT oid, dept', ['1.1.1'], '1.1',
                executable_sql="SELECT oid, dept FROM Offering",
                namespace=["Offering: oid, dept"]),

            QueryStep('1.2', 'AS LimitedCols', ['1.1'], '1',
                executable_sql="SELECT * FROM (SELECT oid, dept FROM Offering) AS LimitedCols "
                namespace=["LimitedCols: oid, dept"]),

        QueryStep('2', 'SELECT LimitedCols.oid', ['1'], '2',
                executable_sql="SELECT LimitedCols.oid FROM (SELECT oid, dept FROM Offering) AS LimitedCols"),
    ]

    tables = {
        '1.1.1': Table(t_name='Offering',
                    step = '1.1.1',
                    col_names=['oid', 'dept', 'cNum', 'instructor'],
                    tuples=[
                            ('1', 'csc', '209', 'K. Reid'),
                            ('2', 'csc', '343', 'D. Horton'),
                            ('3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', 'ger', '100', 'E. Luzi')]
                    ),

        '1.1': Table(t_name='Offering',
                    step = '1.1',
                    col_names=['oid', 'dept'],
                    tuples=[
                            ('1', 'csc'),
                            ('2', 'csc'),
                            ('3', 'mat'),
                            ('4', 'ger')]
                    ),

        '1': Table(t_name='LimitedCols',
                    step = '1',
                    col_names=['oid', 'dept'],
                    tuples=[
                            ('1', 'csc'),
                            ('2', 'csc'),
                            ('3', 'mat'),
                            ('4', 'ger')]
                    ),

        '2': Table(t_name='LimitedCols',
                    step = '2',
                    col_names=['oid'],
                    tuples=[
                            ('1'),
                            ('2'),
                            ('3'),
                            ('4')]
                    ),
    }


    DESIRED_ASTS['simple_subquery'] =\
        [
            [ 'SELECT', [['LimitedCols.oid']] ],
            [ 'FROM', [[
                [
                    [ 'SELECT', [['oid'], ['dept']] ],
                    [ 'FROM', [['Offering']] ]
                ]

                , 'LimitedCols']] ]]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with an AND in its WHERE clause '''
def generate_simple_and_query():
    query_text =\
    ' SELECT email, cgpa' +\
    ' FROM Student' +\
    ' WHERE cgpa > 3' +\
    ' AND firstName=\'Martin\''

    steps = [
        QueryStep('1', 'FROM Student', [], 'Student',
            executable_sql="SELECT * FROM Student",
            namespace=["Student: sid, firstName, email, cgpa"]),

        QueryStep('2', 'WHERE cgpa > 3 AND firstName=\'Martin\'', ['Student'], '2',
            executable_sql="SELECT * FROM Student WHERE cgpa > 3 AND firstName=\'Martin\'"),

        QueryStep('3', 'SELECT email, cgpa', ['2'], '3',
            executable_sql="SELECT email, cgpa FROM Student WHERE cgpa > 3 AND firstName=\'Martin\'")
    ]

    tables = {
        '1': Table(t_name='Student',
                    step='1',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),

        '2': Table(t_name='Student',
                    step='2',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4')],
                    reasons= {
                                0: Reason(["cgpa > 3", "firstName='Martin'"]),
                                1: Reason(["cgpa > 3", "firstName='Martin'"])
                            }
                    ),
        '3': Table(t_name='Student',
                    step='3',
                    col_names=['email', 'cgpa'],
                    tuples=[
                            ('martin@mail.com', '3.4')]
                    ),
    }


    DESIRED_ASTS['simple_and_query'] =\
        [
            [ 'SELECT', [['email'], ['cgpa']] ],
            [ 'FROM', [['Student']] ],
            [ 'WHERE', [[['cgpa', '>', '3'], 'AND', ['firstName', '=', '\'Martin\''] ] ]],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with an OR in its WHERE clause '''
def generate_simple_or_query():
    query_text =\
    ' SELECT email, cgpa' +\
    ' FROM Student' +\
    ' WHERE cgpa > 3' +\
    ' OR firstName=\'Sophia\''

    steps = [
        QueryStep('1', 'FROM Student', [], 'Student',
            executable_sql="SELECT * FROM Student",
            namespace=["Student: sid, firstName, email, cgpa"]),

        QueryStep('2', 'WHERE cgpa > 2 OR firstName=\'Sophia\'', ['Student'], '2',
            executable_sql="SELECT * FROM Student WHERE cgpa > 2 OR firstName=\'Sophia\'"),

        QueryStep('3', 'SELECT email, cgpa', ['2'], '3',
            executable_sql="SELECT email, cgpa FROM Student WHERE cgpa > 2 OR firstName=\'Sophia\'"),
    ]

    tables = {
        '1': Table(t_name='Student',
                    step='1',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),

        '2': Table(t_name='Student',
                    step='2',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'not_martin@mail.com', '1.7')],
                    reasons = {
                                0: Reason(["cgpa > 2", "firstname=\'Sophia\'"]),
                                1: Reason(["cgpa > 2"]),
                                2: Reason(["cgpa > 2"]),
                                3: Reason(["firstName=\'Sophia\'"])
                            }
                    ),

        '3': Table(t_name='Student',
                    step='3',
                    col_names=['email', 'cgpa'],
                    tuples=[
                            ('martin@mail.com', '3.4'),
                            ('kathy@mail.com', '4.0'),
                            ('not_martin@mail.com', '1.7')]
                    ),
    }


    DESIRED_ASTS['simple_or_query'] =\
        [
            [ 'SELECT', [['email'], ['cgpa']] ],
            [ 'FROM', [['Student']] ],
            [ 'WHERE', [[ ['cgpa', '>', '3'], 'OR', ['firstName', '=', '\'Sophia\''] ] ]]
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with both AND and OR in its WHERE statement '''
def generate_complex_and_plus_or():
    query_text =\
    ' SELECT email, cgpa' +\
    ' FROM Student' +\
    ' WHERE (cgpa > 3)' +\
    ' AND (firstName=\'Martin\'' +\
    '    OR firstName=\'Kathy\')'

    steps = [
        QueryStep('1', 'FROM Student', [], 'Student',
            executable_sql="SELECT * FROM Student",
            namespace=["Student: sid, firstName, email, cgpa"]),

        QueryStep('2', 'WHERE (cgpa > 3) AND (firstName=\'Martin\' OR firstName=\'Kathy\')', ['Student'], '2',
            executable_sql="SELECT * FROM Student WHERE (cgpa > 3) AND (firstName=\'Martin\' OR firstName=\'Kathy\')"),

        QueryStep('3', 'SELECT email, cgpa', ['2'], '3',
            executable_sql="SELECT email, cgpa FROM Student WHERE (cgpa > 3) AND (firstName=\'Martin\' OR firstName=\'Kathy\')"),
    ]

    tables = {
        '1': Table(t_name='Student',
                    step='1',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')],
                    reasons = {
                                0: Reason(["cgpa > 3", "firstName=\'Martin\' OR firstName=\'Kathy\'"]),
                                1: Reason(["cgpa > 3", "firstName='Martin'"]),
                                2: Reason(["cgpa > 3", "firstName='Kathy'"]),
                            }
                    ),
        '2': Table(t_name='Student',
                    step='2',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0')]
                    ),
        '3': Table(t_name='Student',
                    step='3',
                    col_names=['email', 'cgpa'],
                    tuples=[
                            ('martin@mail.com', '3.4'),
                            ('kathy@mail.com', '4.0')]
                    ),
    }


    DESIRED_ASTS['complex_and_plus_or'] =\
        [
            [ 'SELECT', [['email'], ['cgpa']] ],
            [ 'FROM', [['Student']] ],
            [ 'WHERE', [[['cgpa', '>', '3'], 'AND', [ ['firstName', '=', '\'Martin\''], 'OR', ['firstName', '=', '\'Kathy\''] ] ] ]],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with renaming of tables '''
def generate_complex_renaming():
    query_text =\
    ' SELECT t.sid, o.oid' +\
    ' FROM Took t, Offering o'

    steps = [
        QueryStep('1', 'FROM Took t, Offering o', [], '1',
            executable_sql="SELECT * FROM Took t, Offering o",
            namespace=["t: sid, ofid, grade",
                        "o: oid, dept, cNum, instructor"]),

            QueryStep('1.1', 'Took t', ['Took'], '1.1',
                executable_sql="SELECT * FROM Took t",
                namespace=["t: sid, ofid, grade"]),

            QueryStep('1.2', 'Offering o', ['Offering'], '1.2', # t_name = 'o'
                executable_sql="SELECT * FROM Offering",
                namespace=["t: sid, ofid, grade",
                            "o: oid, dept, cNum, instructor"]),

            QueryStep('1.3', 'Took t, Offering o', ['1.1', '1.2'], '1',
                executable_sql="SELECT * FROM Took t, Offering o",
                namespace=["t: sid, ofid, grade",
                            "o: oid, dept, cNum, instructor"]),

        QueryStep('2', 'SELECT t.sid, o.oid', ['1'], '2',
            executable_sql="SELECT t.sid, o.oid FROM Took t, Offering o",
            namespace=["t: sid, ofid, grade",
                        "o: oid, dept, cNum, instructor"]),
    ]

    tables = {
        '1.1': Table(t_name='t',
                    step='1.1',
                    col_names=['t.sid', 't.ofid', 't.grade'],
                    tuples=[
                            ('1', '2', '87'),
                            ('1', '4', '73'),
                            ('2', '2', '92'),
                            ('3', '1', '80'),
                            ('4', '1', '60')]
                    ),
        '1.2': Table(t_name='o',
                    step='1.2',
                    col_names=['o.oid', 'o.dept', 'o.cNum', 'o.instructor'],
                    tuples=[
                            ('1', 'csc', '209', 'K. Reid'),
                            ('2', 'csc', '343', 'D. Horton'),
                            ('3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', 'ger', '100', 'E. Luzi')]
                    ),
        '1': Table(t_name='1',
                    step='1',
                    col_names=['t.sid', 't.ofid', 't.grade', 'o.oid', 'o.dept', 'o.cNum', 'o.instructor'],
                    tuples=[
                            ('1', '2', '87', '1', 'csc', '209', 'K. Reid'),
                            ('1', '4', '73', '1', 'csc', '209', 'K. Reid'),
                            ('2', '2', '92', '1', 'csc', '209', 'K. Reid'),
                            ('3', '1', '80', '1', 'csc', '209', 'K. Reid'),
                            ('4', '1', '60', '1', 'csc', '209', 'K. Reid'),

                            ('1', '2', '87', '2', 'csc', '343', 'D. Horton'),
                            ('1', '4', '73', '2', 'csc', '343', 'D. Horton'),
                            ('2', '2', '92', '2', 'csc', '343', 'D. Horton'),
                            ('3', '1', '80', '2', 'csc', '343', 'D. Horton'),
                            ('4', '1', '60', '2', 'csc', '343', 'D. Horton'),

                            ('1', '2', '87', '3', 'mat', '137', 'J. Kamnitzer'),
                            ('1', '4', '73', '3', 'mat', '137', 'J. Kamnitzer'),
                            ('2', '2', '92', '3', 'mat', '137', 'J. Kamnitzer'),
                            ('3', '1', '80', '3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', '1', '60', '3', 'mat', '137', 'J. Kamnitzer'),

                            ('1', '2', '87', '4', 'ger', '100', 'E. Luzi'),
                            ('1', '4', '73', '4', 'ger', '100', 'E. Luzi'),
                            ('2', '2', '92', '4', 'ger', '100', 'E. Luzi'),
                            ('3', '1', '80', '4', 'ger', '100', 'E. Luzi'),
                            ('4', '1', '60', '4', 'ger', '100', 'E. Luzi')]
                    ),
        '2': Table(t_name='2',
                    step='2',
                    col_names=['Took.sid', 'Offering.oid'],
                    tuples=[
                            ('1', '1'),
                            ('1', '1'),
                            ('2', '1'),
                            ('3', '1'),
                            ('4', '1'),

                            ('1', '2'),
                            ('1', '2'),
                            ('2', '2'),
                            ('3', '2'),
                            ('4', '2'),

                            ('1', '3'),
                            ('1', '3'),
                            ('2', '3'),
                            ('3', '3'),
                            ('4', '3'),

                            ('1', '4'),
                            ('1', '4'),
                            ('2', '4'),
                            ('3', '4'),
                            ('4', '4')]
                    ),
    }


    DESIRED_ASTS['complex_renaming'] =\
        [
            [ 'SELECT', [['t.sid'], ['o.oid']] ],
            [ 'FROM', [['Took', 'AS', 't'], 'JOIN', ['Offering', 'AS', 'o']] ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with a subquery in the WHERE that's not repeated for each row '''
def generate_complex_subquery_in_where_not_repeated():
    query_text =\
    ' SELECT sid, firstName' +\
    ' FROM Student' +\
    ' WHERE cgpa >' +\
    '    (SELECT cgpa' +\
    '     FROM Student' +\
    '     WHERE sid=4)'

    steps = [
        QueryStep('1', 'FROM Student', [], 'Student',
            executable_sql="SELECT * FROM Student",
            namespace=["Student: sid, firstName, email, cgpa"]),

        QueryStep('2', 'WHERE cgpa > (SELECT cgpa FROM Student WHERE sid=4)', ['Student'], '2',
            executable_sql="SELECT * FROM Student WHERE cgpa > (SELECT cgpa FROM Student WHERE sid=4)",
            namespace=["Student: sid, firstName, email, cgpa"]),

        QueryStep('3', 'SELECT sid, firstName', ['2'], '3',
            executable_sql="SELECT sid, firstName FROM Student WHERE cgpa > (SELECT cgpa FROM Student WHERE sid=4",
            namespace=["Student: sid, firstName"])
        ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),
        '2': Table(t_name='2',
                    step='2',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                    ],
                    reasons={
                        0: Reason(["cgpa > (SELECT cgpa FROM Student WHERE sid=4"],
                            {"cgpa > (SELECT cgpa FROM Student WHERE sid=4": 
                                ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Student', [], 'Student',
                                        executable_sql="SELECT * FROM Student",
                                        namespace=["Student: sid, firstName, email, cgpa"]),
                                    QueryStep('2', 'WHERE sid=4', ['Student'], '2',
                                        executable_sql="SELECT * FROM Student WHERE sid=4",
                                        namespace=["Student: sid, firstName, email, cgpa"]),
                                    QueryStep('3', 'SELECT cgpa', ['2'], '3',
                                        executable_sql="SELECT cgpa FROM Student WHERE sid=4",
                                        namespace=["Student: cgpa"])
                                ],
                                {
                                    '1': Table(t_name='Student',
                                                step='1',
                                                col_names=["sid, firstName, email, cgpa"],
                                                tuples=[
                                                    ('1', 'Martin', 'martin@mail.com', '3.4'),
                                                    ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                                                    ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                                                    ('4', 'James', 'james@mail.com', '2.8')]
                                                ),
                                    '2': Table(t_name='2',
                                                step='2',
                                                col_names=["sid, firstName, email, cgpa"],
                                                tuples=[
                                                    ('2', 'Kathy', 'kathy@mail.com', '4.0')],
                                                reasons={
                                                    0: Reason(["sid=4"]),
                                                    1: Reason(["sid=4"])
                                                    }
                                                ),
                                    '3': Table(t_name='3',
                                                step='3',
                                                col_names=["cgpa"],
                                                tuples=[
                                                    ('4.0')]
                                                )
                                }, "SELECT cgpa FROM Student WHERE sid=4")
                            }),
                        1: Reason(["cgpa > (SELECT cgpa FROM Student WHERE sid=4"],
                            {"cgpa > (SELECT cgpa FROM Student WHERE sid=4": 
                                ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Student', [], 'Student',
                                        executable_sql="SELECT * FROM Student",
                                        namespace=["Student: sid, firstName, email, cgpa"]),
                                    QueryStep('2', 'WHERE sid=4', ['Student'], '2',
                                        executable_sql="SELECT * FROM Student WHERE sid=4",
                                        namespace=["Student: sid, firstName, email, cgpa"]),
                                    QueryStep('3', 'SELECT cgpa', ['2'], '3',
                                        executable_sql="SELECT cgpa FROM Student WHERE sid=4",
                                        namespace=["Student: cgpa"])
                                ],
                                {
                                    '1': Table(t_name='Student',
                                                step='1',
                                                col_names=["sid, firstName, email, cgpa"],
                                                tuples=[
                                                    ('1', 'Martin', 'martin@mail.com', '3.4'),
                                                    ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                                                    ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                                                    ('4', 'James', 'james@mail.com', '2.8')]
                                                ),
                                    '2': Table(t_name='2',
                                                step='2',
                                                col_names=["sid, firstName, email, cgpa"],
                                                tuples=[
                                                    ('2', 'Kathy', 'kathy@mail.com', '4.0')],
                                                reasons={
                                                    0: Reason(["sid=4"]),
                                                    1: Reason(["sid=4"])
                                                    }
                                                ),
                                    '3': Table(t_name='3',
                                                step='3',
                                                col_names=["cgpa"],
                                                tuples=[
                                                    ('4.0')]
                                                )
                                }, "SELECT cgpa FROM Student WHERE sid=4")
                            }),
                        2: Reason(["cgpa > (SELECT cgpa FROM Student WHERE sid=4"],
                            {"cgpa > (SELECT cgpa FROM Student WHERE sid=4": 
                                ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Student', [], 'Student',
                                        executable_sql="SELECT * FROM Student",
                                        namespace=["Student: sid, firstName, email, cgpa"]),
                                    QueryStep('2', 'WHERE sid=4', ['Student'], '2',
                                        executable_sql="SELECT * FROM Student WHERE sid=4",
                                        namespace=["Student: sid, firstName, email, cgpa"]),
                                    QueryStep('3', 'SELECT cgpa', ['2'], '3',
                                        executable_sql="SELECT cgpa FROM Student WHERE sid=4",
                                        namespace=["Student: cgpa"])
                                ],
                                {
                                    '1': Table(t_name='Student',
                                                step='1',
                                                col_names=["sid, firstName, email, cgpa"],
                                                tuples=[
                                                    ('1', 'Martin', 'martin@mail.com', '3.4'),
                                                    ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                                                    ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                                                    ('4', 'James', 'james@mail.com', '2.8')]
                                                ),
                                    '2': Table(t_name='2',
                                                step='2',
                                                col_names=["sid, firstName, email, cgpa"],
                                                tuples=[
                                                    ('2', 'Kathy', 'kathy@mail.com', '4.0')],
                                                reasons={
                                                    0: Reason(["sid=4"]),
                                                    1: Reason(["sid=4"])
                                                    }
                                                ),
                                    '3': Table(t_name='3',
                                                step='3',
                                                col_names=["cgpa"],
                                                tuples=[
                                                    ('4.0')]
                                                )
                                }, "SELECT cgpa FROM Student WHERE sid=4")
                            })
                    }),

                    
        '3': Table(t_name='3',
                    step='3',
                    col_names=['Student.sid', 'Student.firstName'],
                    tuples=[
                            ('1', 'Martin'),
                            ('2', 'Kathy')]
                    ),
    }


    DESIRED_ASTS['complex_subquery_in_where_not_repeated'] =\
        [
            [ 'SELECT', [['sid'], ['firstName']] ],
            [ 'FROM', [['Student'] ]],
            [ 'WHERE', [[ 'cgpa', '>',
                            [
                                [ 'SELECT', [['cgpa']] ],
                                [ 'FROM', [['Student']] ],
                                [ 'WHERE', [['sid', '=', '4']] ],
                            ]
                        ]] ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

# ============= FIXED ================
''' A query with a subquery in the WHERE that's repeated for each row '''
def generate_complex_subquery_in_where_repeated():
    query_text =\
    ' SELECT instructor' +\
    ' FROM Offering o1' +\
    ' WHERE EXISTS (' +\
    '     SELECT o2.oid' +\
    '     FROM Offering o2' +\
    '     WHERE o2.oid <> o1.oid)'

    steps = [
        QueryStep('1', 'FROM Offering o1', [], 'o1', # t_name = 'o1'
            executable_sql="SELECT * FROM Offering o1",
            namespace=["o1: oid, dept, cNum, instructor"]),

        QueryStep('2', 'WHERE EXISTS (SELECT o2.oid FROM Offering o2 WHERE o2.oid <> o1.oid)',
            ['o1'], '2',
            executable_sql="SELECT * FROM Offering o1 WHERE EXISTS (SELECT o2.oid FROM Offering o2 WHERE o2.oid <> o1.oid)",
            namespace=["o1: oid, dept, cNum, instructor"]),

        QueryStep('3', 'SELECT instructor', ['2'], '3',
            executable_sql="SELECT instructor FROM Offering o1 WHERE EXISTS (SELECT o2.oid FROM Offering o2 WHERE o2.oid <> o1.oid)",
            namespace=["o1: instructor"])
        ]

    tables = {

        '1': Table(t_name='1',
                    step='1',
                    col_names=["oid, dept, cNum, instructor"],
                    tuples=[
                        ('1', 'csc', '209', 'K. Reid'),
                        ('2', 'csc', '343', 'D. Horton'),
                        ('3', 'mat', '137', 'J. Kamnitzer'),
                        ('4', 'ger', '100', 'E. Luzi')
                    ]),

        '2': Table(t_name='2',
                    step='2',
                    col_names=["oid, dept, cNum, instructor"],
                    tuples=[
                        ('1', 'csc', '209', 'K. Reid'),
                        ('2', 'csc', '343', 'D. Horton'),
                        ('3', 'mat', '137', 'J. Kamnitzer'),
                        ('4', 'ger', '100', 'E. Luzi')],
                    reasons = {
                        1: Reason(["EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)"],
                        {
                        'EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)':
                            ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Offering o2', [], '1',
                                        namespace=["o1: oid, dept, cNum, instructor",
                                                    "o2: oid, dept, cNum, instructor"]),
                                    QueryStep('2', 'WHERE o2.oid <> o1.oid', ['1'], '2',),
                                    QueryStep('3', 'SELECT o2.oid', ['2'], '3'),
                                ],
                                {
                                    '1': Table(t_name='o2',
                                    step='1',
                                    col_names=['o2.oid', 'o2.dept', 'o2.cNum', 'o2.instructor'],
                                    tuples=[
                                            ('1', 'csc', '209', 'K. Reid'),
                                            ('2', 'csc', '343', 'D. Horton'),
                                            ('3', 'mat', '137', 'J. Kamnitzer'),
                                            ('4', 'ger', '100', 'E. Luzi')]
                                    ),
                                    '2': Table(t_name='o2',
                                    step='2',
                                    col_names=['o2.oid', 'o2.dept', 'o2.cNum', 'o2.instructor'],
                                    tuples=[
                                            ('2', 'csc', '343', 'D. Horton'),
                                            ('3', 'mat', '137', 'J. Kamnitzer'),
                                            ('4', 'ger', '100', 'E. Luzi')],
                                    reasons={
                                        0: Reason(["o2.oid <> o1.oid"]),
                                        1: Reason(["o2.oid <> o1.oid"]),
                                        2: Reason(["o2.oid <> o1.oid"]),
                                        3: Reason(["o2.oid <> o1.oid"])
                                        }
                                    ),
                                    '3': Table(t_name='o2',
                                    step='3',
                                    col_names=['o2.oid'],
                                    tuples=[
                                            ('2'),
                                            ('3'),
                                            ('4')]
                                    ),
                                },
                                "SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid")
                        }),

                2: Reason(["EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)"],
                        {
                        'EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)':
                            ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Offering o2', [], '1',
                                        namespace=["o1: oid, dept, cNum, instructor",
                                                    "o2: oid, dpet, cNum, instructor"]),
                                    QueryStep('2', 'WHERE o2.oid <> o1.oid', ['1'], '2'),
                                    QueryStep('3', 'SELECT o2.oid', ['2'], '3'),
                                ],
                                {
                                    '1': Table(t_name='1',
                                    step='1',
                                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                                    tuples=[
                                            ('1', 'csc', '209', 'K. Reid'),
                                            ('2', 'csc', '343', 'D. Horton'),
                                            ('3', 'mat', '137', 'J. Kamnitzer'),
                                            ('4', 'ger', '100', 'E. Luzi')]
                                    ),
                                    '2': Table(t_name='2',
                                    step='2',
                                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                                    tuples=[
                                            ('1', 'csc', '209', 'K. Reid'),
                                            ('3', 'mat', '137', 'J. Kamnitzer'),
                                            ('4', 'ger', '100', 'E. Luzi')],
                                    reasons={
                                        0: Reason(["o2.oid <> o1.oid"]),
                                        1: Reason(["o2.oid <> o1.oid"]),
                                        2: Reason(["o2.oid <> o1.oid"]),
                                        3: Reason(["o2.oid <> o1.oid"])
                                        }
                                    ),
                                    '3': Table(t_name='3',
                                    step='3',
                                    col_names=['Offering.oid'],
                                    tuples=[
                                            ('1'),
                                            ('3'),
                                            ('4')]
                                    ),
                                },
                                "SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid")
                        }),

                3: Reason(["EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)"],
                        {
                        'EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)':
                            ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Offering o2', [], '1',
                                        namespace=["o1: oid, dept, cNum, instructor",
                                                    "o2: oid, dpet, cNum, instructor"]),
                                    QueryStep('2', 'WHERE o2.oid <> o1.oid', ['1'], '2'),
                                    QueryStep('3', 'SELECT o2.oid', ['2'], '3'),
                                ],
                                {
                                    '1': Table(t_name='1',
                                    step='1',
                                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                                    tuples=[
                                            ('1', 'csc', '209', 'K. Reid'),
                                            ('2', 'csc', '343', 'D. Horton'),
                                            ('3', 'mat', '137', 'J. Kamnitzer'),
                                            ('4', 'ger', '100', 'E. Luzi')]
                                    ),
                                    '2': Table(t_name='2',
                                    step='2',
                                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                                    tuples=[
                                            ('1', 'csc', '209', 'K. Reid'),
                                            ('2', 'csc', '343', 'D. Horton'),
                                            ('4', 'ger', '100', 'E. Luzi')],
                                    reasons={
                                        0: Reason(["o2.oid <> o1.oid"]),
                                        1: Reason(["o2.oid <> o1.oid"]),
                                        2: Reason(["o2.oid <> o1.oid"]),
                                        3: Reason(["o2.oid <> o1.oid"])
                                        }
                                    ),
                                    '3': Table(t_name='3',
                                    step='3',
                                    col_names=['Offering.oid'],
                                    tuples=[
                                            ('1'),
                                            ('2'),
                                            ('4')]
                                    ),
                                },
                                "SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid")
                        }),

                4: Reason(["EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)"],
                        {
                        'EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)':
                            ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Offering o2', [], '1',
                                        namespace=["o1: oid, dept, cNum, instructor",
                                                    "o2: oid, dpet, cNum, instructor"]),
                                    QueryStep('2', 'WHERE o2.oid <> o1.oid', ['1'], '2'),
                                    QueryStep('3', 'SELECT o2.oid', ['2'], '3'),
                                ],
                                {
                                    '1': Table(t_name='1',
                                    step='1',
                                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                                    tuples=[
                                            ('1', 'csc', '209', 'K. Reid'),
                                            ('2', 'csc', '343', 'D. Horton'),
                                            ('3', 'mat', '137', 'J. Kamnitzer'),
                                            ('4', 'ger', '100', 'E. Luzi')]
                                    ),
                                    '2': Table(t_name='2',
                                    step='2',
                                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                                    tuples=[
                                            ('1', 'csc', '209', 'K. Reid'),
                                            ('2', 'csc', '343', 'D. Horton'),
                                            ('3', 'mat', '137', 'J. Kamnitzer')],
                                    reasons={
                                        0: Reason(["o2.oid <> o1.oid"]),
                                        1: Reason(["o2.oid <> o1.oid"]),
                                        2: Reason(["o2.oid <> o1.oid"]),
                                        3: Reason(["o2.oid <> o1.oid"])
                                        }
                                    ),
                                    '3': Table(t_name='3',
                                    step='3',
                                    col_names=['Offering.oid'],
                                    tuples=[
                                            ('1'),
                                            ('2'),
                                            ('3')]
                                    ),
                                },
                                "SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid")
                        }) }
                    ),

        '3': Table(t_name='3',
                    step='3',
                    col_names=["instructor"],
                    tuples=[
                        ('K. Reid'),
                        ('D. Horton'),
                        ('J. Kamnitzer'),
                        ('E. Luzi')
                    ])
        }

    DESIRED_ASTS['complex_subquery_in_where_repeated'] =\
        [
            [ 'SELECT', [['instructor']] ],
            [ 'FROM', [['Offering', 'o1']] ],
            [ 'WHERE', [[ 'EXISTS',
                            [
                                [ 'SELECT', [['o2.oid']] ],
                                [ 'FROM', [['Offering', 'o2']] ],
                                [ 'WHERE', [['o2.oid', '<>', 'o1.oid']] ],
                            ]
                        ]]
            ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}



# ============= FIXED ================
''' Multiple queries which don't reference each other '''
def generate_multiple_queries_unrelated():
    query_text1 =\
    ' SELECT email' +\
    ' FROM Student'

    steps1 = [
        QueryStep('1', 'FROM Student', [], '1',
            namespace=["Student: sid, firstName, email, cgpa"],
            executable_sql="SELECT * FROM Student"),
        QueryStep('2', 'SELECT email', ['1'], '2',
            namespace=["Student: email"],
            executable_sql="SELECT email FROM Student"),
    ]

    tables1 = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),
        '2': Table(t_name='2',
                    step='2',
                    col_names=['Student.email'],
                    tuples=[
                            ('martin@mail.com'),
                            ('kathy@mail.com'),
                            ('not_martin@mail.com'),
                            ('james@mail.com')]
                    ),
    }


    DESIRED_ASTS['multiple_queries_unrelated_1'] =\
        [
            [ 'SELECT', ['email'] ],
            [ 'FROM', [['Student']] ],
        ]


    query_text2 =\
    ' SELECT oid' +\
    ' FROM Offering'

    steps2 = [
        QueryStep('1', 'FROM Offering', [], '1',
            namespace=["Offering: oid, dept, cNum, instructor"],
            executable_sql="SELECT * FROM Offering"),
        QueryStep('2', 'SELECT oid', ['1'], '2',
            namespace=["Offering: oid"],
            executable_sql="SELECT oid FROM Offering")
    ]

    tables2 = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                    tuples=[
                            ('1', 'csc', '209', 'K. Reid'),
                            ('2', 'csc', '343', 'D. Horton'),
                            ('3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', 'ger', '100', 'E. Luzi')]
                    ),
        '2': Table(t_name='2',
                    step='2',
                    col_names=['Offering.oid'],
                    tuples=[
                            ('1'),
                            ('2'),
                            ('3'),
                            ('4')]
                    ),
    }


    DESIRED_ASTS['multiple_queries_unrelated_2'] =\
        [[
            [ 'SELECT', ['oid'] ],
            [ 'FROM', [['Offering']] ],
        ]]

    parsed_query1 = ParsedQuery(steps1, tables1, query_text1)
    parsed_query2 = ParsedQuery(steps2, tables2, query_text2)
    return {"global_tables": global_tables, "all_queries": [parsed_query1, parsed_query2]}


# ============= FIXED ================
''' Multiple queries which do reference each other '''
def generate_multiple_queries_related():
    query_text1 =\
    ' CREATE VIEW pizza AS' +\
    '   SELECT sid, email, cgpa' +\
    '   FROM Student' +\
    '   WHERE cgpa<3'

    steps1 = [
        QueryStep('1', 'CREATE VIEW pizza AS SELECT sid, email, cgpa FROM Student WHERE cgpa<3', [], 'pizza',
            namespace=["pizza: sid, email, cgpa"],
            executable_sql="CREATE VIEW pizza AS SELECT sid, email, cgpa FROM Student WHERE cgpa<3"),

            QueryStep('1.1', 'FROM Student', [], '1.1',
                namespace=["Student: sid, firstName, email, cgpa"],
                executable_sql="SELECT * FROM Student"),

            QueryStep('1.2', 'WHERE cgpa<3', ['1.1'], '1.2',
                      executable_sql="SELECT * FROM Student WHERE cgpa <3"),

            QueryStep('1.3', 'SELECT sid, email, cgpa', ['1.2'], '1.3',
                namespace=["Student: sid, email, cgpa"],
                executable_sql="SELECT sid, email, cgpa FROM Student"),

            QueryStep('1.4', 'CREATE VIEW pizza', ['1.3'], 'pizza',
                namespace=["pizza: sid, email, cgpa"],
                executable_sql="SELECT * FROM pizza"),
    ]

    tables1 = {
        '1.1': Table(t_name='1.1',
                    step='1.1',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sopia', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),
        '1.2': Table(t_name='1.2',
                    step='1.2',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('3', 'Martin', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')],
                    reasons={
                        0: Reason(["cgpa<3"]),
                        1: Reason(["cgpa<3"]),
                        2: Reason(["cgpa<3"])
                        }
                    ),
        '1.3': Table(t_name='1.3',
                    step='1.3',
                    col_names=['Student.sid', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('3', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    )
    }


    DESIRED_ASTS['multiple_queries_related_1'] =\
        [
            ['CREATE VIEW', 'pizza',
                [
                    [ 'SELECT', ['sid','email','cgpa'] ],
                    [ 'FROM', [['Student']] ],
                    [ 'WHERE', [['cgpa', '<', '3']] ],
                ]
            ]
        ]


    query_text2 =\
    ' SELECT email' +\
    ' FROM pizza'

    steps2 = [
        QueryStep('1', 'FROM pizza', ['pizza'], '1',
            namespace=["pizza: sid, email, cgpa"]),
        QueryStep('2', 'SELECT email', ['1'], '2'),
    ]

    tables2 = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['sid', 'email', 'cgpa'],
                    tuples=[
                            ('3', 'not_martin@mail.com', '1.7'),
                            ('4', 'james@mail.com', '2.8')]
                    ),

        '2': Table(t_name='2',
                    step='2',
                    col_names=['sid', 'email', 'cgpa'],
                    tuples=[
                            ('3', 'not_martin@mail.com', '1.7'),
                            ('4', 'james@mail.com', '2.8')]
                    ),

    }


    DESIRED_ASTS['multiple_queries_related_2'] =\
        [
            [ 'SELECT', ['email'] ],
            [ 'FROM', ['pizza'] ],
        ]

    parsed_query1 = ParsedQuery(steps1, tables1, query_text1)
    parsed_query2 = ParsedQuery(steps2, tables2, query_text2)

    global_views = {};
    global_views["pizza"] =\
        Table(t_name='pizza',
                step='0',
                col_names=['sid', 'email', 'cgpa'],
                tuples=[
                        ('3', 'not_martin@mail.com', '1.7'),
                        ('4', 'james@mail.com', '2.8')]
                )

    return {"global_tables": global_tables, "global_views": global_views, "all_queries": [parsed_query1, parsed_query2]}


""" Diane's test cases """
''' A query with a subquery in the WHERE that's repeated for each row '''
def generate_diane_subquery_in_from():
    query_text =\
    ' SELECT sid, dept||cnum as course, grade' +\
    ' FROM Took,' +\
    '   (SELECT *' +\
    '   FROM Offering' +\
    '   WHERE instructor="Horton") H' +\
    ' WHERE Took.oid = H.oid;'

    steps = [
        QueryStep('1', 'FROM Took, (SELECT * FROM Offering WHERE instructor="Horton") H', ['Took'], '1', namespace=["Took: oid, dept, cNum, instructor", "H: oid, dept, cNum, instructor"]),

            QueryStep('1.1', 'Took', ['Took'], '1.1', namespace=["Took: oid, dept, cNum, instructor"]),
            QueryStep('1.2', '(SELECT * FROM Offering WHERE instructor="Horton") H', [], '1.2', namespace=["Took: oid, dept, cNum, instructor", "H: oid, dept, cNum, instructor"]),
                QueryStep('1.2.1', 'FROM Offering', ['Offering'], '1.2.1', namespace=["Took: oid, dept, cNum, instructor", "Offering: 'oid', 'dept', 'cNum', 'instructor'"]),
                QueryStep('1.2.2', 'WHERE instructor="Horton"', ['1.2.1'], '1.2.2',
                    reasons={
                        0: Reason(['instructor="Horton"'])
                    }),
                QueryStep('1.2.3', 'SELECT *', ['1.2.2'], '1.2'),
            QueryStep('1.3', 'Took, (SELECT * FROM Offering WHERE instructor="Horton") H', ['1.1','1.2'], '1'),


        QueryStep('2', 'WHERE Took.oid = H.oid', ['1'], '2',
            reasons={
                0: Reason(["Took.oid = H.oid"])
            }),

        QueryStep('3', 'SELECT sid, dept||cnum as course, grade', ['2'], '3'),
    ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=[],
                    tuples=[]
                    ),

        '1.1': Table(t_name='1.1',
                    step='1.1',
                    col_names=[],
                    tuples=[]
                    ),

        '1.2': Table(t_name='H',
                    step='1.2',
                    col_names=[],
                    tuples=[]
                    ),

        '1.2.1': Table(t_name='1.2.1',
                    step='1.2.1',
                    col_names=[],
                    tuples=[]
                    ),

        '1.2.2': Table(t_name='1.2.2',
                    step='1.2.2',
                    col_names=[],
                    tuples=[]
                    ),

        '2': Table(t_name='2',
                    step='2',
                    col_names=[],
                    tuples=[]
                    ),

        '3': Table(t_name='3',
                    step='3',
                    col_names=[],
                    tuples=[]
                    ),

    }


    DESIRED_ASTS['diane_subquery_in_from'] =\
        [
            [ 'SELECT', ['sid', [['dept', '||', 'cnum'], 'course'], 'grade'] ],
            [ 'FROM', ['Took', ',',
                [[

                    [ 'SELECT', ['*'] ],
                    [ 'FROM', ['Offering'] ],
                    [ 'WHERE', [['instructor','=','Horton']] ],

                ], 'H']
            ] ],
            [ 'WHERE', [['Took.oid','=','H.oid']] ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

def generate_diane_where_any():
    query_text =\
    ' SELECT sid' +\
    ' FROM Student' +\
    ' WHERE gpa > ANY' +\
    '   (SELECT gpa' +\
    '    FROM Student NATURAL JOIN Took' +\
    '    WHERE grade > 100);'

    steps = [
        QueryStep('1', 'FROM Student', [], '1', namespace=['Student: sid, firstName, email, cgpa']),
        QueryStep('2', 'WHERE gpa > ANY (SELECT gpa FROM Student NATURAL JOIN Took WHERE grade > 100)', ['1'], '2'),
            # ???
        QueryStep('3', 'SELECT sid', ['2'], '3'),
    ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=[],
                    tuples=[]
                    ),
    }


    DESIRED_ASTS['diane_where_any'] =\
        [
            [ 'SELECT', ['sid'] ],
            [ 'FROM', ['Student'] ],
            [ 'WHERE', [['gpa', '>', 'ANY',
                [
                    [ 'SELECT', ['gpa'] ],
                    [ 'FROM', ['Student', 'NATURAL JOIN', 'Took'] ],
                    [ 'WHERE', [['grade', '>', '100']] ],
                ]
            ]] ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

def generate_diane_where_in():
    query_text =\
    ' SELECT sid, dept||cnum AS course, grade' +\
    ' FROM Took NATURAL JOIN Offering' +\
    ' WHERE' +\
    '  grade >= 80 AND' +\
    '  (cnum, dept) IN (' +\
    '      SELECT cnum, dept' +\
    '      FROM Took NATURAL JOIN Offering' +\
    '                NATURAL JOIN Student' +\
    '      WHERE surname = "Lakemeyer");'

    steps = [
        QueryStep('1', '', [''], '', namespace=[]),
    ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=[],
                    tuples=[]
                    ),
    }


    DESIRED_ASTS['diane_where_in'] =\
        [
            [ 'SELECT', ['sid', [['dept', '||', 'cnum'], 'course'], 'grade'] ],
            [ 'FROM', ['Took', 'NATURAL JOIN', 'Offering'] ],
            [ 'WHERE', [['grade', '>=', '80'],
                            'AND', ['(cnum, dept)', 'IN',
                            [
                                [ 'SELECT', ['cnum', 'dept'] ],
                                [ 'FROM', ['Took', 'NATURAL JOIN', 'Offering', 'NATURAL JOIN', 'Student'] ],
                                [ 'WHERE', [['surname', '=', '"Lakemeyer"']] ],
                            ]]
                        ]
            ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}

def generate_diane_where_exists():
    query_text =\
    ' SELECT instructor' +\
    ' FROM Offering Off1' +\
    ' WHERE NOT EXISTS (' +\
    '  SELECT *' +\
    '  FROM Offering' +\
    '  WHERE' +\
    '      oid <> Off1.oid AND' +\
    '      instructor = Off1.instructor );'

    steps = [

        QueryStep('1', 'FROM Offering Offl', [], 'Offering',
            executable_sql="SELECT * FROM Offering Off1",
            namespace=["Offl: oid, dept, cNum, instructor"]),

        QueryStep('2', 
            "WHERE NOT EXISTS (SELECT * FROM Offering WHERE oid <> Offl.oid AND instructor = Offl.instructor)",
            ['Offering'], '2',
            executable_sql="SELECT * FROM Offering Offl WHERE NOT EXISTS (SELECT * FROM Offering \
                WHERE oid <> Offl.oid AND instructor = Offl.instructor",
            namespace=["Offl: oid, dept, cNum, instructor"]),

        QueryStep('3', 'SELECT instructor', ['2'], '3',
            executable_sql="SELECT instructor FROM Offering Offl WHERE NOT EXISTS (SELECT * FROM Offering \
                WHERE oid <> Offl.oid AND instructor = Offl.instructor",
            namespace=["Offl: instructor"])
        ]


    tables = {
        '1': Table(t_name='Offering',
                    step='1',
                    col_names=['oid', 'dept', 'cNum', 'instructor'],
                    tuples=[
                            ('1', 'csc', '209', 'K. Reid'),
                            ('2', 'csc', '343', 'D. Horton'),
                            ('3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', 'ger', '100', 'E. Luzi')]
                    ),
        '2': Table(t_name='2',
                   step='2',
                   col_names=['oid', 'dept', 'cNum', 'instructor'],
                    tuples=[
                            ('1', 'csc', '209', 'K. Reid'),
                            ('2', 'csc', '343', 'D. Horton'),
                            ('3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', 'ger', '100', 'E. Luzi')],
                    reasons= {
                        0: ["not exists (SELECT * FROM Offering where oid <> Offl.oid"]
                    }
                    ),
        '3': Table(t_name='Student',
                   step='3',
                   col_names=['instructor'],
                   tuples=[
                           ('K. Reid'),
                           ('D. Horton'),
                           ('J. Kamnitzer'),
                           ('E. Luzi'),
                    ]
                   )
        }

    DESIRED_ASTS['diane_where_exists'] =\
        [
            [ 'SELECT', [['instructor']] ],
            [ 'FROM',   [['Offering', 'Off1']] ],
            [ 'WHERE',  [['NOT', 'EXISTS',
                            [
                                [ 'SELECT', ['*'] ],
                                [ 'FROM',   [['Offering']] ],
                                [ 'WHERE',  [[['oid', '<>', 'Off1.oid'], 'AND', ['instructor', '=', 'Off1.instructor']] ]],
                        ]]]
            ]
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}



#=====================================================================================================================
TRACES = {
    'simple_query': generate_simple_query(),
    'simple_cross_product_query': generate_simple_cross_product_query(),
    'simple_natural_join_query': generate_simple_natural_join_query(),
    'simple_condition_join_query': generate_simple_condition_join_query(),

    'simple_subquery': generate_simple_subquery(),
    'simple_and_query': generate_simple_and_query(),
    'simple_or_query': generate_simple_or_query(),
    'complex_and_plus_or': generate_complex_and_plus_or(),

    'complex_renaming': generate_complex_renaming(),
    'complex_subquery_in_where_not_repeated': generate_complex_subquery_in_where_not_repeated(),
    'complex_subquery_in_where_repeated': generate_complex_subquery_in_where_repeated(),

    'multiple_queries_unrelated': generate_multiple_queries_unrelated(),
    'multiple_queries_related': generate_multiple_queries_related(),

    'diane_subquery_in_from': generate_diane_subquery_in_from(),
    'diane_where_any': generate_diane_where_any(),
    'diane_where_in': generate_diane_where_in(),
    'diane_where_exists': generate_diane_where_exists(),
}

JSON_TRACES = {
    trace_name:
        {
            "global_tables": {t_name: t.to_json() for t_name,t in tables_and_queries["global_tables"].items()},
            "all_queries": [pq.to_json() for pq in tables_and_queries["all_queries"]]
        } for trace_name,tables_and_queries in TRACES.items()
}


def main():
    print("TRACES =")
    pprint(TRACES)

    print()
    print("=====================================================================================================")
    print()

    print("DESIRED_ASTS =")
    pprint(DESIRED_ASTS)



if __name__ == '__main__':
    main()
