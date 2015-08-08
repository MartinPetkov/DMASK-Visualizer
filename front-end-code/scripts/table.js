function Table(t, query){
    this.columns = t.col_names;
    this.rows = t.tuples;
    this.reasons = t.reasons;
    this.id = t.t_id;
    this.t_name = t.t_name;
    
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

    var tablename = "<div class='tablename' id=\"name-" + toID(this.id) +"\">" + this.t_name + "</div>";

    // Create the div container
    var html = tablename + "<div class='tablecontainer' id=\"table-" + toID(this.id) + "\" onmouseover=\"hoverText('"+this.hovertext+"')\" onmouseout=\"hoverText('')\"><table>";

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
    
    // initialize the set of reasons
    for (i = 1; i <= $(table).find(".output-row").length; i++){
        var uncorrelated_subqueries = JSON.parse(reasons[0].conditions_matched).subqueries;
        var passed_uncorrelated_subqueries = JSON.parse(reasons[0].conditions_matched).passed_subqueries;
        
        var new_reason = new Reasons();
        new_reason.conditions = all_reasons;
        $(table).find("#row-"+i).val(new_reason);

        // add uncorrelated subqueries
        var keys = Object.keys(uncorrelated_subqueries);
        
        var j;
        for (j = 0; j < keys.length; j++){
            var key = keys[j];
            
            var uncorrelated_reason = new Reason(key);
            uncorrelated_reason.subquery = JSON.parse(uncorrelated_subqueries[key]);
            uncorrelated_reason.uncorrelated = true;
            
            new_reason.reasons.push(uncorrelated_reason);
        }
    }
    
    // add the reasons
    for (i = 1; i < num_reasons; i++){
        // read the information
        var conditions_matched = JSON.parse(reasons[i].conditions_matched).conditions_matched;
        var subqueries = JSON.parse(reasons[i].conditions_matched).subqueries;
        var passed_subqueries = JSON.parse(reasons[i].conditions_matched).passed_subqueries;

        // find the old value
        var row = reasons[i].row;
        var table_row = $(table).find("#row-"+row);

        var old_value = table_row.val();

        // set whether the row passed or not
        if (old_value.passed == undefined)
            old_value.passed = JSON.parse(reasons[i].conditions_matched).passed;

        // add new reasons
        var j;
        var matched_length = conditions_matched.length;

        for (j = 0; j < matched_length; j++){
            var new_reason = new Reason(conditions_matched[j]);
            if (subqueries[conditions_matched[j]] != undefined){
                new_reason.subquery = JSON.parse(subqueries[conditions_matched[j]]);
                new_reason.passed_subqueries = passed_subqueries;
            }
            old_value.reasons.push(new_reason);
        }

        table_row.val(old_value);
    }

    var rows = $(table).find(".output-row");
    for (i = 0; i < rows.length; i++){
        var row = $(rows[i]);
        if (row.val() && row.val().passed)
            row.addClass("kept");
        else
            row.addClass("removed");
    }

    return table;
}
