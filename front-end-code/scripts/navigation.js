/*
    Given a step's id, load the step into display
*/
function loadStep(id){
    current_step = id;
    var step = $("#" + id);
    $(".step").removeClass("selected");
    step.addClass("selected");
    
    // Expand all collapsed cells containing id
    var parent_to_show = step;

    // Expand all ancestors until the step is shown
    while (step.is(':hidden')){
        // Find the parent (which might be collapsed)
        var parentitem = parent_to_show.parent().closest("tr");
        var collapsible = parentitem.find(".collapsible")[0];

        // If the parent is already expanded, don't collapse it
        if (jQuery(collapsible).html() == "[+]")
            collapseHandler(collapsible);

        parent_to_show = parentitem;
    }

    // Load the input and output tables
    replaceInputTables(idsToHTML(steps_dictionary[id][1]));
    replaceOutputTable(tables_dictionary[steps_dictionary[id][5]]);

}

function stepOut(){
    if (current_step == step_keys[0]){
        return
    } else {
        var index = step_keys.indexOf(toKey(current_step));
        while (hasNested(step_keys, index - 1)){
            index -= 1;
        }
        loadStep(toID(step_keys[index - 1]));
    }
}

function stepBack(){
    if (current_step == step_keys[0]){
        return
    } else {
        var index = step_keys.indexOf(toKey(current_step));
        if (hasNested(step_keys, index - 1) && differentLevels(step_keys, index, index - 1)){
            // The initial step is the first part of a nested step (ex. 2.1)
            // Step out of the nested component and go to the next one on the same level
            while (hasNested(step_keys, index - 1)){
                index -= 1;
            }
        }
        
        var initial = index;
        
        // Move to the next step on the same depth
        while (index > 0 && differentLevels(step_keys, initial, index - 1)){
            index -= 1;
        }

        loadStep(toID(step_keys[index - 1]));
    }
}

function stepNext(){
    if (current_step == step_keys[step_keys.length-1]){
        return
    } else {
        var index = step_keys.indexOf(toKey(current_step));
        var initial = index;
        
        if (!isLastNested(step_keys, index)) {
            // Move to the next step on the same depth
            while (differentLevels(step_keys, initial, index + 1)){
                index += 1;
            }
        }
        loadStep(toID(step_keys[index + 1]));
    }
}

function stepIn(){
    if (current_step == step_keys[step_keys.length - 1]){
        return
    } else {
        var index = step_keys.indexOf(toKey(current_step));
        while (hasNested(step_keys, index + 1)){
            index += 1;
        }
        loadStep(toID(step_keys[index + 1]));
    }
}
