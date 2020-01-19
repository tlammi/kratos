
function load_table(id, uri){
    let tableref = document.getElementById(id);
    fetch(uri).then(
        function(response){
            return response.text();
        }
    ).then(function(html){
        tableref.innerHTML = html;
    });
}

function loadtables() {
    load_table("competition_list_table", "tables/competitions");
    load_table("competitor_table", "tables/competitors");
    load_table("current_competition_table", "tables/current_competition");
}

function start(){
    loadtables();
    let browser = navigator.userAgent.toLocaleLowerCase()
                    .indexOf("firefox") > -1 ? "firefox" : "other";
    if(browser == "firefox"){
        document.head.innerHTML += '<link rel="stylesheet" href="/css/firefox.css">'
    }
}

window.onload = start();
// Handles tab button press by opening a corresponding tab
function opentab(event, tabname) {
    function hide_tabs() {
        var tabs = document.getElementsByClassName("tab");
        for (var i=0; i < tabs.length; i++){
            tabs[i].style.display="none";
        }
    }

    function reset_tabbuttons(){
        var tabbuttons = document.getElementsByClassName("toolchain")[0]
                                    .getElementsByClassName("tabbuttonholder")[0]
                                    .getElementsByTagName("button");

        for(var i=0; i < tabbuttons.length; i++){
            tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
        }

    }

    function show_tab(tabname){
        document.getElementById(tabname).style.display = "block";
    }

    function activate_button(targetbutton){
        targetbutton.className += " active";
    }

    hide_tabs();
    reset_tabbuttons();
    show_tab(tabname);
    activate_button(event.currentTarget);
}

$("#MyTable tbody tr").click(function () {
    $(this).addClass("selected").siblings().removeClass("selected")
});
$("#MyTable tr td").keypress(function (event) {
    if (event.which === 13) {
        var x = this.cellIndex;
        var y = this.parentNode.rowIndex;
        var text = $(this).text()
        $.post("/postcell", {
            "x": x,
            "y": y,
            "text": text
        })
        console.log("Enter pressed: (" + x + ", " + y + ")" + " " + text);
        return false;
    }
});

function add_lifter() {
    console.log("Add lifter pressed");
    $.post("/postnewline")
};

function remove_lifter() {
    var selected_line = document.getElementsByClassName("selected")[0]
    if (selected_line) {
        console.log("Remove lifter pressed: " + selected_line.rowIndex);
        $.post("/postpopline", {
            "index": selected_line.rowIndex
        });
    }
};
