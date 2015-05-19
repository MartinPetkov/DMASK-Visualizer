from parsed_query import ParsedQuery
from query_step import QueryStep
from table import Table

import pprint

'''
The schema:
Student(_sid_, firstName, email, cgpa)
Course(_dept,cNum_, name)
Offering(_oid_, dept, cNum, instructor)
Took(_sid,ofid_, grade)
'''



''' A simple SELECT-FROM-WHERE query '''
def generate_simple_query():
    query_text =\
    ' SELECT sid, cgpa'
    ' FROM Student'
    ' WHERE cgpa > 3'

    steps = [
        QueryStep('1', 'FROM Student', [], '1'),
        QueryStep('2', 'WHERE cgpa > 3', ['1'], '2'),
        QueryStep('3', 'SELECT sid', ['2'], '3'),
    ]

    tables = {
        '1': Table(t_id='1',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Martin', 'not_martin@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    ),

        '2': Table(t_id='2',
                    col_names=['sid', 'firstName', 'email', 'cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0')]
                    ),

        '3': Table(t_id='3',
                    col_names=['sid', 'cgpa'],
                    tuples=[
                            ('1', '3.4'),
                            ('2', '4.0')]
                    ),
    }


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with a cross product in it '''
def generate_simple_cross_product_query():
    query_text =\
    ' SELECT sid, email, cgpa'
    ' FROM Student, Took'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with one natural JOIN in it '''
def generate_simple_natural_join_query():
    query_text =\
    ' SELECT sid, email, cgpa'
    ' FROM Student NATURAL JOIN Took'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with a LEFT JOIN on a condition in it '''
def generate_simple_condition_join_query():
    query_text =\
    ' SELECT term, instructor'
    ' FROM Took LEFT JOIN Offering ON Took.ofID=Offering.oid'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with one subquery in the FROM '''
def generate_simple_subquery():
    query_text =\
    ' SELECT WhyUDoThis.oid'
    ' FROM'
    '    (SELECT oid, dept'
    '    FROM Offering'
    '    ) AS WhyUDoThis'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with an AND in its WHERE clause '''
def generate_simple_and_query():
    query_text =\
    ' SELECT email, cgpa'
    ' FROM Student'
    ' WHERE cgpa > 3'
    ' AND firstName=\'Martin\''

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with an OR in its WHERE clause '''
def generate_simple_or_query():
    query_text =\
    ' SELECT email, cgpa'
    ' FROM Student'
    ' WHERE cgpa > 3'
    ' OR firstName=\'Martin\''

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with both AND and OR in its WHERE statement '''
def generate_complex_and_plus_or():
    query_text =\
    ' SELECT email, cgpa'
    ' FROM Student'
    ' WHERE (cgpa > 3)'
    ' AND (firstName=\'Martin\''
    '    OR firstName=\'Kathy\')'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]



''' A query with renaming of tables '''
def generate_complex_renaming():
    query_text =\
    ' SELECT t.sid, t.oid'
    ' FROM Took t'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with a subquery in the WHERE that's not repeated for each row '''
def generate_complex_subquery_in_where_not_repeated():
    query_text =\
    ' SELECT sid, surName'
    ' FROM Student'
    ' WHERE cgpa >'
    '    (SELECT cgpa'
    '     FROM Student'
    '     WHERE sid=999)'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]


''' A query with a subquery in the WHERE that's repeated for each row '''
def generate_complex_subquery_in_where_repeated():
    query_text =\
    ' SELECT instructor'
    ' FROM Offering o1'
    ' WHERE NOT EXISTS ('
    '     SELECT oid'
    '     FROM Offering o2'
    '     WHERE o2.oid <> o1.oid)'

    steps = [
    ]

    tables = [
    ]


    parsed_query = ParsedQuery(steps, tables, query_text)
    return [parsed_query]



''' Multiple queries which don't reference each other '''
def generate_multiple_queries_unrelated():
    query_text1 =\
    ' SELECT email'
    ' FROM Student'

    steps1 = [
    ]

    tables1 = [
    ]


    query_text2 =\
    ' SELECT oid'
    ' FROM Took'

    steps2 = [
    ]

    tables2 = [
    ]


    parsed_query1 = ParsedQuery(steps1, tables1, query_text1)
    parsed_query2 = ParsedQuery(steps2, tables2, query_text2)
    return [parsed_query1, parsed_query2]


''' Multiple queries which do reference each other '''
def generate_multiple_queries_related():
    query_text1 =\
    ' CREATE VIEW pizza AS'
    ' SELECT sid, email, cgpa'
    ' FROM Student'
    ' WHERE cgpa<3'

    steps1 = [
    ]

    tables1 = [
    ]


    query_text2 =\
    ' SELECT email'
    ' FROM pizza'

    steps2 = [
    ]

    tables2 = [
    ]


    parsed_query1 = ParsedQuery(steps1, tables1, query_text1)
    parsed_query2 = ParsedQuery(steps2, tables2, query_text2)
    return [parsed_query1, parsed_query2]



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


def main():
    pprint.pprint(TRACES)

if __name__ == '__main__':
    main()
