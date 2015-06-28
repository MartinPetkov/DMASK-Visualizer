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
            if (step != undefined){
                var id = step[0].id;
                loadStep(id);
            }
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
        if (currentWindow.steps_dictionary[toKey(stepid)])
            loadStep(stepid);
    });

    // -- 'Reasons' box handler
    $("#outbox").on("click", ".output-row", function(e){
        var id = e.target.closest(".output-row").id;
        var reasons = getReasons(id);
        var tooltip = $("#tooltip");
        // ---
        if (reasons != ""){
            tooltip.css( {position:"absolute", top:e.pageY, left: e.pageX});
            tooltip.html("<p class='tooltipheader'>Reasons</p>" + getReasons(id));
            tooltip.show();
            tooltip.val(id);
            
        } else{
            tooltip.hide();
        }
    });

    // -- Subquery onclick handler
    $(document).on("click", ".subquery", function(e){
        var tooltip = $("#tooltip");
        var id = tooltip.val();
        var reason = getReasonsEntry(id)[0];
        openModalWindow(reason.subquery);
    });

    loadStep(currentWindow.step_keys[0]);
}

/*
    Adjusts the hovertext display
*/
function hoverText(newtext){
    $(currentWindow.hovertext).text(newtext);
}

/*
    Temporary function to load a single parsed query
*/
function parseAndLoad(){
    // Parse the JSON content and load them into the ToC
    currentWindow.steps_dictionary = stepsToDict(parsedquery.steps);
    currentWindow.step_keys = Object.keys(currentWindow.steps_dictionary).sort();
    parseTablesToDict(global_tables);
    parseTablesToDict(parsedquery.tables);
    generateReasons();
    loadQuery(parsedquery.query_text);
    loadSteps(currentWindow.steps_dictionary);
}

/*
    MOVE THIS SOMEWHERE ELSE
*/
function openModalWindow(query){
    parsedquery = query;
    currentWindow = ModalWindow;
    $("#modalcontainer").show();
    parseAndLoad();
    sizeContent();
}
