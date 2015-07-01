// Initial load of page
$(document).ready(onPageLoad);

// Every resize of window
$(window).resize(sizeContent);

function onPageLoad(){
    sizeContent();
    parseAndLoad(parsedquery);

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
    $("#inbox, #modal-inbox").on("click", ".tablecontainer", function(e){
        var id = e.target.closest(".tablecontainer").id;
        var stepid = getStepIDFromTable(id);
        if (currentWindow.steps_dictionary[toKey(stepid)])
            loadStep(stepid);
    });

    // -- 'Reasons' box handler
    $("#outbox, #modal-outbox").on("click", ".output-row", function(e){
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

    $(document).on("click", "#modalcontainer", function(e){
        if (e.target.id == "modalcontainer"){
            $("#modalcontainer").hide();
            currentWindow = MainWindow;
            $("#tooltip").hide();
        }
    });

}

/*
    Adjusts the hovertext display
*/
function hoverText(newtext){
    $(currentWindow.namebox).text(newtext);
}

/*
    Input: An array of parsedqueries
*/
function parseAndLoad(parsedquery){
    // Parse the JSON content and load them into the ToC
    var i = 0;
    for (i = 0; i < parsedquery.length; i++){
        currentWindow.steps_dictionary = stepsToDict(parsedquery[i].steps);
        currentWindow.step_keys = Object.keys(currentWindow.steps_dictionary).sort();
        parseTablesToDict(global_tables);
        parseTablesToDict(parsedquery[i].tables);
        generateReasons();
        loadQuery(parsedquery[i].query_text);
        loadSteps(currentWindow.steps_dictionary);
    }
}

