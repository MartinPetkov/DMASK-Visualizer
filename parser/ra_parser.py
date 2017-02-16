# All the functiosn for parsing and converting ra reside here

from parser.parsed_query import *
from parser.query_step import *
from parser.table import *


""" Split a string containing multiple RA queries into a list of single RA queries """
def split_ra_queries(ra_queries):
    # TODO: Implement
    pass

""" Convert a single RA query into an AST """
def ra_to_ast(query):
    # TODO: Implement
    pass

""" Convert a single RA AST into a list of QueryStep objects """
def ra_ast_to_steps(ast):
    # TODO: Implement
    pass
