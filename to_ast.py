from pyparsing import (ParseResults, Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional,
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, commaSeparatedList,
    opAssoc, operatorPrecedence, ZeroOrMore, restOfLine, Keyword as KEYWORD, Suppress, nestedExpr, Empty, replaceWith)

# ============== Define SQL KEYWORDS ========================
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
ASC_             =  KEYWORD("ASC", caseless=True)
DESC_            =  KEYWORD("DESC", caseless=True)
USING           =   KEYWORD("USING", caseless=True)
LIMIT           =   KEYWORD("LIMIT", caseless=True)
OFFSET          =   KEYWORD("OFFSET", caseless=True)
AND_            =   KEYWORD("AND", caseless=True)
OR_             =   KEYWORD("OR", caseless=True)
IS_             =   KEYWORD("IS", caseless=True)
IN_             =   KEYWORD("IN", caseless=True)
EXISTS_         =   KEYWORD("EXISTS", caseless=True)
NOT_            =   KEYWORD("NOT", caseless=True)
ANY_            =   KEYWORD("ANY", caseless=True)
SOME_           =   KEYWORD("SOME", caseless=True)
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
                    CREATE | VIEW | AS | DISTINCT | ON | ASC_ | DESC_ | USING | 
                    LIMIT | OFFSET | AND_ | OR_ | IS_ | IN_ | EXISTS_ | NOT_ | 
                    ANY_ | SOME_ | ALL_ | UNION_ | INTERSECT_ | EXCEPT_ | DISTINCT_ | 
                    JOIN_ | NATURAL_ | CROSS_ | INNER_ | OUTER_ | LEFT_ | RIGHT_ | FULL_ |
                    NULL_ | ISNULL_ | NOTNULL_ | BETWEEN_)

# ================= Define SQL CLAUSES =======================
# Grammar for clauses will be defined below. 
# The following statements can be recursively defined.

sqlStmt         =   Forward()
subquery        =   Forward()
query           =   Forward()
createView      =   Forward()
setOp           =   Forward()
whereClause     =   Forward()
whereCondition  =   Forward()

# =========== PRECEDENCE FUNCTION ============

def precedence(num):
    if num is None:
        initlen = 2
        incr = 1
    else:
        initlen = {0:1, 1:2, 2:3, 3:5}[num]
        incr = {0:1, 1:1, 2:2, 3:4}[num]

    def pa(s, l, t):
        t = t[0]
        if len(t) > initlen:
            ret = ParseResults(t[:initlen])
            i = initlen
            while i < len(t):
                ret = ParseResults([ret] + t[i:i+incr])
                i+= incr
            return ParseResults(ret)
    return pa

# ========== Define column values/operations ================

# Binary operators
BINOP           =   oneOf("= != < > <> >= <= || eq ne lt le gt ge LIKE", caseless=True)

# Column operators
COLOPS          =   (oneOf("+ - * / % // DIV || ==",caseless=True) | BINOP)

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

posParam        =   Combine('$' + (realNum | intNum))

space           =   Empty().addParseAction(replaceWith(''))

# ============= Define Tokens ===============================
ident           =   (~KEYWORDS 
                    + (Word(alphas, alphanums + "_$")
                        | realNum
                        | intNum)
                    )


token           =   delimitedList(ident, ".", combine=True)


# Aggregate functions
aggregatefns    =   (Combine(Word(alphas) + ("(") + token + (")")))

# Possible column values
columnRval      =   (realNum | intNum | quotedString | posParam | aggregatefns | token)

tokenObs        =   Group(
                    (Group(columnRval + (COLOPS) + columnRval) | columnRval)
                    + Optional((COLOPS) + columnRval)
                    + Optional(AS) + Optional(token)
                    | (subquery + Optional(AS) + Optional(token))
                    )

tokenList       =   delimitedList(tokenObs)


#========= SELECT CLAUSE ===========

# Possible attributes to SELECT over
selectColumn    =   ('*' | tokenList | columnRval)

# SELECT CLAUSE
selectClause    =   Group(selectColumn)

selectCalculator=   Group(SELECT + 
                    (Group( 
                        Group((intNum | realNum) + COLOPS + (intNum | realNum) 
                            + Optional(AS) + Optional(token)))))

# ========== FROM CLAUSE =========== 

# Grammar for JOINS
joins           =   (Literal(',')
                    | JOIN_
                    | Combine(( NATURAL_ 
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
tableBlock      =   (Group((token | subquery) 
                    + Optional((AS | space) + token)
                    ))

tableOnBlock    =   Group(tableBlock 
                    + (Optional(ON + Group(token + BINOP + columnRval))
                    | Optional(USING + Group(token))
                    ))

fromClause      =   (tableOnBlock + ZeroOrMore(joins + tableOnBlock))

# ========= WHERE CLAUSE ===========

whereCondition  <<   Group(
                    # Optional(Suppress("(")) + 
                    (
                        (token + BINOP + ( 
                            columnRval 
                            | (Optional(ANY_ | SOME_ | ALL_) + subquery)))
                        | (token + IN_ + (
                            (Suppress("(") + delimitedList(columnRval) + Suppress(")"))
                            | subquery))
                        | (EXISTS_ + subquery)
                        | (token + Combine(IS_ + Suppress(" ") + (NULL_ | NOTNULL_)))
                        | (token + (ISNULL_ | NOTNULL_))
                        | (token + Optional(NOT_) + BETWEEN_ + columnRval + AND_ + columnRval)
                    )
                    # + Optional(Suppress(")"))
                    )

whereNested     =  nestedExpr("(", ")", whereCondition)

whereClause     <<  (whereNested | operatorPrecedence(
                        whereNested | whereCondition,
                        [   ( (AND_ | OR_), 2, opAssoc.LEFT, precedence(2)), 
                            ( (NOT_, 1, opAssoc.RIGHT, precedence(1)))
                        ]
                    ))

#==========HAVING CLAUSE ===========
havingCondition = Group(
                    #Optional(Suppress("("))
                    (
                        (aggregatefns + BINOP + (((ANY_ | SOME_ | ALL_) + subquery) | columnRval))
                        | (aggregatefns + IN_ + Suppress("(") + delimitedList(columnRval) + Suppress(")"))
                        | (aggregatefns + IN_ + subquery)
                        | (aggregatefns + Combine(IS_ + Suppress(" ") + (NULL_ | NOTNULL_)))
                        | (aggregatefns + (ISNULL_ | NOTNULL_))
                        | (aggregatefns + Optional(NOT_) + BETWEEN_ + columnRval + AND_ + columnRval)
                    )
                    #+ Optional(Suppress(")"))
                    )

havingNested    = nestedExpr("(", ")", havingCondition)

havingClause    =   (havingNested | operatorPrecedence(
                        havingNested | havingCondition,
                        [   ( (AND_ | OR_), 2, opAssoc.LEFT, precedence(2)), 
                            ( (NOT_, 1, opAssoc.RIGHT, precedence(1)))
                        ]
                    ))

#=========== SQL STATEMENT =========
# Define the grammar for SQL query.
sqlStmt         <<  ( Group(    SELECT + Optional(DISTINCT) + selectClause)
                    + Group(    FROM + Group(fromClause) ) 
                    + Optional( Group( WHERE + Group( whereClause )))
                    + Optional( Group( Combine( GROUP + " " + BY) + (tokenList)))
                    + Optional( Group( HAVING + Group(havingClause)))
                    + Optional( Group( Combine( ORDER + " " + BY) + (tokenList) + Optional(ASC_ | DESC_) ))
                    + Optional( Group( LIMIT + Group(columnRval)))
                    + Optional( Group( OFFSET + Group(columnRval)))
                    )


subquery        <<   Suppress("(") + Group(sqlStmt) + Suppress(")")

createView      <<  (Combine( CREATE + " " + VIEW) 
                    + token 
                    + Optional(AS) 
                    + subquery
                    )

setOp           <<  (operatorPrecedence(
                        (subquery),
                        [( (UNION_ | INTERSECT_ | EXCEPT_) + Optional(ALL_), 2, opAssoc.LEFT, )]
                    )   + Optional(Group (Combine (ORDER + " " + BY) + tokenList))
                        + Optional(Group(LIMIT + Group(columnRval )))
                        + Optional(Group(OFFSET + Group(columnRval)))
                    )

query           <<  (selectCalculator | sqlStmt | setOp | createView) + Optional(Suppress(";"))

# ============= TESTING TRACES ===============

def ast(string):
    return query.parseString(string)
