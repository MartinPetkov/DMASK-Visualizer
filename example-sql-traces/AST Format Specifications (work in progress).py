"""
READ:
<sql_query> = a symbol built based on rules defined elsewhere in the document
"SELECT"    = the literal word SELECT
'col_name'  = any string representing the column name
[<arg>]     = a list containing one example of <arg>
[<arg> ...] = a list containing any number of <arg>s

"""


<AST> = <sql_query>

<sql_query> = [ <sql_statement> ... ]

<sql_statement> = [ "SELECT", [ <select_arg> ... ] ]
                    |   [ "FROM", [ <from_arg> ... ] ]
                    |   [ "WHERE", [ <where_arg> ... ] ]

# For SELECT
<select_arg> = 'col_name'
                |   [ ('col_name' | <col_equation>), 'new_name' ]

<col_equation> = 'col_name' <operator> 'col_name'
<oprator> = "+" | "-" | "*" | "/"

# For FROM
<from_arg> = 'table_name'
                |   [ ('table_name' | <sql_query>), 'new_name' ]


# For WHERE
<where_arg> = []
