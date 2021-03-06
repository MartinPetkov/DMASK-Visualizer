// deprecated



/*
    Given a Query string, add it to the ToC
*/
function loadQuery(text){
    var querytext = "<tr><td class='query'>" + text + ";</td></tr>";
    $(currentWindow.steps).append(querytext);
}

/*
    Given a dictionary of steps, load them into the ToC
*/
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
    $(currentWindow.steps).append(allsteps);
}

/*
    Convert steps (2.1.1) into ids (2-1-1)
*/
function toID(id){
    return id.split(".").join("-");
}

/*
    Convert steps (2-1-1) into ids (2.1.1)
*/
function toKey(id){
    return id.split("-").join(".");
}


/*
    Check if the current step has nested components
*/
function hasNested(keys, i){
    if (i + 1 >= keys.length || keys[i+1].lastIndexOf(".") <= keys[i].lastIndexOf("."))
        return 0;
    return 1;
}

/*
    Check if the current step is the last in a nested group
*/
function isLastNested(keys, i){
    if (i + 1 >= keys.length || keys[i+1].lastIndexOf(".") >= keys[i].lastIndexOf("."))
        return 0;
    return 1;
}

function differentLevels(keys, i, j){
    if (keys[i].lastIndexOf(".") == keys[j].lastIndexOf("."))
        return 0;
    return 1;
}

/*
    Check if keys[i] is nested inside keys[j]
    Example: nestedInside("1.1.1", "1") == True
*/
function nestedInside(keys, i, j){
    if (differentLevels(keys, i, j) && keys[i].slice(0, keys[j].length) == keys[j])
        return 1;
    return 0;
}

/*
    Given an array of steps (JSON), parse them into a dictionary in the format:
    step_number : [sql_chunk, input_tables, reasons, namespace, res_table_name, result_table]
*/
function stepsToDict(steps){ // replace with stepsToDict(steps, query)
    var dict = [];
    var i;
    for (i = 0; i < steps.length; i++){
        var step = JSON.parse(steps[i]);
        var stepnumber = step.step_number;
        dict[stepnumber] = [step.sql_chunk, step.input_tables, step.reasons, step.namespace, step.res_table_name, step.result_table]; // replace with = Step(step, query);
    }
    return dict;
}

