from pyparsing import (Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional,
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString,
    ZeroOrMore, restOfLine, Keyword as KEYWORD, Suppress)

# Define SQL KEYWORDS
SELECT          =   KEYWORD("SELECT", caseless=True)
FROM            =   KEYWORD("FROM", caseless=True)
WHERE           =   KEYWORD("WHERE", caseless=True)
GROUP           =   KEYWORD("GROUP", caseless=True)
BY              =   KEYWORD("BY", caseless=True)
HAVING          =   KEYWORD("HAVING", caseless=True)
ORDER           =   KEYWORD("ORDER", caseless=True)
CREATE          =   KEYWORD("CREATE", caseless=True)
VIEW            =   KEYWORD("VIEW", caseless=True)
AS              =   KEYWORD("AS", caseless=True)
DISTINCT        =   KEYWORD("DISTINCT", caseless=True)
ON              =   KEYWORD("ON", caseless=True)
ASC             =   KEYWORD("ASC", caseless=True)
DESC            =   KEYWORD("DESC", caseless=True)
USING           =   KEYWORD("USING", caseless=True)
LIMIT           =   KEYWORD("LIMIT", caseless=True)
OFFSET          =   KEYWORD("OFFSET", caseless=True)

# Define OPERATORS
AND_            =   KEYWORD("AND", caseless=True)
OR_             =   KEYWORD("OR", caseless=True)
IN_             =   KEYWORD("IN", caseless=True)
EXISTS_         =   KEYWORD("EXISTS", caseless=True)
NOT_            =   KEYWORD("NOT", caseless=True)
ANY_            =   KEYWORD("ANY", caseless=True)
ALL_            =   KEYWORD("ALL", caseless=True)
UNION_          =   KEYWORD("UNION", caseless=True)
INTERSECT_      =   KEYWORD("INTERSECT", caseless=True)
EXCEPT_         =   KEYWORD("EXCEPT", caseless=True)
DISTINCT_       =   KEYWORD("DISTINCT", caseless=True)
JOIN_           =   KEYWORD("JOIN", caseless=True)
NATURAL_        =   KEYWORD("NATURAL", caseless=True)
CROSS_          =   KEYWORD("CROSS", caseless=True)
INNER_          =   KEYWORD("INNER", caseless=True)
OUTER_          =   KEYWORD("OUTER", caseless=True)
LEFT_           =   KEYWORD("LEFT", caseless=True)
RIGHT_          =   KEYWORD("RIGHT", caseless=True)
FULL_           =   KEYWORD("FULL", caseless=True)
COMMA_          =   KEYWORD(",", caseless=True)

# Define SQL CLAUSES
# Grammar for clauses will be defined below
sqlStmt         =   Forward()
selectColumn    =   Forward()
whereClause     =   Forward()
query           =   Forward()
createView      =   Forward()
setOp           =   Forward()

# Define column names, column renames, table names, table renames
ident           =   Word(alphas, alphanums + "_$").setName("identifier")
columnName      =   delimitedList(ident, ".", combine=True)
columnRename    =   delimitedList(ident, ".", combine=True)
tableName       =   delimitedList(ident, ".", combine=True)
tableRename     =   delimitedList(ident, ".", combine=True)
columnNameList  =   (delimitedList(columnName) + Optional(Suppress(AS) + columnRename))
columnRenameList=   Group(delimitedList(columnRename))
tableNameList   =   Group(delimitedList(tableName, ", ", combine=True))
tableRenameList =   Group(delimitedList(tableRename))

BINOP           =   oneOf("= != < > <> >= <= || eq ne lt le gt ge LIKE", caseless=True)
arithSign       =   Word("-=",exact=1)

E = CaselessLiteral("E")
realNum         =   Combine( Optional(arithSign) 
                    + ( Word( nums ) + "." + Optional( Word(nums) ) | ( "." + Word(nums) ) ) 
                    + Optional( E + Optional(arithSign) + Word(nums) ) 
                    )

intNum          =   Combine( Optional(arithSign) 
                    + Word( nums ) 
                    + Optional( E + Optional("+") + Word(nums) ) 
                    )

columnRval      =   (realNum | intNum | quotedString | columnName) # need to add support for alg expressions

#========= SELECT CLAUSE ===========

selectColumn    <<  ('*' | columnNameList | columnRval)



selectClause    =   ( Group(selectColumn) | Suppress("(") + Group(sqlStmt) + Suppress(")"))


# ========== FROM CLAUSE =========== 

# Grammar for JOINS
joins           =   (Literal(',') 
                    | Optional(NATURAL_ | INNER_ | CROSS_ | LEFT_ + OUTER_ | 
                        RIGHT_ + OUTER_ | FULL_ + OUTER_ | FULL_ | RIGHT_ | LEFT_ | OUTER_ ) 
                    + JOIN_
                    )

# tableBlock nested within joinBlock, includes renames
tableBlock      =   Group(tableName + Optional (Suppress(AS) + tableRename))

# <tableBlock> {JOIN} <tableBlock>
joinBlock       =   (joins 
                    + tableBlock 
                    + (Optional(ON + Group(columnName + BINOP + columnRval))
                        | Optional(USING + Group(columnName)))
                    )
# subquery
fromSub         =   Suppress("(") + Group(sqlStmt) + Suppress(")")

# FROM CLAUSE
fromClause      =   ((tableBlock +  ZeroOrMore(joinBlock)) 
                    | fromSub + Optional(tableRename | Suppress(AS) + tableRename)
                    )

# ========= WHERE CLAUSE ===========
whereCondition  =   Group(
                    ( columnName + BINOP + Optional(ANY_ | ALL_) + columnRval ) |
                    ( columnName + IN_ + Suppress("(") + delimitedList( columnRval ) + Suppress(")") ) |
                    ( columnName + IN_ + Suppress("(") + Group(sqlStmt) + Suppress(")") ) |
                    ( NOT_ + EXISTS_ + Suppress("(") + Group(sqlStmt) + Suppress(")")) | 
                    ( Suppress("(") + whereClause + Suppress(")") )
                    )

whereCompound   =   whereCondition + ZeroOrMore( (AND_ | OR_) + whereCondition)

whereClause     <<  Group(whereCompound + ZeroOrMore( (AND_ | OR_) + whereCompound))

#=========== SQL STATEMENT =========
# Define the grammar for SQL query.
sqlStmt         <<  ( Group(    SELECT + Optional(DISTINCT) + selectClause)
                    + Group(    FROM + Group(fromClause) ) 
                    + Optional( Group( WHERE + ( whereClause ).setResultsName("where")))
                    + Optional( Group( HAVING)) 
                    + Optional( Group( GROUP + BY ))
                    + Optional( Group( ORDER + BY  + columnNameList))
                    + Optional( Group(LIMIT + Group(columnRval)))
                    + Optional( Group(OFFSET + Group(columnRval)))
                    + Optional( Suppress(";"))
                    )

createView      <<  (CREATE + VIEW + AS 
                    + Group(Optional(Suppress("(")) 
                    + sqlStmt 
                    + Optional(Suppress(")")))
                    )

setOp           <<  ((Suppress("(") + Group(sqlStmt) + Suppress(")")) 
                    + (UNION_ | INTERSECT_ | EXCEPT_) 
                    + (Suppress("(") + Group(sqlStmt) + Suppress(")"))
                    )

query           <<  (sqlStmt | setOp | createView)

# ============= TESTING TRACES ===============

def test( string ):
    print (string,"->")
    try:
        tokens = query.parseString( string )
        print( "tokens = ",        tokens)
        print( "tokens.columns =", tokens.columns)
        print ("tokens.tables =",  tokens.tables)
        print ("tokens.where =", tokens.where) 
    except ParseException:
        print (" "*err.loc + "^\n" + err.msg)
        print (err)
    print('================\n')

def ast(string):
    return query.parseString(string)
