# simpleSQL.py
# simple demo of using the parsing library to do simple-minded SQL parsing
# could be extended to include where clauses etc
# Copyright (c) 2003, Paul McGuire

from pyparsing import Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional, \
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, \
    ZeroOrMore, restOfLine, Keyword as KEYWORD

# Define SQL KEYWORDS
SELECT      = KEYWORD("SELECT", caseless=True)
FROM        = KEYWORD("FROM", caseless=True)
WHERE       = KEYWORD("WHERE", caseless=True)
GROUP       = KEYWORD("GROUP", caseless=True)
BY          = KEYWORD("BY", caseless=True)
HAVING      = KEYWORD("HAVING", caseless=True)
ORDER       = KEYWORD("ORDER", caseless=True)
CREATE      = KEYWORD("CREATE", caseless=True)
VIEW        = KEYWORD("VIEW", caseless=True)
AS          = KEYWORD("AS", caseless=True)
DISTINCT    = KEYWORD("DISTINCT", caseless=True)
ON          = KEYWORD("ON", caseless=True)

# Define SQL CLAUSES
# Grammar for clauses will be defined below
selectClause    = Forward()
whereClause     = Forward()

# Define attribute (column) and table names
ident           = Word(alphas, alphanums + "_$").setName("identifier")
columnName      = delimitedList(ident, ".", combine=True)
columnNameList  = Group(delimitedList(columnName))
tableName       = delimitedList(ident, ".", combine=True)
tableNameList   = Group(delimitedList(tableName))
tableRename     = delimitedList(ident, ".", combine=True)
tableRenameList = Group(delimitedList(tableRename))

# Define OPERATORS
AND_        = KEYWORD("AND", caseless=True)
OR_         = KEYWORD("OR", caseless=True)
IN_         = KEYWORD("IN", caseless=True)
EXISTS_     = KEYWORD("EXISTS", caseless=True)
NOT_        = KEYWORD("NOT", caseless=True)
ANY_        = KEYWORD("ANY", caseless=True)
ALL_        = KEYWORD("ALL", caseless=True)
UNION_      = KEYWORD("UNION", caseless=True)
INTERSECT_  = KEYWORD("INTERSECT", caseless=True)
EXCEPT_     = KEYWORD("EXCEPT", caseless=True)
DISTINCT_   = KEYWORD("DISTINCT", caseless=True)
JOIN_       = KEYWORD("JOIN", caseless=True)
NATURAL_    = KEYWORD("NATURAL", caseless=True)
CROSS_      = KEYWORD("CROSS", caseless=True)
INNER_      = KEYWORD("INNER", caseless=True)
OUTER_      = KEYWORD("OUTER", caseless=True)
LEFT_       = KEYWORD("LEFT", caseless=True)
RIGHT_      = KEYWORD("RIGHT", caseless=True)
FULL_       = KEYWORD("FULL", caseless=True)
COMMA_      = KEYWORD(",", caseless=True)

BINOP      = oneOf("= != < > >= <= eq ne lt le gt ge LIKE", caseless=True)
arithSign   = Word("-=",exact=1)


def test( string ):
    print (string,"->")
    try:
        tokens = simpleSQL.parseString( string )
        print( "tokens = ",        tokens)
/bin/bash: q: command not found
        print ("tokens.tables =",  tokens.tables)
        print ("tokens.where =", tokens.where) 
    except ParseException:
        print (" "*err.loc + "^\n" + err.msg)
        print (err)
    print('================\n')


E = CaselessLiteral("E")
realNum = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  |
                                                         ( "." + Word(nums) ) ) + 
            Optional( E + Optional(arithSign) + Word(nums) ) )
intNum = Combine( Optional(arithSign) + Word( nums ) + 
            Optional( E + Optional("+") + Word(nums) ) )

columnRval = realNum | intNum | quotedString | columnName # need to add support for alg expressions

# ========== FROM CLAUSE =========== 

# Grammar for JOINS
joins = COMMA_ | (Optional(NATURAL_) + Optional(INNER_ | CROSS_ | LEFT_ + OUTER_ | LEFT_ | OUTER_ )) + JOIN_

# Table block, nested list within join Block
tableBlock = Group(tableName + Optional(AS + tableRename))
joinBlock = joins + tableBlock + Optional(ON + Group(columnName + BINOP + columnRval))
fromClause = Group(tableBlock +  ZeroOrMore(joinBlock))

# ========= WHERE CLAUSE ===========
whereCondition = Group(
    ( columnName + BINOP + columnRval ) |
    ( columnName + IN_ + "(" + delimitedList( columnRval ) + ")" ) |
    ( columnName + IN_ + Group(selectClause)) |
    ( "(" + whereClause + ")" )
    )

whereCompound = whereCondition + ZeroOrMore( (AND_ | OR_) + whereCondition)

whereClause << Group(whereCompound + ZeroOrMore( (AND_ | OR_) + whereCompound))


# Define the grammar for SQL query.
selectClause    <<  ( Group(    SELECT + 
                                ('*' | columnNameList).setResultsName( "columns" ))

                    + Group(    FROM +
                                fromClause) 
                    + Optional( Group( WHERE + ( whereClause ).setResultsName("where")))
                    
                    + Optional( Group( HAVING )) 
                    + Optional( Group( GROUP + BY ))
                    + Optional( Group( ORDER + BY ))
                    )
simpleSQL = selectClause

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
simpleSQL.ignore( oracleSqlComment )


# ============= TESTING TRACES ===============

''' TEST 1:
    A simple select-from-where query.
    Expected output:
        [
            [ 'SELECT', ['sid', 'cgpa'] ],
            [ 'FROM',   [['Student']] ],
            [ 'WHERE',  [ ['cgpa', '>', '3'] ] ]
        ]
'''
print('TEST 1:')
print('A simple SELECT-FROM-WHERE query.')
test('select sid, cgpa from student where cgpa > 3')

''' TEST 2:
    A query with a cross product in it, comma formatted.
    Expected output:
        [
            [ 'SELECT', ['Student.sid','Student.email','Took.grade'] ],
            [ 'FROM',   [ ['Student'], ',', ['Took'] ] ],
        ]
''' 
print('TEST 2:')
print('A query with a cross product, comma formatted')
test('select student.sid, student.email, took.grade from student, took')


''' TEST 3:
    A query with a cross product in it, using keyword JOIN.
    Expected output:
        [
            [ 'SELECT', ['Student.sid', Student.email', 'Took.grade'] ],
            [ 'FROM',   [ ['Student'], 'JOIN', ['Took'] ] ]
        ]
'''
print('TEST 3:')
print('A query with a cross product in it, using keyword JOIN.')
test('select student.sid, student.email, took.grade from student join took')


''' TEST 4:
    A query with one NATURAL JOIN.
    Expected output:
        [
            [ 'SELECT', ['sid', 'email', 'cpa'] ],
            [ 'FROM',   [ ['Student'], 'NATURAL JOIN', ['Took'] ] ]
        ]
'''
print('TEST 4: ')
print('A query with one NATURAL JOIN.')
test('select sid, email, cgpa from Student natural join Took')

''' TEST 5:
    A query with two NATURAL JOINS.
    Expected output:
        [
            [ 'SELECT', ['sid', 'email', 'cgpa' ] ],
            [ 'FROM',   [ ['Student'], 'NATURAL JOIN', ['Took'] ] ]
        ]
'''
print('TEST 5:')
print('A query with two NATURAL JOINS.')
test('select sid, email, cgpa from Student natural join took natural join offering')

''' TEST 6: 
    A query with a LEFT JOIN on a condition.
    Expected output:
        [
            [ 'SELECT', ['sid', 'grade', 'instructor'] ],
            [ 'FROM',   [['Took'], 'LEFT JOIN', ['Offering'], 'ON', ['Took.oid', '=', 'Offering.oid'] ] ]
        ]
'''
print('TEST 6: ')
print('A query with a LEFT JOIN on a condition.')
test('select sid, grade, instructor from Took left join Offering on Took.oid=Offering.oid')

''' Test 7:
    A query with a rename and a JOIN.
    Expected output:
        [
            [ 'SELECT', ['sid', 'grade'] ],
            [ 'FROM',   [['Took', 'AS', 'T'], 'JOIN', ['Offering'] ] ]
        ]
'''
print('TEST 7: ')
print('A query with a rename and a JOIN')
test('select sid, grade from Took as T JOIN Offering')

''' TEST 8:
    A query with an AND in its WHERE clause
    Expected output:
        [
            [ 'SELECT', ['email', 'cgpa'] ],
            [ 'FROM',   [['Student']]],
            [ 'WHERE',  [['cgpa', '>', '3'], 'AND', ['firstName='Martin''] ] ]
        ]
'''
print('TEST 8: ')
print('A query with an AND in its WHERE clause.')
test('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\'')

''' TEST 9:
    A query with a OR condition in its WHERE clause, also using bin op LIKE.
    Expected output:
        [
            [ 'SELECT', ['email', 'cgpa'] ],
            [ 'FROM',   [['Student', AS 'S']] ],
            [ 'WHERE',  [['cgpa', '>', '3'], 'OR', ['firstName', 'LIKE', '%Mart%''] ] ]
        ]
'''
print('TEST 9: ')
print('A query with an OR in its WHERE clause.')
test('select email, cgpa from Student as S where cgpa > 3 or firstName like \'%Mart$\'')


''' TEST 10:
    A query with both AND and OR in its WHERE statement. Left evaluation, no brackets.
    Expected output:
        [
            [ 'SELECT', ['email', 'cgpa'] ],
            [ 'FROM',   [['Student'] ] ],
            [ 'WHERE',  [ [['cgpa', '>', '3'], 'AND', ['firstName', '=', 'Martin'] ],
                            'OR', ['firstName', 'LIKE', '%Kat%'] ] ]
        ]
'''
print('TEST 10: ')
print('A query with an AND and OR in its WHERE statement. Left evaluation, no brackets.')
test('select email, cgpa from Student where cgpa > 3 and firstName=\'Martin\' or firstName like \'%Kat%\'')

''' TEST 11:
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
print('TEST 11: ')
print('A query with an AND and OR in its WHERE statement. With brackets.')
test('select email, cgpa from Student where cgpa > 3 and (firstName=\'Martin\' or firstName like \'%Kat%\'')

''' TEST 12: 
    A query with two ANDS and one OR in its WHERE statement. (Multiple compounded conditions).
    Expected output:
        [
            [ 'SELECT', ['email']],
            [ 'FROM',   [['Student']] ],
            [ 'WHERE',  [ [[['cgpa', '<', '1.5'], 'AND', ['cgpa', '>', '3']], 
                            'OR', ['firstName', 'LIKE', '%Kat%']],
                            'AND', ['sid', '!=', '0']]
            ]
        ]

'''
print('TEST 12: ')
print('A query with two ANDS and an OR in its WHERE statement. Multiple compounded conditions.')
test('select email, cgpa from Student where cgpa < 1.5 and cgpa > 3 or firstName like \'%Kat%\' and sid != 0')





''' TEST 8: 
    A query with one subquery in the FROM
    Expected output: 
        [
            [ 'SELECT', ['LimitedCols.oid'] ],
            [ 'FROM',   [
                            ['SELECT',  ['oid', 'dept'] ],
                            ['FROM',    ['Offering'] ]
                        ]
                        , 'AS', 'LimitedCols'
            ]
        ]

'''
print('TEST 8: ')
print('A query with one subquery in the FROM')
#test('select LimitedCols.oid from (select oid, dept from Offering as LimitedCols)')

''' Test for having clause
test("select A, B from T join T2 order by B")
'''

