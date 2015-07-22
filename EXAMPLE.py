i''' A query with a cross product in it '''
def generate_simple_cross_product_query():
    query_text =\
    ' SELECT Student.sid, Student.email, Took.grade' +\
    ' FROM Student, Took'

    steps = [
        QueryStep('1', 'FROM Student, Took', ['1.3'], '1', 'SELECT * FROM Student, Took',
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade"]),
        QueryStep('1.1', 'Student', [], '1.1', 'SELECT * FROM Student',
            namespace=[ "Student: sid, firstName, email, cgpa"]),
        QueryStep('1.2', 'Took', [], '1.2', 'SELECT * FROM Took',
            namespace=[ "Took: sid, ofid, grade"])
        QueryStep('1.3', 'Student, Took', [1.1, 1.2], 1.3, 'SELECT * FROM Student, Took',
            namespace=[ "Student: sid, firstName, email, cgpa",
                        "Took: sid, ofid, grade"])
        QueryStep('2', 'SELECT Student.sid, Student.email, Took.grade', ['1'], '2', 'SELECT Student.sid, Student.email, Took.grade FROM Student, Took')
        ]

    tables = {
        '1': Table(t_name='1',
                    step='1',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa', 'Took.sid', 'Took.ofid', 'Took.grade'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4',   '1', '2', '87'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '1', '2', '87'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '2', '87'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '2', '87'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '1', '4', '73'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '1', '4', '73'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '1', '4', '73'),
                            ('4', 'James', 'james@mail.com', '2.8',     '1', '4', '73'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '2', '2', '92'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '2', '2', '92'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '2', '2', '92'),
                            ('4', 'James', 'james@mail.com', '2.8',     '2', '2', '92'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '3', '1', '80'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '3', '1', '80'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '3', '1', '80'),
                            ('4', 'James', 'james@mail.com', '2.8',     '3', '1', '80'),

                            ('1', 'Martin', 'martin@mail.com', '3.4',   '4', '1', '60'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0',     '4', '1', '60'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7',   '4', '1', '60'),
                            ('4', 'James', 'james@mail.com', '2.8',     '4', '1', '60')]
                    ),
        '2': Table(t_name='1.1',
                    step='1.1',
                    col_names=['Student.sid', 'Student.firstName', 'Student.email', 'Student.cgpa'],
                    tuples=[
                            ('1', 'Martin', 'martin@mail.com', '3.4'),
                            ('2', 'Kathy', 'kathy@mail.com', '4.0'),
                            ('3', 'Sophia', 'sophia@mail.com', '1.7'),
                            ('4', 'James', 'james@mail.com', '2.8')]
                    )


        '2': Table(t_name='2',
                    step='2',
                    col_names=['Student.sid', 'Student.email', 'Took.grade'],
                    tuples=[
                            ('1', 'martin@mail.com', '87'),
                            ('2', 'kathy@mail.com', '87'),
                            ('3', 'sophia@mail.com', '87'),
                            ('4', 'james@mail.com', '87'),

                            ('1', 'martin@mail.com', '73'),
                            ('2', 'kathy@mail.com', '73'),
                            ('3', 'sophia@mail.com', '73'),
                            ('4', 'james@mail.com', '73'),

                            ('1', 'martin@mail.com', '92'),
                            ('2', 'kathy@mail.com', '92'),
                            ('3', 'sophia@mail.com', '92'),
                            ('4', 'james@mail.com', '92'),

                            ('1', 'martin@mail.com', '80'),
                            ('2', 'kathy@mail.com', '80'),
                            ('3', 'sophia@mail.com', '80'),
                            ('4', 'james@mail.com', '80'),

                            ('1', 'martin@mail.com', '60'),
                            ('2', 'kathy@mail.com', '60'),
                            ('3', 'sophia@mail.com', '60'),
                            ('4', 'james@mail.com', '60')]
                    ),
    }


    DESIRED_ASTS['simple_cross_product_query'] =\
        [
            [ 'SELECT', ['Student.sid','Student.email','Took.grade'] ],
            [ 'FROM',   [ ['Student'], ',', ['Took'] ] ],
        ]

    parsed_query = ParsedQuery(steps, tables, query_text)
    return {"global_tables": global_tables, "all_queries": [parsed_query]}