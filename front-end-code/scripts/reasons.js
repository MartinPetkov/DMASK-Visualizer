// only one subquery will be shown at a time, so their dictionary can be different
// alternatively, make a class for a window to store its information
// andddddddd we still need to separate queries, so maybe classes for those too
// or simpler: the step keys will be labelled "q1-1-1-1-" where q1 is the query number
// subqueries will be "sq1-1-1-1"


// GOALS: design the div
// div appears on row click @ location clicked
// list all the reasons as specified below
// queries will be underlined
// clicking on a query will load (provides step, row, and query)

function generateReasons(row_id){
    if (step.reasons.length > 0){
        // add the steps to the steps div
        // for all conditions in [0], every div will display that condition
        // conditions in [n] are listed for row [n]
        console.log(step.reasons);
        var universal_reasons = "";
        var rows = Object.keys(step.reasons).sort();
        var reasons = [];
        var i;
        for (i = 0; i < rows.length; i++){
            if (rows[i] == 0){
                universal_reasons += JSON.parse(step.reasons[0].conditions_matched).conditions_matched.join("<br>");
            }
            else {
                reasons[rows[i]] = universal_reasons + JSON.parse(step.reasons[rows[i]].conditions_matched).conditions_matched.join("<br>");
            }
        }
    }   
}
