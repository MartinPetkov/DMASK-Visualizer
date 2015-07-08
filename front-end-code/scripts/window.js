function Window(prefix){
    this.prefix = prefix;
    
}

Window.prototype.generateBase = function(){
    var html = "";
    
    // Set up basic template
    html += "<div id='" + this.generateID('bodybag') + "' class='bodybag'>";

    // Table of Contents
    html += "<div id='" + this.generateID('leftbar') + "' class='leftbar'>";
        html += "<div id='" + this.generateID('toc') + "' class='toc'>";
            html += "<table id='" + this.generateID('steps') + "' class='steps'></table></div>";

    // Navigation Bar
    html += "<div id='" + this.generateID('navbar') + "' class='navbar'>";
        html += "<div id='stepout' class='navigation'><img src='icons/out.png'></div>";
        html += "<div id='back' class='navigation'><img src='icons/back.png'></div>";
        html += "<div id='next' class='navigation'><img src='icons/next.png'></div>";
        html += "<div id='stepin' class='navigation'><img src='icons/in.png'></div>";
    html += "</div></div>";

    // Display (right side)
    html += "<div id='" + this.generateID('workspace') + "' class='workspace'>";
        html += "<div id='" + this.generateID('tablespace') + "' class='tablespace'>";
            // Input
            html += "<div id='" + this.generateID('inbox') + "' class='inbox'></div>";
            
            // Output
            html += "<div id='" + this.generateID('outbox') + "' class='outbox'></div>";
    html += "<div id='" + this.generateID('') + "' class=''>";
    html += "<div id='" + this.generateID('') + "' class=''>";
    html += "<div id='" + this.generateID('') + "' class=''>";
    html += "<div id='" + this.generateID('') + "' class=''>";
}

Window.prototype.generateID = function(elem_class){
    return this.prefix + "-" + elem_class
}
