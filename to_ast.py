from pyparsing import (Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional,
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString,
    opAssoc, operatorPrecedence, ZeroOrMore, restOfLine, Keyword as KEYWORD, Suppress)

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
IS_             =   KEYWORD("IS", caseless=True)
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
NULL_           =   KEYWORD("NULL", caseless=True)
ISNULL_         =   KEYWORD("ISNULL", caseless=True)
NOTNULL_        =   KEYWORD("NOTNULL", caseless=True)
BETWEEN_        =   KEYWORD("BETWEEN", caseless=True)

KEYWORDS        = ( SELECT | FROM | WHERE | GROUP | BY | HAVING | ORDER | 
                    CREATE | VIEW | AS | DISTINCT | ON | ASC | DESC | USING | 
                    LIMIT | OFFSET | AND_ | OR_ | IS_ | IN_ | EXISTS_ | NOT_ | 
                    ANY_ | ALL_ | UNION_ | INTERSECT_ | EXCEPT_ | DISTINCT_ | 
                    JOIN_ | NATURAL_ | CROSS_ | INNER_ | OUTER_ | LEFT_ | RIGHT_ | FULL_ |
                    NULL_ | ISNULL_ | NOTNULL_ | BETWEEN_)

# Define SQL CLAUSES
# Grammar for clauses will be defined below
sqlStmt         =   Forward()
whereCompound   =   Forward()
whereClause     =   Forward()
query           =   Forward()
createView      =   Forward()
setOp           =   Forward()

# Define view names, column names, column renames, table names, table renames
ident           =   ~KEYWORDS + Word(alphas, alphanums + "_$")
viewName        =   delimitedList(ident, ".", combine=True)
columnName      =   delimitedList(ident, ".", combine=True)
columnRename    =   delimitedList(ident, ".", combine=True)
tableName       =   delimitedList(ident, ".", combine=True)
tableRename     =   delimitedList(ident, ".", combine=True)
columnNameList  =   (delimitedList(columnName) 
                    + Optional((Suppress(AS) + columnRename) |('||' + columnRename) | columnRename)
                    )
columnRenameList=   Group(delimitedList(columnRename))
tableNameList   =   Group(delimitedList(tableName, ", ", combine=True))
tableRenameList =   Group(delimitedList(tableRename))

# Define column values/operations
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

subquery        =   Suppress("(") + Group(sqlStmt) + Suppress(")")
'''
UNARY, BINARY, TERNARY = 1, 2, 3
operators       =   operatorPrecedence(
                    [
                    (oneOf ('+ -'), UNARY, opAssoc.RIGHT), 
                    (oneOf('^ ||'), opAssoc.LEFT), 
                    (oneOf('* / %'), BINARY, opAssoc.LEFT), 
                    (oneOf('+ -'), BINARY, opAssoc.LEFT),
                    (oneOf('<< >> & |'), BINARY, opAssoc.LEFT),
                    (oneOf('< <= > >= lt le gt ge'), BINARY, opAssoc.LEFT),
                    (oneOf('= == != <> eq ne') | IS_ | IN_ | LIKE_, BINARY, opAssoc.LEFT),
                    ('||', BINARY, opAssoc.LEFT),
                    ((BETWEEN, AND), TERNARY, opAssoc.LEFT),   
                    ]) 
'''
#========= SELECT CLAUSE ===========

# Aggregate functions
aggregatefns    =   Combine(Word(alphas) + ("(") + columnName + (")"))

# Concatenated columns
concatcolumn    =   Group (columnName + '||' + columnName)

# Possible column values
columnRval      =   (realNum | intNum | quotedString | columnName)

# Possible attributes to SELECT over
selectColumn    =   ('*' | aggregatefns |  columnNameList | columnRval)

# SELECT CLAUSE
selectClause    =   ( Group(selectColumn) | subquery)


# ========== FROM CLAUSE =========== 

# Grammar for JOINS
joins           =   (Literal(',')
                    | JOIN_
                    | Combine(Optional( NATURAL_ 
                        | INNER_ 
                        | CROSS_ 
                        | Combine(LEFT_ + " " + OUTER_) 
                        | Combine(RIGHT_ + " " + OUTER_)
                        | Combine(FULL_ + " " + OUTER_)
                        | FULL_ 
                        | RIGHT_ 
                        | LEFT_ 
                        | OUTER_ ) + " "
                    + JOIN_)
                    )

# tableBlock nested within joinBlock, includes renames
tableBlock      =   Group(tableName 
                    + Optional ((Suppress(AS) + tableRename) | tableRename)
                    )

# <tableBlock> {JOIN} <tableBlock>
joinBlock       =   (joins 
                    + tableBlock 
                    + (Optional(ON + Group(columnName + BINOP + columnRval))
                        | Optional(USING + Group(columnName)))
                    )
# FROM CLAUSE
fromClause      =   ((tableBlock +  ZeroOrMore(joinBlock)) 
                    | subquery + Optional(tableRename | Suppress(AS) + tableRename)
                    )

# ========= WHERE CLAUSE ===========
whereCondition  =   Group(
                    Optional(Suppress("(")) 
                    + (
                        (columnName + BINOP + Optional(ANY_ | ALL_) + columnRval)
                        | (columnName + IN_ + Suppress("(") + delimitedList(columnRval) + Suppress(")"))
                        | (columnName + (IN_ | BINOP + (ANY_ | ALL_)) + subquery )
                        | ( EXISTS_ + subquery)
                        | (columnName + Combine(IS_ + Suppress(" ") + (NULL_ | NOTNULL_))) 
                        | (columnName + (ISNULL_ | NOTNULL_))
                        | (columnName + Optional(NOT_) + BETWEEN_ + columnRval + AND_ + columnRval)
                    ) 
                    + Optional(Suppress(")"))
                    )


whereClause     <<  (operatorPrecedence(
                        Group(whereCondition),
                        [   ( (AND_ | OR_), 2, opAssoc.LEFT), 
                            ( (NOT_, 1, opAssoc.LEFT))
                        ]
                    ))



#whereCompound   =   whereCondition + ZeroOrMore( (AND_ | OR_) + whereCondition)

#whereClause     <<  Group(whereCompound + ZeroOrMore( (AND_ | OR_) + whereCompound))

#==========HAVING CLAUSE ===========
havingClause    =   Group(aggregatefns + BINOP + columnRval)

#=========== SQL STATEMENT =========
# Define the grammar for SQL query.
sqlStmt         <<  ( Group(    SELECT + Optional(DISTINCT) + selectClause)
                    + Group(    FROM + Group(fromClause) ) 
                    + Optional( Group( WHERE + ( whereClause )))
                    + Optional( Group( Combine( GROUP + " " + BY) + Group(columnNameList)))
                    + Optional( Group( HAVING + havingClause))
                    + Optional( Group( Combine(ORDER + " " + BY) + Group(columnNameList)))
                    + Optional( Group(LIMIT + Group(columnRval)))
                    + Optional( Group(OFFSET + Group(columnRval)))
                    + Optional( Suppress(";"))
                    )

createView      <<  (Combine( CREATE + " " + VIEW) 
                    + viewName 
                    + Suppress(AS) 
                    + subquery
                    )

setOp           <<  ((subquery) 
                    + (UNION_ | INTERSECT_ | EXCEPT_) 
                    + (subquery)
                    )

query           <<  (sqlStmt | setOp | createView)

# ============= TESTING TRACES ===============

def ast(string):
    return query.parseString(string)
