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
	'''
	
	# ======== TESTING PARSE_WHERE AND PARSE_GROUP_BY ==========
	a = ast('select sid from Took')
	x = ast('select sid from Student where sid = 0')
	y = ast('select sid from Student where (sid = 0 and firstName like \'Kathy\');')
	z = ast('select sid from Student where sid in (select sid from Took)')
	print(x)
	astep = parse_sql_query(a)
	xstep = parse_sql_query(x)
	ystep = parse_sql_query(y)
	zstep = parse_sql_query(z)

	printout(astep)
	printout(xstep)
	printout(ystep)
	printout(zstep)

	g1 = ast('select sid, max(sid) from Took group by sid')
	g2 = ast('select sid from Took where sid > 10 group by sid')

	g1step = parse_sql_query(g1)
	g2step = parse_sql_query(g2)

	printout(g1step)
	printout(g2step)
	
	
	# ========= TESTING SELECT AND DISTINCT =================
	z = ast('select sid from Student where sid in (select sid from Took)')
	zstep = parse_sql_query(z)
	printout(zstep)
	a = ast('select distinct name, max(sid), grade from Took where sid in (select sid from Took)')
	asteps = parse_sql_query(a)
	printout(asteps)



	a = ast('select distinct name, max(sid), (select max(grade) from Took) themax from Took where exists (select sid from Took) group by name having max(sid) > 0')
	asteps = sql_ast_to_steps(a)
	printout(asteps)


	x = ast('select distinct sid, max(grade) from Student where sid = 0 group by sid having max(grade) > 40 order by firstname limit 5;')
	z = sql_ast_to_steps(x)
	printout(z)
	
	a = ast('(select sid from Student) union (select sid from Took) order by firstName')
	b = sql_ast_to_steps(a)
	printout(b)

	w = ast('select sid from (select sid from Took) T')
	wsteps = sql_ast_to_steps(w)
	printout(wsteps)

	
	b = ast('(select sid from Student) INTERSECT (select sid from Took)')
	d = sql_ast_to_steps(b)

	printout(d)
	'''

	c =  ast('create view name (select * from Took)')
	print(c)
	e = sql_ast_to_steps(c)
	printout(e)
	

