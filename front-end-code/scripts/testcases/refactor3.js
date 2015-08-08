var pq = ['{"steps": ["{\\"executable_sql\\": \\"SELECT * FROM Offering o1;\\", \\"result_table\\": \\"o1\\", \\"input_tables\\": [], \\"sql_chunk\\": \\"FROM Offering o1\\", \\"step_number\\": \\"1\\", \\"namespace\\": []}", "{\\"executable_sql\\": \\"SELECT * FROM Offering o1 WHERE oid = ( SELECT oid FROM Offering o2 WHERE oid = 2 );\\", \\"result_table\\": \\"2\\", \\"input_tables\\": [\\"o1\\"], \\"sql_chunk\\": \\"WHERE oid = ( SELECT oid FROM Offering o2 WHERE oid = 2 )\\", \\"step_number\\": \\"2\\", \\"namespace\\": []}", "{\\"executable_sql\\": \\"SELECT instructor FROM Offering o1 WHERE oid = ( SELECT oid FROM Offering o2 WHERE oid = 2 );\\", \\"result_table\\": \\"3\\", \\"input_tables\\": [\\"2\\"], \\"sql_chunk\\": \\"SELECT instructor\\", \\"step_number\\": \\"3\\", \\"namespace\\": \\"\\"}"], "query_text": "SELECT instructor FROM Offering o1 WHERE oid = (SELECT oid FROM Offering o2 WHERE oid = 2);", "tables": {"o1": "{\\"reasons\\": [{\\"conditions_matched\\": \\"{\\\\\\"conditions_matched\\\\\\": [\\\\\\"oid = (SELECT oid FROM Offering o2 WHERE oid = 2)\\\\\\"], \\\\\\"subqueries\\\\\\": {\\\\\\"oid = (SELECT oid FROM Offering o2 WHERE oid = 2)\\\\\\": \\\\\\"{\\\\\\\\\\\\\\"steps\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"executable_sql\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"SELECT * FROM Offering o2;\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"result_table\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"o2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"input_tables\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"sql_chunk\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"FROM Offering o2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step_number\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"namespace\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": []}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"executable_sql\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"SELECT * FROM Offering o2 WHERE oid = 2;\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"result_table\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"input_tables\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"o2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"sql_chunk\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"WHERE oid = 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step_number\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"namespace\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": []}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"executable_sql\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"SELECT oid FROM Offering o2 WHERE oid = 2;\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"result_table\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"input_tables\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"sql_chunk\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"SELECT oid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step_number\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"namespace\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\"query_text\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"SELECT oid FROM Offering o2 WHERE oid = 2\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"tables\\\\\\\\\\\\\\": {\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"reasons\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"tuples\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [[2]], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"t_name\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"o2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"col_names\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"oid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"2\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"reasons\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"tuples\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [[2, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"csc\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", 343, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"D. Horton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"t_name\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"o2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"col_names\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"oid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"dept\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"cnum\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"instructor\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]}\\\\\\\\\\\\\\", \\\\\\\\\\\\\\"o2\\\\\\\\\\\\\\": \\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"reasons\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"conditions_matched\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"conditions_matched\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"oid = 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"subqueries\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": {}, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"passed_subqueries\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": []}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"row\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": 0}, {\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"conditions_matched\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"conditions_matched\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"oid = 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"subqueries\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": {}, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"passed_subqueries\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": []}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"row\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": 2}], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"tuples\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [[1, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"csc\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", 209, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"K. Reid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], [2, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"csc\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", 343, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"D. Horton\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], [3, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"mat\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", 137, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"J. Kamnitzer\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"], [4, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"ger\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", 100, \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"E. Luzi\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]], \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"t_name\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"o2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"step\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"col_names\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\": [\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"oid\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"dept\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"cnum\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"instructor\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"]}\\\\\\\\\\\\\\"}}\\\\\\"}, \\\\\\"passed_subqueries\\\\\\": []}\\", \\"row\\": 0}, {\\"conditions_matched\\": \\"{\\\\\\"conditions_matched\\\\\\": [\\\\\\"oid = (SELECT oid FROM Offering o2 WHERE oid = 2)\\\\\\"], \\\\\\"subqueries\\\\\\": {}, \\\\\\"passed_subqueries\\\\\\": []}\\", \\"row\\": 2}], \\"tuples\\": [[1, \\"csc\\", 209, \\"K. Reid\\"], [2, \\"csc\\", 343, \\"D. Horton\\"], [3, \\"mat\\", 137, \\"J. Kamnitzer\\"], [4, \\"ger\\", 100, \\"E. Luzi\\"]], \\"t_name\\": \\"o1\\", \\"step\\": \\"1\\", \\"col_names\\": [\\"oid\\", \\"dept\\", \\"cnum\\", \\"instructor\\"]}", "3": "{\\"reasons\\": [], \\"tuples\\": [[\\"D. Horton\\"]], \\"t_name\\": \\"o1\\", \\"step\\": \\"3\\", \\"col_names\\": [\\"instructor\\"]}", "2": "{\\"reasons\\": [], \\"tuples\\": [[2, \\"csc\\", 343, \\"D. Horton\\"]], \\"t_name\\": \\"o1\\", \\"step\\": \\"2\\", \\"col_names\\": [\\"oid\\", \\"dept\\", \\"cnum\\", \\"instructor\\"]}"}}'];
var parsedquery = [JSON.parse(pq[0])]
