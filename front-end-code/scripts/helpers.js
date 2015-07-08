/*
    Convert steps (2.1.1) into ids (2-1-1)
*/
function toID(id){
    return id.split(".").join("-");
}

/*
    Convert steps (2-1-1) into ids (2.1.1)
*/
function toKey(id){
    return id.split("-").join(".");
}


/*
    Check if the current step has nested components
*/
function hasNested(keys, i){
    if (i + 1 >= keys.length || keys[i+1].lastIndexOf(".") <= keys[i].lastIndexOf("."))
        return 0;
    return 1;
}

/*
    Check if the current step is the last in a nested group
*/
function isLastNested(keys, i){
    if (i + 1 >= keys.length || keys[i+1].lastIndexOf(".") >= keys[i].lastIndexOf("."))
        return 0;
    return 1;
}

function differentLevels(keys, i, j){
    if (keys[i].lastIndexOf(".") == keys[j].lastIndexOf("."))
        return 0;
    return 1;
}

/*
    Check if keys[i] is nested inside keys[j]
    Example: nestedInside("1.1.1", "1") == True
*/
function nestedInside(keys, i, j){
    if (differentLevels(keys, i, j) && keys[i].slice(0, keys[j].length) == keys[j])
        return 1;
    return 0;
}


/*
    Return the row number of a clicked output row
*/
function extractTableRow(id){
    var row = id.split("-");
    var rownumber = row[1];
    // var stepnumber = row.splice(3).join(".");
    return rownumber;
}

