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

# Define SQL CLAUSES
# Grammar for clauses will be defined below
sqlStmt         = Forward()
whereClause     = Forward()
simpleSQL       = Forward()

# Define attribute (column), table names, table renames
ident           = Word(alphas, alphanums + "_$").setName("identifier")
columnName      = delimitedList(ident, ".", combine=True)
columnNameList  = Group(delimitedList(columnName))
tableName       = delimitedList(ident, ".", combine=True)
tableNameList   = Group(delimitedList(tableName, ", ", combine=True))

tableNameList   = Group(delimitedList(tableName))
tableRename     = delimitedList(ident, ".", combine=True)
tableRenameList = Group(delimitedList(tableRename))

BINOP      = oneOf("= != < > <> >= <= eq ne lt le gt ge LIKE", caseless=True)
arithSign   = Word("-=",exact=1)

E = CaselessLiteral("E")
realNum = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  |
                                                         ( "." + Word(nums) ) ) + 
            Optional( E + Optional(arithSign) + Word(nums) ) )
intNum = Combine( Optional(arithSign) + Word( nums ) + 
            Optional( E + Optional("+") + Word(nums) ) )

columnRval = realNum | intNum | quotedString | columnName # need to add support for alg expressions

#========= SELECT CLAUSE ===========

selectClause = ('*' | columnNameList | columnRval | "(" + Group(sqlStmt) + ")" ).setResultsName("columns")

# ========== FROM CLAUSE =========== 

# Grammar for JOINS
joins = (COMMA_ | (Optional(NATURAL_) + Optional(INNER_ | CROSS_ | LEFT_ + OUTER_ | LEFT_ | OUTER_ )) + JOIN_)

# tableBlock nested within joinBlock, includes renames
tableBlock = Group(tableName + Optional (AS + tableRename))

# <tableBlock> {JOIN} <tableBlock>
joinBlock = Combine(joins, " ") + tableBlock + Optional(ON + Group(columnName + BINOP + columnRval))

# FROM CLAUSE
fromClause = (Group(tableBlock) +  ZeroOrMore(joinBlock)) | "(" + Group(sqlStmt) + ")"


# ========= WHERE CLAUSE ===========
whereCondition = Group(
    ( columnName + BINOP + columnRval ) |
    ( columnName + IN_ + "(" + delimitedList( columnRval ) + ")" ) |
    ( columnName + IN_ + "(" + Group(sqlStmt) + ")" ) |
    ( "(" + whereClause + ")" )
    )

whereCompound = whereCondition + ZeroOrMore( (AND_ | OR_) + whereCondition)

whereClause << Group(whereCompound + ZeroOrMore( (AND_ | OR_) + whereCompound))


# Define the grammar for SQL query.
sqlStmt         <<  ( Group(    SELECT + selectClause)
                    + Group(    FROM + fromClause ) 
                    + Optional( Group( WHERE + ( whereClause ).setResultsName("where")))
                    + Optional( Group( HAVING )) 
                    + Optional( Group( GROUP + BY ))
                    + Optional( Group( ORDER + BY ))
                    )

simpleSQL <<     Optional(CREATE + VIEW + AS) + Group(Optional("(") + sqlStmt + Optional(")"))



'''
simpleSQL =     (Optional(CREATE + VIEW + AS) + 
                + Group(sqlStmt) 
                + Optional( (UNION_ | INTERSECT_ | EXCEPT_) + (sqlStmt)))
'''
# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
simpleSQL.ignore( oracleSqlComment )


# ============= TESTING TRACES ===============

def test( string ):
    print (string,"->")
    try:
        tokens = simpleSQL.parseString( string )
        print( "tokens = ",        tokens)
        print( "tokens.columns =", tokens.columns)
        print ("tokens.tables =",  tokens.tables)
        print ("tokens.where =", tokens.where) 
    except ParseException:
        print (" "*err.loc + "^\n" + err.msg)
        print (err)
    print('================\n')

    
