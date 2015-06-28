/*
    Given a step's id, load the step into display
*/
function loadStep(id){
    $("#tooltip").hide();

    currentWindow.current_step = id;
    var step = $(currentWindow.toc + " #" + id);
    $(currentWindow.toc + " .step").removeClass("selected");
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
    replaceInputTables(idsToHTML(currentWindow.steps_dictionary[toKey(id)][1]));
    replaceOutputTable(currentWindow.tables_dictionary[currentWindow.steps_dictionary[toKey(id)][5]]);

}

function stepOut(){
    if (currentWindow.current_step == currentWindow.step_keys[0]){
        return
    } else {
        var index = currentWindow.step_keys.indexOf(toKey(currentWindow.current_step));
        var initial = index;
        while (index > 1 && hasNested(currentWindow.step_keys, index - 1)){
            index -= 1;
        }
        
        if (nestedInside(currentWindow.step_keys, initial, index) || (index == 1 && nestedInside (currentWindow.step_keys, initial, 0))){
            index = initial + 1;
        }
        
        loadStep(toID(currentWindow.step_keys[index - 1]));
    }
}

function stepBack(){
    if (currentWindow.current_step == currentWindow.step_keys[0]){
        return
    } else {
        var index = currentWindow.step_keys.indexOf(toKey(current_step));
        if (hasNested(step_keys, index - 1) && differentLevels(step_keys, index, index - 1)){
            // The initial step is the first part of a nested step (ex. 2.1)
            // Step out of the nested component and go to the next one on the same level
            while (index > 1 && hasNested(currentWindow.step_keys, index - 1)){
                index -= 1;
            }
        }
        
        var initial = index;
        
        // Move to the next step on the same depth
        while (index > 1 && differentLevels(currentWindow.step_keys, initial, index - 1)){
            index -= 1;
        }

        if (nestedInside(currentWindow.step_keys, initial, index) || (index == 1 && nestedInside (currentWindow.step_keys, initial, 0))){
            index = initial + 1;
        }

        loadStep(toID(currentWindow.step_keys[index - 1]));
    }
}

function stepNext(){
    if (currentWindow.current_step == currentWindow.step_keys[step_keys.length-1]){
        return
    } else {
        var index = currentWindow.step_keys.indexOf(toKey(current_step));
        var initial = index;
        
        if (!isLastNested(currentWindow.step_keys, index)) {
            // Move to the next step on the same depth
            while (index < currentWindow.step_keys.length - 1 && differentLevels(currentWindow.step_keys, initial, index + 1)){
                index += 1;
            }
        }
        loadStep(toID(currentWindow.step_keys[index + 1]));
    }
}

function stepIn(){
    if (currentWindow.current_step == currentWindow.step_keys[currentWindow.step_keys.length - 1]){
        return
    } else {
        var index = currentWindow.step_keys.indexOf(toKey(currentWindow.current_step));
        while (index < currentWindow.step_keys.length - 1 && hasNested(currentWindow.step_keys, index + 1)){
            index += 1;
        }
        loadStep(toID(currentWindow.step_keys[index + 1]));
    }
}
