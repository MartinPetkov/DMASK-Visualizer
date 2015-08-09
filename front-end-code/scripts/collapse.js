/*
    Given the collapsible div, produce the appropriate response.
*/
function collapseHandler(collapsible){
    var parent = collapsible.closest("tr");
    if (jQuery(collapsible).html() == "[-]"){
        collapse(parent.id);
        jQuery(collapsible).html("[+]");
    }
    else{
        expand(parent.id);
        jQuery(collapsible).html("[-]");
    }
}

/*
    Collapse a given tr
*/
function collapse(parent){
    var prefix = "#" + current_window.generateElemID("leftbar") + " ";
    jQuery($(prefix + "#"+parent).find(".nested")[0]).hide();
};

/*
    Expand a given tr
*/
function expand(parent){
    var prefix = "#" + current_window.generateElemID("leftbar") + " ";
    jQuery($(prefix + "#"+parent).find(".nested")[0]).show();
};

/*
    Collapse all steps
*/
function collapseAll(){
    var prefix = "#" + current_window.generateElemID("leftbar") + " ";
    $(prefix + ".step").each(function(){collapse(this.id)});
    $(prefix + ".collapsible").html("[+]");
}

/*
    Expand all steps
*/
function expandAll(){
    var prefix = "#" + current_window.generateElemID("leftbar") + " ";
    $(prefix + ".step").each(function(){expand(this.id)});
    $(prefix + ".collapsible").html("[-]");

}
