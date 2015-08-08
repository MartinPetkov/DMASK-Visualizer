function Reasons(){
    this.reasons = [];
    this.conditions = [];
}

Reasons.prototype.toDisplay = function(){
    var i;
    var result = [];
    for (i = 0; i < this.conditions.length; i++){
        result.push(fail(this.conditions[i]));
    }
    
    for (i = 0; i < this.reasons.length; i++){
        result[result.indexOf(fail(this.reasons[i].condition))] = this.reasons[i].toDisplay();
    }
    
    return "<p>" + result.join("</p><p>") + "</p>";
}

function fail(condition){
    return "<span class='failed'>"+condition+"</span>";
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
    this.passed_subqueries = undefined;
}

Reason.prototype.toDisplay = function(){
    // subqueries can be opened in a window by a onclick handler added later
    // the handler can easily find the step and row, and the span clicked will hold the condition
    var classes = [];
    var kept = "passed";
    
    if (this.subquery != undefined){
        classes.push("subquery")
        if (this.uncorrelated)
            kept = "uncorrelated";
        else if (this.passed_subqueries && this.passed_subqueries.indexOf(this.condition) == -1)
            kept = "failed";
    }
    
    classes.push(kept);
    return "<span class='"+classes.join(" ")+"'>" + this.condition + "</span>";
}
