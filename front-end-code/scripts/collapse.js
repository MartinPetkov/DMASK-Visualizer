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
    jQuery($("#"+parent).find(".nested")[0]).hide();
};

/*
    Expand a given tr
*/
function expand(parent){
    jQuery($("#"+parent).find(".nested")[0]).show();
};

/*
    Collapse all steps
*/
function collapseAll(){
    $(".step").each(function(){collapse(this.id)});
    $(".collapsible").html("[+]");
}

/*
    Expand all steps
*/
function expandAll(){
    $(".step").each(function(){expand(this.id)});
    $(".collapsible").html("[-]");

}
