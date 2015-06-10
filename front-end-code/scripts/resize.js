//Dynamically assign height
function sizeContent() {
    var newHeight = $("html").height() - $("#header").height() - $("#footer").height() + "px";
    $("#content").css("height", newHeight);
    
    // Update the height of the Table of Contents
    var newheight = $("#leftbar").height() - $("#navbar").height();
    $("#toc").height(newheight);

    // Update the height of the table display area
    updateTableDisplay();
}

// Update the height of the table display area
function updateTableDisplay(){
    $("#tablespace").height(updateHeight());
    var tableheight = $("#tablespace").height();
    $('.input').height(updateInputHeight(tableheight));
}

// Return the height for the input tables
function updateInputHeight(maxheight){
    var numberOfTables = $('.input').length;
    if (numberOfTables == 0)
        numberOfTables = 1;
    return (maxheight / numberOfTables);
}

// Return the new height of the table display area (accounting for inventory toggle)
function updateHeight(){
    var newheight;
    if (!toggled){
        newheight = $("#workspace").height() - $("#namebox").height() - $("#inventoryheader").height();
    } else {
        newheight = $("#workspace").height() - $("#namebox").height() - $("#inventory").height();
    }
    return newheight;
}

// Toggle the inventory's appearance
function toggleInventory(){
    toggled = 1 - toggled;
    var newheight = updateHeight();
    $("#tablespace").animate({height: newheight});
    $('.input').animate({height: updateInputHeight(newheight)});
}

