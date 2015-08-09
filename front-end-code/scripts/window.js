var main;
var base;

function Window(prefix, modal, parent){
    this.prefix = prefix;
    this.toggled = 1;
    this.queries = [];
    this.current_step_id = "";
    this.current_step = undefined;
    this.modal = modal;
    this.parent = parent;
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

Window.prototype.generateElemID = function(elem_class){
    if (this.prefix === "")
        return elem_class;
    return this.prefix + "-" + elem_class
}

function openModalWindow(prefix){
    var new_window = new Window(prefix, "modal-"+generateModalNumber(), current_window);
    var shadow = $("<div>", {id:new_window.generateElemID("shadow"), class: "shadow"});
    var old = $("#" + current_window.generateElemID("bodybag"));
    old.append(shadow);
    old.append(new_window.generateBase());
    current_window = new_window;
}

function closeModalWindow(){
    var parent = current_window.parent;
    $("#" + current_window.generateElemID("bodybag")).remove();
    $("#" + current_window.generateElemID("shadow")).remove();
    current_window = parent;
    $("#tooltip").hide();
    sizeContent();
}

var modal_index = 0;
function generateModalNumber(){
    modal_index += 1;
    return modal_index;
}
