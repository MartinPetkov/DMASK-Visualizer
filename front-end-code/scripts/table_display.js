/*
    Given a Table (in JSON format) and a hovertext, returns a string with the 
    table in formatted HTML
*/
function toTable(t){
    var num_columns = t.col_names.length;
    var num_rows = t.tuples.length;
    var hovertext;
    if (step_keys.indexOf(t.t_id) > -1)
        hovertext = t.t_id + ". " + steps_dictionary[t.t_id][0];
    else
        hovertext = t.t_id;
    
    var html = "<div class='tablecontainer' onmouseover=\"hoverText('"+hovertext+"')\" onmouseout=\"hoverText('')\"><table>";
    var i, j;
    html += "<tr>";
    for (i = 0; i < num_columns; i++){
        html += "<th>"+t.col_names[i]+"</th>";
    }
    html += "</tr>";
    for (i = 0; i < num_rows; i++){
        html+="<tr>";
        for (j = 0; j < num_columns; j++){
            html+="<td>"+t.tuples[i][j]+"</td>";
        }
        html += "</tr>";
    }
    html += "</table></div>";
    return html;
    
}

function parseTablesToDict(t){
    var keys = Object.keys(t);
    var i;
    for (i = 0; i < keys.length; i++){
        tables_dictionary[keys[i]] = toTable(JSON.parse(t[keys[i]]));
    }
}

function idsToHTML(ids){
    var output = [];
    var i;
    for (i = 0; i < ids.length; i++){
        output.push(tables_dictionary[ids[i]]);
    }
    return output;
}

/*
    Given a list of table HTML, replace the corresponding tables
    replaceInputTables([toTable(took), toTable(student)])
*/
function replaceInputTables(tableHTML){
    var inbox = $("#inbox");
    inbox.empty();
    var html = "";
    var i;
    for (var i = 0; i < tableHTML.length; i++){
        html += "<div class='input'>"+tableHTML[i]+"</div>";
    }
    inbox.append(html);
    updateTableDisplay();
}
/*
    Given a list of table HTML, replace the corresponding tables
    replaceInputTables([toTable(took), toTable(student)])
*/
function replaceOutputTable(tableHTML){
    var outbox = $("#outbox");
    outbox.empty();
    outbox.append("<div class='output'>"+tableHTML+"</div>");
}
