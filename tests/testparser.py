from parser.sql_parser import *
from parser.to_ast import ast

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
	c = ast('select sid from Student Natural join Took natural join Student S')
	d = ast('select sid, grade, instructor from Took left join Offering on took.ofid = Offering.oid')
	e = ast('select sid, oid from Took, (select oid, dept, sid from Offering, Student) as H')
	e2 = ast('select oid from (select oid, dept from Offering) as H')
	f = ast('select email, cgpa from Student where cgpa > 3 and firstname = \'Martin\'')
	g = ast('select email, cgpa from Student where cgpa > 3 and (firstname=\'Martin\' or firstname=\'Kathy\') group by sid having max(sid) > 3')
	h = ast('select t.sid, o.oid from Took t, Offering o')
	i = ast('select sid, firstName from Student where cgpa > (select cgpa from Student where sid=4')
	j = ast('select instructor from Offering o1 where exists (select o2.oid from Offering o2 where o2.oid <> o1.oid')
	k = ast('create view pizza as (Select sid, email, cgpa from Student where cgpa < 3)')
	l = ast('select sid, dept || cnum as course, grade from Took, (select * from Offering where instructor="Horton") H where Took.ofid = H.oid')
	m = ast('select sid from Student where gpa > any (select gpa from Student natural join Took where grade > 100')
	n = ast('select sid, dept || cnum as course, grade from Took natural join Offering where grade >= 80 and dept in (select dept from Took natural join Offering natural join Student where surname = "Lakemeyer")')
	o = ast('select instructor from Offering Off1 where not exists (select * from Offering where oid <> Off1.oid and instructor = Off1.instructor)')
	p = ast('(select sid from Student) union (select sid from Took) order by firstName')
	p2 = ast('((select sid from Student) union (select sid from Took)) union (select sid from Student)')
	p3 = ast('(select sid from Student) union (select sid from Student) union (select sid from Took)')
	p4 = ast('(select sid from Student) union ((select sid from Took) union (select sid from Student))')
	q = ast('select distinct sid, dept || cnum as course, count(grade), (select max(sid) from Took) maxsid from Took, Offering where sid > 0 group by sid having count(grade) > 0 order by sid limit 5')
	r = ast('select sid from Student where (cgpa > 3) and (grade > 0 or grade < 40) ')
	s = ast('select * from (select * from took) t, took')

	x = sql_ast_to_steps(s, schema)
	printout(x)
