function Table(t, query){
    this.columns = t.col_names;
    this.rows = t.tuples;
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
        html+="<tr class='output-row' id='row-" + (i + 1) + "-step-" + toID(this.id) + "'>";
        for (j = 0; j < num_columns; j++){
            if (num_columns == 1)
                html += "<td>" + this.rows[i] + "</td>";
            else
                html += "<td>"+this.rows[i][j]+"</td>";
        }
        html += "</tr>";
    }

    html += "</table></div>";

    return html;
}

