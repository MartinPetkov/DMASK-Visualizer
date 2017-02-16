# Run with python server.py

from http.server import HTTPServer, SimpleHTTPRequestHandler
from cmdmask import visualize_query

import urllib.request, urllib.parse, urllib.error

import pdb


# Defaults
conn_string = "host='localhost' dbname='bge' user='bge' password=''"
schema = {
    "Student":  ["sid", "firstName", "email", "cgpa"],
    "Course":   ["dept", "cNum", "name"],
    "Offering": ["oid" ,"dept", "cNum", "instructor"],
    "Took":     ["sid", "oid", "grade"]
}
to_search = ""

class DMASKHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(content_length).decode('utf-8'))
        sql_query = post_data["sql_query"][0]

        print("Query received:")
        print(sql_query)
        visualize_query(sql_query, conn_string, schema, to_search)


PORT = 9001
httpd = HTTPServer(("127.0.0.1",PORT), DMASKHandler)

print("Serving on port: {}".format(PORT))
httpd.serve_forever()
