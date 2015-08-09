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
			print(step.namespace)
			print('==============\n')
	else:
		print(l)



if __name__ == "__main__":

	schema = {
		'Student': ['sid', 'firstName', 'email', 'cgpa'],
		'Course': ['dept', 'cNum', 'name'],
		'Offering': ['oid', 'dept', 'cNum', 'instructor'],
		'Took': ['sid', 'ofid', 'grade']
	}

	star = ast('select * from Took')
	a = ast('select dept || cnum from Student where cgpa > 3')
	b = ast('select Student.sid, Student.email, Took.grade from Student, Took')
	c = ast('select sid, email from Student Natural join Took natural join Course')
	d = ast('select sid, grade, instructor from Took left join Offering on took.ofid = Offering.oid')
	e = ast('select oid from (select oid, dept from Offering) as H')
	f = ast('select email, cgpa from Student where cgpa > 3 and firstname = \'Martin\'')
	g = ast('select email, cgpa from Student where cgpa > 3 and (firstname=\'Martin\' or firstname=\'Kathy\'')
	h = ast('select t.sid, o.oid from Took t, Offering o')
	i = ast('select sid, firstName from Student where cgpa > (select cgpa from Student where sid=4')
	j = ast('select instructor from Offering o1 where exists (select o2.oid from Offering o2 where o2.oid <> o1.oid')
	k = ast('create view pizza as (Select sid, email, cgpa from Student where cgpa < 3)')
	l = ast('select sid, dept || cnum as course, grade from Took, (select * from Offering where instructor="Horton") H where Took.ofid = H.oid')
	m = ast('select sid from Student where gpa > any (select gpa from Student natural join Took where grade > 100')
	n = ast('select sid, dept || cnum as course, grade from Took natural join Offering where grade >= 80 and dept in (select dept from Took natural join Offering natural join Student where surname = "Lakemeyer")')
	o = ast('select instructor from Offering Off1 where not exists (select * from Offering where oid <> Off1.oid and instructor = Off1.instructor)')
	p = ast('(select sid from Student) union (select sid from Took) order by firstName')
	q = ast('select distinct sid, dept || cnum as course, count(grade), (select max(sid) from Took) maxsid from Took, Offering where sid > 0 group by sid having count(grade) > 0 order by sid limit 5')

	x = sql_ast_to_steps(l, schema)
	printout(x)
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

	b = ast('((select sid from Student) union (select sid from Took)) union (select sid from Offering)')
	bsteps = sql_ast_to_steps(b)
	printout(bsteps)
	

	
	w = ast('select sid from (select sid from Took) T')
	wsteps = sql_ast_to_steps(w)
	printout(wsteps)
	
	
	b = ast('(select sid from Student) INTERSECT (select sid from Took)')
	d = sql_ast_to_steps(b)

	printout(d)

	c =  ast('create view name (select * from Took)')
	print(c)
	e = sql_ast_to_steps(c)
	printout(e)
	'''

