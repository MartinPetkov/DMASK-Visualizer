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



''' A simple SELECT-FROM-WHERE query
SELECT sid
FROM Student
WHERE cgpa > 3
'''
def generate_simple_query():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with a cross product in it
SELECT sid, email, cgpa
FROM Student, Took
'''
def generate_simple_cross_product_query():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with one natural JOIN in it
SELECT sid, email, cgpa
FROM Student NATURAL JOIN Took
'''
def generate_simple_natural_join_query():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with a LEFT JOIN on a condition in it
SELECT term, instructor
FROM Took LEFT JOIN Offering ON Took.ofID=Offering.oid
'''
def generate_simple_condition_join_query():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with one subquery in the FROM
SELECT WhyUDoThis.oid
FROM
    (SELECT oid, dept
     FROM Offering
     ) AS WhyUDoThis
'''
def generate_simple_subquery():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with an AND in its WHERE clause
SELECT email, cgpa
FROM Student
WHERE cgpa > 3
AND firstName='Martin'
'''
def generate_simple_and_query():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with an OR in its WHERE clause
SELECT email, cgpa
FROM Student
WHERE cgpa > 3
OR firstName='Martin'
'''
def generate_simple_or_query():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with both AND and OR in its WHERE statement
SELECT email, cgpa
FROM Student
WHERE (cgpa > 3)
AND (firstName='Martin'
    OR firstName='Kathy')
'''
def generate_complex_and_plus_or():
    parsed_query = ParsedQuery()

    return [parsed_query]



''' A query with renaming of tables
SELECT t.sid, t.oid
FROM Took t
'''
def generate_complex_renaming():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with a subquery in the WHERE that's not repeated for each row
SELECT sid, surName
FROM Student
WHERE cgpa >
    (SELECT cgpa
     FROM Student
     WHERE sid=999)
'''
def generate_complex_subquery_in_where_not_repeated():
    parsed_query = ParsedQuery()

    return [parsed_query]


''' A query with a subquery in the WHERE that's repeated for each row
SELECT instructor
FROM Offering o1
WHERE NOT EXISTS (
    SELECT *
    FROM Offering o2
    WHERE o2.oid <> o1.oid)
'''
def generate_complex_subquery_in_where_repeated():
    parsed_query = ParsedQuery()

    return [parsed_query]



''' Multiple queries which don't reference each other
SELECT email
FROM Student

SELECT oid
FROM Took
'''
def generate_multiple_queries_unrelated():
    parsed_query1 = ParsedQuery()
    parsed_query2 = ParsedQuery()

    return [parsed_query1, parsed_query2]


''' Multiple queries which do reference each other
CREATE VIEW pizza AS
SELECT sid, email, cgpa
FROM Student
WHERE cgpa<3

SELECT email
FROM pizza
'''
def generate_multiple_queries_related():
    parsed_query1 = ParsedQuery()
    parsed_query2 = ParsedQuery()

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
