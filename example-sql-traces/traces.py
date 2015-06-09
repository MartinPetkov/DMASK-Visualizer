from parsed_query import *
from query_step import *
from table import *

import pprint

'''
The schema:
Student(_sid_, firstName, email, cgpa)
Course(_dept,cNum_, name)
Offering(_oid_, dept, cNum, instructor)
Took(_sid,ofid_, grade)
'''

# Starting Values:
Student_colnames = ['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa']
Student_tuples=[
('1', 'Martin', 'martin@mail.com', '3.4'),
('2', 'Kathy', 'kathy@mail.com', '4.0'),
('3', 'Sophia', 'sophia@mail.com', '1.7'),
('4', 'James', 'james@mail.com', '2.8')]
Student_table = Table(t_name='Student', step = '0', col_names=Student_colnames, tuples=Student_tuples)

Course_colnames = ['Course.dept', 'Course.cNum', 'Course.name']
Course_tuples=[
('csc', '148', 'Intro to Computer Science'),
('csc', '209', 'Systems Programming'),
('csc', '343', 'Intro to Databases'),
('mat', '137', 'Calculus'),
('ger', '100', 'Intro to German')]
Course_table = Table(t_name='Course', step = '0', col_names=Course_colnames, tuples=Course_tuples)

Offering_colnames = ['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor']
Offering_tuples=[
('1', 'csc', '209', 'K. Reid'),
('2', 'csc', '343', 'D. Horton'),
('3', 'mat', '137', 'J. Kamnitzer'),
('4', 'ger', '100', 'E. Luzi'),]
Offering_table = Table(t_name='Offering', step = '0', col_names=Offering_colnames, tuples=Offering_tuples)

Took_colnames = ['Took.sid', 'Took.ofid', 'Took.grade']
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




''' A simple SELECT-FROM-WHERE query '''
def generate_simple_query():
    query_text =\
    ' SELECT sid, cgpa' +\
    ' FROM Student' +\
    ' WHERE cgpa > 3'

    steps = [
        QueryStep('1', 'FROM Student', [], '1'),
        QueryStep('2', 'WHERE cgpa > 3', ['1'], '2',
                    reasons={
                        0: Reason(["cgpa > 3"]),
                    }),
        QueryStep('3', 'SELECT sid, cgpa', ['2'], '3'),
    ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Martin', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),

        '2': Table(t_name='2',
                    step='2',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0')]
                    ),

        '3': Table(t_name='3',
                    step='3',
                    col_names=['Student.sid', 'Student.cgpa'],
                    tuples=[
                            ('1', '3.4'),
                            ('2', '4.0')]
                    ),
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with a cross product in it '''
def generate_simple_cross_product_query():
    query_text =\
    ' SELECT Student.sid, Student.email, Took.grade' +\
    ' FROM Student, Took'

    steps = [
        QueryStep('1', 'FROM Student, Took', ['Student', 'Took'], '1'),
        QueryStep('2', 'SELECT Student.sid, Student.email, Took.grade', ['1'], '2')
    ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa', 'Took.sid', 'Took.ofid', 'Took.grade'],
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

        '2': Table(t_name='2',
                    step='2',
                    col_names=['Student.sid', 'Student.email', 'Took.grade'],
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


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with one natural JOIN in it '''
def generate_simple_natural_join_query():
    query_text =\
    ' SELECT sid, email, cgpa' +\
    ' FROM Student NATURAL JOIN Took NATURAL JOIN Course'

    steps = [
        QueryStep('1', 'FROM Student NATURAL JOIN Took NATURAL JOIN Course', ['Student', 'Took', 'Course'], '1'),
            QueryStep('1.1', 'Student NATURAL JOIN Took', ['Student', 'Took'], '1.1',
                reasons = {
                    0: Reason(["Student.sid=Took.sid"]),
                }),
            QueryStep('1.2', 'Student NATURAL JOIN Took NATURAL JOIN Course', ['1.1', 'Course'], '1',
                reasons= {
                    0: Reason([""]),
                }),
        QueryStep('2', 'SELECT sid, email, cgpa', ['1'], '2')
    ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['1.1.sid', 'Student.firstName', 'Student.email', 'Student.cgpa', 'Took.ofid', 'Took.grade', 'Course.dept', 'Course.cNum', 'Course.name'],
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
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60', 'ger', '100', 'Intro to German'),]

                    ),

        '1.1': Table(t_name='1.1',
                    step='1.1',
                    col_names=['1.1.sid', 'Student.firstName', 'Student.email', 'Student.cgpa', 'Took.ofid', 'Took.grade'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '87'),
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '73'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '92'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '80'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '60')]
                    ),

        '2': Table(t_name='2',
                    step='2',
                    col_names=['1.1.sid','Student.email', 'Student.cgpa'],
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

                    ),
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with a LEFT JOIN on a condition in it '''
def generate_simple_condition_join_query():
    query_text =\
    ' SELECT sid, grade, instructor' +\
    ' FROM Took LEFT JOIN Offering ON Took.ofid=Offering.oid'

    steps = [
        QueryStep('1', 'FROM Took LEFT JOIN Offering ON Took.ofid=Offering.oid', ['Took', 'Offering'], '1',
            reasons = {
                0: Reason(["Took.ofid=Offering.oid"]),
            }),
        QueryStep('2', 'SELECT sid, grade, instructor', ['1'], '2'),
    ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['Took.sid', 'Took.ofid', 'Took.grade', 'Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                    tuples=[
                            ('1', '2', '87', '1', 'csc', '209', 'K. Reid'),
                            ('1', '4', '73', '1', 'csc', '209', 'K. Reid'),
                            ('2', '2', '92', '2', 'csc', '343', 'D. Horton'),
                            ('3', '1', '80', '3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', '1', '60', '4', 'ger', '100', 'E. Luzi')]
                    ),

        '2': Table(t_name='2',
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


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with one subquery in the FROM '''
def generate_simple_subquery():
    query_text =\
    ' SELECT WhyUDoThis.oid' +\
    ' FROM' +\
    '    (SELECT oid, dept' +\
    '     FROM Offering' +\
    '    ) AS WhyUDoThis'

    steps = [
        QueryStep('1', 'FROM (SELECT oid, dept FROM Offering) AS WhyUDoThis', ['Offering'], '1'),
            QueryStep('1.1', 'FROM Offering', [], '1.1'),
            QueryStep('1.2', 'SELECT oid, dept', ['1.1'], '1.2'),
            QueryStep('1.3', 'AS WhyUDoThis', ['1.2'], '1'),
        QueryStep('2', 'SELECT WhyUDoThis.oid', ['1'], '2'),
    ]

    tables = {
        '1.1': Table(t_name='1.1',
                    step = '1.1',
                    col_names=['Offering.oid', 'Offering.dept', 'Offering.cNum', 'Offering.instructor'],
                    tuples=[
                            ('1', 'csc', '209', 'K. Reid'),
                            ('2', 'csc', '343', 'D. Horton'),
                            ('3', 'mat', '137', 'J. Kamnitzer'),
                            ('4', 'ger', '100', 'E. Luzi')]
                    ),

        '1.2': Table(t_name='1.2',
                    step = '1.2',
                    col_names=['Offering.oid', 'Offering.dept'],
                    tuples=[
                            ('1', 'csc'),
                            ('2', 'csc'),
                            ('3', 'mat'),
                            ('4', 'ger')]
                    ),

        '1': Table(t_name='WhyUDoThis',
                    step = '1',
                    col_names=['WhyUDoThis.oid', 'WhyUDoThis.dept'],
                    tuples=[
                            ('1', 'csc'),
                            ('2', 'csc'),
                            ('3', 'mat'),
                            ('4', 'ger')]
                    ),

        '2': Table(t_name='2',
                    step = '2',
                    col_names=['WhyUDoThis.oid'],
                    tuples=[
                            ('1'),
                            ('2'),
                            ('3'),
                            ('4')]
                    ),
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with an AND in its WHERE clause '''
def generate_simple_and_query():
    query_text =\
    ' SELECT email, cgpa' +\
    ' FROM Student' +\
    ' WHERE cgpa > 3' +\
    ' AND firstName=\'Martin\''

    steps = [
        QueryStep('1', 'FROM Student', [], '1'),
        QueryStep('2', 'WHERE cgpa > 3 AND firstName=\'Martin\'', ['1'], '2',
            reasons= {
                0: Reason(["cgpa > 3", "firstName='Martin'"]),
            }),
        QueryStep('3', 'SELECT email, cgpa', ['2'], '3')
    ]

    tables = {
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with an OR in its WHERE clause '''
def generate_simple_or_query():
    query_text =\
    ' SELECT email, cgpa' +\
    ' FROM Student' +\
    ' WHERE cgpa > 3' +\
    ' OR firstName=\'Martin\''

    steps = [
        QueryStep('1', 'FROM Student', [], '1'),
        QueryStep('2', 'WHERE cgpa > 2 OR firstName=\'Martin\'', ['1'], '2',
            reasons = {
                1: Reason(["cgpa > 2", "firstName='Martin'"]),
                2: Reason(["cgpa > 2"]),
                3: Reason(["cgpa > 2"]),
            }),
        QueryStep('3', 'SELECT email, cgpa', ['2'], '3'),
    ]

    tables = {
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with both AND and OR in its WHERE statement '''
def generate_complex_and_plus_or():
    query_text =\
    ' SELECT email, cgpa' +\
    ' FROM Student' +\
    ' WHERE (cgpa > 3)' +\
    ' AND (firstName=\'Martin\'' +\
    '    OR firstName=\'Kathy\')'

    steps = [
        QueryStep('1', 'FROM Student', [], '1'),
        QueryStep('2', 'WHERE (cgpa > 3) AND (firstName=\'Martin\' OR firstName=\'Kathy\')', ['1'], '2',
            reasons = {
                1: Reason(["cgpa > 3", "firstName='Martin'"]),
                2: Reason(["cgpa > 3", "firstName='Kathy'"]),
            }),
        QueryStep('3', 'SELECT email, cgpa', ['2'], '3'),
    ]

    tables = {
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}



''' A query with renaming of tables '''
def generate_complex_renaming():
    query_text =\
    ' SELECT t.sid, o.oid' +\
    ' FROM Took t, Offering o'

    steps = [
        QueryStep('1', 'FROM Took t, Offering o', [], '1'),
            QueryStep('1.1', 'Took t', ['Took'], 't'),
            QueryStep('1.2', 'Offering o', ['Offering'], 'o'),
            QueryStep('1.3', 'FROM Took t, Offering o', ['t', 'o'], '1'),
        QueryStep('2', 'SELECT t.sid, o.oid', ['1'], '2'),
    ]

    tables = {
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with a subquery in the WHERE that's not repeated for each row '''
def generate_complex_subquery_in_where_not_repeated():
    query_text =\
    ' SELECT sid, surName' +\
    ' FROM Student' +\
    ' WHERE cgpa >' +\
    '    (SELECT cgpa' +\
    '     FROM Student' +\
    '     WHERE sid=4)'

    steps = [
        QueryStep('1', 'FROM Student', [], '1'),
        QueryStep('2', 'WHERE cgpa > (SELECT cgpa FROM Student WHERE sid=4)', ['1'], '2'),
            QueryStep('2.1', '(SELECT cgpa FROM Student WHERE sid=4)', [''], '2.1'),
                QueryStep('2.1.1', 'FROM Student', [], '2.1.1'),
                QueryStep('2.1.2', 'WHERE sid=4', ['2.1.1'], '2.1.2',
                    reasons = {
                        0: Reason(["sid=4"]),
                    }),
                QueryStep('2.1.3', 'SELECT cgpa', ['2.1.2'], '2.1'),
            QueryStep('2.2', 'WHERE cgpa > (SELECT cgpa FROM Student WHERE sid=4)', ['1', '2.1'], '2',
                reasons = {
                    0: Reason(["cgpa > (SELECT cgpa FROM Student WHERE sid=4)"],
                        {
                            0: ParsedQuery(
                                [
                                    QueryStep('1', 'FROM Student', [], '1'),
                                    QueryStep('2', 'WHERE sid=4', ['1'], '2',
                                        reasons = {
                                            0: Reason(["sid=4"])
                                        }),
                                    QueryStep('3', 'FROM Student', ['2'], '3'),
                                ],
                                {},
                                "SELECT cgpa FROM Student WHERE sid=4")
                        }),
                }),
        QueryStep('3', 'SELECT sid, surName', ['2'], '3'),
    ]

    tables = {
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}


''' A query with a subquery in the WHERE that's repeated for each row '''
def generate_complex_subquery_in_where_repeated():
    query_text =\
    ' SELECT instructor' +\
    ' FROM Offering o1' +\
    ' WHERE NOT EXISTS (' +\
    '     SELECT oid' +\
    '     FROM Offering o2' +\
    '     WHERE o2.oid <> o1.oid)'

    steps = [
        QueryStep('1', 'FROM Offering o1', [], '1'),
            QueryStep('1.1', 'Offering o1', ['Offering'], 'o1'),
            QueryStep('1.2', 'FROM Offering o1', ['o1'], '1'),
        QueryStep('2', 'WHERE NOT EXISTS (SELECT oid FROM Offering o2 WHERE o2.oid <> o1.oid)', ['1'], '2',
            reasons = {
                # Not sure how many rows will be here yet
            }),
        QueryStep('3', 'SELECT instructor', ['2'], '3'),
    ]

    tables = {
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}



''' Multiple queries which don't reference each other '''
def generate_multiple_queries_unrelated():
    query_text1 =\
    ' SELECT email' +\
    ' FROM Student'

    steps1 = [
        QueryStep('1', 'FROM Student', [], '1'),
        QueryStep('2', 'SELECT email', ['1'], '2'),
    ]

    tables1 = {
    }


    query_text2 =\
    ' SELECT oid' +\
    ' FROM Offering'

    steps2 = [
        QueryStep('1', 'FROM Offering', [], '1'),
        QueryStep('2', 'SELECT oid', ['1'], '2'),
    ]

    tables2 = {
    }


    parsed_query1 = ParsedQuery(steps1, tables1, query_text1)
    parsed_query2 = ParsedQuery(steps2, tables2, query_text2)
    return {"global_tables": global_tables, "all_queries": [parsed_query1, parsed_query2]}


''' Multiple queries which do reference each other '''
def generate_multiple_queries_related():
    query_text1 =\
    ' CREATE VIEW pizza AS' +\
    ' SELECT sid, email, cgpa' +\
    ' FROM Student' +\
    ' WHERE cgpa<3'

    steps1 = [
        QueryStep('1', 'CREATE VIEW pizza AS SELECT sid, email, cgpa FROM Student WHERE cgpa<3', [], 'pizza'),
            QueryStep('1.1', 'FROM Student', [], '1.1'),
            QueryStep('1.2', 'WHERE cgpa<3', ['1.1'], '1.2',
                reasons = {
                    0: Reason(["cgpa<3"]),
                }),
            QueryStep('1.3', 'SELECT sid, email, cgpad', ['1.2'], 'pizza'),
    ]

    tables1 = {
    }


    query_text2 =\
    ' SELECT email' +\
    ' FROM pizza'

    steps2 = [
        QueryStep('1', 'FROM pizza', ['pizza'], '1'),
        QueryStep('2', 'SELECT email', ['1'], '2'),
    ]

    tables2 = {

    }


    parsed_query1 = ParsedQuery(steps1, tables1, query_text1)
    parsed_query2 = ParsedQuery(steps2, tables2, query_text2)
    new_global_tables = global_tables;
    new_global_tables["pizza"] =\
        Table(t_name='pizza',
                step = '0',
                col_names=['sid', 'email', 'cgpa'],
                tuples=[
                        ('3', 'not_martin@mail.com', '1.7'),
                        ('4', 'james@mail.com', '2.8')]
                )

    return {"global_tables": new_global_tables, "all_queries": [parsed_query1, parsed_query2]}



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
    'multiple_queries_related': generate_multiple_queries_related()
}

JSON_TRACES = {
    trace_name:
        {
            "global_tables": {t_name: t.to_json() for t_name,t in tables_and_queries["global_tables"].items()},
            "all_queries": [pq.to_json() for pq in tables_and_queries["all_queries"]]
        } for trace_name,tables_and_queries in TRACES.items()
}


def main():
    pprint.pprint(TRACES)



if __name__ == '__main__':
    main()
