var parsedquery = {"tables": {}, "query_text": " SELECT sid, surName FROM Student WHERE cgpa >    (SELECT cgpa     FROM Student     WHERE sid=999)", "steps": ["{\"sql_chunk\": \"FROM Student\", \"input_tables\": [], \"reasons\": [], \"namespace\": [], \"step_number\": \"1\", \"res_table_name\": \"\", \"result_table\": \"1\"}", "{\"sql_chunk\": \"WHERE cgpa > (SELECT cgpa FROM Student WHERE sid=999)\", \"input_tables\": [\"1\"], \"reasons\": [], \"namespace\": [], \"step_number\": \"2\", \"res_table_name\": \"\", \"result_table\": \"2\"}", "{\"sql_chunk\": \"(SELECT cgpa FROM Student WHERE sid=999)\", \"input_tables\": [\"\"], \"reasons\": [], \"namespace\": [], \"step_number\": \"2.1\", \"res_table_name\": \"\", \"result_table\": \"2.1\"}", "{\"sql_chunk\": \"FROM Student\", \"input_tables\": [], \"reasons\": [], \"namespace\": [], \"step_number\": \"2.1.1\", \"res_table_name\": \"\", \"result_table\": \"2.1.1\"}", "{\"sql_chunk\": \"WHERE sid=999\", \"input_tables\": [\"2.1.1\"], \"reasons\": [], \"namespace\": [], \"step_number\": \"2.1.2\", \"res_table_name\": \"\", \"result_table\": \"2.1.2\"}", "{\"sql_chunk\": \"SELECT cgpa\", \"input_tables\": [\"2.1.2\"], \"reasons\": [], \"namespace\": [], \"step_number\": \"2.1.3\", \"res_table_name\": \"\", \"result_table\": \"2.1\"}", "{\"sql_chunk\": \"cgpa > (SELECT cgpa FROM Student WHEE sid=999)\", \"input_tables\": [\"1\", \"2.1\"], \"reasons\": [], \"namespace\": [], \"step_number\": \"2.2\", \"res_table_name\": \"\", \"result_table\": \"2\"}", "{\"sql_chunk\": \"SELECT sid, surName\", \"input_tables\": [\"2\"], \"reasons\": [], \"namespace\": [], \"step_number\": \"3\", \"res_table_name\": \"\", \"result_table\": \"3\"}"]};
var student = {"t_id":"Took", "col_names":["sid", "firstName", "email", "cgpa"], "tuples":[
["1", "Martin", "martin@mail.com", "3.4"],
["2", "Kathy", "kathy@mail.com", "4.0"],
["3", "Sophia", "sophia@mail.com", "1.7"],
["4", "James", "james@mail.com", "2.8"]]};
var took = {"t_id":"sid","col_names":["sid","ofid", "grade"], "tuples":[
["1", "2", "87"],
["1", "4", "73"],
["2", "2", "92"],
["3", "1", "80"],
["4", "1", "60"]]};
