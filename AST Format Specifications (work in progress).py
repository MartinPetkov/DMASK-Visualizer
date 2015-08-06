"""
LEGEND:
    <sql_query> = symbol built based on rules defined elsewhere in the document
    "SELECT"    = the literal word SELECT
    'col_name'  = any string representing the column name
    [<arg>]     = a list containing one example of <arg>
    [<arg> ...] = a list containing any number of <arg>s
    (<elem>?)   = optional element
    (<elem>)+   = 1 or more of this element
    (<elem>)*   = 0 or more of this element
"""

<AST>               = <sql_query> | <create_view> | [ <sql_query> (<set_operation> <sql_query>)+ ]

<set_operation>     = "UNION" | "INTERSECT" | "EXCEPT"

<sql_query>         = [ <sql_statement> ... ]

<sql_statement>     =       [ "SELECT",     [ <select_arg> ... ]],
                            [ "FROM",       [ <from_arg>, (<from_connector>, <from_arg>?) ... ] ],
                            ([ "WHERE",     [ <where_arg> (<where_connector>, <where_arg>?) ... ] ])?,
                            ([ "GROUP BY",  [ 'col_name' ... ] ])?,
                            ([ "HAVING",    [ <aggregate_fn>, <comparator>, <val> ]])?,
                            ([ "ORDER BY",  [ 'col_name' ... ] ])?,
                            ([ "LIMIT",     [ <numeric>] ] )?,
                            ([ "OFFSET",    [ <numeric>] ] )?

<create_view>       = [ "CREATE VIEW", 'view_name', ("AS"?), <sql_query> ]


# For SELECT
<select_arg>        = ['col_name']
                        |   [ ('col_name'
                            | <col_equation>
                            | <aggregate_fn>
                            | <val> ), <as>, 'new_name']


<col_equation>      = ['col_name', (<operator>, 'col_name')+ ]

<aggregate_fn>      = function('col_name')

<operator>          = "+" | "-" | "*" | "/" | "||"

<as>                = " " | "AS"


# For FROM
<from_arg>          = ['table_name']
                        |   [ ('table_name' | <sql_query>), <as>, 'new_name']
                        |   [ ['table_name' (, <as>, 'new_name')?], 'ON', <reason> ]

<from_connector>    = ","
                        | ("NATURAL"
                            | "INNER"
                            | ("LEFT" | "RIGHT" | "FULL")? "OUTER"
                            | "CROSS"
                            | "LEFT"
                            | "RIGHT"
                            | "FULL"
                        )? "JOIN"


# For WHERE
<where_arg>         = [("NOT", ?) <reason> ] | [<where_arg>]

<where_connector>   = "AND" | "OR"

<reason>            = ['col_name', <comparator>, <val>
                        | 'col_name', "IN", <val>
                        | 'col_name', ("IN" | (<comparator>, ("ANY" | "ALL"))), <sql_query>
                        | "EXISTS", <sql_query>
                        | 'col_name', (("IS", ("NULL" | "NOTNULL")) | "ISNULL")
                        | 'col_name', ("NOT"),? "BETWEEN", <val>, "AND", <val>
                       ]


<as>                = " " | "AS"

<comparator>        = "=" | "<>" | "!=" | ">" | ">=" | "<" | "<="

<numeric>           = /^[1-9][0-9]*$/

<val>               = <numeric> | 'quoted string'



