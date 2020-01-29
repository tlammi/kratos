
/**
 * Helper class for managing HTML tables
 */
class Table {
    /**
     * Constructs a new HTML table inside the HTML element with the given ID.
     * @param {String} table_holder_id Container HTMl element where the table will be placed
     */
    constructor(table_holder_id){
        this.table_elem = document.createElement("table");
        document.getElementById(table_holder_id).appendChild(this.table_elem);
        let table_head = this.table_elem.createTHead();
        let header_row = document.createElement("tr");
        table_head.appendChild(header_row);
        this.table_elem.createTBody();

    };

    /**
     * Set the header of the table instance. Overwrites the old header.
     * 
     * @param {Array} header_data Header elements from left to right
     */
    set_header(header_data){
        let row = this.table_elem.tHead.children[0];
        while(row.children.length > 0)
            row.removeChild(row.children[0]);
        
        for(let h of header_data){
            let elem = document.createElement("th");
            elem.innerHTML = h;
            row.appendChild(elem);
        }
    }

    /**
     * Inserts a row to table.
     * 
     * @param {int} index Index where to insert the row. With -1, will be placed last
     * @param {Array} row_data Array of elements that will be inserted to the table
     */
    insert_row(index, row_data) {
        let row = this.table_elem.tBodies[0].insertRow(index);
        for(let d of row_data){
            let elem = row.insertCell(-1);
            elem.innerHTML = d;
        }
    }

    /**
     * Replaces the row with the lowest index
     * having the value matching to the given value in the given column.
     * 
     * NOTE: Replaces the whole row!
     * 
     * @param {int} column Index of the column to compare
     * @param {any} value Value to compare against column value
     * @param {Array} new_row_data New data inserted to the table
     */
    replace_row_by_value_in_column(column, value, new_row_data) {
        let rows = this.table_elem.tBodies[0].rows;
        for(let i = 0; i < rows.length; i++){
            if(rows[i].cells[column].innerHTML == value){
                this.table_elem.tBodies[0].deleteRow(i);
                this.insert_row(i, new_row_data);
                return;
            }
        }
    }
    
    /**
     * Sets HTML element attributes columnwise
     * 
     * @param {int} column_index Index of the column to access
     * @param {Attr} attr Attribute to add to the cells
     */
    set_column_attributes(column_index, attr){
        for(let row of this.table_elem.tBodies[0].rows){
            let tmp = attr.cloneNode();
            row.cells[column_index].setAttributeNode(attr);
        }
    }

    /**
     * Sets HTML attribute of a cell in the table
     * 
     * @param {int} row_index Row of the cell to access
     * @param {int} column_index Column of the cell to access
     * @param {Attr} attr Attribute to add to the cell
     */
    set_cell_attribute(row_index, column_index, attr){
        this.table_elem.tBodies[0].rows[row_index]
            .cells[column_index].setAttributeNode(attr);
    }
    
    /**
     * Deletes the first row in table that has a matching value stored in the specified column
     * 
     * @param {int} column Column index to compare
     * @param {any} value Value to compare against
     */
    delete_row_by_value_in_column(column, value){
        let rows = this.table_elem.tBodies[0].rows;
        for(let i = 0; i < rows.length; i++){
            if(rows[i].cells[column].innerHTML == value){
                this.table_elem.tBodies[0].deleteRow(i);
                return;
            }
        }
        alert("Failed to delete row in page. Please refresh the page.");
    }

    /**
     * Returns the firsth row with matching value stored in the specified column
     * 
     * @param {int} column Column index to compare
     * @param {any} value Value to compare against
     * 
     * @returns {Array} Of data stored in the row, or null in case of no match
     */
    get_row_by_value_in_column(column, value){
        for(let row of this.table_elem.tBodies[0].rows){
            if(row.cells[column].innerHTML == value){
                let res = [];
                for(let cell of row.cells){
                    res.push(cell.innerHTML);
                }
                return res;
            }
        }
        return null;
    }
};
/**
 * Class for constructing buttons
 */
class Button{

    /**
     * Ctor
     * 
     * @param {String} container_id ID of the element containing the button, or null if no need
     * @param {String} onclick_handler String inserted to the HTML element for callbacks
     * @param {String} text Text to place onto the button
     */
    constructor(container_id, onclick_handler, text){
        this.button = document.createElement("button");
        if(text != null) this.button.innerHTML = text;
        if(container_id != null) document.getElementById(container_id).appendChild(this.button);
        if(onclick_handler != null){
            let tmp = document.createAttribute("onclick");
            tmp.value = onclick_handler;
            this.button.setAttributeNode(tmp);
        }
    }

    /**
     * Return outer HTML
     * 
     * @returns {String} With outer html representation
     */
    outer_html(){
        return this.button.outerHTML;
    }

};

/**
 * Class for handling competition table
 */
class CompetitionTable {

    /**
     * Ctor
     * 
     * @param {String} myname Name of the object, injected to html for callbacks (Should be exactly the same as the variable)
     * @param {String} container_id ID of the HTML element containing the table
     * @param {WebSocket} wsock WebSocket used for notifying server on events
     */
    constructor(myname, container_id, wsock){
        this.myname = myname;
        this.wsock = wsock;
        this.button_new = new Button(container_id, this.myname + ".new_competition_handler()", "New Competition");

        this.tbl = new Table(container_id);
        this.tbl.set_header(["ID", "Name", "Date", "Manage"]);
    }

    /**
     * Add a new competition to the table
     * 
     * @param {Object} new_row  Either an Array or Object to append to the table
     */
    add_competition(new_row){

        let row = []
        if(Array.isArray(new_row)){
            row = new_row;
        } else {
            row = [new_row["ID"], new_row["Name"], new_row["CompetitionDate"]];
        }
        let id = row[0];
        let activate_button = new Button(null, this.myname + ".activate_handler("+id+")", "Activate");
        let modify_button = new Button(null, this.myname + ".modify_handler("+id+")", "Modify");
        let delete_button = new Button(null, this.myname + ".delete_handler("+id+")", "Delete");

        this.tbl.insert_row(-1, row.concat([activate_button.outer_html() + modify_button.outer_html() + delete_button.outer_html()]));
    }

    /**
     * Remove a competition
     * 
     * @param {any} id Competition ID to delete
     */
    remove_competition(id){
        console.log("Deleting competition with ID: " + id);
        this.tbl.delete_row_by_value_in_column(0, id);
    }

    /**
     * Replaces a competition with given ID
     * 
     * @param {any} id ID of the competition to replace
     * @param {Array} values Array of values to replace the row with outside of Management column
     */
    replace_competition(id, values){
        let activate_button = new Button(null, this.myname + ".activate_handler("+id+")", "Activate");
        let modify_button = new Button(null, this.myname + ".modify_handler("+id+")", "Modify");
        let delete_button = new Button(null, this.myname + ".delete_handler("+id+")", "Delete");
        this.tbl.replace_row_by_value_in_column(0, id, 
                                                values.concat([activate_button.outer_html() +  
                                                               modify_button.outer_html() +
                                                               delete_button.outer_html()]));
    }

    /**
     * Callback invoked by HTML button. Sends a new competition request to the server.
     */
    new_competition_handler(){
        let name = prompt("New competition name");
        if(name == null) return;
        let today = new Date();
        let year = today.getFullYear().toString();
        let month = (today.getMonth()+1).toString();
        let day = (today.getDate()).toString();
        console.log(month);
        console.log(day);
        if(month.length < 2) month = "0" + month;
        if(day.length < 2) day = "0" + day;

        let date = prompt("New competition date (empty value evaluates to server's date)", 
                          year + "-" + month + "-" + day);
        if(date == null) return;
        
        let obj = {"event": "newRow", "target": "competitions", "values": {"Name": name}};
        if(date != "")
        obj["values"]["CompetitionDate"] = date;
        wsock.send(JSON.stringify(obj));
    }

    /**
     * Callback invoked by HTML button. Sets the corresponding competition as the active competition
     * 
     * TODO: implement
     * 
     * @param {any} id ID of the competition for which the event was invoked
     */
    activate_handler(id){
        alert("Competition activation has not been implemented yet");
    }

    /**
     * Callback invoked by HTML button. Modifies the competition row.
     *
     *  @param {any} id ID of the competition to modify.
     */
    modify_handler(id){
        let row = this.tbl.get_row_by_value_in_column(0, id);
        let name = row[1];
        let date = row[2];
        name = prompt("Give new name", name);
        if(name == null) return;
        date = prompt("Give new date", date);
        if(date == null) return;
        let obj = {
            "event": "rowModified",
            "target": "competitions", 
            "id": id, 
            "values": {
                "Name": name, 
                "CompetitionDate": date
            }
        };
        wsock.send(JSON.stringify(obj));
    }

    /**
     * Callback invoked by HTML button. Deletes a competition
     * 
     * @param {any} id ID of the competition to delete 
     */
    delete_handler(id){
        let row = this.tbl.get_row_by_value_in_column(0, id);
        if(confirm("Are you sure? This will permanently delete the competition with name " + row[1])){
            let obj = {"event": "rmRow", "target": "competitions", "id": id};
            wsock.send(JSON.stringify(obj));
        }
    }

};


let wsock = new WebSocket("ws://"+ location.host +"/websocket");
let competitions_tbl = new CompetitionTable("competitions_tbl", "competition_list_table", wsock);


wsock.onopen = function(event){
    let obj = {event: "getTable", target: "competitions"};
    wsock.send(JSON.stringify(obj));
};

wsock.onmessage = function(event){
    let obj = JSON.parse(event.data);
    if(obj.event == "getTable"){
        if(obj.target == "competitions"){
            for(let val of obj.rows)
            competitions_tbl.add_competition(val);
        }

    } else if (obj.event == "newRow"){
        if(obj.target == "competitions"){
            competitions_tbl.add_competition(obj.values);
        }
    } else if (obj.event == "rmRow"){
        if(obj.target == "competitions"){
            competitions_tbl.remove_competition(obj.id);
        }
    } else if(obj.event == "rowModified"){
        if(obj.target == "competitions"){
            competitions_tbl.replace_competition(obj.id, [obj.id].concat([obj.values.Name, obj.values.CompetitionDate]))
        }
    }
}

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

/*
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

*/