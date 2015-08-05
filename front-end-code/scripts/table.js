function Table(t, query){
    this.columns = t.col_names;
    this.rows = t.tuples;
    this.reasons = t.reasons;
    this.id = t.t_id;
    
    if (!this.id)
        this.id = t.step;
        
    this.hovertext = this.generateHovertext(query);
}

Table.prototype.generateHovertext = function(query){
    var hovertext;
    if (query.step_keys.indexOf(this.id) > -1)
        hovertext = "Table " + this.id + ". " + query.steps_dictionary[this.id].sql;
    else
        hovertext = this.id;

    // Temporary quotation mark escape; leaves a trailing \, however.
    hovertext = hovertext.replace(/"/g, '\\\\\\"');
    hovertext = hovertext.replace(/'/g, "\\\\\\'");

    return hovertext;
}

Table.prototype.toDisplay = function(){
    var num_columns = this.columns.length;
    var num_rows = this.rows.length;

    // Create the div container
    var html = "<div class='tablecontainer' id=\"table-" + toID(this.id) + "\" onmouseover=\"hoverText('"+this.hovertext+"')\" onmouseout=\"hoverText('')\"><table>";

    var i, j;

    // Add the column names
    html += "<tr>";
    for (i = 0; i < num_columns; i++){
        html += "<th>" + this.columns[i] + "</th>";
    }
    html += "</tr>"

    // Add the rows
    for (i = 0; i < num_rows; i++){
        html+="<tr class='output-row' id='row-" + (i + 1) + "'>";
        for (j = 0; j < num_columns; j++){
            if (num_columns == 1)
                html += "<td>" + this.rows[i] + "</td>";
            else
                html += "<td>"+this.rows[i][j]+"</td>";
        }
        html += "</tr>";
    }

    html += "</table></div>";
    var table = $.parseHTML(html);
    return addReasons(this.reasons, table);
}


function addReasons(reasons, table){
    if (reasons == undefined || reasons.length == 0)
        return table;
    
    var num_reasons = reasons.length;
    var i;
    var all_reasons = JSON.parse(reasons[0].conditions_matched).conditions_matched;
    
    // add the reasons
    for (i = 1; i < num_reasons; i++){
        // read the information
        var conditions_matched = JSON.parse(reasons[i].conditions_matched).conditions_matched;
        var subqueries = JSON.parse(reasons[i].conditions_matched).subqueries;

        // find the old value
        var row = reasons[i].row;
        var table_row = $(table).find("#row-"+row);

        var old_value = table_row.val();
        if (!old_value)
            old_value = new Reasons();

        // add new reasons
        var j;
        var matched_length = conditions_matched.length;

        for (j = 0; j < matched_length; j++){
            var new_reason = new Reason(conditions_matched[j]);
            if (subqueries[conditions_matched[j]] != undefined){
                new_reason.subquery = JSON.parse(subqueries[conditions_matched[j]]);
            }
            old_value.reasons.push(new_reason);
        }

        table_row.val(old_value);
    }
    return table;
}
