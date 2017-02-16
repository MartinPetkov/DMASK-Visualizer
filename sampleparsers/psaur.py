import sqlparse
import sqlparse.sql
from sqlparse import lexer
from sqlparse import sql
from sqlparse.tokens import *



def printtree(l):
    
    
    if l == []:
        pass
    else:
        for item in l:
            if isinstance(item, list):
                printtree(item)
            else:
                print(item)




if __name__ == '__main__':

    s1 = 'select * from foo;'
    tree1 = sqlparse.parse(s1)[0]
    for items in tree1.tokens:
        print(items)

    s2 = 'select bar from foo where bar >= 85 and sid in (select sid from ant);'
    tree2 = sqlparse.parse(s2)[0]
    for items in tree2.tokens:
        print(items)

    print(tree2._pprint_tree())
    
    x = tree2.get_sublists()
    printtree(x)


    s3 = 'select * from foo; select * from bar;'
    tree3 = sqlparse.parse(s3)
    for items in tree3:
        print(items)

    s4 = 'select * from foo where something = "Rome";'
    tree4 = sqlparse.parse(s4)[0]
    for items in tree4.tokens:
        print(items)

    s5 = 'select min(bar), name from foo where cgpa >= 4 group by name;'
    tree5 = sqlparse.parse(s5)[0]
    for items in tree5.tokens:
        print(items)

    t1 = 'select * from foo;'
    stream = lexer.tokenize(s5)
    tokens = list(stream)
    for item in tokens:
        print(item)




