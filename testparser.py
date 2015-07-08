from to_ast import test, ast
import unittest

class TestSQL(unittest.TestCase):
   
    def tearDown(self):
        print("============================\n")

    def test_simple(self):

        ''' TEST SIMPLE SELECT-FROM-WHERE:
            A simple select-from-where query.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'cgpa'] ],
                    [ 'FROM',   [['Student']] ],
                    [ 'WHERE',  [ ['cgpa', '>', '3'] ] ]
                ]
        '''
        print('TEST SIMPLE SELECT-FROM-WHERE:')
        print('A simple SELECT-FROM-WHERE query.')
        expected = "[['SELECT', ['sid', 'cgpa']], ['FROM', [['Student']]], ['WHERE', [['cgpa', '>', '3']]]]"
        output = ast("select sid, cgpa from Student where cgpa > 3;")
        print(expected)
        print(output)

    def test_simple_dotcol(self):
        ''' TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:
            A simple SELECT-FROM query using table.col format.
            Expected output:
                [
                    [ 'SELECT', ['Student.sid']] ,
                    [ 'FROM',   [['Student']] ]
                ]
        '''
        print('TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:')
        print('A simple SELECT-FROM query using table.col format.')
        expected = "[['SELECT', ['Student.sid']], ['FROM', [['Student']]]]"
        output = ast("select Student.sid from Student")
        print(expected)
        print(output)


    def test_select_constant(self):

        ''' TEST SELECT STRING CONSTANT:
            A query selecting a string constant.
            Expected output:
                [
                    [ 'SELECT', ['foo']]
                    [ 'FROM',   [['Student']] ]
                ]
        '''
        print('TEST SELECT STRING CONSTANT')
        print('A query selecting a string constant.')
        expected = "[['SELECT', ['foo']], ['FROM', [['Student']]]]"
        output = ast('select \"foo\" from Student')
        print(expected)
        print(output)


    def test_crossproduct_comma(self):
        #************************************************
        ''' TEST CROSS PRODUCT ",":
            A query with a cross product in it, comma formatted.
            Expected output:
                [
                    [ 'SELECT', ['Student.sid','Student.email','Took.grade'] ],
                    [ 'FROM',   [ ['Student'], ',', ['Took'] ] ]]
                ]
        ''' 
        print('TEST CROSS PRODUCT ","')
        print('A query with a cross product, comma formatted')
        expected = "[['SELECT', ['Student.sid', 'Student.email', 'Took.grade']], ['FROM', [['Student'], ',', ['Took']]]]"
        testquery = "select student.sid, student.email, took.grade from Student, Took"
        output = ast(testquery)
        print(expected)
        print(output)

    def test_crossproduct_join(self):

        ''' TEST JOIN:
            A query with a cross product in it, using keyword JOIN.
            Expected output:
                [
                    [ 'SELECT', ['Student.sid', 'Student.email', 'Took.grade'] ],
                    [ 'FROM',   [ ['Student'], 'JOIN', ['Took'] ] ]
                ]
        '''
        print('TEST JOIN:')
        print('A query with a cross product in it, using keyword JOIN.')
        expected = "[['SELECT', ['Student.sid', 'Student.email', 'Took.grade']], ['FROM', [['Student'], 'JOIN', ['Took']]]]"
        output = ast('select student.sid, student.email, took.grade from Student join Took')
        print(expected)
        print(output)

    def test_natural_join_1(self):
        ''' TEST NATURAL JOIN:
            A query with one NATURAL JOIN.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'email', 'cgpa'] ],
                    [ 'FROM',   [ ['Student'], 'NATURAL', ' JOIN', ['Took'] ] ]
                ]
        '''
        print('TEST NATURAL JOIN')
        print('A query with one NATURAL JOIN.')
        expected = "[['SELECT', ['sid', 'email', 'cgpa']], ['FROM', [['Student'], 'NATURAL', 'JOIN', ['Took']]]]"
        output = ast('select sid, email, cgpa from Student natural join Took')
        print(expected)
        print(output)

    def test_natural_join_2(self):

        #*************************************************
        ''' TEST TWO NATURAL JOINS:
            A query with two NATURAL JOINS.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'email', 'cgpa' ] ],
                    [ 'FROM',   [[ ['Student'], 'NATURAL', 'JOIN', ['Took'] ], 
                                                'NATURAL', 'JOIN', ['Offering']] ]
                ]
        '''
        print('TEST TWO NATURAL JOINS')
        print('A query with two NATURAL JOINS.')
        expected = "[['SELECT', ['sid', 'email', 'cgpa']], ['FROM', [[['Student'], 'NATURAL', 'JOIN', ['Took']], 'NATURAL', 'JOIN', ['Offering']]]]"
        output = ast('select sid, email, cgpa from Student natural join Took natural join Offering')
        print(expected)
        print(output)

    def test_left_join(self):
    
        ''' TEST LEFT JOIN ON <condition>: 
            A query with a LEFT JOIN on a condition.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'grade', 'instructor'] ],
                    [ 'FROM',   [['Took'], 'LEFT, 'JOIN', ['Offering'], 'ON', ['Took.oid', '=', 'Offering.oid'] ] ]
                ]
        '''
        print('TEST LEFT JOIN ON <condition>')
        print('A query with a LEFT JOIN on a condition.')
        expected = "[['SELECT', ['sid', 'grade', 'instructor']], ['FROM', [['Took'], 'LEFT', 'JOIN', ['Offering'], 'ON', ['Took.oid', '=', 'Offering.oid']]]]"
        output = ast('select sid, grade, instructor from Took left join Offering on Took.oid=Offering.oid')
        print(expected)
        print(output)

    def test_full_outer_join(self):


        ''' TEST FULL OUTER JOIN
            A query with a FULL OUTER JOIN.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'grade'] ],
                    [ 'FROM',   [['Took'], 'FULL', 'OUTER', 'JOIN', ['Offering']] ],
                ]
        '''
        print('TEST FULL OUTER JOIN')
        print('A query with a FULL OUTER JOIN.')
        expected = "[['SELECT', ['sid', 'grade']], ['FROM', [['Took'], 'FULL', 'OUTER', 'JOIN', ['Offering']]]]"
        output = ast('select sid, grade from Took full outer join Offering')
        print(expected)
        print(output)


    def test_create_view(self):

        
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
        expected = "['CREATE', 'VIEW', 'AS', [['SELECT', ['email']], ['FROM', [['Student']]]]]"
        output = ast('create view as select email from Student')
        print(expected)
        print(output)

    def test_rename_and_join(self):


        ''' TEST RENAME AND JOIN:
            A query with a rename and a JOIN.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'grade'] ],
                    [ 'FROM',   [['Took', 'AS', 'T'], 'JOIN', ['Offering'] ] ]
                ]
        '''
        print('TEST RENAME AND JOIN')
        print('A query with a rename and a JOIN')
        expected = "[['SELECT', ['sid', 'grade']], ['FROM', [['Took', 'T'], 'JOIN', ['Offering']]]]"
        output = ast('select sid, grade from Took as T JOIN Offering')
        print(expected)
        print(output)

    def test_compound_cond_and(self):

        ''' TEST COMPOUND CONDITION: AND
            A query with an AND in its WHERE clause
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   [['Student']]],
                    [ 'WHERE',  [['cgpa', '>', '3'], 'AND', ['firstName='Martin''] ] ]
                ]
        '''
        print('TEST COMPOUND CONDITION: AND')
        print('A query with an AND in its WHERE clause.')
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', [['Student']]], ['WHERE', [['cgpa', '>', '3'], 'AND', ['firstName', '=', \"'Martin'\"]]]]"
        output = ast('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\'')
        print(expected)
        print(output)


    def test_compound_cond_or(self):

        ''' TEST COMPOUND CONDITION: OR:
            A query with a OR condition in its WHERE clause, also using bin op LIKE.
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   [['Student', AS 'S']] ],
                    [ 'WHERE',  [['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', '%Mart%''] ] ]
                ]
        '''
        print('TEST COMPOUND CONDITION: OR')
        print('A query with an OR in its WHERE clause.')
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', [['Student', 'S']]], ['WHERE', [['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', \"'%Mart%'\"]]]]"
        output = ast('select email, cgpa from Student as S where cgpa > 3 or firstName like \'%Mart$\'')
        print(expected)
        print(output)

    def test_compound_cond_andor_nobrackets(self):

        #*****************************************
        ''' TEST COMPOUND CONDITION: AND + OR, NO BRACKETS
            A query with both AND and OR in its WHERE statement. Left evaluation, no brackets.
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   [['Student'] ] ],
                    [ 'WHERE',  [ [['cgpa', '>', '3'], 'AND', ['firstName', '=', 'Martin'] ],
                                    'OR', ['firstName', 'LIKE', '%Kat%'] ] ]
                ]
        '''
        print('TEST COMPOUND CONDITION: AND + OR, NO BRACKETS')
        print('A query with an AND and OR in its WHERE statement. Left evaluation, no brackets.')
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', [['Student']]], ['WHERE', [[['cgpa', '>', '3'], 'AND', ['firstName', '=', \"'Martin'\"]], 'OR', ['firstName', 'LIKE', \"'%Kat$'\"]]]]"
        output = ast('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\' or firstName like \'%Kat%\'')
        print(expected)
        print(output)

    def test_compound_condition_andor_withbrackets(self):

        #***************************************
        ''' TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS
            A query with both AND and OR in its WHERE statement. With brackets.
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   [['Student']] ],
                    [ 'WHERE',  [ ['cgpa', '>', '3'], 'AND', 
                                    [ ['firstName', '=', 'Martin'], 'OR', ['firstName', 'LIKE', '%Kat%']]
                                ]
                    ]
                ]
        '''
        print('TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS')
        print('A query with an AND and OR in its WHERE statement. With brackets.')
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', [['Student']]], ['WHERE', [['cgpa', '>', '3'], 'AND', [['firstName', '=', \"'Martin'\"], 'OR', ['firstName', 'LIKE', \"'%Kat%'\"]]]]]"
        output = ast('select email, cgpa from Student where cgpa > 3 and (firstName=\'Martin\' or firstName like \'%Kat%\'')
        print(expected)
        print(output)


    def test_compound_condition_2and_1or(self):

        #*****************************************
        ''' TEST COMPOUND CONDITION: 2 AND + 1 OR 
            A query with two ANDS and one OR in its WHERE statement. (Multiple compounded conditions).
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa']],
                    [ 'FROM',   [['Student']] ],
                    [ 'WHERE',  [ [[['cgpa', '<', '1.5'], 'AND', ['cgpa', '>', '3']], 
                                    'OR', ['firstName', 'LIKE', '%Kat%']],
                                    'AND', ['sid', '!=', '0']]
                    ]
                ]

        '''
        print('TEST COMPOUND CONDITION: 2 AND + 1 OR')
        print('A query with two ANDS and an OR in its WHERE statement. Multiple compounded conditions.')
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', [['Student']]], ['WHERE', [[[['cgpa', '<', '1.5'], 'AND' ['cgpa', '>', '3']], 'OR', ['firstName', 'LIKE', \"'%Kat%'\"]], 'AND', ['sid', '!=', '0']]]]"
        output = ast('select email, cgpa from Student where cgpa < 1.5 and cgpa > 3 or firstName like \'%Kat%\' and sid != 0')
        print(expected)
        print(output)


    def test_subquery_from(self):
                
        ''' TEST SUBQUERY IN FROM CLAUSE: 
            A query with one subquery in the FROM clause
            Expected output: 
                [
                    [ 'SELECT', ['LimitedCols.oid'] ],
                    [ 'FROM',   [
                                    ['SELECT',  ['oid', 'dept'] ],
                                    ['FROM',    ['Offering'] ]
                                ]
                                , 'AS', 'LimitedCols']
                ]

        '''
        print('TEST SUBQUERY IN FROM CLAUSE: ')
        print('A query with one subquery in the FROM')
        expected = "[['SELECT', ['LimitedCols.oid']], ['FROM', [[['SELECT', ['oid', 'dept']], ['FROM', [['Offering']]]], 'LimitedCols']]]"
        output = ast('select LimitedCols.oid from (select oid, dept from Offering) as LimitedCols')
        print(expected)
        print(output)

    def test_subquery_where(self):

        ''' TEST SUBQUERY IN WHERE CONDITION:
            A query with one subquery in the WHERE clause
            Expected output:
                [
                    [ 'SELECT', ['pizza'] ],
                    [ 'FROM',   [['Student']] ],
                    [ 'WHERE',  [['cgpa', 'IN', [[  'SELECT',   ['cgpa'] ], 
                                                [   'FROM',     [['Took']] ]]
                                                ]
                                ]
                    ]
                ]
        '''
        print('TEST SUBQUERY IN WHERE CONDITION')
        print('A query with one subquery in the WHERE clause')
        expected = "[['SELECT', ['pizza']], ['FROM', [['Student']]], ['WHERE', [['cgpa', 'IN', [['SELECT', ['cgpa']], ['FROM', [['Took']]]]]]]]"
        output = ast('select pizza from Student where cgpa in (select cgpa from Took)')
        print(expected)
        print(output)

    def test_subquery_select(self):
            
        ''' TEST SUBQUERY IN SELECT CLAUSE:
            A query with one subquery in the SELECT clause
            Expected output:
                [
                    [   'SELECT', [ 
                            ['SELECT', ['only']], ['FROM', [['Took']] ]
                            ] ],
                        ['FROM', [['Offering']] ]
                ]
        '''
        print('TEST SUBQUERY IN SELECT CLAUSE:')
        print('A query with one subquery in the SELECT clause')
        expected = "[['SELECT', [['select', ['only']], ['FROM', [['Took']]]]], ['FROM', [['Offering']]]]"
        output = ast('select (select only from Took) from Offering')
        print(expected)
        print(output)
        
#    def test_union(self):

        ''' TEST UNION
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

        '''
        print('TEST UNION:')
        print('A union of two SQL queries.')
        expected = "[["
        output = ast('(select sid from student) union (select sid from took)')
        print(expected)
        print(output)
'''

if __name__ == "__main__":
    unittest.main()
