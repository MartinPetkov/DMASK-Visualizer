function drawLines(window){
    //clear all lines
    var bodybag = "#" + window.generateElemID("bodybag");
    $(bodybag).remove(".line");
    var border = $(bodybag + " .outbox").offset().left;

    // add the lines from the input table to the middle
    var first_top;
    var last_top;
    var input_containers = $(bodybag + " .input .tablecontainer");
    var i;
    for (i = 0; i < input_containers.length; i++){
        var container = $(input_containers[0]);
        var line = $($.parseHTML("<div class='line'></div>"));
        var right = container.offset().left + container.width();
        var top = container.offset().top + container.height() / 2;
        var width = border - right;
        line.css({left: right, top: top, width: width});
        $(bodybag).append(line);
        if (i == 0)
            first_top = top;
        last_top = top;
    }

    // add a vertical line from the first input to the last
    // add a horizontal line from the middle of the inputs to the output
    // add an arrowhead
}
