var q = '{"steps": ["{\\"sql_chunk\\": \\"FROM (SELECT oid, dept FROM Offering) AS LimitedCols\\", \\"input_tables\\": [\\"Offering\\"], \\"reasons\\": [], \\"step_number\\": \\"1\\", \\"namespace\\": [\\"LimitedCols(oid, dept)\\"], \\"result_table\\": \\"1\\"}", "{\\"sql_chunk\\": \\"(SELECT oid, dept FROM Offering)\\", \\"input_tables\\": [\\"Offering\\"], \\"reasons\\": [], \\"step_number\\": \\"1.1\\", \\"namespace\\": [\\"Offering(oid, dept)\\"], \\"result_table\\": \\"1.1\\"}", "{\\"sql_chunk\\": \\"FROM Offering\\", \\"input_tables\\": [], \\"reasons\\": [], \\"step_number\\": \\"1.1.1\\", \\"namespace\\": [\\"Offering(oid, dept, cNum, instructor)\\"], \\"result_table\\": \\"1.1.1\\"}", "{\\"sql_chunk\\": \\"SELECT oid, dept\\", \\"input_tables\\": [\\"1.1.1\\"], \\"reasons\\": [], \\"step_number\\": \\"1.1.2\\", \\"namespace\\": [\\"Offering(oid, dept)\\"], \\"result_table\\": \\"1.1\\"}", "{\\"sql_chunk\\": \\"AS LimitedCols\\", \\"input_tables\\": [\\"1.1\\"], \\"reasons\\": [], \\"step_number\\": \\"1.2\\", \\"namespace\\": [\\"LimitedCols(oid, dept)\\"], \\"result_table\\": \\"1\\"}", "{\\"sql_chunk\\": \\"SELECT LimitedCols.oid\\", \\"input_tables\\": [\\"1\\"], \\"reasons\\": [], \\"step_number\\": \\"2\\", \\"namespace\\": [\\"LimitedCols(oid)\\"], \\"result_table\\": \\"2\\"}"], "query_text": " SELECT LimitedCols.oid FROM    (SELECT oid, dept     FROM Offering    ) AS LimitedCols", "tables": {"1.1.1": "{\\"t_name\\": \\"1.1.1\\", \\"step\\": \\"1.1.1\\", \\"tuples\\": [[\\"1\\", \\"csc\\", \\"209\\", \\"K. Reid\\"], [\\"2\\", \\"csc\\", \\"343\\", \\"D. Horton\\"], [\\"3\\", \\"mat\\", \\"137\\", \\"J. Kamnitzer\\"], [\\"4\\", \\"ger\\", \\"100\\", \\"E. Luzi\\"]], \\"col_names\\": [\\"Offering.oid\\", \\"Offering.dept\\", \\"Offering.cNum\\", \\"Offering.instructor\\"]}", "1": "{\\"t_name\\": \\"LimitedCols\\", \\"step\\": \\"1\\", \\"tuples\\": [[\\"1\\", \\"csc\\"], [\\"2\\", \\"csc\\"], [\\"3\\", \\"mat\\"], [\\"4\\", \\"ger\\"]], \\"col_names\\": [\\"LimitedCols.oid\\", \\"LimitedCols.dept\\"]}", "2": "{\\"t_name\\": \\"2\\", \\"step\\": \\"2\\", \\"tuples\\": [\\"1\\", \\"2\\", \\"3\\", \\"4\\"], \\"col_names\\": [\\"LimitedCols.oid\\"]}", "1.1": "{\\"t_name\\": \\"1.1\\", \\"step\\": \\"1.1\\", \\"tuples\\": [[\\"1\\", \\"csc\\"], [\\"2\\", \\"csc\\"], [\\"3\\", \\"mat\\"], [\\"4\\", \\"ger\\"]], \\"col_names\\": [\\"Offering.oid\\", \\"Offering.dept\\"]}"}}';
var parsedquery = [JSON.parse(q)];
