function Reasons(){
    this.reasons = [];
}

Reasons.prototype.toDisplay = function(){
    var i;
    var result = [];
    for (i = 0; i < this.reasons.length; i++){
        result.push(this.reasons[i].toDisplay());
    }
    
    return "<p>" + result.join("</p><p>") + "</p>";
}

Reasons.prototype.getSubquery = function(subquery){
    var i;
    for (i = 0; i < this.reasons.length; i++){
        if (this.reasons[i].condition == subquery)
            return this.reasons[i].subquery;
    }
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
