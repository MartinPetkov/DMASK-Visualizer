var parsedquery = [{"steps": ["{\"sql_chunk\": \"FROM Student\", \"input_tables\": [], \"step_number\": \"1\", \"executable_sql\": \"\", \"namespace\": [\"Student: sid, firstName, email, cgpa\"], \"result_table\": \"Student\"}", "{\"sql_chunk\": \"WHERE cgpa > 2 OR firstName='Sophia'\", \"input_tables\": [\"Student\"], \"step_number\": \"2\", \"executable_sql\": \"\", \"namespace\": [], \"result_table\": \"2\"}", "{\"sql_chunk\": \"SELECT email, cgpa\", \"input_tables\": [\"2\"], \"step_number\": \"3\", \"executable_sql\": \"\", \"namespace\": [], \"result_table\": \"3\"}"], "query_text": " SELECT email, cgpa FROM Student WHERE cgpa > 3 OR firstName='Sophia'", "tables": {"1": "{\"t_name\": \"Student\", \"reasons\": [], \"step\": \"1\", \"tuples\": [[\"1\", \"Martin\", \"martin@mail.com\", \"3.4\"], [\"2\", \"Kathy\", \"kathy@mail.com\", \"4.0\"], [\"3\", \"Sophia\", \"not_martin@mail.com\", \"1.7\"], [\"4\", \"James\", \"james@mail.com\", \"2.8\"]], \"col_names\": [\"sid\", \"firstName\", \"email\", \"cgpa\"]}", "3": "{\"t_name\": \"3\", \"reasons\": [], \"step\": \"3\", \"tuples\": [[\"martin@mail.com\", \"3.4\"], [\"kathy@mail.com\", \"4.0\"], [\"not_martin@mail.com\", \"1.7\"]], \"col_names\": [\"email\", \"cgpa\"]}", "2": "{\"t_name\": \"2\", \"reasons\": [{\"conditions_matched\": \"{\\\"subqueries\\\": {}, \\\"conditions_matched\\\": [\\\"cgpa > 2\\\", \\\"firstname='Sophia'\\\"]}\", \"row\": 0}, {\"conditions_matched\": \"{\\\"subqueries\\\": {}, \\\"conditions_matched\\\": [\\\"cgpa > 2\\\"]}\", \"row\": 1}, {\"conditions_matched\": \"{\\\"subqueries\\\": {}, \\\"conditions_matched\\\": [\\\"cgpa > 2\\\"]}\", \"row\": 2}, {\"conditions_matched\": \"{\\\"subqueries\\\": {}, \\\"conditions_matched\\\": [\\\"firstName='Sophia'\\\"]}\", \"row\": 3}], \"step\": \"2\", \"tuples\": [[\"1\", \"Martin\", \"martin@mail.com\", \"3.4\"], [\"2\", \"Kathy\", \"kathy@mail.com\", \"4.0\"], [\"3\", \"Sophia\", \"not_martin@mail.com\", \"1.7\"]], \"col_names\": [\"sid\", \"firstName\", \"email\", \"cgpa\"]}"}}];

