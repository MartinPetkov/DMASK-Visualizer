function Query(steps, tables, query_text, query_number){
    this.query_text = query_text;
    this.steps_dictionary = this.addStepsToDictionary(steps);
    this.step_keys = Object.keys(this.steps_dictionary).sort();
    this.tables_dictionary = [];
    this.reasons_dictionary = [];
    this.number = query_number;
    this.addTablesToDictionary(global_tables);  // alternatively: take these out??
    this.addTablesToDictionary(tables);
}

Query.prototype.toTOC = function(){
    var querytext = "<tr><td class='query'>" + this.query_text;
    var steps_header = "<table class='nested'>";
    var steps_footer = "</table></td></tr>";

    // Parse the steps in the TOC
    var i;
    var key_length = this.step_keys.length;
    var allsteps = "";
    for (i = 0; i < key_length; i++){
        // Create the step header
        var step = "<tr id='" + this.getStepID(i) + "' class='step'><td>";

        // Add the collapsible div handler if needed
        var nested = hasNested(this.step_keys, i);
        if (nested)
            step += "<div class='collapsible'>[-]</div>";

        // Add the step and sql chunk
        step += this.step_keys[i] + "." + this.steps_dictionary[this.step_keys[i]].sql;

        if (nested)
            step += "<table class='nested'>";

        if (isLastNested(this.step_keys, i))
            step += "</table></td></tr>";

        allsteps += step;
    }

    // Set the value of each step in the DOM to the step object
    var toc = jQuery.parseHTML(querytext + steps_header + allsteps + steps_footer);
    for (i = 0; i < key_length; i++){
        $(toc).find("#" + this.getStepID(i)).val(this.steps_dictionary[this.step_keys[i]]);
    }

    return toc;
}

Query.prototype.getKeysIndex = function (stepnumber){
    return this.step_keys.indexOf(stepnumber);
}

Query.prototype.getStepID = function (index){
    return "q" + this.number + "-" + toID(this.step_keys[index]);
}


/*
    Given a set of tables (t), whose keys are names of other tables,
    parses and adds those new tables to dictionary

    Also calls on initializeTableReasons
*/
Query.prototype.addTablesToDictionary = function(t){
    var keys = Object.keys(t);
    var i;
    for (i = 0; i < keys.length; i++){
        this.tables_dictionary[keys[i]] = new Table(JSON.parse(t[keys[i]]), this);

        this.reasons_dictionary[keys[i]] = initializeTableReasons(JSON.parse(t[keys[i]]));
    }
}

/*
    Set the reasons for every step's rows to [].
*/
function initializeTableReasons(t){
    var num_rows = t.tuples.length;
    var i;
    var result_dict = [];
    for (i = 1; i <= num_rows; i++){
        result_dict[i] = [];
    }
    return result_dict;
}

/*
    Given an array of steps (JSON), parse them into a dictionary in the format:
    step_number : Step(...)
*/
Query.prototype.addStepsToDictionary = function(steps){
    var dict = [];
    var i;
    for (i = 0; i < steps.length; i++){
        var step = JSON.parse(steps[i]);
        var stepnumber = step.step_number;
        dict[stepnumber] = new Step(step, this);
    }
    return dict;
}
