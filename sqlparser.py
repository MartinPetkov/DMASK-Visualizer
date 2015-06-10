# simpleSQL.py
# simple demo of using the parsing library to do simple-minded SQL parsing
# could be extended to include where clauses etc
# Copyright (c) 2003, Paul McGuire

from pyparsing import Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional, \
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, \
    ZeroOrMore, restOfLine, Keyword

def test( str ):
    print str,"->"
    try:
        tokens = simpleSQL.parseString( str )
        print "tokens = ",        tokens
        print "tokens.columns =", tokens.columns
        print "tokens.tables =",  tokens.tables
        print "tokens.where =", tokens.where
    except ParseException, err:
        print " "*err.loc + "^\n" + err.msg
        print err
    print

# Define SQL tokens
selectStmt = Forward()
whereExpression = Forward()
selectToken = Keyword("SELECT", caseless=True)
fromToken = Keyword("FROM", caseless=True)
whereToken = Keyword("WHERE", caseless=True)
groupByToken = Keyword("GROUP BY", caseless=True)
havingToken = Keyword("HAVING", caseless=True)
orderByToken = Keyword("ORDER BY", caseless=True)
createToken = Keyword("CREATE", caseless=True)
# insertToken = Keyword("INSERT", caseless=True)
# deleteToken = Keyword("DELETE", caseless=True)
# updateToken = Keyword("UPDATE", caseless=True)
# setToken = Keyword("SET", caseless=True)
asToken = Keyword("AS", caseless=True)

# Identifiers
ident           = Word( alphas, alphanums + "_$" ).setName("identifier")
columnName      = delimitedList( ident, ".", combine=True )
columnNameList  = Group( delimitedList( columnName ) )
tableName       = delimitedList( ident, ".", combine=True )
tableNameList   = Group( delimitedList( tableName ) )
tableRename     = delimitedList(ident, ".", combine=True )
tableRenameList = Group ( delimitedList(tableRename))

# Define operators
and_ = Keyword("AND", caseless=True)
or_ = Keyword("OR", caseless=True)
in_ = Keyword("IN", caseless=True)
exists_ = Keyword("EXISTS", caseless=True)
not_ = Keyword("NOT", caseless=True)
like_ = Keyword("LIKE", caseless=True)
any_ = Keyword("ANY", caseless=True)
all_ = Keyword("ALL", caseless=True)
union_ = Keyword("UNION", caseless=True)
intersect_ = Keyword("INTERSECT", caseless=True)
except_ = Keyword("EXCEPT", caseless=True)
distinct_ = Keyword("DISTINCT", caseless=True)

exists_ = Upcase( Keyword("exists", caseless=True))
not_ = Upcase( Keyword("not", caseless=True))
like_ = Upcase( Keyword("like", caseless = True))
any_ = Upcase( Keyword("any", caseless=True))
all_ = Upcase( Keyword("all", caseless=True))
union_ = Upcase( Keyword("union", caseless=True))
intersect_ = Upcase( Keyword("intersect", caseless=True))
except_ = Upcase( Keyword("except", caseless=True))
distinct_ = Upcase( Keyword("distinct", caseless=True))
join_ = Upcase( Keyword("join", caseless=True))
natural_ = Upcase( Keyword("natural", caseless=True))
cross_ = Upcase( Keyword("cross", caseless=True))
inner_ = Upcase( Keyword("inner", caseless=True))
outer_ = Upcase( Keyword("outer", caseless=True))
left_ = Upcase( Keyword("left", caseless=True))
right_ = Upcase( Keyword("right", caseless=True))
full_ = Upcase( Keyword("full", caseless=True))
into_ = Upcase( Keyword("into", caseless=True))
comma_ = Keyword(",")

E = CaselessLiteral("E")
binop = oneOf("= != < > >= <= eq ne lt le gt ge like", caseless=True)
arithSign = Word("+-",exact=1)
realNum = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  |
                                                         ( "." + Word(nums) ) ) + 
            Optional( E + Optional(arithSign) + Word(nums) ) )
intNum = Combine( Optional(arithSign) + Word( nums ) + 
            Optional( E + Optional("+") + Word(nums) ) )

columnRval = realNum | intNum | quotedString | columnName # need to add support for alg expressions

joins = comma_ | (Optional(natural_) + Optional(inner_ | cross_ | left_ + outer_ | left_ | outer_ ) + join_)

tableBlock = Group( tableNameList + Optional(asToken + tableRenameList))
joinBlock = joins + tableBlock
fromClause = Group(tableBlock +  ZeroOrMore(joinBlock))

whereCondition = Group(
    ( columnName + binop + columnRval ) |
    ( columnName + in_ + "(" + delimitedList( columnRval ) + ")" ) |
    ( columnName + in_ + Group(selectStmt)) |
    ( "(" + whereExpression + ")" )
    )
whereExpression << whereCondition + ZeroOrMore( ( and_ | or_ ) + whereExpression ) 

# define the grammar
selectStmt      <<  ( selectToken + 
                    ('*' | columnNameList).setResultsName( "columns" ) +
                    fromToken +
                    fromClause +
                    Optional( whereToken +  Group ( whereExpression ), "").setResultsName("where") +
                    Optional( havingToken ) + 
                    Optional( groupByToken ) +
                    Optional( orderByToken ) +
                    Optional( distinct_ )
                    )
simpleSQL = selectStmt

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
simpleSQL.ignore( oracleSqlComment )


'''test( "SELECT * from XYZZY, ABC" )
test( "select * from SYS.XYZZY" )
test( "Select A from Sys.dual" )
test( "Select A,B,C from Sys.dual" )
test( "Select A, B, C from Sys.dual" )
test( "Select A, B, C from Sys.dual, Table2   " )
test( "Select A, B, C from Sys.dual" )
test( "Xelect A, B, C frox Sys.dual" )
test( "Select" )
test( "Select &&& frox Sys.dual" )
test( "Select A from Sys.dual where a in ('RED','GREEN','BLUE')" )
test( "Select A from Sys.dual where a in ('RED','GREEN','BLUE') and b in (10,20,30)" )
test( "Select A,b from table1,table2 where table1.id eq table2.id -- test out comparison operators" )
test( "Select A from Sys.dual where a in (select A from Sys.dual)")
test( "Select A from Sys.dual as P where A in (select A from Sys.dual)")
test( "Select A from T1 as T where A like '%something$'")
test( "select A from T, T2")
test( "select A from T join t2")
'''

''' Test simple query '''
test("select A from T")

''' Test simple join '''
test("select A from S as P, T")


''' Test for more than one JOIN with renames '''
test( "select A from T join T2 as T4 join T3")




"""
Test output:
>pythonw -u simpleSQL.py
SELECT * from XYZZY, ABC ->
tokens =  ['select', '*', 'from', ['XYZZY', 'ABC']]
tokens.columns = *
tokens.tables = ['XYZZY', 'ABC']

select * from SYS.XYZZY ->
tokens =  ['select', '*', 'from', ['SYS.XYZZY']]
tokens.columns = *
tokens.tables = ['SYS.XYZZY']

Select A from Sys.dual ->
tokens =  ['select', ['A'], 'from', ['SYS.DUAL']]
tokens.columns = ['A']
tokens.tables = ['SYS.DUAL']

Select A,B,C from Sys.dual ->
tokens =  ['select', ['A', 'B', 'C'], 'from', ['SYS.DUAL']]
tokens.columns = ['A', 'B', 'C']
tokens.tables = ['SYS.DUAL']

Select A, B, C from Sys.dual ->
tokens =  ['select', ['A', 'B', 'C'], 'from', ['SYS.DUAL']]
tokens.columns = ['A', 'B', 'C']
tokens.tables = ['SYS.DUAL']

Select A, B, C from Sys.dual, Table2    ->
tokens =  ['select', ['A', 'B', 'C'], 'from', ['SYS.DUAL', 'TABLE2']]
tokens.columns = ['A', 'B', 'C']
tokens.tables = ['SYS.DUAL', 'TABLE2']

Xelect A, B, C from Sys.dual ->
^
Expected 'select'
Expected 'select' (0), (1,1)

Select A, B, C frox Sys.dual ->
               ^
Expected 'from'
Expected 'from' (15), (1,16)

Select ->
      ^
Expected '*'
Expected '*' (6), (1,7)

Select &&& frox Sys.dual ->
       ^
Expected '*'
Expected '*' (7), (1,8)

>Exit code: 0
"""
