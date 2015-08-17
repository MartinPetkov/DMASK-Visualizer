# DMASK-Visualizer
A SQL visualizer, De-MASKing the code to show its internal workings. There are future plans for RA visualizion as well.

# Setup
1. Install psycopg2 (pip install psycopg2)
2. Install pyparsing (pip install pyparsing or easy install pyparsing)
3. Set up database (the test suite we used can be found in test-database-setup, from which you can call  \i schema.ddl \i sampledata.ddt)
4. (Optional) Put these into a relation/give them a search path (ex. set search_path to NAME) -- if you do this, you will need to provide a schema name
5. (Optional) Install CodeMirror (for the test page)  
5a. Go to the folder above the DMASK-Visualizer folder  
5b. Run this command: git clone https://github.com/codemirror/CodeMirror.git

# Importing as a Module  
Example of how to visualize a query:
```python
# Import all the required components from the module
from dmask import *

# Set the database connection parameters
conn_string = "host='localhost' dbname='postgres' user='postgres' password=''"

# Define the schema and search path
schema = {
    "Student":  ["sid", "firstName", "email", "cgpa"],
    "Course":   ["dept", "cNum", "name"],
    "Offering": ["oid" ,"dept", "cNum", "instructor"],
    "Took":     ["sid", "oid", "grade"]
}
search_path = ""

# Both can be omitted; they default to conn_string="" and schema={}, but queries will not visualize without them
dmask = DMASK(conn_string, schema)
dmask.set_connection(search_path)

# Both the schema and the search path can be set manually later on
dmask.set_schema(new_schema)
dmask.set_connection(new_search_path)

# Obtain the JSON results for the query to be visualize
json = dmask.sql_to_json(sql)

# Close the connection
dmask.connection.close()

# Send the JSON file to the frontend to visualize and save it as a variable called pq
# The file results.html should store that variable, then loading it will allow you to visualize the query
```

# Visualizing from the Command Line  
1. Run cmdmask.py
2. You’ll be prompted for connection information (localhost, dbname, etc.) in order to connect
3. Submit queries; if successful, the results will open in a new tab in your default browser (or in the default .html file handling program)

# Visualizing from the Sample Webpage  
1. Open the file query_test_page.html in your default browser
2. Open a shell and run
3. python query_server.py
4. Submit queries in the web page; if successful, the results will open in a new tab in your default browser (or in the default .html file handling program)

# Samples
The front-end-code/samples folder contains sample files with completed queries, to test out just the visualizer component.
