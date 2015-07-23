from to_ast import ast, precedence
import unittest

class TestSQL(unittest.TestCase):
   
    def tearDown(self):
        print("============================\n")

    def test_00_simple(self):

        ''' TEST SIMPLE SELECT-FROM-WHERE:
            A simple select-from-where query.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['cgpa']] ],
                    [ 'FROM',   [['Student']] ],
                    [ 'WHERE',  [['cgpa', '>', '3']] ]
                ]
        '''
        print('TEST SIMPLE SELECT-FROM-WHERE:')
        print('A simple SELECT-FROM-WHERE query.')
        expected = "[['SELECT', [['sid'], ['cgpa']]], ['FROM', [['Student']]], ['WHERE', [['cgpa', '>', '3']]]]"
        output = ast("select sid, cgpa from Student where cgpa > 3;")
        print(expected)
        print(output)

    def test_01_simple_dotcol(self):
        ''' TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:
            A simple SELECT-FROM query using table.col format.
            Expected output:
                [
                    [ 'SELECT', [['Student.sid']]] ,
                    [ 'FROM',   [['Student']] ]
                ]
        '''
        print('TEST SIMPLE SELECT-FROM USING TABLE.COL FORMAT:')
        print('A simple SELECT-FROM query using table.col format.')
        expected = "[['SELECT', [['Student.sid']]], ['FROM', [['Student']]]]"
        output = ast("select Student.sid from Student")
        print(expected)
        print(output)


    def test_02a_select_constant(self):

        ''' TEST SELECT STRING CONSTANT:
            A query selecting a string constant.
            Expected output:
                [
                    [ 'SELECT', [["'foo'"]]],
                    [ 'FROM',   [['Student']] ]
                ]
        '''
        print('TEST SELECT STRING CONSTANT')
        print('A query selecting a string constant.')
        expected = "[['SELECT', [[\"'foo'\"]]], ['FROM', [['Student']]]]"
        output = ast('select \'foo\' from Student')
        print(expected)
        print(output)

    def test_02b_select_concatenatedcolumns(self):
        ''' TEST CONCATENATED COLUMNS
            A query selecting two columns concatenated.
            Expected output:
                [
                    [ 'SELECT', [[['dept', '||' ,'cnum']]]],
                    [ 'FROM',   [['Student']]]
                ]
        '''
        print('TEST CONCATENATED COLUMNS')
        print('A query selecting two columns concatenated.')
        expected = "[['SELECT', [[['dept', '||', 'cnum']]]], ['FROM', [['Student']]]]"
        output = ast('select dept || cnum from Student')
        print(expected)
        print(output)

    def test_02c_select_constant_and_column(self):
        ''' TEST SELECT COLUMN AND A CONSTANT:
            A query selecting a column and a constant, 2.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['2']]],
                    [ 'FROM',   [['Student', 'AS', 'S']]]
                ]
        '''
        print('TEST SELECT COLUMN AND A CONSTANT: ')
        print('A query selecting a column and a constant, 2.')
        expected  = "[['SELECT', [['sid'], ['2']]], ['FROM', [['Student', 'AS', 'S']]]]"
        output = ast('select sid, 2 from Student as S')
        print(expected)
        print(output)

    def test_03_rename_column_without_as(self):

        ''' TEST RENAMING A COLUMN:
            A query with a renamed column without keyword AS.
            Expected output:
                [
                    ['SELECT',  [['cnum', 'course']]],
                    ['FROM',    [['Courses']]],
                ]
        '''
        print('TEST RENAMING A COLUMN:')
        print('A query with a renamed column without keyword AS')
        expected = "[['SELECT', [['cnum', 'course']]], ['FROM', [['Courses']]]]"
        output = ast('select cnum course from Courses')
        print(expected)
        print(output)
    
    def test_04_rename_column_with_as(self):
        ''' TEST RENAMING A COLUMN WITH AS:
            A query with a renamed column using keyword AS.
            Expected output:
                [
                    ['SELECT',  [['cnum', 'AS', 'course']]],
                    ['FROM',    [['Courses']]],
                ]
        '''
        print('TEST RENAMING A COLUMN:')
        print('A query with a renamed column using keyword AS')
        expected = "[['SELECT', [['cnum', 'AS', 'course']]], ['FROM', [['Courses']]]]"
        output = ast('select cnum as course from Courses')
        print(expected)
        print(output)

    def test_05_rename_table_without_as(self):
        ''' TEST RENAME TABLE WITHOUT AS:
            A query with a table rename without keyword AS.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['grade']]],
                    [ 'FROM',   [['Took', 'T'], 'JOIN', ['Offering']]]
                ]
        '''
        print('TEST RENAME TABLE WITHOUT AS')
        print('A query with a table rename without keyword AS')
        expected = "[['SELECT', [['sid'], ['grade']]], ['FROM', [['Took', 'T'], 'JOIN', ['Offering']]]]"
        output = ast('select sid, grade from Took T JOIN Offering')
        print(expected)
        print(output)

    def test_06_rename_table_with_as(self):

        ''' TEST RENAME TABLE WITH AS:
            A query with a table rename using keyword AS.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['grade']] ],
                    [ 'FROM',   [['Took', 'AS', 'T'], 'JOIN', ['Offering'] ] ]
                ]
        '''
        print('TEST RENAME TABLE WITH AS')
        print('A query with a table rename with keyword AS')
        expected = "[['SELECT', [['sid'], ['grade']]], ['FROM', [['Took', 'AS', 'T'], 'JOIN', ['Offering']]]]"
        output = ast('select sid, grade from Took as T JOIN Offering')
        print(expected)
        print(output)

    def test_07_crossproduct_comma(self):
        ''' TEST CROSS PRODUCT ",":
            A query with a cross product in it, comma formatted.
            Expected output:
                [
                    [ 'SELECT', [['Student.sid'], ['Student.email'], ['Took.grade']] ],
                    [ 'FROM',   [ ['Student'], ',', ['Took' ] ]]
                ]
        ''' 
        print('TEST CROSS PRODUCT ","')
        print('A query with a cross product, comma formatted')
        expected = "[['SELECT', [['Student.sid'], ['Student.email'], ['Took.grade']]], ['FROM', [['Student'], ',', ['Took']]]]"
        testquery = "select student.sid, student.email, took.grade from Student, Took"
        output = ast(testquery)
        print(expected)
        print(output)

    def test_08_crossproduct_join(self):

        ''' TEST JOIN:
            A query with a cross product in it, using keyword JOIN.
            Expected output:
                [
                    [ 'SELECT', [['Student.sid'], ['Student.email'], ['Took.grade']] ],
                    [ 'FROM',   [ ['Student'], 'JOIN', ['Took'] ] ]
                ]
        '''
        print('TEST JOIN:')
        print('A query with a cross product in it, using keyword JOIN.')
        expected = "[['SELECT', [['Student.sid'], ['Student.email'], ['Took.grade']]], ['FROM', [['Student'], 'JOIN', ['Took']]]]"
        output = ast('select student.sid, student.email, took.grade from Student join Took')
        print(expected)
        print(output)

    def test_09_natural_join_1(self):
        ''' TEST NATURAL JOIN:
            A query with one NATURAL JOIN.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['email'], ['cgpa']] ],
                    [ 'FROM',   [ ['Student'], 'NATURAL JOIN', ['Took'] ] ]
                ]
        '''
        print('TEST NATURAL JOIN')
        print('A query with one NATURAL JOIN.')
        expected = "[['SELECT', [['sid'], ['email'], ['cgpa']]], ['FROM', [['Student'], 'NATURAL JOIN', ['Took']]]]"
        output = ast('select sid, email, cgpa from Student natural join Took')
        print(expected)
        print(output)

    def test_10_natural_join_2(self):

        #*************************************************
        ''' TEST TWO NATURAL JOINS:
            A query with two NATURAL JOINS.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['email'], ['cgpa' ]] ],
                    [ 'FROM',   [ ['Student'], 'NATURAL JOIN', ['Took'], 
                                                'NATURAL JOIN', ['Offering'] ]]
                ]
        '''
        print('TEST TWO NATURAL JOINS')
        print('A query with two NATURAL JOINS.')
        expected = "[['SELECT', [['sid'], ['email'], ['cgpa']]], ['FROM', [['Student'], 'NATURAL JOIN', ['Took'], 'NATURAL JOIN', ['Offering']]]]"
        output = ast('select sid, email, cgpa from Student natural join Took natural join Offering')
        print(expected)
        print(output)

    def test_11_left_join(self):
    
        ''' TEST LEFT JOIN ON <condition>: 
            A query with a LEFT JOIN on a condition.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['grade'], ['instructor']] ],
                    [ 'FROM',   [['Took'], 'LEFT JOIN', ['Offering'], 'ON', ['Took.oid', '=', 'Offering.oid'] ] ]
                ]
        '''
        print('TEST LEFT JOIN ON <condition>')
        print('A query with a LEFT JOIN on a condition.')
        expected = "[['SELECT', [['sid'], ['grade'], ['instructor']]], ['FROM', [['Took'], 'LEFT JOIN', ['Offering'], 'ON', ['Took.oid', '=', 'Offering.oid']]]]"
        output = ast('select sid, grade, instructor from Took left join Offering on Took.oid=Offering.oid')
        print(expected)
        print(output)

    def test_12_full_outer_join(self):


        ''' TEST FULL OUTER JOIN
            A query with a FULL OUTER JOIN.
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['grade']] ],
                    [ 'FROM',   [['Took'], 'FULL OUTER JOIN', ['Offering']] ],
                ]
        '''
        print('TEST FULL OUTER JOIN')
        print('A query with a FULL OUTER JOIN.')
        expected = "[['SELECT', [['sid'], ['grade']]], ['FROM', [['Took'], 'FULL OUTER JOIN', ['Offering']]]]"
        output = ast('select sid, grade from Took full outer join Offering')
        print(expected)
        print(output)


    def test_13_create_view(self):

        
        ''' TEST CREATE VIEW AS:
            A query with CREATE VIEW.
            Expected output:
                ['CREATE VIEW', 'students', 
                        [[ 'SELECT', [['email']]],
                        [ 'FROM',   [['Student']] ]
                        ]
                ]
        '''
        print('TEST CREATE VIEW AS')
        print('A query with CREATE VIEW.')
        expected = "['CREATE VIEW', 'students', [['SELECT', [['email']]], ['FROM', [['Student']]]]]"
        output = ast('create view students (select email from Student)')
        print(expected)
        print(output)

    def test_14_compound_cond_and(self):

        ''' TEST COMPOUND CONDITION: AND
            A query with an AND in its WHERE clause
            Expected output:
                [
                    [ 'SELECT', [['email'], ['cgpa']] ],
                    [ 'FROM',   [['Student']]],
                    [ 'WHERE',  [[['cgpa', '>', '3'], 'AND', ['firstName='Martin''] ] ]]
                ]
        '''
        print('TEST COMPOUND CONDITION: AND')
        print('A query with an AND in its WHERE clause.')
        expected = "[['SELECT', [['email'], ['cgpa']]], ['FROM', [['Student']]], ['WHERE', [[['cgpa', '>', '3'], 'AND', ['firstName', '=', \"'Martin'\"]]]]]"
        output = ast('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\'')
        print(expected)
        print(output)


    def test_15_compound_cond_or(self):

        ''' TEST COMPOUND CONDITION: OR:
            A query with a OR condition in its WHERE clause, also using bin op LIKE.
            Expected output:
                [
                    [ 'SELECT', [['email'], ['cgpa']] ],
                    [ 'FROM',   [['Student', 'AS', 'S']] ],
                    [ 'WHERE',  [['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', '%Mart%''] ] ]
                ]
        '''
        print('TEST COMPOUND CONDITION: OR')
        print('A query with an OR in its WHERE clause.')
        expected = "[['SELECT', [['email'], ['cgpa']]], ['FROM', [['Student', 'AS', 'S']]], ['WHERE', [[['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', \"'%Mart%'\"]]]]]"
        output = ast('select email, cgpa from Student as S where cgpa > 3 or firstName like \'%Mart$\'')
        print(expected)
        print(output)

    def test_16a_compound_cond_andor_nobrackets(self):

        ''' TEST COMPOUND CONDITION: AND + OR, NO BRACKETS
            A query with both AND and OR in its WHERE statement. Left evaluation, no brackets.
            Expected output:
                [
                    [ 'SELECT', [['email'], ['cgpa']] ],
                    [ 'FROM',   [['Student']] ],
                    [ 'WHERE',  [ [[['cgpa', '>', '3'], 'AND', ['firstName', '=', 'Martin'] ],
                                    'OR', ['firstName', 'LIKE', '%Kat%'] ] ]]
                ]
        '''
        print('TEST COMPOUND CONDITION: AND + OR, NO BRACKETS')
        print('A query with an AND and OR in its WHERE statement. Left evaluation, no brackets.')
        expected = "[['SELECT', [['email'], ['cgpa']]], ['FROM', [['Student']]], ['WHERE', [[[['cgpa', '>', '3'], 'AND', ['firstName', '=', \"'Martin'\"]], 'OR', ['firstName', 'LIKE', \"'%Kat$'\"]]]]]"
        output = ast('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\' or firstName like \'%Kat%\'')
        print(expected)
        print(output)

    def test_16b_compound_condition_andor_withbrackets(self):

        ''' TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS
            A query with both AND and OR in its WHERE statement. With brackets.
            Expected output:
                [
                    [ 'SELECT', [['email'], ['cgpa']] ],
                    [ 'FROM',   [['Student']] ],
                    [ 'WHERE',  [ [['cgpa', '>', '3'], 'AND', 
                                    [ ['firstName', '=', 'Martin'], 'OR', ['firstName', 'LIKE', '%Kat%']]
                                ]]
                    ]
                ]
        '''
        print('TEST COMPOUND CONDITION: AND + OR, WITH BRACKETS')
        print('A query with an AND and OR in its WHERE statement. With brackets.')
        expected = "[['SELECT', [['email'], ['cgpa']]], ['FROM', [['Student']]], ['WHERE', [[['cgpa', '>', '3'], 'AND', [['firstName', '=', \"'Martin'\"], 'OR', ['firstName', 'LIKE', \"'%Kat%'\"]]]]]]"
        output = ast('select email, cgpa from Student where cgpa > 3 and (firstName=\'Martin\' or firstName like \'%Kat%\'')
        print(expected)
        print(output)

    def test_17_compound_condition_not_and(self):
        ''' TEST COMPOUND CONDITION: NOT (cond AND cond)
            A query with NOT (cond AND cond).
            Expected output:
                [
                    [ 'SELECT', [['sid'], ['cgpa']]],
                    [ 'FROM',   [['Student']]],
                    [ 'WHERE',  [['NOT', [['sid', '>', '0'], 'AND', ['cgpa', '>=', '3.5']]]]]
                ]
        '''
        print('TEST COMPOUND CONDITION: NOT (cond AND cond)')
        print('A query with NOT (cond AND cond')
        expected = "[['SELECT', [['sid'], ['cgpa']]], ['FROM', [['Student']]], ['WHERE', [['NOT', [['sid', '>', '0'], 'AND', ['cgpa', '>=', '3.5']]]]]]"
        output = ast('select sid, cgpa from Student where not sid > 0 and cgpa >= 3.5')
        print(expected)
        print(output)

    def test_18_compound_condition_2and_1or(self):

        #*****************************************
        ''' TEST COMPOUND CONDITION: 2 AND + 1 OR 
            A query with two ANDS and one OR in its WHERE statement. (Multiple compounded conditions).
            Expected output:
                [
                    [ 'SELECT', [['email'], ['cgpa']]],
                    [ 'FROM',   [['Student']]],
                    [ 'WHERE',  [ [[[['cgpa', '<', '1.5'], 'AND', ['cgpa', '>', '3']], 
                                    'OR', ['firstName', 'LIKE', '%Kat%']],
                                    'AND', ['sid', '!=', '0']]]
                    ]
                ]

        '''
        print('TEST COMPOUND CONDITION: 2 AND + 1 OR')
        print('A query with two ANDS and an OR in its WHERE statement. Multiple compounded conditions.')
        expected = "[['SELECT', [['email'], ['cgpa']]], ['FROM', [['Student']]], ['WHERE', [[[[['cgpa', '<', '1.5'], 'AND', ['cgpa', '>', '3']], 'OR', ['firstName', 'LIKE', \"'%Kat%'\"]], 'AND', ['sid', '!=', '0']]]]]"
        output = ast('select email, cgpa from Student where cgpa < 1.5 and cgpa > 3 or firstName like \'%Kat%\' and sid != 0')
        print(expected)
        print(output)

    def test_19a_subquery_from(self):
        ''' TEST SUBQUERY IN FROM CLAUSE:
            A query with one subquery in the FROM clause
            Expected output:
                [
                    [ 'SELECT', [['sid']]], 
                    [ 'FROM',   [[
                        [
                            [ 'SELECT', 'DISTINCT', [['instructor']]], 
                            [ 'FROM',   [['Course']]]
                        ], 'H']]
                                ]
            ]
        '''
        print('TEST SUBQUERY IN FROM CLAUSE:')
        print('A query with one subquery in the FROM clause')
        expected = "[['SELECT', [['sid']]], ['FROM', [[[['SELECT', 'DISTINCT', [['instructor']]], ['FROM', [['Course']]]], 'H']]]]"
        output = ast('select sid from (select distinct instructor from Course) H')
        print(expected)
        print(output)


    def test_19b_subquery_from(self):
                
        ''' TEST SUBQUERY IN FROM CLAUSE (COMPLEX): 
            A query with one subquery in the FROM clause
            Expected output: 
                [
                    [ 'SELECT', [['sid'], [['dept', '||', 'cnum'], 'course'], ['grade']]],
                    [ 'FROM',   [['Took'], ',', [
                                    ['SELECT',  ['*'] ],
                                    ['FROM',    [['Offering']] ],
                                    ['WHERE',   [[['instructor', '=', '\'Horton\'']]]]
                                    ]
                                , 'H']], 
                    ['WHERE', [['Took.oid', '=', 'H.oid']]]
                ]

        '''

        print('TEST SUBQUERY IN FROM CLAUSE (COMPLEX): ')
        print('A query with one subquery in the FROM')
        expected = "[['SELECT', [['sid'], [['dept', '||', 'cnum'], 'course'], ['grade']]], ['FROM', [['Took'], ',', [[['SELECT', ['*']], ['FROM', [['Offering']]], ['WHERE', [['instructor', '=', '\'Horton\'']]]], 'H']]], ['WHERE', [['Took.oid', '='. 'H.oid']]]]"
        output = ast('select sid, dept || cnum course, grade from Took, (select * from Offering where instructor=\'Horton\';) H where Took.oid = H.oid;')
        print(expected)
        print(output)


    def test_20a_subquery_where(self):

        ''' TEST SUBQUERY IN WHERE CONDITION:
            A query with one subquery in the WHERE clause
            Expected output:
                [
                    [ 'SELECT', [['pizza']] ],
                    [ 'FROM',   [['Student'] ]],
                    [ 'WHERE',  [['cgpa', 'IN', [   ['SELECT',  [['cgpa']]],
                                                    ['FROM',    [['Took']]]
                                                ]]]]
                ]
        '''
        print('TEST SUBQUERY IN WHERE CONDITION')
        print('A query with one subquery in the WHERE clause')
        expected = "[['SELECT', [['pizza']]], ['FROM', [['Student']]], ['WHERE', [['cgpa', 'IN', [['SELECT', [['cgpa']]], ['FROM', [['Took']]]]]]]]"
        output = ast('select pizza from Student where cgpa in (select cgpa from Took;)')
        print(expected)
        print(output)

    def test_20b_subquery_where(self):
        ''' TEST SUBQUERY IN WHERE CONDITION (COMPLEX):
            A query with one subquery in the WHERE clause
            Expected output:
                [
                    [ 'SELECT', [['pizza']] ],
                    [ 'FROM',   [['Student'] ]],
                    [ 'WHERE',  [['cgpa', 'IN', [['SELECT', ['*']],
                                    ['FROM',    [['Offering']]],
                                    ['WHERE',   [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]]
                ]
        '''
        print('TEST SUBQUERY IN WHERE CONDITION (COMPLEX):')
        print('A query with one subquery in the WHERE clause')
        expected = "[['SELECT', [['pizza']]], ['FROM', [['Student']]], ['WHERE', [['cgpa', 'IN', [['SELECT', ['*']], ['FROM', [['Offering']]], ['WHERE', [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]]]"
        output = ast('select pizza from Student where cgpa in (select * from Offering where oid <> Offl.oid and instructor = Offl.instructor;)')
        print(expected)
        print(output)


    def test_21_subquery_select(self):
            
        ''' TEST SUBQUERY IN SELECT CLAUSE:
            A query with one subquery in the SELECT clause
            Expected output:
                [
                    [   'SELECT', [
                            ['SELECT', [['only']]], ['FROM', [['Took']] ]
                            ], 'H'],
                        ['FROM', [['Offering']] ]
                ]
        '''
        print('TEST SUBQUERY IN SELECT CLAUSE:')
        print('A query with one subquery in the SELECT clause')
        expected = "[['SELECT', [['SELECT', [['only']]], ['FROM', [['Took']]], 'H']], ['FROM', [['Offering']]]]"
        output = ast('select (select only from Took;) H from Offering')
        print(expected)
        print(output)

    def test_22_union(self):

        ''' TEST UNION
            A UNION of two SQL queries.
            Expected Output:
                [
                    [   [ 'SELECT', [['sid']]],
                        [ 'FROM,    [['Student']] ]
                    ], 
                    'UNION',
                    [   [ 'SELECT', [['sid']] ],
                        [ 'FROM',   [['Took'] ]]
                    ]
                ]
        '''

        print('TEST UNION:')
        print('A union of two SQL queries.')
        expected = "[[['SELECT', [['sid']]], ['FROM', [['Student']]]], 'UNION', [['SELECT', [['sid']]], ['FROM', [['Took']]]]]"
        output = ast('(select sid from Student;) union (select sid from Took;)')
        print(expected)
        print(output)

    def test_23_any_subquery(self):
        ''' TEST ANY
            A query containing a subquery using keyword ANY in WHERE condition.
            Expected output:
                [
                    [ 'SELECT', [['sid']]],
                    [ 'FROM'    [['Student']]],
                    [ 'WHERE',  [['gpa', '>', 'ANY', [
                                                ['SELECT', [['gpa']]], 
                                                ['FROM', [['Student'], 'NATURAL JOIN', ['Took']]], 
                                                ['WHERE', [['grade', '>', '100']]]
                                            ]]]
                    ]
                ]
        '''
        print('TEST ANY')
        print('A query using keyword ANY in WHERE condition.')
        expected = "[['SELECT', [['sid']]], ['FROM', [['Student']]], ['WHERE', [['gpa', '>', 'ANY', [['SELECT', [['gpa']]], ['FROM', [['Student'], 'NATURAL JOIN', ['Took']]], ['WHERE', [['grade', '>', '100']]]]]]]]"
        output = ast('select sid from Student where gpa > ANY (select gpa from Student NATURAL JOIN Took where grade > 100;);')
        print(expected)
        print(output)


    def test_24_in_subquery(self):
        ''' TEST IN
            A query containing a subquery using keyword IN.
            Expected output:
                [
                    [ 'SELECT', [['sid'], [['dept', '||', 'cnum'], 'AS', 'course'], ['grade']]],
                    [ 'FROM',   [['Took'], 'NATURAL JOIN', ['Offering']]],
                    [ 'WHERE',  [[['grade', '>=', '80'], 'AND', ['dept', 'IN', 
                                [   ['SELECT',  [['dept']]], 
                                    ['FROM',    [['Took'], 'NATURAL JOIN', ['Offering'], 'NATURAL JOIN', ['Student']]],
                                    ['WHERE',   [['surname', '=', "'Lakemeyer'"]]]
                                ]]]]
                    ]
                ]
        '''
        print('TEST IN')
        print('A query containing a subquery using keyword IN.')
        expected = "[['SELECT', [['sid'], [['dept', '||', 'cnum'], 'AS', 'course'], ['grade']]], ['FROM', [['Took'], 'NATURAL JOIN', ['Offering']]], ['WHERE', [[['grade', '>=', '80'], 'AND', ['dept', 'IN', [['SELECT', [['dept']]], ['FROM', [['Took'], 'NATURAL JOIN', ['Offering'], 'NATURAL JOIN', ['Student']]], ['WHERE', [['surname', '=', \"'Lakemeyer'\"]]]]]]]]]"
        output = ast('select sid, dept || cnum as course, grade from Took natural join Offering where grade >= 80 and dept in (select dept from Took natural join offering natural join Student where surname = \'Lakemeyer\';);')
        print(expected)
        print(output)

    def test_25a_not_exists_subquery(self):
        ''' TEST NOT EXISTS
            A query containing a subquery using keyword EXISTS.
            Expected output:
                [
                    [ 'SELECT', [['instructor']]],
                    [ 'FROM',   [['Offering', 'AS', 'Offl']],
                    [ 'WHERE',  [['NOT', ['EXISTS', 
                                    [['SELECT', ['*']],
                                    ['FROM',    [['Offering']]],
                                    ['WHERE',   [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]]
                ]]]
        '''

        print('TEST NOT EXISTS')
        print('A query containing a subquery using keyword NOT EXISTS.')
        expected = "[['SELECT', [['instructor']]], ['FROM', [['Offering', 'AS', 'Offl']]], ['WHERE', [['NOT', ['EXISTS', [['SELECT', ['*']], ['FROM', [['Offering']]], ['WHERE', [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]]]]"
        output = ast('select instructor from Offering as Offl where not exists (select * from Offering where oid <> Offl.oid and instructor = Offl.instructor;);')
        print(expected)
        print(output)

        print('Subquery')
        expected2 = "[['SELECT', ['*']], ['FROM', [['Offering']]], ['WHERE', [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]"
        output2 = ast('select * from Offering where oid <> Offl.oid and instructor = Offl.instructor')
        print(expected2)
        print(output2)

    def test_25b_exists_subquery(self):
        ''' TEST EXISTS
            A query containing a subquery using keyword EXISTS.
            Expected output:
                [
                    [ 'SELECT', [['instructor']]],
                    [ 'FROM',   [['Offering', 'AS', 'Offl']]],
                    [ 'WHERE',  [['EXISTS', 
                                    [['SELECT', ['*']],
                                    ['FROM',    [['Offering']]],
                                    ['WHERE',   [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]]
                ]]
        '''

        print('TEST EXISTS')
        print('A query containing a subquery using keyword EXISTS.')
        expected = "[['SELECT', [['instructor']]], ['FROM', [['Offering', 'AS', 'Offl']]], ['WHERE', [['EXISTS', [['SELECT', ['*']], ['FROM', [['Offering']]], ['WHERE', [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]]]]]"
        output = ast('select instructor from Offering as Offl where exists (select * from Offering where oid <> Offl.oid and instructor = Offl.instructor;);')
        print(expected)
        print(output)

        print('Subquery')
        expected2 = "[['SELECT', ['*']], ['FROM', [['Offering']]], ['WHERE', [[['oid', '<>', 'Offl.oid'], 'AND', ['instructor', '=', 'Offl.instructor']]]]]"
        output2 = ast('select * from Offering where oid <> Offl.oid and instructor = Offl.instructor')
        print(expected2)
        print(output2)

  

    def test_26_distinct(self):
        ''' TEST DISTINCT
            A query selecting distinct entries for a column.
            Expected output:
                [
                    [ 'SELECT', 'DISTINCT', ['*']],
                    [ 'FROM',   [['Took']]]
                ]
        '''
        print('TEST DISTINCT')
        print('A query selecting distinct entries for a column.')
        expected = "[['SELECT', 'DISTINCT', ['*']], ['FROM', [['Took']]]]"
        output = ast('select distinct * from Took')
        print(expected)
        print(output)

    def test_27_limit(self):
        ''' TEST LIMIT
            A query limiting the number of entries in the query result.
            Expected output:
                [
                    [ 'SELECT', [['sid']]],
                    [ 'FROM",   [['Took']]],
                    [ 'LIMIT', ['10']]
                ]
        '''
        print('TEST LIMIT')
        print('A query limiting the number of entries in the query result.')
        expected = "[['SELECT', [['sid']]], ['FROM', [['Took']]], ['LIMIT', ['10']]]"
        output = ast('select sid from Took limit 10')
        print(expected)
        print(output)

    def test_28_limit_offset(self):
        ''' TEST LIMIT AND OFFSET
            A query limiting the number of entries in the query result and offset by a value.
            Expected output:
                [
                    [ 'SELECT', [['sid']]],
                    [ 'FROM",   [['Took']]],
                    [ 'LIMIT',  ['10']],
                    [ 'OFFSET', ['4']]
                ]
        '''
        print('TEST LIMIT AND OFFSET')
        print('A query limiting number of entries in the query result and offset by a value')
        expected = "[['SELECT', [['sid']]], ['FROM', [['Took']]], ['LIMIT', ['10']], ['OFFSET', ['4']]]"
        output = ast('select sid from Took limit 10 offset 4')
        print(expected)
        print(output)

    def test_29_aggregate_function_only(self):
        ''' TEST AGGREGATE FUNCTION ONLY
            A query selecting over one aggregated column. 
            Expected output:
                [
                    [ 'SELECT', [['max(sid)']]],
                    [ 'FROM',   [['Student']]],
                ]
        '''
        print('TEST AGGREGATE FUNCTION ONLY')
        print('A query selecting over one aggregated column. ')
        expected = "[['SELECT', [['max(sid)']]], ['FROM', [['Student']]]]"
        output = ast('select max(sid) from Student')
        print(expected)
        print(output)
 
    def test_30_group_by(self):
        ''' TEST GROUP BY
            A query selecting over one aggregated column and one unaggregated column
            Expected output:
                [
                    [ 'SELECT', [['max(cgpa)'], ['sid']]],
                    [ 'FROM',   [['Student']]],
                    [ 'GROUP BY', ['sid']]
                ]
        '''
        print('TEST GROUP BY')
        print('A  query selecting over one aggregated column and one unaggregated column')
        expected = "[['SELECT', [['max(cgpa)'], ['sid']]], ['FROM', [['Student']]], ['GROUP BY', ['sid']]]"
        output = ast('select max(cgpa), sid from Student group by sid')
        print(expected)
        print(output)


    def test_31_having(self):
        ''' TEST HAVING
            A query HAVING a condition.
            Expected output:
                [
                    [ 'SELECT', [['max(cgpa)', 'H']] ],
                    [ 'FROM',   [['Student']]],
                    [ 'HAVING', [['max(cgpa)', '>=', '3.5']]]
                ]
        '''
        print('TEST HAVING')
        print('A query HAVING a condition.')
        expected = "[['SELECT', [['max(cgpa)', 'H']]], ['FROM', [['Student']]], ['HAVING', [['max(cgpa)', '>=', '3.5']]]]"
        output = ast('select max(cgpa) H from Student having max(cgpa) >= 3.5')
        print(expected)
        print(output)

    def test_32_having_notinselect(self):
        ''' TEST HAVING CONDITION NOT IN SELECT CLAUSE
            A query containing a HAVING condition over aggregate function not in select clause.
            Expected output:
                [
                    [ 'SELECT', [['sum(salary)']]], 
                    [ 'FROM',   [['Department'], 'JOIN', ['Employee'], 'ON', ['dept', '=', 'did']]],
                    [ 'GROUP BY', ['dept']],
                    [ 'HAVING', [['min(salary)', '>=', '100']]]
                ]
        '''
        print('TEST HAVING CONDITION NOT IN SELECT CLAUSE')
        print('A query containing a HAVING condition over aggregate function not in select clause.')
        expected = "[['SELECT', [['sum(salary)']]], ['FROM', [['Department'], 'JOIN', ['Employee'], 'ON', ['dept', '=', 'did']]], ['GROUP BY', ['dept']], ['HAVING', [['min(salary)', '>=', '100']]]]"
        output = ast('select sum(salary) from Department join Employee on dept = did group by dept having min(salary) >= 100')
        print(expected)
        print(output)

    def test_33_order_by(self):
        ''' TEST ORDER BY
            A query which orders by a certain column.
            Expected output:
                [
                    [ 'SELECT', [['country'], ['population']]],
                    [ 'FROM',   [['Countries', 'AS', 'C']]],
                    [ 'ORDER BY', ['country']]
                ]
        '''
        print('TEST ORDER BY')
        print('A query which orders by a certain column.')
        expected = "[['SELECT', [['country'], ['population']]], ['FROM', [['Countries', 'AS', 'C']]], ['ORDER BY', ['country']]]"
        output = ast('select country, population from Countries as C order by country')
        print(expected)
        print(output)

    def test_34_is_null(self):
        ''' TEST ISNULL
            A query which checks if a column ISNULL or IS NULL.
            Expected output:
                [   
                    [ 'SELECT', [['country'], ['population']]],
                    [ 'FROM',   [['Countries']]],
                    [ 'WHERE',  [['gpa', 'ISNULL']]]
                ]
        '''
        print('TEST ISNULL')
        print('A query which checks if a column ISNULL or IS NULL.')
        expected = "[['SELECT', [['country'], ['population']]], ['FROM', [['Countries']]], ['WHERE', [['gpa', 'ISNULL']]]]"
        output1 = ast('select country, population from Countries where gpa ISNULL')
        output2 = ast('select country, population from Countries where gpa IS NULL')
        print(expected)
        print(output1)
        print(output2)

    def test_35_notnull(self):
        ''' TEST NOTNULL
            A query which checks if a column NOTNULL.
            Expected output:
                [
                    [ 'SELECT', [['country']]],
                    [ 'FROM',   [['Countries']]],
                    [ 'WHERE',  [['gpa', 'NOTNULL']]]
                ]
        '''
        print('TEST NOTNULL')
        print('A query which checks if a column NOTNULL.')
        expected = "[['SELECT', [['country']]], ['FROM', [['Countries']]], ['WHERE', [['gpa', 'NOTNULL']]]]"
        output = ast('select country from Countries where gpa notnull')
        print(expected)
        print(output)

    def test_36_between(self):
        ''' TEST BETWEEN
            A query which checks if a column is BETWEEN values x and y.
            Expected output:
                [
                    [ 'SELECT', [['gpa']]],
                    [ 'FROM',   [['Countries']]],
                    [ 'WHERE',  [['gpa', 'BETWEEN', 'x', 'AND', 'y']]]
                ]
        '''
        print('TEST BETWEEN')
        print('A query which checks if a column is BETWEEN x and y.')
        expected = "[['SELECT', [['gpa']]], ['FROM', [['Countries']]], ['WHERE', [['gpa', 'BETWEEN', 'x', 'AND', 'y']]]]"
        output = ast('select gpa from Countries where gpa between x and y')
        print(expected)
        print(output)

if __name__ == "__main__":
    unittest.main()
