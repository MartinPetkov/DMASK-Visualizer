//Dynamically assign height
function sizeContent() {

    $("#tooltip").hide();

    // center modalwindow
    $('#modalwindow').css({
        top: ($('#modalcontainer').height() - $('#modalwindow').outerHeight())/2,
        left: ($('#modalcontainer').width() - $('#modalwindow').outerWidth())/2
    });
    
    adjustHeight(MainWindow);
    adjustHeight(ModalWindow);
    adjustNamespace();
}

function adjustNamespace(){
    $("#" + current_window.generateElemID("namespacebody")).height($("#" + current_window.generateElemID("namespace")).height() - $("#" + current_window.generateElemID("namespaceheader")).outerHeight());
}

function adjustHeight(window){
    var newHeight = $(window.body).height();
    $(window.content).css("height", newHeight);
    
    // Update the height of the Table of Contents
    var newheight = $(window.leftbar).height() - $(window.navbar).height();
    $(window.toc).height(newheight);

    // Update the height of the table display area
    updateTableDisplay(window);
}

// Update the height of the table display area
function updateTableDisplay(window){
    $(window.tablespace).height($(window.workspace).height() - $(window.namebox).height() - $(window.tablefooter).height());
    var tableheight = $(window.tablespace).height();
    $(window.inbox + ' .input').height(updateInputHeight(tableheight, window));
    if (window.toggled == 1){
        $(window.inventory).height($(window.tablefooter).height());
    }
}

// Return the height for the input tables
function updateInputHeight(maxheight, window){
    var numberOfTables = $(window.inbox + ' .input').length;
    if (numberOfTables == 0)
        numberOfTables = 1;
    return (maxheight / numberOfTables);
}

// Return the new height of the table display area (accounting for inventory toggle)
function updateHeight(window){
    var newheight;
    if (!current_window.toggled){
        newheight = $(window.workspace).height() - $(window.namebox).height() - $(window.inventoryheader).height();
    } else {
        newheight = $(window.workspace).height() - $(window.namebox).height() - $(window.inventory).height();
    }
    return newheight;
}

// Toggle the inventory's appearance
function toggleInventory(window){
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

