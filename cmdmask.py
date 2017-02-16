from parser.dmask import *

import webbrowser
import os

def visualize_query(sql, conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'",
                    schema = {"Student" : ["sid", "firstName", "email", "cgpa"],
                              "Course": ["dept", "cNum", "name"],
                              "Offering": ["oid" ,"dept", "cNum", "instructor"],
                              "Took": ["sid", "oid", "grade"]
                             },
                    to_search = "sophiadmask"):
    schema = schema.copy()
    for key in schema:
        schema[key] = schema[key][:]
    dmask = DMASK(conn_string, schema)
    dmask.set_connection(to_search)

    # get_namespace works
    json = ""
    try:
        json = dmask.sql_to_json(sql)
    except Exception as e:
        print("Exception encountered: ")
        print(e)
        dmask.connection.close()
        return

    # nothing gets commited -- closing the connection will prevent hanging
    dmask.connection.close()

    import os
    f = open("front-end-code/template.html")
    copy = f.readlines()
    for i in range(len(copy)):
        if copy[i].strip() == "<!-- INSERT TEST BELOW -->":
            copy[i] = "<script>var pq = " + str(json) +";</script>"

    # MODIFY THIS PATH -- Need to get the current directory to append front-end-code/results.html
    url = "/front-end-code/results.html"
    output = open(os.getcwd() + url, "w")
    for line in copy:
        output.write(line)
    f.close()
    output.close()

    # Redirect standard error to avoid annoying messages in the console
    savout = os.dup(1)
    os.close(1)
    saverr = os.dup(2)
    os.close(2)
    os.open(os.devnull, os.O_RDWR)
    try:
        webbrowser.open("file://" + os.getcwd() + url)
    finally:
        os.dup2(savout, 1)
        os.dup2(saverr, 2)


if __name__ == '__main__':
    sql = "test"
    "host='localhost' dbname='postgres' user='postgres' password='password'"
    host = input("Enter host name (localhost by default): ")
    if not host:
        host = "localhost"

    dbname = input("Enter database name (postgres by default): ")
    if not dbname:
        dbname = "postgres"

    user = input("Enter username (postgres by default): ")
    if not user:
        user = "postgres"

    password = input("Enter password (empty by default): ")

    conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, user, password)

    to_search = input("Enter search path (empty by default): ")

    i = "temp"
    schema = {}
    if (input("Setting up schema. Press d to use default, any other key to specify your own: ").lower() != "d"):
        while (i):
            i = input("Enter table name or empty to quit: ")
            if (i):
                j = "temp"
                columns = []
                while (j):
                    j = input("Enter column name or empty to enter another table: ")
                    if (j):
                        columns.append(j)
                schema[i] = columns

    else:
        schema = {"Student" : ["sid", "firstName", "email", "cgpa"],
                              "Course": ["dept", "cNum", "name"],
                              "Offering": ["oid" ,"dept", "cNum", "instructor"],
                              "Took": ["sid", "oid", "grade"]
                             }


    while (sql):
        sql = input("Enter query (empty to exit): ")
        if (sql):
            visualize_query(sql, conn_string = conn_string, schema = schema, to_search = to_search)
