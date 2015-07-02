var q = '{"steps": ["{\\"sql_chunk\\": \\"FROM Student\\", \\"input_tables\\": [], \\"reasons\\": [], \\"step_number\\": \\"1\\", \\"namespace\\": [\\"Student(sid, firstName, email, cgpa)\\"], \\"result_table\\": \\"1\\"}", "{\\"sql_chunk\\": \\"WHERE cgpa > (SELECT cgpa FROM Student WHERE sid=4)\\", \\"input_tables\\": [\\"1\\"], \\"reasons\\": [{\\"conditions_matched\\": \\"{\\\\\\"subqueries\\\\\\": {\\\\\\"cgpa > (SELECT cgpa FROM Student WHERE sid=4)\\\\\\": \\\\\\"{\\\\\\\\\\\\\\"steps\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"sql_chunk\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"FROM Student\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"input_tables\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"reasons\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step_number\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"namespace\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student(sid, firstName, email, cgpa)\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"result_table\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"sql_chunk\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"WHERE sid=4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"input_tables\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"reasons\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"conditions_matched\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"subqueries\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": {}, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"conditions_matched\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"sid=4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"row\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": 0}], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step_number\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"namespace\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"result_table\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"sql_chunk\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"SELECT cgpa\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"input_tables\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"reasons\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step_number\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"namespace\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student(cgpa)\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"result_table\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\"query_text\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"SELECT cgpa FROM Student WHERE sid=4\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"tables\\\\\\\\\\\\\\": {\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"t_name\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"tuples\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Martin\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"martin@mail.com\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3.4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Kathy\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"kathy@mail.com\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"4.0\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Sophia\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"not_martin@mail.com\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1.7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"James\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"james@mail.com\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2.8\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"col_names\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.sid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.firstName\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.email\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.cgpa\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"3\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"t_name\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"tuples\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2.8\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"col_names\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.cgpa\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"2\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"t_name\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"tuples\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"James\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"james@mail.com\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2.8\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"col_names\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.sid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.firstName\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.email\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"Student.cgpa\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]}\\\\\\\\\\\\\\"}}\\\\\\"}, \\\\\\"conditions_matched\\\\\\": [\\\\\\"cgpa > (SELECT cgpa FROM Student WHERE sid=4)\\\\\\"]}\\", \\"row\\": 0}], \\"step_number\\": \\"2\\", \\"namespace\\": [], \\"result_table\\": \\"2\\"}", "{\\"sql_chunk\\": \\"SELECT sid, firstName\\", \\"input_tables\\": [\\"2\\"], \\"reasons\\": [], \\"step_number\\": \\"3\\", \\"namespace\\": [\\"Student(sid, firstName)\\"], \\"result_table\\": \\"3\\"}"], "query_text": " SELECT sid, firstName FROM Student WHERE cgpa >    (SELECT cgpa     FROM Student     WHERE sid=4)", "tables": {"1": "{\\"t_name\\": \\"1\\", \\"step\\": \\"1\\", \\"tuples\\": [[\\"1\\", \\"Martin\\", \\"martin@mail.com\\", \\"3.4\\"], [\\"2\\", \\"Kathy\\", \\"kathy@mail.com\\", \\"4.0\\"], [\\"3\\", \\"Sophia\\", \\"not_martin@mail.com\\", \\"1.7\\"], [\\"4\\", \\"James\\", \\"james@mail.com\\", \\"2.8\\"]], \\"col_names\\": [\\"Student.sid\\", \\"Student.firstName\\", \\"Student.email\\", \\"Student.cgpa\\"]}", "3": "{\\"t_name\\": \\"3\\", \\"step\\": \\"3\\", \\"tuples\\": [[\\"1\\", \\"Martin\\"], [\\"2\\", \\"Kathy\\"]], \\"col_names\\": [\\"Student.sid\\", \\"Student.firstName\\"]}", "2": "{\\"t_name\\": \\"2\\", \\"step\\": \\"2\\", \\"tuples\\": [[\\"1\\", \\"Martin\\", \\"martin@mail.com\\", \\"3.4\\"], [\\"2\\", \\"Kathy\\", \\"kathy@mail.com\\", \\"4.0\\"]], \\"col_names\\": [\\"Student.sid\\", \\"Student.firstName\\", \\"Student.email\\", \\"Student.cgpa\\"]}"}}';
var parsedquery = [JSON.parse(q)];
