// needs to be refactored

//Dynamically assign height
function sizeContent() {

    $("#tooltip").hide();

    var window = current_window;
    while (window != undefined){
        adjustHeight(window);
        centerWindow(window);
        adjustInventory(window);
        adjustNamespace(window);
        drawLines(window);
        window = window.parent;
    }
}

function centerWindow(window){
    var container = $("#" + window.generateElemID("shadow"));
    if (window.parent != undefined){
        container = $("#" + window.parent.generateElemID("bodybag"));
    }
    $("#" + window.generateElemID("bodybag")).css({
        top: (container.height() - $("#" + window.generateElemID("bodybag")).outerHeight())/2,
        left: (container.width() - $("#" + window.generateElemID("bodybag")).outerWidth())/2
    });
}

function adjustNamespace(window){
    $("#" + window.generateElemID("namespacebody")).height($("#" + window.generateElemID("namespace")).height() - $("#" + window.generateElemID("namespaceheader")).outerHeight());
}

function adjustHeight(window){
    var newHeight = $("#" + window.generateElemID("bodybag")).height();
    
    // Update the height of the Table of Contents
    var newheight = $("#" + window.generateElemID("leftbar")).height() - $("#" + window.generateElemID("navbar")).height();
    $("#" + window.generateElemID("toc")).height(newheight);

    // Update the height of the table display area
    updateTableDisplay(window);
}

// Update the height of the table display area
function updateTableDisplay(window){
    $("#" + window.generateElemID("tablespace")).height($("#" + window.generateElemID("workspace")).height() - $("#" + window.generateElemID("namebox")).height() - $("#" + window.generateElemID("tablefooter")).height());
    var tableheight = $("#" + window.generateElemID("tablespace")).height();
    $("#" + window.generateElemID("inbox") + ' .input').height(updateInputHeight(tableheight, window));
    if (window.toggled == 1){
        $("#" + window.generateElemID("inventory")).height($("#" + window.generateElemID("tablefooter")).height());
    }
}

// Return the height for the input tables
function updateInputHeight(maxheight, window){
    var numberOfTables = $("#" + window.generateElemID("inbox") + ' .input').length;
    if (numberOfTables == 0)
        numberOfTables = 1;
    return (maxheight / numberOfTables);
}

// Return the new height of the table display area (accounting for inventory toggle)
function updateHeight(window){
    var newheight;
    if (!window.toggled){
        newheight = $("#" + window.generateElemID("workspace")).height() - $("#" + window.generateElemID("namebox")).height() - $("#" + window.generateElemID("inventoryheader")).height();
    } else {
        newheight = $("#" + window.generateElemID("workspace")).height() - $("#" + window.generateElemID("namebox")).height() - $("#" + window.generateElemID("inventory")).height();
    }
    return newheight;
}

// Toggle the inventory's appearance
function toggleInventory(){
    var newheight;
    if (current_window.toggled == 1){
        newheight = $("#" + current_window.generateElemID("inventoryheader")).height();
    } else {
        newheight = $("#" + current_window.generateElemID("tablefooter")).height();
    }
    $("#" + current_window.generateElemID("inventory")).animate({height: newheight});
    $("#tooltip").hide();
    current_window.toggled = 1 - current_window.toggled;
}

function adjustInventory(window){
    var newheight;
    if (window.toggled != 1){
        newheight = $("#" + window.generateElemID("inventoryheader")).height();
    } else {
        newheight = $("#" + window.generateElemID("tablefooter")).height();
    }
    $("#" + window.generateElemID("inventory")).height(newheight);
}
