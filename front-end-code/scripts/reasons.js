function Reasons(){
    this.reasons = [];
}

function Reason(condition){
    this.condition = condition;
    this.subquery = undefined;
}

Reason.prototype.toDisplay = function(){
    // subqueries can be opened in a window by a onclick handler added later
    // the handler can easily find the step and row, and the span clicked will hold the condition
    if (this.subquery != undefined){
        return "<span class='subquery'>"+this.condition+"</span>";
    }
    return this.condition;
}

/*
    Given the id of a table row, display the reasons.
*/
function getReasons(row_id){
    // look up in reasons_dictionary
    // given: row and step number (later: maybe query number?)
    var reasons = $("#" + current_window.generateElemID("outbox") + " #"+row_id).val().reasons;
    if (reasons == undefined)
        return "";

    var i;

    var result = [];
    for (i = 0; i < reasons.length; i++){
        result.push(reasons[i].toDisplay());
    }

    if (result.length > 0)
        return "<p>" + result.join("</p><p>") + "</p>";
        
    return "";
    
    
}
