from to_ast import ast, precedence
import unittest

class TestSQL(unittest.TestCase):

    def test_00_simple(self):

        ''' TEST SIMPLE SELECT-FROM-WHERE:
            A simple select-from-where query.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'cgpa'] ],
                    [ 'FROM',   ['Student'] ],
                    [ 'WHERE',  ['cgpa', '>', '3'] ]
                ]
        '''
        query = 'select sid, cgpa from Student where cgpa > 3;'
        expected = "[['SELECT', ['sid', 'cgpa']], ['FROM', ['Student']], ['WHERE', ['cgpa', '>', '3']]]"
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM-WHERE:\nA simple select-from-where query.\n Expected: {}, Output: {} doesn't match".format(expected, output))


    def test_01_simple_dotcol(self):
        ''' TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:
            A simple SELECT-FROM query using table.col format.
            Expected output:
                [
                    [ 'SELECT', ['Student.sid']] ,
                    [ 'FROM',   ['Student'] ]
                ]
        '''
        query = 'select Student.sid from Student'
        expected = "[['SELECT', ['Student.sid']], ['FROM', ['Student']]]"
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\nA simple SELECT-FROM query using table.col format.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_02a_select_constant(self):

        ''' TEST SELECT STRING CONSTANT:
            A query selecting a string constant.
            Expected output:
                [
                    [ 'SELECT', ["'foo'"]]
                    [ 'FROM',   ['Student'] ]
                ]
        '''
        query = 'select \'foo\' from Student'
        expected = "[['SELECT', [\"'foo'\"]], ['FROM', ['Student']]]"
        output = ast(query)
        self.assertEqual(expected, output, "TEST SELECT STRING CONSTANT:\nA query selecting a string constant.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_02b_select_concatenatedcolumns(self):
        ''' TEST CONCATENATED COLUMNS
            A query selecting two columns concatenated.
            Expected output:
                [
                    [ 'SELECT', [['dept', '||' ,'cnum']]],
                    [ 'FROM',   ['Student']]
                ]
        '''
        expected = "[['SELECT', [['dept', '||', 'cnum']]], ['FROM', ['Student']]]"
        query = 'select dept || cnum from Student'
        output = ast(query)
        self.assertEqual(expected, output, "TEST CONCATENATED COLUMNS:\nA query selecting two columns concatenated.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_02c_select_constant_and_column(self):
        ''' TEST SELECT COLUMN AND A CONSTANT:
            A query selecting a column and a constant, 2.
            Expected output:
                [
                    [ 'SELECT', ['sid', '2']],
                    [ 'FROM',   [['Student', 'S']]]
                ]
        '''
        expected = "[['SELECT', ['sid', '2']], ['FROM', [['Student', 'S']]]]"
        query = ('select sid, 2 from Student as S')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SELECT COLUMN AND A CONSTANT:\nA query selecting a column and a constant, 2.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_03_rename_column_without_as(self):

        ''' TEST RENAMING A COLUMN:
            A query with a renamed column without keyword AS.
            Expected output:
                [
                    ['SELECT',  [['cnum', 'course']]],
                    ['FROM',    ['Courses']],
                ]
        '''
        expected = "[['SELECT', [['cnum', 'course']]], ['FROM', ['Courses']]]"
        query = ('select cnum course from Courses')
        output = ast(query)
        self.assertEqual(expected, output, "TEST RENAMING A COLUMN WITHOUT AS:\nA query with a renamed column without keyword AS.\n Expected: {}, Output: {} don't match".format(expected, output))
    
    def test_04_rename_column_with_as(self):
        ''' TEST RENAMING A COLUMN WITH AS:
            A query with a renamed column using keyword AS.
            Expected output:
                [
                    ['SELECT',  [['cnum', 'course']]],
                    ['FROM',    ['Courses']],
                ]
        '''
        expected = "[['SELECT', [['cnum', 'course']]], ['FROM', ['Courses']]]"
        query = ('select cnum as course from Courses')
        output = ast(query)
        self.assertEqual(expected, output, "TEST RENAMING A COLUMN WITH AS:\nA query with a renamed column using keyword AS.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_05_rename_table_without_as(self):
        ''' TEST RENAME TABLE WITHOUT AS:
            A query with a table rename without keyword AS.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'grade']],
                    [ 'FROM',   [['Took', 'T'], 'JOIN', 'Offering']]
                ]
        '''
        expected = "[['SELECT', ['sid', 'grade']], ['FROM', [['Took', 'T'], 'JOIN', 'Offering']]]"
        query = ('select sid, grade from Took T JOIN Offering')
        output = ast(query)
        self.assertEqual(expected, output, "TEST RENAME TABLE WITHOUT AS:\nA query with a table rename without keyword AS.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_06_rename_table_with_as(self):

        ''' TEST RENAME TABLE WITH AS:
            A query with a table rename using keyword AS.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'grade'] ],
                    [ 'FROM',   [['Took', 'T'], 'JOIN', 'Offering' ] ]
                ]
        '''
        expected = "[['SELECT', ['sid', 'grade']], ['FROM', [['Took', 'T'], 'JOIN', 'Offering']]]"
        query = ('select sid, grade from Took as T JOIN Offering')
        output = ast(query)
        self.assertEqual(expected, output, "TEST RENAME TABLE WITH AS:\nA query with a table rename using keyword AS.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_07_crossproduct_comma(self):
        ''' TEST CROSS PRODUCT ",":
            A query with a cross product in it, comma formatted.
            Expected output:
                [
                    [ 'SELECT', ['Student.sid','Student.email','Took.grade'] ],
                    [ 'FROM',   [ 'Student', ',', 'Took' ] ]]
                ]
        ''' 
        expected = "[['SELECT', ['Student.sid', 'Student.email', 'Took.grade']], ['FROM', ['Student', ',', 'Took']]]"
        query = "select student.sid, student.email, took.grade from Student, Took"
        output = ast(query)
        self.assertEqual(expected, output, "TEST CROSS PRODUCT \",\":\nA query with a cross product in it, comma formatted.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_08_crossproduct_join(self):

        ''' TEST JOIN:
            A query with a cross product in it, using keyword JOIN.
            Expected output:
                [
                    [ 'SELECT', ['Student.sid', 'Student.email', 'Took.grade'] ],
                    [ 'FROM',   [ 'Student', 'JOIN', 'Took' ] ]
                ]
        '''
        expected = "[['SELECT', ['Student.sid', 'Student.email', 'Took.grade']], ['FROM', ['Student', 'JOIN', 'Took']]]"
        query = ('select student.sid, student.email, took.grade from Student join Took')
        output = ast(query)
        self.assertEqual(expected, output, "TEST JOIN:\nA query with a cross product in it, using keyword JOIN.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_09_natural_join_1(self):
        ''' TEST NATURAL JOIN:
            A query with one NATURAL JOIN.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'email', 'cgpa'] ],
                    [ 'FROM',   [ 'Student', 'NATURAL JOIN', 'Took' ] ]
                ]
        '''
        expected = "[['SELECT', ['sid', 'email', 'cgpa']], ['FROM', ['Student', 'NATURAL JOIN', 'Took']]]"
        query = ('select sid, email, cgpa from Student natural join Took')
        output = ast(query)
        self.assertEqual(expected, output, "TEST NATURAL JOIN:\nA query with one NATURAL JOIN.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_10_natural_join_2(self):

        #*************************************************
        ''' TEST TWO NATURAL JOINS:
            A query with two NATURAL JOINS.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'email', 'cgpa' ] ],
                    [ 'FROM',   [[ 'Student', 'NATURAL JOIN', 'Took' ], 
                                                'NATURAL JOIN', 'Offering'] ]
                ]
        '''
        expected = "[['SELECT', ['sid', 'email', 'cgpa']], ['FROM', [['Student', 'NATURAL JOIN', 'Took'], 'NATURAL JOIN', 'Offering']]]"
        query = ('select sid, email, cgpa from Student natural join Took natural join Offering')
        output = ast(query)
        self.assertEqual(expected, output, "TEST TWO NATURAL JOINS:\nA query with two NATURAL JOINS.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_11_left_join(self):
    
        ''' TEST LEFT JOIN ON <condition>: 
            A query with a LEFT JOIN on a condition.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'grade', 'instructor'] ],
                    [ 'FROM',   ['Took', 'LEFT JOIN', 'Offering', 'ON', ['Took.oid', '=', 'Offering.oid'] ] ]
                ]
        '''
        expected = "[['SELECT', ['sid', 'grade', 'instructor']], ['FROM', ['Took', 'LEFT JOIN', 'Offering', 'ON', ['Took.oid', '=', 'Offering.oid']]]]"
        query = ('select sid, grade, instructor from Took left join Offering on Took.oid=Offering.oid')
        output = ast(query)
        self.assertEqual(expected, output, "TEST LEFT JOIN ON <condition>:\nA query with a LEFT JOIN on a condition.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_12_full_outer_join(self):


        ''' TEST FULL OUTER JOIN
            A query with a FULL OUTER JOIN.
            Expected output:
                [
                    [ 'SELECT', ['sid', 'grade'] ],
                    [ 'FROM',   ['Took', 'FULL OUTER JOIN', 'Offering'] ],
                ]
        '''
        expected = "[['SELECT', ['sid', 'grade']], ['FROM', ['Took', 'FULL OUTER JOIN', 'Offering']]]"
        query = ('select sid, grade from Took full outer join Offering')
        output = ast(query)
        self.assertEqual(expected, output, "TEST FULL OUTER JOIN:\nA query with a FULL OUTER JOIN.\n Expected: {}, Output: {} don't match".format(expected, output))


    def test_13_create_view(self):

        
        ''' TEST CREATE VIEW AS:
            A query with CREATE VIEW.
            Expected output:
                ['CREATE VIEW', 'students', 
                        [[ 'SELECT', ['email']],
                        [ 'FROM',   ['Student'] ]
                        ]
                ]
        '''
        expected = "['CREATE VIEW', 'students', [['SELECT', ['email']], ['FROM', ['Student']]]]"
        query = ('create view students as (select email from Student)')
        output = ast(query)
        self.assertEqual(expected, output, "TEST CREATE VIEW:\nA query with CREATE VIEW\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_14_compound_cond_and(self):

        ''' TEST COMPOUND CONDITION: AND
            A query with an AND in its WHERE clause
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   ['Student']],
                    [ 'WHERE',  [['cgpa', '>', '3'], 'AND', ['firstName='Martin''] ] ]
                ]
        '''
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', ['Student']], ['WHERE', [['cgpa', '>', '3'], 'AND', ['firstName', '=', \"'Martin'\"]]]]"
        query = ('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\'')
        output = ast(query)
        self.assertEqual(expected, output, "TEST COMPOUND CONDITION: AND\nA query with an AND in its WHERE clause\n Expected: {}, Output: {} don't match".format(expected, output))


    def test_15_compound_cond_or(self):

        ''' TEST COMPOUND CONDITION: OR:
            A query with a OR condition in its WHERE clause, also using bin op LIKE.
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   [['Student', 'S']] ],
                    [ 'WHERE',  [['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', '%Mart%''] ] ]
                ]
        '''
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', [['Student', 'S']]], ['WHERE', [['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', \"'%Mart%'\"]]]]"
        query = ('select email, cgpa from Student as S where cgpa > 3 or firstName like \'%Mart%\'')
        output = ast(query)
        self.assertEqual(expected, output, "TEST COMPOUND CONDITION: OR:\nA query with a OR condition in its WHERE clause, also using bin op LIKE.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_16a_compound_cond_andor_nobrackets(self):

        ''' TEST COMPOUND CONDITION: AND + OR, NO BRACKETS
            A query with both AND and OR in its WHERE statement. Left evaluation, no brackets.
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   ['Student'] ],
                    [ 'WHERE',  [ [['cgpa', '>', '3'], 'AND', ['firstName', '=', 'Martin'] ],
                                    'OR', ['firstName', 'LIKE', '%Kat%'] ] ]
                ]
        '''
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', ['Student']], ['WHERE', [[['cgpa', '>', '3'], 'AND', ['firstName', '=', \"'Martin'\"]], 'OR', ['firstName', 'LIKE', \"'%Kat$'\"]]]]"
        query = ('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\' or firstName like \'%Kat%\'')
        output = ast(query)
        self.assertEqual(expected, output, "TEST COMPOUND CONDITION: AND + OR, NO BRACKETS\nA query with both AND and OR in its WHERE statement. Left evaluation, no brackets.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_16b_compound_condition_andor_withbrackets(self):

        #***************************************
        ''' TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS
            A query with both AND and OR in its WHERE statement. With brackets.
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa'] ],
                    [ 'FROM',   ['Student'] ],
                    [ 'WHERE',  [ ['cgpa', '>', '3'], 'AND', 
                                    [ ['firstName', '=', 'Martin'], 'OR', ['firstName', 'LIKE', '%Kat%']]
                                ]
                    ]
                ]
        '''
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', ['Student']], ['WHERE', [['cgpa', '>', '3'], 'AND', [['firstName', '=', \"'Martin'\"], 'OR', ['firstName', 'LIKE', \"'%Kat%'\"]]]]]"
        query = ('select email, cgpa from Student where cgpa > 3 and (firstName=\'Martin\' or firstName like \'%Kat%\'')
        output = ast(query)
        self.assertEqual(expected, output, "TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS:\nA query with both AND and OR in its WHERE statement. With brackets.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_17_compound_condition_not_and(self):
        ''' TEST COMPOUND CONDITION: NOT (cond AND cond)
            A query with NOT (cond AND cond).
            Expected output:
                [
                    [ 'SELECT', ['sid', 'cgpa']],
                    [ 'FROM',   ['Student']],
                    [ 'WHERE',  ['NOT', [['sid', '>', '0'], 'AND', ['cgpa', '>=', '3.5']]]],
                ]
        '''
        expected = "[['SELECT', ['sid', 'cgpa']], ['FROM', ['Student']], ['WHERE', ['NOT', [['sid', '>', '0'], 'AND', ['cgpa', '>=', '3.5']]]]]"
        query = ('select sid, cgpa from Student where not sid > 0 and cgpa >= 3.5')
        output = ast(query)
        self.assertEqual(expected, output, "TEST COMPOUND CONDITION: NOT (cond AND cond):\nA query with NOT (cond AND cond)\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_18_compound_condition_2and_1or(self):

        #*****************************************
        ''' TEST COMPOUND CONDITION: 2 AND + 1 OR 
            A query with two ANDS and one OR in its WHERE statement. (Multiple compounded conditions).
            Expected output:
                [
                    [ 'SELECT', ['email', 'cgpa']],
                    [ 'FROM',   ['Student']],
                    [ 'WHERE',  [ [[['cgpa', '<', '1.5'], 'AND', ['cgpa', '>', '3']], 
                                    'OR', ['firstName', 'LIKE', '%Kat%']],
                                    'AND', ['sid', '!=', '0']]
                    ]
                ]

        '''
        expected = "[['SELECT', ['email', 'cgpa']], ['FROM', ['Student']], ['WHERE', [[[['cgpa', '<', '1.5'], 'AND', ['cgpa', '>', '3']], 'OR', ['firstName', 'LIKE', \"'%Kat%'\"]], 'AND', ['sid', '!=', '0']]]]"
        query = ('select email, cgpa from Student where cgpa < 1.5 and cgpa > 3 or firstName like \'%Kat%\' and sid != 0')
        output = ast(query)
        self.assertEqual(expected, output, "TEST COMPOUND CONDITION: 2 AND + 1 OR:\nA query with two ANDS and one OR in its WHERE statement. (Multiple compounded conditions).\n Expected: {}, Output: {} don't match".format(expected, output))


    def test_19_subquery_from(self):
                
        ''' TEST SUBQUERY IN FROM CLAUSE: 
            A query with one subquery in the FROM clause
            Expected output: 
                [
                    [ 'SELECT', ['sid', [['dept', '||', 'cnum'], 'course'], 'grade']],
                    [ 'FROM',   [[
                                    ['SELECT',  ['*'] ],
                                    ['FROM',    ['Offering'] ],
                                    ['WHERE',   ['instructor', '=', \'Horton\']]
                                    ]
                                , 'H']], 
                    ['WHERE', ['Took.oid', '=', 'H.oid']]
                ]

        '''

        expected = "[['SELECT', ['sid', [['dept', '||', 'cnum'], 'course'], 'grade']], ['FROM', [[['SELECT', ['*']], ['FROM', ['Offering']], ['WHERE', ['instructor', '=', '\'Horton\'']]], 'H']], ['WHERE', ['Took.oid', '='. 'H.oid']]]"
        query = ('select sid, dept || cnum as course, grade from Took, (select * from Offering where instructor=\'Horton\') H where Took.oid = H.oid;')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SUBQUERY IN FROM CLAUSE:\nA query with one subquery in the FROM clause\n Expected: {}, Output: {} don't match".format(expected, output))


    def test_20_subquery_where(self):

        ''' TEST SUBQUERY IN WHERE CONDITION:
            A query with one subquery in the WHERE clause
            Expected output:
                [
                    [ 'SELECT', ['pizza'] ],
                    [ 'FROM',   ['Student'] ],
                    [ 'WHERE',  ['cgpa', 'IN', [[  'SELECT',   ['cgpa'] ], 
                                                [   'FROM',     ['Took'] ]
                                                ]
                                ]
                    ]
                ]
        '''
        expected = "[['SELECT', ['pizza']], ['FROM', ['Student']], ['WHERE', ['cgpa', 'IN', [['SELECT', ['cgpa']], ['FROM', ['Took']]]]]]"
        query = ('select pizza from Student where cgpa in (select cgpa from Took)')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SUBQUERY IN WHERE CONDITION:\n query with one subquery in the WHERE clause\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_21_subquery_select(self):
            
        ''' TEST SUBQUERY IN SELECT CLAUSE:
            A query with one subquery in the SELECT clause
            Expected output:
                [
                    [   'SELECT', [ 
                            ['SELECT', ['only']], ['FROM', ['Took'] ]
                            ] ],
                        ['FROM', ['Offering'] ]
                ]
        '''
        expected = "[['SELECT', [['SELECT', ['only']], ['FROM', ['Took']]]], ['FROM', ['Offering']]]"
        query = ('select (select only from Took) from Offering')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SUBQUERY IN SELECT CLAUSE:\nA  query with one subquery in the SELECT clause\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_22_union(self):

        ''' TEST UNION
            A UNION of two SQL queries.
            Expected Output:
                [
                    [   [ 'SELECT', ['sid']],
                        [ 'FROM,    ['Student'] ]
                    ], 
                    'UNION',
                    [   [ 'SELECT', ['sid'] ],
                        [ 'FROM',   ['Took'] ]
                    ]
                ]
        '''

        print('TEST UNION:')
        print('A union of two SQL queries.')
        expected = "[[['SELECT', ['sid']], ['FROM', ['Student']]], 'UNION', [['SELECT', ['sid']], ['FROM', ['Took']]]]"
        output = ('(select sid from Student) union (select sid from Took)')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_23_any_subquery(self):
        ''' TEST ANY
            A query containing a subquery using keyword ANY in WHERE condition.
            Expected output:
                [
                    [ 'SELECT', ['sid']],
                    [ 'FROM'    ['Student']],
                    [ 'WHERE',  ['gpa', '>', 'ANY', [
                                                ['SELECT', ['gpa']], 
                                                ['FROM', [['Student'], 'NATURAL JOIN', ['Took']]], 
                                                ['WHERE', [['grade', '>', '100']]]
                                            ]]
                    ]
                ]
        '''
        print('TEST ANY')
        print('A query using keyword ANY in WHERE condition.')
        expected = "[['SELECT', ['sid']], ['FROM', ['Student']], ['WHERE', ['gpa', '>', 'ANY', [['SELECT', ['gpa']], ['FROM', [['Student'], 'NATURAL JOIN', ['Took']]], ['WHERE', [['grade', '>', '100']]]]]]]"
        output = ('select sid from Student where gpa > ANY (select gpa from Student NATURAL JOIN Took where grade > 100);')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))


    def test_24_in_subquery(self):
        ''' TEST IN
            A query containing a subquery using keyword IN.
            Expected output:
                [
                    [ 'SELECT', ['sid', [['dept', '||', 'cnum'], 'course'], 'grade']],
                    [ 'FROM',   ['Took', 'NATURAL JOIN', 'Offering']],
                    [ 'WHERE',  [['grade', '>=', '80'], 'AND', ['(cnum, dept)', 'IN', 
                                [   ['SELECT',  ['cnum', 'dept']], 
                                    ['FROM',    [['Took', 'NATURAL JOIN', 'Offering'], 'NATURAL JOIN', 'Offering']],
                                    ['WHERE',   [['surname', '=', "'Lakemeyer'"]]]
                                ]]]
                    ]
                ]
        '''
        print('TEST IN')
        print('A query containing a subquery using keyword IN.')
        expected = "[['SELECT', ['sid', [['dept', '||', 'cnum'], 'course'], 'grade']], ['FROM', ['Took', 'NATURAL JOIN', 'Offering']], ['WHERE', [['grade', '>=', '80'], 'AND', ['cnum', 'IN', [['SELECT', ['cnum']], ['FROM', [['Took', 'NATURAL JOIN', 'Offering'], 'NATURAL JOIN', 'Offering']], ['WHERE', [['surname', '=', "'Lakemeyer'"]]]]]]]]"
        output = ('select sid, dept || cnum as course, grade from Took natural join Offering where grade >= 80 and cnum in (select cnum from Took natural join offering natural join Student where surname = \'Lakemeyer\');')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_25a_not_exists_subquery(self):
        ''' TEST NOT EXISTS
            A query containing a subquery using keyword EXISTS.
            Expected output:
                [
                    [ 'SELECT', ['instructor']],
                    [ 'FROM',   [['Offering', 'Offl']],
                    [ 'WHERE',  ['NOT', 'EXISTS', 
                                    [['SELECT', ['*']],
                                    ['FROM',    ['Offering']],
                                    ['WHERE',   [['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]
                ]]
        '''

        print('TEST NOT EXISTS')
        print('A query containing a subquery using keyword NOT EXISTS.')
        expected = "[['SELECT', ['instructor']], ['FROM', [['Offering', 'Offl']]], ['WHERE', ['NOT', 'EXISTS', [['SELECT', ['*']], ['FROM', ['Offering']], ['WHERE', [['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]"
        output = ('select instructor from Offering as Offl where not exists (select * from Offering where oid <> Offl.oid and instructor = Offl.instructor);')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))

        print('Subquery')
        expected2 = "[['SELECT', ['*']], ['FROM', ['Offering']], ['WHERE', [['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]"
        output2 = ('select * from Offering where oid <> Offl.oid and instructor = Offl.instructor')
        print(expected2)
        print(output2)

    def test_25b_exists_subquery(self):
        ''' TEST EXISTS
            A query containing a subquery using keyword EXISTS.
            Expected output:
                [
                    [ 'SELECT', ['instructor']],
                    [ 'FROM',   [['Offering', 'Offl']],
                    [ 'WHERE',  ['EXISTS', 
                                    [['SELECT', ['*']],
                                    ['FROM',    ['Offering']],
                                    ['WHERE',   [['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]
                ]]
        '''

        print('TEST EXISTS')
        print('A query containing a subquery using keyword EXISTS.')
        expected = "[['SELECT', ['instructor']], ['FROM', [['Offering', 'Offl']]], ['WHERE', ['EXISTS', [['SELECT', ['*']], ['FROM', ['Offering']], ['WHERE', [['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]"
        output = ast('select instructor from Offering as Offl where exists (select * from Offering where oid <> Offl.oid and instructor = Offl.instructor);')
        output = (query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))

        print('Subquery')
        expected2 = "[['SELECT', ['*']], ['FROM', ['Offering']], ['WHERE', [['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]"
        output2 = ast('select * from Offering where oid <> Offl.oid and instructor = Offl.instructor')
        print(expected2)
        print(output2)

  

    def test_26_distinct(self):
        ''' TEST DISTINCT
            A query selecting distinct entries for a column.
            Expected output:
                [
                    [ 'SELECT', 'DISTINCT', ['*']],
                    [ 'FROM',   ['Took']]
                ]
        '''
        print('TEST DISTINCT')
        print('A query selecting distinct entries for a column.')
        expected = "[['SELECT', 'DISTINCT', ['*']], ['FROM', ['Took']]]"
        output = ('select distinct * from Took')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_27_limit(self):
        ''' TEST LIMIT
            A query limiting the number of entries in the query result.
            Expected output:
                [
                    [ 'SELECT', ['sid']],
                    [ 'FROM",   ['Took']],
                    [ 'LIMIT', ['10']]
                ]
        '''
        print('TEST LIMIT')
        print('A query limiting the number of entries in the query result.')
        expected = "[['SELECT', ['sid']], ['FROM', ['Took']], ['LIMIT', ['10']]]"
        output = ('select sid from Took limit 10')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_28_limit_offset(self):
        ''' TEST LIMIT AND OFFSET
            A query limiting the number of entries in the query result and offset by a value.
            Expected output:
                [
                    [ 'SELECT', ['sid']],
                    [ 'FROM",   ['Took']],
                    [ 'LIMIT',  ['10']],
                    [ 'OFFSET', ['4']]
                ]
        '''
        print('TEST LIMIT AND OFFSET')
        print('A query limiting number of entries in the query result and offset by a value')
        expected = "[['SELECT', ['sid']], ['FROM', ['Took']], ['LIMIT', ['10']], ['OFFSET', ['4']]]"
        output = ('select sid from Took limit 10 offset 4')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_29_aggregate_function_only(self):
        ''' TEST AGGREGATE FUNCTION ONLY
            A query selecting over one aggregated column. 
            Expected output:
                [
                    [ 'SELECT', ['max(sid)']],
                    [ 'FROM',   ['Student']],
                ]
        '''
        print('TEST AGGREGATE FUNCTION ONLY')
        print('A query selecting over one aggregated column. ')
        expected = "[['SELECT', ['max(sid)']], ['FROM', ['Student']]]"
        output = ('select max(sid) from Student')
        output = ast(query)
        self.assertEqual(expected, output, "TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:\n Expected: {}, Output: {} don't match".format(expected, output))
 
    def test_30_group_by(self):
        ''' TEST GROUP BY
            A query selecting over one aggregated column and one unaggregated column
            Expected output:
                [
                    [ 'SELECT', ['max(cgpa)', 'sid']],
                    [ 'FROM',   ['Student']],
                    [ 'GROUP BY', ['sid']]
                ]
        '''
        expected = "[['SELECT', ['max(cgpa)', 'sid']], ['FROM', ['Student']], ['GROUP BY', ['sid']]]"
        query = ('select max(cgpa), sid from Student group by sid')
        output = ast(query)
        self.assertEqual(expected, output, "TEST GROUP BY:\nA query selecting over one aggregated column and one unaggregated column\n Expected: {}, Output: {} don't match".format(expected, output))


    def test_31_having(self):
        ''' TEST HAVING
            A query HAVING a condition.
            Expected output:
                [
                    [ 'SELECT', ['max(cgpa)']],
                    [ 'FROM',   ['Student']],
                    [ 'HAVING', ['max(cgpa)', '>=', '3.5']]
                ]
        '''
        expected = "[['SELECT', ['max(cgpa)']], ['FROM', ['Student']], ['HAVING', ['max(cgpa)', '>=', '3.5']]]"
        query = ('select max(cgpa) from Student having max(cgpa) >= 3.5')
        output = ast(query)
        self.assertEqual(expected, output, "TEST HAVING:\n A query HAVING a condition.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_32_having_notinselect(self):
        ''' TEST HAVING CONDITION NOT IN SELECT CLAUSE
            A query containing a HAVING condition over aggregate function not in select clause.
            Expected output:
                [
                    [ 'SELECT', ['sum(salary)']], 
                    [ 'FROM',   ['Department', 'JOIN', 'Employee', 'ON', ['dept', '=', 'did']]],
                    [ 'GROUP BY', ['dept']],
                    [ 'HAVING', ['min(salary)', '>=', '100']]
                ]
        '''
        expected = "[['SELECT', ['sum(salary)']], ['FROM', ['Department', 'JOIN', 'Employee', 'ON', ['dept', '=', 'did']]], ['GROUP BY', ['dept']], ['HAVING', ['min(salary)', '>=', '100']]]"
        query = ('select sum(salary) from Department join Employee on dept = did group by dept having min(salary) >= 100')
        output = ast(query)
        self.assertEqual(expected, output, "TEST HAVING CONDITION NOT IN SELECT CLAUSE:\nA query containing a HAVING condition over aggregate function not in select clause.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_33_order_by(self):
        ''' TEST ORDER BY
            A query which orders by a certain column.
            Expected output:
                [
                    [ 'SELECT', ['country', 'population']],
                    [ 'FROM',   [['Countries', 'C']]],
                    [ 'ORDER BY', ['country']]
                ]
        '''
        expected = "[['SELECT', ['country', 'population']], ['FROM', [['Countries', 'C']]], ['ORDER BY', ['country']]]"
        query = ('select country, population from Countries as C order by country')
        output = ast(query)
        self.assertEqual(expected, output, "TEST ORDER BY:\nA query which orders by a certain column.\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_34_is_null(self):
        ''' TEST ISNULL
            A query which checks if a column ISNULL or IS NULL.
            Expected output:
                [   
                    [ 'SELECT', ['country', 'population']],
                    [ 'FROM',   ['Countries']],
                    [ 'WHERE',  ['gpa', 'ISNULL']]
                ]
        '''
        expected = "[['SELECT', ['country', 'population']], ['FROM', ['Countries']], ['WHERE', ['gpa', 'ISNULL']]]"
        query1 = ('select country, population from Countries where gpa ISNULL')
        query2 = ('select country, population from Countries where gpa IS NULL')
        output1 = ast(query1)
        output2 = ast(query2)
        self.assertEqual(expected, output1, "TEST ISNULL:\nA query which checks if a column ISNULL or IS NULL.\n Expected: {}, Output: {} don't match".format(expected, output1))
        self.assertEqual(expected, output2, "TEST ISNULL:\nA query which checks if a column ISNULL or IS NULL.\n Expected: {}, Output: {} don't match".format(expected, output2))

    def test_35_notnull(self):
        ''' TEST NOTNULL
            A query which checks if a column NOTNULL.
            Expected output:
                [
                    [ 'SELECT', ['country']],
                    [ 'FROM',   ['Countries']],
                    [ 'WHERE',  ['gpa', 'NOTNULL']]
                ]
        '''
        expected = "[['SELECT', ['country']], ['FROM', ['Countries']], ['WHERE', ['gpa', 'NOTNULL']]]"
        query = ('select country from Countries where gpa notnull')
        output = ast(query)
        self.assertEqual(expected, output, "TEST NOTNULL:\nA query which checks of a column NOTNULL\n Expected: {}, Output: {} don't match".format(expected, output))

    def test_36_between(self):
        ''' TEST BETWEEN
            A query which checks if a column is BETWEEN values x and y.
            Expected output:
                [
                    [ 'SELECT', ['gpa']],
                    [ 'FROM',   ['Countries']],
                    [ 'WHERE',  ['gpa', 'BETWEEN', 'x', 'AND', 'y']]
                ]
        '''
        expected = "[['SELECT', ['gpa']], ['FROM', ['Countries']], ['WHERE', ['gpa', 'BETWEEN', 'x', 'AND', 'y']]]"
        query = ('select gpa from Countries where gpa between x and y')
        output = ast(query)
        self.assertEqual(expected, output, "TEST BETWEEN:\nA query which checks if a column is BETWEEN values x and y.\n Expected: {}, Output: {} don't match".format(expected, output))


if __name__ == "__main__":
    unittest.main()
