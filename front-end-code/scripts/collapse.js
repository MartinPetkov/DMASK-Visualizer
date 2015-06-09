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

function collapse(parent){
    jQuery($("#"+parent).find(".nested")[0]).hide();
};

function expand(parent){
    jQuery($("#"+parent).find(".nested")[0]).show();
};

function collapseAll(){
    $(".step").each(function(){collapse(this.id)});
    $(".collapsible").html("[+]");
}

