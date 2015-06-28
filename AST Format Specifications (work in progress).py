"""
LEGEND:
<sql_query> = a symbol built based on rules defined elsewhere in the document
"SELECT"    = the literal word SELECT
'col_name'  = any string representing the column name
[<arg>]     = a list containing one example of <arg>
[<arg> ...] = a list containing any number of <arg>s
(<elem>?)   = optional element

"""


<AST>               = <sql_query> | <create_view>

<sql_query>         = [ <sql_statement> ... ]

<sql_statement>     = [ "SELECT", [ <select_arg> ... ] ]
                        |   [ "FROM", [ <from_arg> (<from_connector>?) ... ] ]
                        |   [ "WHERE", [ <where_arg> (<where_connector>?) ... ] ]

<create_view>       = [ "CREATE VIEW", 'view_name', <sql_query> ]

# For SELECT
<select_arg>        = 'col_name'
                        |   [ ('col_name' | <col_equation>), 'new_name' ]

<col_equation>      = 'col_name' <operator> 'col_name'
<oprator>           = "+" | "-" | "*" | "/"


# For FROM
<from_arg>          = 'table_name'
                        |   [ ('table_name' | <sql_query>), 'new_name' ]
                        |   [ 'table_name', <reason> ]
<from_connector>    = ",", "NATURAL JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN"


# For WHERE
<where_arg>         = <reason>
                        | [<where_arg>]
<where_connector>   = "AND" | "OR"
<reason>            = [("NOT",?) "EXISTS", <sql_query>]
                        |   [("NOT",?) 'col_name', "IN", <sql_query>]
                        |   [("NOT",?) 'col1_name', <comparator>, ('col2_name' | <sql_query>)]
<comparator>        = "=" | "<>" | "!=" | ">" | ">=" | "<" | "<="
