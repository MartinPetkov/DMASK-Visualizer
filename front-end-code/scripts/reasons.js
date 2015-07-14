function Reason(condition){
    this.condition = condition;
    this.subquery = undefined;
}

Reason.prototype.toDisplay = function(){
    // subqueries can be opened in a window by a onclick handler added later
    // the handler can easily find the step and row, and the span clicked will hold the condition
    if (this.subquery != undefined){
        return "<span class='subquery'>"+this.condition+"</span>";
    }
    return this.condition;
}

function generateReasons(){
    var step;
    var i = 0;
    for (i = 0; i < currentWindow.step_keys.length; i++){
        step = currentWindow.steps_dictionary[currentWindow.step_keys[i]][5];   // The output of the step (since it might not be the same as the step, ex. 1.1 vs 1.1.2)
        var reasons = currentWindow.steps_dictionary[step][2];
        
        var j;
        var shared_reasons = [];

        // gather all shared reasons (row = 0)
        for (j = 0; j < reasons.length; j++){
            var reasons_object = JSON.parse(reasons[j].conditions_matched);
            if (reasons[j].row == 0){
                var matched_conditions = reasons_object.conditions_matched
                var k;
                for (k = 0; k < matched_conditions.length; k++){
                    var reason = new Reason(matched_conditions[k]);
                    if (reasons_object.subqueries[matched_conditions[k]] != undefined){
                        reason.subquery = JSON.parse(reasons_object.subqueries[matched_conditions[k]]);
                    }
                    shared_reasons.push(reason);
                }
            }
        }

        // add all shared reasons to the every row
        for (j = 1; j < currentWindow.reasons_dictionary[step].length; j++){
            currentWindow.reasons_dictionary[step][j] = shared_reasons.slice();
        }

        // get the remaining reasons (row != 0)
        for (j = 0; j < reasons.length; j++){
            var reasons_object = JSON.parse(reasons[j].conditions_matched);
            if (reasons[j].row != 0){
                var row = reasons[j].row;
                var matched_conditions = reasons_object.conditions_matched;
                var k;
                for (k = 0; k < matched_conditions.length; k++){
                    var reason = new Reason(matched_conditions[k]);
                    if (reasons_object.subqueries[matched_conditions[k]] != undefined){
                        reason.subquery = JSON.parse(reasons_object.subqueries[matched_conditions[k]]);
                    }
                    currentWindow.reasons_dictionary[step][row].push(reason);
                }
            }
        }
    }
}

/*
    Given the id of a table row, display the reasons.
*/
function getReasons(row_id){
    // look up in reasons_dictionary
    // given: row and step number (later: maybe query number?)
    var reasons = getReasonsEntry(row_id);
    var i;

    var result = [];
    for (i = 0; i < reasons.length; i++){
        result.push(reasons[i].toDisplay());
    }

    if (result.length > 0)
        return "<p>" + result.join("</p><p>") + "</p>";
        
    return "";
    
    
}


/*
    Given the id of a table row, return the reasons (lookup in the dictionary)
*/
function getReasonsEntry(row_id){
    var steprow = getStepRow(row_id);
    var step = steprow.step;
    var row = steprow.row;
    return current_window.current_step.query.reasons_dictionary[step][row];
}

/*
    Given a tr id (row-n-step-x), return an object containing the row and step
    (so result.row = n
        result.step = x)
*/
function getStepRow(row_id){
    var split_id = row_id.split("-");
    var row = split_id[1];
    var step = split_id.splice(3).join(".");
    return {"row":row, "step":step};
}
