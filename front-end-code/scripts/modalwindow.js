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
    tablefooter: "#tablefooter",
    namespacebody: "#namespacebody",
    namespace: "#namespace",
    namespaceheader: "#namespaceheader",
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
    tablefooter: "#modal-tablefooter",
    namespacebody: "#modal-namespacebody",
    namespace: "#modal-namespace",
    namespaceheader: "#modal-namespaceheader",
    tables_dictionary: [],
    reasons_dictionary: [],
    step_keys: [],
    steps_dictionary: [],
    current_step: 0,
    toggled: 0,
    clear: function(){
            this.tables_dictionary = [];
            this.reasons_dictionary = [];
            this.step_keys = [];
            this.steps_dictionary = [];
            this.current_step = 0;
            this.toggled = 0;
            $(this.steps).empty();
            $(this.inbox).empty();
            $(this.outbox).empty();
            $(this.inventoryspace).empty();
        }
};

var currentWindow = MainWindow;


function openModalWindow(query){
    currentWindow = ModalWindow;
    ModalWindow.clear();
    $("#modalcontainer").show();
    parseAndLoad([query]);
    sizeContent();
}
