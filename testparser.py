from sql_parser import *
from to_ast import ast

def printout(l):

	if l:
		for step in l:
			print(step.step_number)
			print(step.input_tables)
			print(step.result_table)
			print(step.sql_chunk)
			print(step.executable_sql)
			print('==============\n')
	else:
		print(l)


if __name__ == "__main__":


	# ======== TESTING PARSE_WHERE AND PARSE_GROUP_BY ==========
	a = ast('select sid from Took')
	x = ast('select sid from Student where sid = 0')
	y = ast('select sid from Student where (sid = 0 and firstName like \'Kathy\');')
	z = ast('select sid from Student where sid in (select sid from Took)')

	astep = parse_sql_query(a, '1')
	xstep = parse_sql_query(x, '2')
	ystep = parse_sql_query(y, '1')
	zstep = parse_sql_query(z, '1')

	printout(astep)
	printout(xstep)
	printout(ystep)
	printout(zstep)

	g1 = ast('select sid, max(sid) from Took group by sid')
	g2 = ast('select sid from Took where sid > 10 group by sid')

	g1step = parse_sql_query(g1, '1')
	g2step = parse_sql_query(g2, '1')
	g3step = parse_sql_query(x, '1')

	printout(g1step)
	printout(g2step)
	printout(g3step)

	
	# ========= TESTING SELECT AND DISTINCT =================
	a = ast('select distinct name, max(sid), grade from Took where sid in (select sid from Took)')
	asteps = parse_select(a, '1')
	bsteps = parse_distinct(a, '1')
	printout(asteps)
	printout(bsteps)


	a = ast('select distinct name, max(sid), (select max(grade) from Took) themax from Took where exists (select sid from Took) group by name having max(sid) > 0')
	where = parse_where(a, '1')
	groupby = parse_group_by(a, '1')
	having = parse_having(a, '1')
	select = parse_select(a, '1')
	distinct = parse_distinct(a, '1')

	printout(where)
	printout(groupby)
	printout(having)
	printout(select)
	printout(distinct)	

	x = ast('select distinct sid, max(grade) from Student where sid = 0 group by sid having max(grade) > 40 order by firstname limit 5;')
	z = parse_sql_query(x)
	printout(z)

	a = ast('(select sid from Student) union (select sid from Took) order by firstName')
	print(a)

	b = ast('(select sid from Student) INTERSECT (select sid from Took)')
	d = parse_union(b[0], '1', '1')

	printout(d)

	c =  ast('create view name (select * from Took)')
	e = parse_create_view(c, '1')
	printout(e)
	

