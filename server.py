# Run with python server.py

from http.server import HTTPServer, SimpleHTTPRequestHandler
from cmdmask import visualize_query

import urllib.request, urllib.parse, urllib.error

import pdb


conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

class DMASKHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        sql_query = post_data["sql_query"][0]
        print(sql_query)
        visualize_query(sql_query, conn_string)


PORT = 9001
Handler = DMASKHandler
httpd = HTTPServer(("127.0.0.1",PORT), Handler)

print("Serving on port: {}".format(PORT))
httpd.serve_forever()
