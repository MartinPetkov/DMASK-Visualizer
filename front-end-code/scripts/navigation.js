function stepOut(){
    var step_id = current_window.current_step_id;
    if (step_id == ""){
        return;
    }
    if (isFirstStep(step_id)){
        return;
    } else {
        var current_step = current_window.current_step;
        var current_query_number = parseInt(readStepID(step_id)[0]);
        var step_keys = current_step.query.step_keys;
        
        // get the index of the current step in the step_keys dictionary
        var index = current_step.query.getKeysIndex(current_step.stepnumber);
        var initial = index;
        
        // exit the loop when the step doesn't have a nested step in it
        while (index > 1 && hasNested(step_keys, index - 1)){
            index -= 1;        
        }
        
        // if the step found has the initial step nested inside, go to
        // the previous query if it exists. otherwise, go back to the initial step
        var query_index = previousHelper(step_keys, initial, index, current_query_number);
        current_query_number = query_index[0];
        index = query_index[1];

        var query = current_window.queries[current_query_number];
        if (query)
            query.steps_dictionary[query.step_keys[index - 1]].loadStep();
    }
}

function stepBack(){
    var step_id = current_window.current_step_id;
    if (step_id == ""){
        return;
    }
    if (isFirstStep(step_id)){
        return;
    } else {
        var current_step = current_window.current_step;
        var current_query_number = parseInt(readStepID(step_id)[0]);
        var step_keys = current_step.query.step_keys;
        
        // get the index of the current step in the step_keys dictionary
        var index = current_step.query.getKeysIndex(current_step.stepnumber);

        // if the initial step is the first part of a nested step (ex. 2.1.)
        // step out of the nested component and go to the next one on the same level
        if (index > 1 && hasNested(step_keys, index - 1) && differentLevels(step_keys, index, index - 1)){
            while (index > 1 && hasNested(step_keys, index - 1)){
                index -= 1;
            }
        }
        
        var initial = index;

        // move to the previous step on the same depth
        while (index > 1 && differentLevels(step_keys, initial, index - 1)){
            index -= 1;
        }

        // if the step found has the initial step nested inside, go to
        // the previous query if it exists. otherwise, go back to the initial step
        var query_index = previousHelper(step_keys, initial, index, current_query_number);
        current_query_number = query_index[0];
        index = query_index[1];

        var query = current_window.queries[current_query_number];
        if (query)
            query.steps_dictionary[query.step_keys[index - 1]].loadStep();
    }
}

function stepNext(){
    var step_id = current_window.current_step_id;
    if (step_id == ""){
        var first_query = current_window.queries[0];
        first_query.steps_dictionary[first_query.step_keys[0]].loadStep();
        return;
    }
    if (isLastStep(step_id)){
        return;
    } else {
        var current_step = current_window.current_step;
        var current_query_number = parseInt(readStepID(step_id)[0]);
        var step_keys = current_step.query.step_keys;
        
        // get the index of the current step in the step_keys dictionary
        var index = current_step.query.getKeysIndex(current_step.stepnumber);
        var initial = index;

        if (!isLastNested(step_keys, index)){
            // move to the next step on the same depth
            while (index < step_keys.length - 1 && differentLevels(step_keys, initial, index + 1)){
                index += 1;
            }
            if (nestedInside(step_keys, index, initial))
                initial = index;
        }

        // if there's no next step, then move to the next query
        if (index == initial && step_keys[index + 1] == undefined){
            index = -1;
            current_query_number += 1;
        }

        var query = current_window.queries[current_query_number];
        if (query)
            query.steps_dictionary[query.step_keys[index + 1]].loadStep();
    }
}

function stepIn(){
    var step_id = current_window.current_step_id;
    if (step_id == ""){
        var first_query = current_window.queries[0];
        first_query.steps_dictionary[first_query.step_keys[0]].loadStep();
        return;
    }
    if (isLastStep(step_id)){
        return;
    } else {
        var current_step = current_window.current_step;
        var current_query_number = parseInt(readStepID(step_id)[0]);
        var step_keys = current_step.query.step_keys;
        
        // get the index of the current step in the step_keys dictionary
        var index = current_step.query.getKeysIndex(current_step.stepnumber);
        
        // if there's no next step, then move to the next query
        if (step_keys[index + 1] == undefined){
            index = 0;
            current_query_number += 1;
            
            // Traverse into the innermost first step
            var next_query = current_window.queries[current_query_number].step_keys;
            
            while (index < next_query.length - 1 && hasNested(next_query, index + 1)){
                   index += 1;
               }
        } else {
            while (index < step_keys.length - 1 && hasNested(step_keys, index + 1)){
                index += 1;
            }
        }
        
        var query = current_window.queries[current_query_number];
        if (query)
            query.steps_dictionary[query.step_keys[index + 1]].loadStep();
    }
}

// navigation helper functions

function readStepID(step_id){
    var array = step_id.split("-");
    var query_number = array[0].slice(1);
    array.splice(0, 1);
    var step_number = array.join(".");
    return [query_number, step_number];
}

function isFirstStep(step_id){
    var parsed_id = readStepID(step_id);
    var query_number = parsed_id[0];
    var step_number = parsed_id[1];

    if (query_number == 0 && current_window.queries[0].step_keys[0] == step_number)
        return 1;
    return 0;
}

function isLastStep(step_id){
    var parsed_id = readStepID(step_id);
    var query_number = parsed_id[0];
    var step_number = parsed_id[1];

    var last_query_index = current_window.queries.length - 1;
    var last_query = current_window.queries[last_query_index];
    
    if (query_number == last_query_index && 
        last_query.step_keys[last_query.step_keys.length - 1] == step_number)
        return 1;
    return 0;
}

function previousHelper(step_keys, initial, index, current_query_number){
    if ((initial == index && initial == 0) || nestedInside(step_keys, initial, index) || (index == 1 && nestedInside(step_keys, initial, 0))){
        index = 0;
        if (current_query_number > 0){
            // move to the last step in the previous query
            current_query_number -= 1;
            index = current_window.queries[current_query_number].step_keys.length;
        } else {
            index = initial + 1;
        }
    }
    return [current_query_number, index];
}

