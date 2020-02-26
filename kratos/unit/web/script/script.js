
/**
 * Class for handling competition table
 */
class CompetitionTable {

    /**
     * Ctor
     * 
     * @param {String} container_id ID of the HTML element containing the table
     * @param {KratosWebApi} api WebSocket used for notifying server on events
     */
    constructor(container_id, api) {
        this._api = api;

        this.button_new = new Button(
            document.getElementById(container_id),
            () => { this.new_competition_handler(); },
            "New Competition");

        this._tbl = new Table(document.getElementById(container_id), 0,
            ["ID", "Name", "CompetitionDate", "IsActive", "Manage"],
            ["ID", "Name", "Date", "Active", "Manage"]);

        this._tbl.on_cell_modified = (x, y, val) => {
            console.log("Enter pressed on: " + "(" + x + ", " + y + "): " + val)
        }
    }

    /**
     * Add a new competition to the table
     * 
     * @param {Object} new_row  Either an Array or Object to append to the table
     */
    add_competition(new_row) {

        let id = new_row[0];
        if (id === undefined)
            id = new_row["ID"];

        let div = document.createElement("div");

        let activate_button = new Button(div, () => {
            this.activate_handler(id);
        }, "Activate");
        let modify_button = new Button(div, () => {
            this.modify_handler(id);
        }, "Modify");
        let delete_button = new Button(div, () => {
            this.delete_handler(id);
        }, "Delete");

        if (Array.isArray(new_row)) {
            new_row.push(div);
        } else {
            new_row["Manage"] = div;
        }
        this._tbl.append(new_row);
    }

    /**
     * Remove a competition
     * 
     * @param {any} id Competition ID to delete
     */
    remove_competition(id) {
        console.log("Deleting competition with ID: " + id);
        this._tbl.delete_row(id);
    }

    /**
     * Replaces a competition with given ID
     * 
     * @param {any} id ID of the competition to replace
     * @param {Array} values Array of values to replace the row with outside of Management column
     */
    replace_competition(id, values) {
        let row = this._tbl.row_as_dict(id);

        if (values instanceof Array)
            values.push(row["Manage"]);
        else
            values["Manage"] = row["Manage"];
        this._tbl.replace_row(id, values);
    }

    clear(){
        this._tbl.clear();
    }

    /**
     * Callback invoked by HTML button. Sends a new competition request to the server.
     */
    new_competition_handler() {
        let name = prompt("New competition name");
        if (name == null) return;
        let today = new Date();
        let year = today.getFullYear().toString();
        let month = (today.getMonth() + 1).toString();
        let day = (today.getDate()).toString();
        console.log(month);
        console.log(day);
        if (month.length < 2) month = "0" + month;
        if (day.length < 2) day = "0" + day;

        let date = prompt("New competition date (empty value evaluates to server's date)",
            year + "-" + month + "-" + day);
        if (date == null) return;

        let obj = { "event": "newRow", "target": "Competitions", "values": { "Name": name } };
        if (date != "")
            obj["values"]["CompetitionDate"] = date;
        this._api.send_table_event(obj);
    }

    /**
     * Callback invoked by HTML button. Sets the corresponding competition as the active competition
     * 
     * @param {any} id ID of the competition for which the event was invoked
     */
    activate_handler(id) {
        let row = this._tbl.row_as_array(id);

        // The row was active already
        if (row[3] == true) {
            let obj = {
                "event": "rowModified",
                "target": "Competitions",
                "id": id,
                "values": {
                    "IsActive": false
                }
            }
            let activate_button = row[4].childNodes[0].firstChild;
            activate_button.innerHTML = "Activate";
            this._api.send_table_event(obj);
        }
        else {
            let col = this._tbl.get_column("IsActive");
            for (let elem of col) {
                if (elem == true) {
                    alert("Cannot activate a connection while another one is active");
                    return;
                }
            }

            let obj = {
                "event": "rowModified",
                "target": "Competitions",
                "id": id,
                "values": {
                    "IsActive": true
                }
            };

            let activate_button = row[4].childNodes[0].firstChild;
            activate_button.innerHTML = "Deactivate";
            this._api.send_table_event(obj);
        }
    }

    /**
     * Callback invoked by HTML button. Modifies the competition row.
     *
     *  @param {any} id ID of the competition to modify.
     */
    modify_handler(id) {
        let row = this._tbl.row_as_array(id);
        let name = row[1];
        let date = row[2];
        name = prompt("Give new name", name);
        if (name == null) return;
        date = prompt("Give new date", date);
        if (date == null) return;
        let obj = {
            "event": "rowModified",
            "target": "Competitions",
            "id": id,
            "values": {
                "Name": name,
                "CompetitionDate": date
            }
        };
        this._api.send_table_event(obj);
    }

    /**
     * Callback invoked by HTML button. Deletes a competition
     * 
     * @param {any} id ID of the competition to delete 
     */
    delete_handler(id) {
        let row = this._tbl.row_as_array(id);
        if (confirm("Are you sure? \
            This will permanently delete \
            the competition with name " + row[1])) {

            let obj = { "event": "rmRow", "target": "Competitions", "id": id };
            this._api.send_table_event(obj);
        }
    }

};

class CompetitorTable {
    constructor(container_id, api) {
        this._api = api;

        this.new_button = new Button(
            document.getElementById(container_id),
            () => {
                this.new_competitor_handler();
            },
            "New Competitor"
        );

        this._tbl = new Table(document.getElementById(container_id), 0,
            ["ID", "LastName", "FirstNames", "BodyWeight", "Sex", "Delete"],
            ["ID", "Last Name", "First Names", "Body Weight", "Sex", "Delete"])


        this._tbl.on_cell_modified = (x, y, data) => {
            let obj = {
                "event": "rowModified",
                "target": "Competitors"
            };
            obj["id"] = y;
            obj["values"] = {};
            obj["values"][x] = data;
            this._api.send_table_event(obj);
            console.log("Modified (" + x + ", " + y + "): " + data);
        }
        this._tbl.set_rw_mask([false, true, true, true, true, false]);
        this._tbl.set_visible_mask([true, true, true, true, true, true]);
    }

    add_competitor(new_row) {

        let id = new_row[0];
        if(id === undefined)
            id = new_row["ID"];

        let div = document.createElement("div");

        let button = new Button(div, () => {
            this.delete_competitor_handler(id);
        }, "Delete");
        if(new_row instanceof Array) {
            new_row.push(div);
        } else {
            new_row["Delete"] = div;
        }
        this._tbl.append(new_row);
    }

    new_competitor_handler() {
        let obj = {
            "event": "newRow",
            "target": "Competitors",
            "values": {
            }
        };
        this._api.send_table_event(obj);
    }

    replace_competitor(id, values) {
        this._tbl.replace_row(id, values);
    }

    remove_competitor(id) {
        console.debug("Removing element " + id + " from current competitors");
        this._tbl.delete_row(id);
    }

    clear() {
        this._tbl.clear();
    }

    delete_competitor_handler(id) {
        let obj = {"event": "rmRow", "target": "Competitors", "id": id};
        this._api.send_table_event(obj);
    }
};

let kratos_api = new KratosWebApi("ws://" + location.host + "/websocket");
let competitions_tbl = new CompetitionTable("competition_list_table", kratos_api);
let competitor_tbl = new CompetitorTable("competitor_table", kratos_api);

fetch("/tables/Competitions").then(response => response.json()).then(data => {
    competitions_tbl.clear();
    for (let val of data.rows) {
        competitions_tbl.add_competition(val);
    }
});

fetch("/tables/CurrentCompetitors").then(response => response.json()).then(data => {
    competitor_tbl.clear();
    for(let val of data.rows){
        competitor_tbl.add_competitor(val);
    }
});
kratos_api.table_event_handler("Competitions", "newRow", (obj) => {
    competitions_tbl.add_competition(obj.values);
});

kratos_api.table_event_handler("Competitions", "rmRow", (obj) => {
    competitions_tbl.remove_competition(obj.id);
});

kratos_api.table_event_handler("Competitions", "rowModified", (obj) => {
    let tmp = obj.values;
    tmp["ID"] = obj.id;
    competitions_tbl.replace_competition(
        obj.id,
        tmp
    );
});

kratos_api.table_event_handler("CurrentCompetitors", "newRow", (obj) => {
    competitor_tbl.add_competitor(obj.values);
});

kratos_api.table_event_handler("Competitors", "rowModified", (obj) => {
    competitor_tbl.replace_competitor(obj.id, obj.values);
});

kratos_api.table_event_handler("Competitors", "rmRow", (obj) => {
    competitor_tbl.remove_competitor(obj.id);
});

kratos_api.table_event_handler("CurrentCompetitors", "tableOverwritten", (obj) => {
    competitor_tbl.clear();
    for(let val of obj.rows){
        competitor_tbl.add_competitor(val);
    }
});

kratos_api.start();

// Handles tab button press by opening a corresponding tab
function opentab(event, tabname) {
    function hide_tabs() {
        var tabs = document.getElementsByClassName("tab");
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].style.display = "none";
        }
    }

    function reset_tabbuttons() {
        var tabbuttons = document.getElementsByClassName("toolchain")[0]
            .getElementsByClassName("tabbuttonholder")[0]
            .getElementsByTagName("button");

        for (var i = 0; i < tabbuttons.length; i++) {
            tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
        }
    }

    function show_tab(tabname) {
        document.getElementById(tabname).style.display = "block";
    }

    function activate_button(targetbutton) {
        targetbutton.className += " active";
    }

    hide_tabs();
    reset_tabbuttons();
    show_tab(tabname);
    activate_button(event.currentTarget);
}
