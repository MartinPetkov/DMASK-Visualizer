var toggled = 0;
var steps_dictionary;
var tables_dictionary = [];

function updateInputHeight(maxheight){
    // Return the height for the input tables (50% if there are 2, 100% otherwise)
    var numberOfTables = $('.input').length;
    if (numberOfTables == 0)
        numberOfTables = 1;
    return (maxheight / numberOfTables);
}

function updateHeight(){
    // Return the new height of the table display area (accounting for the storage toggle)
    var newheight;
    if (!toggled){
        newheight = $("#workspace").height() - $("#namebox").height() - $("#inventoryheader").height();
    } else {
        newheight = $("#workspace").height() - $("#namebox").height() - $("#inventory").height();
    }
    return newheight;
}

function toggleInventory(){
    // Toggle the inventory's appearance
    toggled = 1 - toggled;
    var newheight = updateHeight();
    $("#tablespace").animate({height: newheight});
    $('.input').animate({height: updateInputHeight(newheight)});
}

function hoverText(newtext){
    // Adjusts the hovertext display
    $('#namebox').text(newtext);
}

//Initial load of page
$(document).ready(onPageLoad);

//Every resize of window
$(window).resize(sizeContent);

function onPageLoad(){
    sizeContent();
}

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

function updateTableDisplay(){
    // Update the height of the table display area
    $("#tablespace").height(updateHeight());
    var tableheight = $("#tablespace").height();
    $('.input').height(updateInputHeight(tableheight));
}

