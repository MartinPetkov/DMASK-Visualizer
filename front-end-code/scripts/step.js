function Step(s, query){
    this.stepnumber = s.step_number;
    this.sql = s.sql_chunk;
    this.input_ids = s.input_tables;
    this.reasons = s.reasons;
    this.namespace = s.namespace;
    this.result_name = s.res_table_name;
    this.result_id = s.result_table;
    
    this.query = query;
}

/*
    Look-up and return the input tables
*/
Step.prototype.getInputTables = function(){
    var tables = [];
    var i;
    var id_length = this.input_ids.length;
    
    for (i = 0; i < id_length; i++){
        tables.push(this.query.tables_dictionary[this.input_ids[i]]);
    }
    
    return tables;
}

Step.prototype.getInputHTML = function(){
    var tables = this.getInputTables();
    
    var html = [];
    var i;
    for (var i = 0; i < tables.length; i++){
        var container = $.parseHTML("<div class='input'></div>");
        $(container).append(tables[i].toDisplay());
        html.push(container);
    }    
    return html;
}

Step.prototype.getOutputHTML = function(){
    var output = this.query.tables_dictionary[this.result_id];
    var container = $.parseHTML("<div class='output'></div>");
    $(container).append(output.toDisplay());
    return container;
}

Step.prototype.loadStep = function(){
    // hide the tooltip
    $("#tooltip").hide();

    // update the current step
    current_window.current_step_id = this.query.getStepID(this.query.getKeysIndex(this.stepnumber));
    current_window.current_step = this;
    
    // update the current bolded step
    var toc = "#" + current_window.generateElemID("toc");
    $(toc + " .step").removeClass("selected");

    var step = $(toc + " #" + this.query.getStepID(this.query.getKeysIndex(this.stepnumber)));
    step.addClass("selected");

    // expand parent steps
    expandParentCells(step);
    
    // update the input
    var input = this.getInputHTML();
    var inbox = $("#" + current_window.generateElemID("inbox"));
    inbox.empty();
    var i;
    for (i = 0; i < input.length; i++){
        inbox.append(input[i]);
    }

    // update the output
    var output = this.getOutputHTML();
    var outbox = $("#" + current_window.generateElemID("outbox"));
    outbox.empty();
    outbox.append(output);

    // update the namespace
    updateNamespace(this);

    // update the screen size
    sizeContent();
}

function expandParentCells(step){
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
}

function updateNamespace(step){
    // If there's nothing in the namespace, traverse backwards until
    // there is one
    var namespace = step.namespace;
    var query = step.query;
    if (namespace.length < 1){
        var index = query.getKeysIndex(step.stepnumber);
        
        while (index > 0 && namespace.length < 1){
            index -= 1;
            namespace = query.steps_dictionary[query.step_keys[index]].namespace;
        }
    }

    var namespacebody = $("#" + current_window.generateElemID("namespacebody"));
    namespacebody.empty();
    namespacebody.append(namespaceToString(namespace));
}

function namespaceToString(namespace){
    // Given a namespace in the format [(name, [columns]), (...)], return
    // the string equivalent ("Name: columns")
    var i;
    namespace_list = [];
    for (i = 0; i < namespace.length; i++){
        item = namespace[i];
        table_name = item[0];
        columns = item[1];
        string = table_name + ": " + (columns.join(", "));
        namespace_list.push(string);
    }
    return namespace_list.join("<br>");
}
