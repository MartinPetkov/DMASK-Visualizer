function loadQuery(text){
    var querytext = "<tr><td class='query'>" + text + ";</td></tr>";
    $("#steps").append(querytext);
}

function loadSteps(dict){
    var keys = Object.keys(dict).sort();
    var i;
    var allsteps = "";
    for (i = 0; i < keys.length; i++){
        var step = "<tr id='" + toID(keys[i]) + "' class='step'><td>";
        var nested = hasNested(keys, i);
        
        if (nested)
            step += "<div class='collapsible'>[-]</div>";
            
        step += keys[i] + ". " + dict[keys[i]][0];
        
        if (nested)
            step += "<table class='nested'>";
            
        if (isLastNested(keys, i))
            step += "</table></td></tr>";
            
        allsteps += step;
    }
    $("#steps").append(allsteps);
}

function toID(id){
    return id.split(".").join("-");
}

function hasNested(keys, i){
    if (i + 1 >= keys.length || keys[i+1].lastIndexOf(".") <= keys[i].lastIndexOf("."))
        return 0;
    return 1;
}

function isLastNested(keys, i){
    if (i + 1 >= keys.length || keys[i+1].lastIndexOf(".") >= keys[i].lastIndexOf("."))
        return 0;
    return 1;
}

function stepsToDict(steps){
    // Parse the steps into a dictionary in the format
    // step_number : [sql_chunk, input_tables, reasons, namespace, res_table_name, result_table]
    var dict = [];
    var i;
    for (i = 0; i < steps.length; i++){
        var step = JSON.parse(steps[i]);
        dict[step.step_number] = [step.sql_chunk, step.input_tables, step.reasons, step.namespace, step.res_table_name, step.result_table];
    }
    return dict;
}

function collapseHandler(collapsible){
    var parent = collapsible.closest("tr");
    if (jQuery(collapsible).html() == "[-]"){
        collapse(parent.id);
        jQuery(collapsible).html("[+]");
    }
    else{
        expand(parent.id);
        jQuery(collapsible).html("[-]");
    }
}

function collapse(parent){
    jQuery($("#"+parent).find(".nested")[0]).hide();
};

function expand(parent){
    jQuery($("#"+parent).find(".nested")[0]).show();
};

function collapseAll(){
    $(".step").each(function(){collapse(this.id)});
    $(".collapsible").html("[+]");
}

$(document).ready(parseAndLoad);

function loadStep(id){
    $(".step").removeClass("selected");
    $("#"+id).addClass("selected");
    
    // replace input and output tables
    replaceInputTables(idsToHTML(steps_dictionary[id][1]));
    replaceOutputTable(tables_dictionary[steps_dictionary[id][5]]);
}

function parseAndLoad(){
    steps_dictionary = stepsToDict(parsedquery.steps);
    parseTablesToDict(global_tables);
    parseTablesToDict(parsedquery.tables);
    loadQuery(parsedquery.query_text);
    loadSteps(steps_dictionary);
    
    $(document).on("click", ".collapsible", function(e){collapseHandler(e.target);});
    collapseAll();

    $(document).on("click", ".step", function(e){
        if (!jQuery(e.target).hasClass("collapsible"))
            var step = jQuery(e.target.closest("tr"));
            var id = step[0].id;
            loadStep(id);
    });
}

