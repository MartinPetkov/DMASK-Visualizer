from rapt import Rapt
from rapt.treebrd.schema import Schema
from rapt.treebrd.node import *
from rapt.treebrd.utility import *

if __name__ == '__main__':


    raptor = Rapt()
    s = '\\project_{Name}(Countries);'
    schema = {'Countries': ['Name', 'Capital'], 'Universities': ['Name', 'Dean']}

    print(raptor.to_sql(s, schema))
    print(raptor.to_sql_sequence(s, schema))
    print(raptor.to_qtree(s, schema))

    x = raptor.to_syntax_tree(s, schema)
    for item in x:
        print(item.operator)
        print(item.name)
        print(item.attributes)


    s2 = '(\\project_{Name}(Countries))\\union(\\project_{Name}(Universities));'
    s3 = '\\project_{Name}(\\select_{Capital="Rome"}(Countries));'
    #print('s2');
    #print(raptor.to_qtree(s2, schema))
    #print(raptor.to_qtree(s3, schema))

    print(raptor.to_sql(s3, schema))
    y = raptor.to_syntax_tree(s3, schema)

    while (isinstance(y, list)):
        for item in y:
            if (isinstance(item, Node)):
                print(item.post_order())
                y = item.post_order()
        
    print(flatten(y))

'''
    for item in tree:
        print(item.operator)
        print(item.name)
        print(item.attributes)
        if (isinstance(item, SelectNode)):
            print(item.condtions)

'''

