/*
    Given a Table (in JSON format) and a hovertext, returns a string with the 
    table in formatted HTML
*/
function toTable(t){
    var num_columns = t.col_names.length;
    var num_rows = t.tuples.length;
    var hovertext;
    var id = t.t_id;

    // Global tables seem to use .id while step tables use step.
    if (!id)
        id = t.step;
    
    if (step_keys.indexOf(id) > -1)
        hovertext = "Table " + id + ". " + steps_dictionary[id][0];
    else
        hovertext = id;
    var html = "<div class='tablecontainer' id=\"table-" + toID(id) + "\" onmouseover=\"hoverText('"+hovertext+"')\" onmouseout=\"hoverText('')\"><table>";
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

function getStepIDFromTable(id){
    console.log(id);
    return id.split("-").splice(1).join("-");
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
