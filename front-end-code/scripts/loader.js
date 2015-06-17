var toggled = 0;
var current_step;
var steps_dictionary;
var step_keys;
var tables_dictionary = [];
var reasons_dictionary = [];

// Initial load of page
$(document).ready(onPageLoad);

// Every resize of window
$(window).resize(sizeContent);

function onPageLoad(){
    sizeContent();
    parseAndLoad();

    // add event handlers
    // -- ToC Handlers (Collapsing, clicking on steps)
    $(document).on("click", ".collapsible", function(e){
        collapseHandler(e.target);
    });
    collapseAll();

    $(document).on("click", ".step", function(e){
        if (!jQuery(e.target).hasClass("collapsible"))
            var step = jQuery(e.target.closest("tr"));
            var id = step[0].id;
            loadStep(id);
    });

    // -- Navigation handlers (stepping through)
    $(document).on("click", "#stepout", stepOut);
    $(document).on("click", "#back", stepBack);
    $(document).on("click", "#next", stepNext);
    $(document).on("click", "#stepin", stepIn);

    // -- Table handlers
    $("#inbox").on("click", ".tablecontainer", function(e){
        var id = e.target.closest(".tablecontainer").id;
        var stepid = getStepIDFromTable(id);
        if (steps_dictionary[toKey(stepid)])
            loadStep(stepid);
    });

    // -- 'Reasons' box handler
    $("#outbox").on("click", ".output-row", function(e){
        var id = e.target.closest(".output-row").id;
        console.log(id);
    });

    loadStep(step_keys[0]);
}

/*
    Adjusts the hovertext display
*/
function hoverText(newtext){
    $('#namebox').text(newtext);
}

/*
    Temporary function to load a single parsed query
*/
function parseAndLoad(){
    // Parse the JSON content and load them into the ToC
    steps_dictionary = stepsToDict(parsedquery.steps);
    step_keys = Object.keys(steps_dictionary).sort();
    parseTablesToDict(global_tables);
    parseTablesToDict(parsedquery.tables);
    loadQuery(parsedquery.query_text);
    loadSteps(steps_dictionary);
}
