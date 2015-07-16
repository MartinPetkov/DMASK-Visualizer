// Initial load of page
$(document).ready(onPageLoad);

// Every resize of window
$(window).resize(sizeContent);

var current_window;

function loadQueries(queries){
    // Parse the JSON content and load them into the current window's ToC
    var toc = $("#" + current_window.generateElemID("toc"));
    toc.empty();
    var i = 0;
    for (i = 0; i < queries.length; i++){
        var q = new Query(queries[i].steps, queries[i].tables, queries[i].query_text, i);
        current_window.queries.push(q);
        toc.append(q.toTOC());
    }
}

function onPageLoad(){
    base = $("#bodybag").clone();
    main = new Window("");
    current_window = main;

    loadQueries(parsedquery);
    sizeContent();

    // add collapse handlers
    $(document).on("click", ".collapsible", function(e){
        collapseHandler(e.target);
    });
    collapseAll();

    // add navigation handlers
    $(document).on("click", ".step", function(e){
        if (!jQuery(e.target).hasClass("collapsible"))
            var step = jQuery(e.target.closest("tr"));
            if (step != undefined){
                var step_object = step.val();
                step_object.loadStep();
            }
    });

    $(document).on("click", "#stepout", stepOut);
    $(document).on("click", "#back", stepBack);
    $(document).on("click", "#next", stepNext);
    $(document).on("click", "#stepin", stepIn);

    
//    parseAndLoad(parsedquery);

    // add event handlers
    // -- ToC Handlers (Collapsing, clicking on steps)


    // -- Navigation handlers (stepping through)

/*
    // -- Table handlers
    $("#inbox, #modal-inbox").on("click", ".tablecontainer", function(e){
        var id = e.target.closest(".tablecontainer").id;
        var stepid = getStepIDFromTable(id);
        if (currentWindow.steps_dictionary[toKey(stepid)])
            loadStep(stepid);
    });
*/

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

    $(document).on("click", ".shadow", closeModalWindow);

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

