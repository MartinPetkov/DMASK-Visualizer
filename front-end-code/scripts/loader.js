// Initial load of page
$(document).ready(onPageLoad);

// Every resize of window
$(window).resize(sizeContent);

var current_window;

function loadQueries(queries){
    // Parse the JSON content and load them into the current window's ToC
    var toc = $("#" + current_window.generateElemID("steps"));
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

    $(document).on("click", ".stepout", stepOut);
    $(document).on("click", ".back", stepBack);
    $(document).on("click", ".next", stepNext);
    $(document).on("click", ".stepin", stepIn);

    // -- 'Reasons' box handler
    $(document).on("click", ".inbox .output-row", function(e){
        var id = e.target.closest(".output-row").id;
        var reasons = $("#" + current_window.generateElemID("inbox") + " #" + id).val();
        var tooltip = $("#tooltip");
        // ---
        if (reasons){
            tooltip.css( {position:"absolute", top:e.pageY, left: e.pageX});
            tooltip.html("<p class='tooltipheader'>Reasons</p>" + reasons.toDisplay());
            tooltip.show();
            tooltip.val(reasons);
            
        } else{
            tooltip.hide();
        }
    });

    // -- Subquery onclick handler
    $(document).on("click", ".subquery", function(e){
        var tooltip = $("#tooltip");
        var reasons = tooltip.val();
        var reason = e.target.textContent;
        var subquery = reasons.getSubquery(reason);
        openModalWindow("modal");
        loadQueries([subquery]);
        sizeContent();
    });

    $(document).on("click", ".shadow", closeModalWindow);

}

/*
    Adjusts the hovertext display
*/
function hoverText(newtext){
    $("#" + current_window.generateElemID("namebox")).text(newtext);
}
