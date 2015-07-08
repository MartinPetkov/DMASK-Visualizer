function Step(s, query){
    this.stepnumber = s.step_number;
    this.sql = s.sql_chunk;
    this.input_ids = s.input_tables;
    this.reasons = s.reasons;
    this.namespace = s.namespace;
    this.result_id = s.res_table_name;
    
    this.query = query;
}

/*
    Look-up and return the input tables
*/
Step.prototype.getInputTables = function(){
    var tables = [];
    var i;
    var id_length = this.input_ids.length;
    
    for (i = 0; i < id_length; i++){
        tables.push(this.query.tables_dictionary[this.input_ids[i]]);
    }
    
    return tables;
}

Step.prototype.getInputHTML = function(){
    var tables = this.getInputTables();
    
    var html = "";
    var i;
    for (var i = 0; i < tables.length; i++){
        html += "<div class='input'>"+tables[i].toDisplay()+"</div>";
    }
    
    return html;
}

Step.prototype.getOutputHTML = function(){
    var output = this.query.tables_dictionary[this.result_id];
    return "<div class='output'>" + output.toDisplay() + "</div>";
}
