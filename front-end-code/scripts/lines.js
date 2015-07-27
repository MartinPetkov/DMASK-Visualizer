function drawLines(window){
    //clear all lines
    var bodybag = "#" + window.generateElemID("bodybag");
    var canvas = "#" + window.generateElemID("canvas");
    $(canvas).empty();
    var border = $(bodybag + " .outbox").offset().left;

    // add the lines from the input table to the middle
    var first_top;
    var last_top;
    var input_containers = $(bodybag + " .input .tablecontainer");
    var i;
    for (i = 0; i < input_containers.length; i++){
        var container = $(input_containers[i]);
        var line = $($.parseHTML("<div class='line'></div>"));
        var right = container.offset().left + container.width();
        var top = container.offset().top + container.height() / 2;
        var width = border - right;
        line.css({left: right, top: top, width: width});
        $(canvas).append(line);
        if (i == 0)
            first_top = top;
        last_top = top;
    }

    // add a vertical line from the first input to the last
    if (first_top != last_top){
        var line = $($.parseHTML("<div class='line'></div>"));
        line.css({top: first_top, height: (last_top - first_top), left: border});
        $(canvas).append(line);
    }
    
    // add a horizontal line from the middle of the inputs to the output
    var output = $(bodybag + " .output .tablecontainer");
    if (input_containers.length > 0){
        var line = $($.parseHTML("<div class='line'></div>"));
        var top = output.offset().top + output.height() / 2;
        var width = output.offset().left - border;
        line.css({left: border, top: top, width: width});
        $(canvas).append(line);
        
        // add an arrowhead
        var arrow = $($.parseHTML("<div class='arrow'></div>"));
        arrow.css({left: output.offset().left - 11, top: top - 4});
        $(canvas).append(arrow);
    }    
}
