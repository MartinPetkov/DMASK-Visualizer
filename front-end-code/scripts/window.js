var main;
var base;

function Window(prefix, modal){
    this.prefix = prefix;
    this.toggled = 1;
    this.queries = [];
    this.current_step_id = "";
    this.current_step = undefined;
    this.modal = modal;
}

Window.prototype.generateBase = function() {
    var prefix = this.prefix;
    var copy = base.clone();

    if (this.modal != undefined){
        copy.attr("id", prefix + "-bodybag");
        copy.addClass("modalbag");
    }
    
    function prefixID(element){
        var id = element.attr("id");
        if (id){
            element.attr("id", prefix + "-" + id);
        }
    }

    copy.find("*").each(function(i, elem){
        prefixID($(elem));
    });
    
    return copy;
}

Window.prototype.gzzz = function(){
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
        html += "</div>";
        // Hovered Name
        html += "<div id='" + this.generateID('namebox') + "' class='namebox'></div>";
        html += "<div id='" + this.generateID('tablefooter') + "' class='tablefooter'>";
            //Toggle-able Temporary Tables
            html += "<div id='" + this.generateID('namespace') + "' class='namespace'>";
                html += "<div id='" + this.generateID('namespaceheader') + "' class='namespaceheader'>Namespace</div>";
                html += "<div id='" + this.generateID('namespacebody') + "' class='namespacebody'></div>";
            html += "</div>";
            html += "<div id='" + this.generateID('inventory') + "' class='inventory'>";
            html += "<div id='" + this.generateID('inventoryheader') + "' class='inventoryheader'>Tables and Views";
            html += "<div id='" + this.generateID('inventoryspace') + "' class=''>";
            html += "<div id='" + this.generateID('') + "' class=''>";
    html += "<div id='" + this.generateID('') + "' class=''>";
}

Window.prototype.generateElemID = function(elem_class){
    if (this.prefix === "")
        return elem_class;
    return this.prefix + "-" + elem_class
}

function openModalWindow(prefix){
    var new_window = new Window(prefix, "modal");
    var shadow = $("<div>", {id:new_window.generateElemID("shadow"), class: "shadow"});
    var old = $("#" + current_window.generateElemID("bodybag"));
    old.append(shadow);
    old.append(new_window.generateBase());
    current_window = new_window;
}
