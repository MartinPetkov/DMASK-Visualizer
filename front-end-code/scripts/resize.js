var MainWindow = {
    body: "#bodybag",
    content: "#content",
    leftbar: "#leftbar",
    steps: "#steps",
    navbar: "#navbar",
    toc: "#toc",
    tablespace: "#tablespace",
    workspace: "#workspace",
    inbox: "#inbox",
    outbox: "#outbox",
    namebox: "#namebox",
    inventory: "#inventory",
    inventoryheader: "#inventoryheader",
    inventoryspace: "#inventoryspace",
    tables_dictionary: [],
    reasons_dictionary: [],
    step_keys: [],
    steps_dictionary: [],
    current_step: 0,
    toggled: 0
};

var ModalWindow = {
    body: "#modalwindow",
    content: "#modal-content",
    leftbar: "#modal-leftbar",
    steps: "#modal-steps",
    navbar: "#modal-navbar",
    toc: "#modal-toc",
    tablespace: "#modal-tablespace",
    workspace: "#modal-workspace",
    inbox: "#modal-inbox",
    outbox: "#modal-outbox",
    namebox: "#modal-namebox",
    inventory: "#modal-inventory",
    inventoryheader: "#modal-inventoryheader",
    inventoryspace: "#modal-inventoryspace",
    tables_dictionary: [],
    reasons_dictionary: [],
    step_keys: [],
    steps_dictionary: [],
    current_step: 0,
    toggled: 0
};

var currentWindow = MainWindow;

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
    $(window.tablespace).height(updateHeight(window));
    var tableheight = $(window.tablespace).height();
    $(window.inbox + ' .input').height(updateInputHeight(tableheight, window));
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
    if (!currentWindow.toggled){
        newheight = $(window.workspace).height() - $(window.namebox).height() - $(window.inventoryheader).height();
    } else {
        newheight = $(window.workspace).height() - $(window.namebox).height() - $(window.inventory).height();
    }
    return newheight;
}

// Toggle the inventory's appearance
function toggleInventory(window){
    currentWindow.toggled = 1 - currentWindow.toggled;
    var newheight = updateHeight(window);
    $(window.tablespace).animate({height: newheight});
    $(window.inbox + ' .input').animate({height: updateInputHeight(newheight, window)});
    $("#tooltip").hide();
}

