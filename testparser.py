from to_ast import test
import unittest

class TestSQL(unittest.TestCase):

    ''' TEST SIMPLE SELECT-FROM-WHERE:
        A simple select-from-where query.
        Expected output:
            [[
                [ 'SELECT', ['sid', 'cgpa'] ],
                [ 'FROM',   [['Student']] ],
                [ 'WHERE',  [ ['cgpa', '>', '3'] ] ]
            ]]
    '''
    print('TEST SIMPLE SELECT-FROM-WHERE:')
    print('A simple SELECT-FROM-WHERE query.')
    

    test('select sid, cgpa from student where cgpa > 3')

''' TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:
    A simple SELECT-FROM query using table.col format.
    Expected output:
        [[
            [ 'SELECT', ['Student.sid']] ,
            [ 'FROM',   [['Student']] ],
        ]]
'''
print('TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:')
print('A simple SELECT-FROM query using table.col format.')
test('select Student.sid from Student')

#************************************************
''' TEST CROSS PRODUCT ",":
    A query with a cross product in it, comma formatted.
    Expected output:
        [[
            [ 'SELECT', ['Student.sid','Student.email','Took.grade'] ],
            [ 'FROM',   [ ['Student'], ',', ['Took'] ] ],
        ]]
''' 
print('TEST CROSS PRODUCT ","')
print('A query with a cross product, comma formatted')
test('select student.sid, student.email, took.grade from student, took')


''' TEST JOIN:
    A query with a cross product in it, using keyword JOIN.
    Expected output:
        [[
            [ 'SELECT', ['Student.sid', Student.email', 'Took.grade'] ],
            [ 'FROM',   [ ['Student'], 'JOIN', ['Took'] ] ]
        ]]
'''
print('TEST JOIN:')
print('A query with a cross product in it, using keyword JOIN.')
test('select student.sid, student.email, took.grade from student join took')


''' TEST NATURAL JOIN:
    A query with one NATURAL JOIN.
    Expected output:
        [[
            [ 'SELECT', ['sid', 'email', 'cpa'] ],
            [ 'FROM',   [ ['Student'], 'NATURAL', ' JOIN', ['Took'] ] ]
        ]]
'''
print('TEST NATURAL JOIN')
print('A query with one NATURAL JOIN.')
test('select sid, email, cgpa from Student natural join Took')

#*************************************************
''' TEST TWO NATURAL JOINS:
    A query with two NATURAL JOINS.
    Expected output:
        [[
            [ 'SELECT', ['sid', 'email', 'cgpa' ] ],
            [ 'FROM',   [[ ['Student'], 'NATURAL', 'JOIN', ['Took'] ], 
                                        'NATURAL', 'JOIN', ['Offering']] ]
        ]]
'''
print('TEST TWO NATURAL JOINS')
print('A query with two NATURAL JOINS.')
test('select sid, email, cgpa from Student natural join took natural join offering')

''' TEST LEFT JOIN ON <condition>: 
    A query with a LEFT JOIN on a condition.
    Expected output:
        [[
            [ 'SELECT', ['sid', 'grade', 'instructor'] ],
            [ 'FROM',   [['Took'], 'LEFT, 'JOIN', ['Offering'], 'ON', ['Took.oid', '=', 'Offering.oid'] ] ]
        ]]
'''
print('TEST LEFT JOIN ON <condition>')
print('A query with a LEFT JOIN on a condition.')
test('select sid, grade, instructor from Took left join Offering on Took.oid=Offering.oid')

''' TEST FULL OUTER JOIN
    A query with a FULL OUTER JOIN.
    Expected output:
        [[
            [ 'SELECT', ['sid', 'grade'] ],
            [ 'FROM',   [['Took'], 'FULL', 'OUTER', 'JOIN', ['Offering']] ],
        ]]
'''
print('TEST FULL OUTER JOIN')
print('A query with a FULL OUTER JOIN.')
test('select sid, grade from took full outer join offering')

''' TEST RENAME AND JOIN:
    A query with a rename and a JOIN.
    Expected output:
        [[
            [ 'SELECT', ['sid', 'grade'] ],
            [ 'FROM',   [['Took', 'AS', 'T'], 'JOIN', ['Offering'] ] ]
        ]]
'''
print('TEST RENAME AND JOIN')
print('A query with a rename and a JOIN')
test('select sid, grade from Took as T JOIN Offering')

''' TEST COMPOUND CONDITION: AND
    A query with an AND in its WHERE clause
    Expected output:
        [[
            [ 'SELECT', ['email', 'cgpa'] ],
            [ 'FROM',   [['Student']]],
            [ 'WHERE',  [['cgpa', '>', '3'], 'AND', ['firstName='Martin''] ] ]
        ]]
'''
print('TEST COMPOUND CONDITION: AND')
print('A query with an AND in its WHERE clause.')
test('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\'')

''' TEST COMPOUND CONDITION: OR:
    A query with a OR condition in its WHERE clause, also using bin op LIKE.
    Expected output:
        [[
            [ 'SELECT', ['email', 'cgpa'] ],
            [ 'FROM',   [['Student', AS 'S']] ],
            [ 'WHERE',  [['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', '%Mart%''] ] ]
        ]]
'''
print('TEST COMPOUND CONDITION: OR')
print('A query with an OR in its WHERE clause.')
test('select email, cgpa from Student as S where cgpa > 3 or firstName like \'%Mart$\'')

#*****************************************
''' TEST COMPOUND CONDITION: AND + OR, NO BRACKETS
    A query with both AND and OR in its WHERE statement. Left evaluation, no brackets.
    Expected output:
        [[
            [ 'SELECT', ['email', 'cgpa'] ],
            [ 'FROM',   [['Student'] ] ],
            [ 'WHERE',  [ [['cgpa', '>', '3'], 'AND', ['firstName', '=', 'Martin'] ],
                            'OR', ['firstName', 'LIKE', '%Kat%'] ] ]
        ]]
'''
print('TEST COMPOUND CONDITION: AND + OR, NO BRACKETS')
print('A query with an AND and OR in its WHERE statement. Left evaluation, no brackets.')
test('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\' or firstName like \'%Kat%\'')

#***************************************
''' TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS
    A query with both AND and OR in its WHERE statement. With brackets.
    Expected output:
        [[
            [ 'SELECT', ['email', 'cgpa'] ],
            [ 'FROM',   [['Student']] ],
            [ 'WHERE',  [ ['cgpa', '>', '3'], 'AND', 
                            [ ['firstName', '=', 'Martin'], 'OR', ['firstName', 'LIKE', '%Kat%']]
                        ]
            ]
        ]]
'''
print('TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS')
print('A query with an AND and OR in its WHERE statement. With brackets.')
test('select email, cgpa from Student where cgpa > 3 and (firstName=\'Martin\' or firstName like \'%Kat%\'')

#*****************************************
''' TEST COMPOUND CONDITION: 2 AND + 1 OR 
    A query with two ANDS and one OR in its WHERE statement. (Multiple compounded conditions).
    Expected output:
        [[
            [ 'SELECT', ['email', 'cgpa']],
            [ 'FROM',   [['Student']] ],
            [ 'WHERE',  [ [[['cgpa', '<', '1.5'], 'AND', ['cgpa', '>', '3']], 
                            'OR', ['firstName', 'LIKE', '%Kat%']],
                            'AND', ['sid', '!=', '0']]
            ]
        ]]

'''
print('TEST COMPOUND CONDITION: 2 AND + 1 OR')
print('A query with two ANDS and an OR in its WHERE statement. Multiple compounded conditions.')
test('select email, cgpa from Student where cgpa < 1.5 and cgpa > 3 or firstName like \'%Kat%\' and sid != 0')

''' TEST CREATE VIEW AS:
    A query with CREATE VIEW.
    Expected output:
        ['CREATE', 'VIEW', 'AS', 
                [[ 'SELECT', ['email']],
                [ 'FROM',   [['Student']] ]
                ]
        ]
'''
print('TEST CREATE VIEW AS')
print('A query with CREATE VIEW.')
test('create view as select email from Student')

''' TEST SELECT STRING CONSTANT:
    A query selecting a string constant.
    Expected output:
        [[
            [ 'SELECT', ['foo']]
            [ 'FROM',   [['Student']] ]
        ]]
'''
print('TEST SELECT STRING CONSTANT')
print('A query selecting a string constant.')
test('select \"foo\" from Student')


''' TEST SUBQUERY IN FROM CLAUSE: 
    A query with one subquery in the FROM clause
    Expected output: 
        [[
            [ 'SELECT', ['LimitedCols.oid'] ],
            [ 'FROM',   [
                            ['SELECT',  ['oid', 'dept'] ],
                            ['FROM',    ['Offering'] ]
                        ]
                        , 'AS', 'LimitedCols'
            ]
        ]

'''
print('TEST SUBQUERY IN FROM CLAUSE: ')
print('A query with one subquery in the FROM')
test('select LimitedCols.oid from (select oid, dept from Offering) as LimitedCols')

''' TEST SUBQUERY IN WHERE CONDITION:
    A query with one subquery in the WHERE clause
    Expected output:
        [[
            [ 'SELECT', ['pizza'] ],
            [ 'FROM',   [['Student']] ],
            [ 'WHERE',  [['cgpa', 'IN', [[  'SELECT',   ['cgpa'] ], 
                                        [   'FROM',     [['Took']] ]]
                                        ]
                        ]
            ]
        ]]
'''
print('TEST SUBQUERY IN WHERE CONDITION')
print('A query with one subquery in the WHERE clause')
test('select pizza from Student where cgpa in (select cgpa from Took)')

''' TEST SUBQUERY IN SELECT CLAUSE:
    A query with one subquery in the SELECT clause
    Expected output:
        [[
            [   'SELECT', [ 
                    ['SELECT', ['only']], ['FROM', [['Took']] ]
                    ] ],
                ['FROM', [['Offering']] ]
        ]]
'''
print('TEST SUBQUERY IN SELECT CLAUSE:')
print('A query with one subquery in the SELECT clause')
test('select (select only from Took) from Offering')

''' TEST
    A UNION of two SQL queries.
    Expected Output:
        [
            [   [ 'SELECT', ['sid']],
                [ 'FROM,    [['Student']] ]
            ], 
            'UNION',
            [   [ 'SELECT', ['sid'] ],
                [ 'FROM',   [['Took']] ]
            ]
        ]
'''
print('TEST :')
print('A union of two SQL queries.')
test('(select sid from student) union (select sid from took)')
