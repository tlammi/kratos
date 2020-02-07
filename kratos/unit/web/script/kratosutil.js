
/**
 * Helper class for managing HTML tables
 */
class Table {
    /**
     * Constructs a new HTML table inside the HTML element with the given ID.
     * 
     * @param {String} table_holder_id Container HTMl element where the table will be placed
     * @param {String|integer} yindex_column Column used for indexing operations on this table
     * @param {*[]} xindex List of values used as X-axis indexes
     * @param {String[]} header List of values placed into the header. Should have equal length
     *                          to xindex.
     */
    constructor(table_holder, yindex_column, xindex, header){
        if(xindex.length != header.length)
            throw "xindex and header lengths do no match: "
                    + xindex.length + ", " + header.length;

        this._tbl = document.createElement("table");
        table_holder.appendChild(this._tbl);
        let table_head = this._tbl.createTHead();
        let header_row = document.createElement("tr");
        table_head.appendChild(header_row);
        this._tbl.createTBody();

        this._xindex = xindex;
        this._yindex_column = this._xindex.indexOf(yindex_column);
        if(this._yindex_column == -1)
            this._yindex_column = yindex_column;

        this._header = header;
        this._vmask = Array.from(this._xindex, x => true);
        this._rwmask = Array.from(this._xindex, x => false);
        this._rows = []
        this.on_cell_modified = null;
        for(let h of header){
            if(this._is_dom_element(h)){
                header_row.insertCell(-1).appendChild(h);
            }
            else {
                let p = document.createElement("div");
                p.innerHTML = h;
                header_row.insertCell(-1).appendChild(p);
            }
        }
    };

    /**
     * Sets visibility mask for the table
     * 
     * True values mean that respective columns are visible in HTML and false
     * that the values are not present in the HTML. Default values are
     * all-trues.
     * 
     * @param {bool[]} mask Mask to set, should have the same length as xindex
     *                      and header passed to constructor
     */
    set_visible_mask(mask){
        if(mask.length != this._vmask.length)
            throw "Invalid mask length";
        this._vmask = mask;
        let header_row = this._tbl.tHead.firstChild;
        while(header_row.firstChild)
            header_row.removeChild(header_row.firstChild);

        mask.forEach((val, index) => {
            if(val){
                let div = document.createElement("div");
                div.innerHTML = this._header[index];
                header_row.insertCell(-1).appendChild(div);
            }
        });
    }

    /**
     * Sets read-write mask for the table
     *
     * True values mean that respective columns are read-write, false values that they
     * are read only. Default value are all-falses.
     *
     * @param {Array} mask Mask to set. Should have the same length as xindex and header passed to the
     *                 constructor.
     */
    set_rw_mask(mask){
        if(mask.length != this._rwmask.length)
            throw "Invalid mask length";
        this._rwmask = mask;
    }
    /**
     * Appends a row to table.
     *
     * @param {Object} row_data Array or Object of elements to be inserted
     */
    append(row_data) {
        let row = this._ensure_array(row_data);
        
        this._rows.push(row);
        
        let domrow = this._tbl.tBodies[0].insertRow(-1);
        let row_index = this._tbl.tBodies[0].rows.length-1;
        this._vmask.forEach((bit, i) =>{
            if(bit){
                let div = this._wrap_value_in_div(row[i], i, row_index);
                let new_cell = domrow.insertCell(-1);
                new_cell.appendChild(div);
            }
        });
    }

    /**
     * Replaces a row in the table
     *
     * @param {String} yindex Index used for accessing the row (typically a value in ID column)
     * @param {Object|Array} newrow New row to insert into the table. Note that in case the ID is to be conserved,
     *                  the ID should be present in the row
     */
    replace_row(yindex, newrow){
        let row_index_to_replace = this._public_to_private_index(yindex);
        if(row_index_to_replace === null)
            throw "Could not find index " + yindex;

        newrow = this._ensure_array(newrow);
        this._rows[row_index_to_replace] = newrow;
        let domrow = this._tbl.tBodies[0].childNodes[row_index_to_replace];

        let tmp = 0;
        this._vmask.forEach((bit, i) => {
            if(bit){
                while(domrow.cells[tmp].firstChild)
                    domrow.cells[tmp].removeChild(domrow.cells[tmp].firstChild);
                
                let div = this._wrap_value_in_div(newrow[i], i, row_index_to_replace);
                domrow.cells[tmp].appendChild(div);
                tmp++;
            }
        });

    }

    /**
     * Clears the data stored in the table
     */
    clear(){
        this._rows = []
        let tbody = this._tbl.tBodies[0];
        while(tbody.firstChild)
            tbody.removeChild(tbody.firstChild);
    }

    /**
     * Deletes the row indicated by the index
     *
     * @param {*} yindex Index corresponding to the table
     */
    delete_row(yindex){
        let row_index_to_delete = this._public_to_private_index(yindex);

        this._rows.splice(row_index_to_delete, 1);

        let domrow = this._tbl.tBodies[0].childNodes[row_index_to_delete];
        this._tbl.tBodies[0].removeChild(domrow);
    }

    /**
     * Gets a row from the table and returns it as a array
     * @param {*} yindex Index corresponding to the row
     */
    row_as_array(yindex){
        yindex = this._public_to_private_index(yindex);
        return this._rows[yindex];
    }
    /**
     * Get a row from the table as a dictionary
     *
     * @param {*} yindex Index corresponding to the row
     */
    row_as_dict(yindex){
        yindex = this._public_to_private_index(yindex);
        let result = {};
        
        this._rows[yindex].forEach((val, index) => {
            result[this._xindex[index]] = val;
        });

        return result;
    }

    /**
     * Get a column from the table as an Array
     *
     * @param {*} xindex Index corresponding to the column
     */
    get_column(xindex){
        let ind;
        if(xindex instanceof String || typeof(xindex) === "string"){
            ind = this._xindex.indexOf(xindex);
            if(ind == -1){
                throw "Invalid index " + ind;
            }
        } else {
            ind = xindex;
        }

        let output = []

        this._rows.forEach(row => {
            output.push(row[ind])
        });

        return output;
    }

    /**
     * Converts the input to array. Used only internally.
     * 
     * Takes an object passed to other methods and converts it to a table row where
     * values are in correct positions.
     * 
     * @param {*} obj Object to convert, if Array, returned as is, if dictionary, converted
     * to a fitting array
     */
    _ensure_array(obj){
        if(obj instanceof Array)
            return obj;
        let result = [];
        this._xindex.forEach((key) => {
            if(key in obj){
                result.push(obj[key])
            }
            else {
                result.push(null);
            }
        });
        return result;
    }

    /**
     * Converts public to private indexes
     * 
     * Public indexing is performed by values stored in "yindex" column.
     * This function converts that value to integer that can be used to access
     * the actual row.
     * @param {*} pubindex Public index to convert to private
     */
    _public_to_private_index(pubindex){
        let res = null;
        this._rows.forEach((row, row_index) => {
            if(row[this._yindex_column] == pubindex){
                res = row_index;
                return;
            }
        });

        return res;
    }

    /**
     * Checks if the element is a dom element
     */
    _is_dom_element(elem){
        return (elem instanceof Element || elem instanceof HTMLElement);
    }

    /**
     * Wraps the value in a div DOM object with correct attributes
     * 
     * @param {*} value Value to wrap
     */
    _wrap_value_in_div(value, x, y){
        let div = document.createElement("div");

        if(!this._is_dom_element(value)) div.innerHTML = value;
        else div.appendChild(value);
        
        let attr = document.createAttribute("contenteditable");
        attr.value = this._rwmask[x];
        div.setAttributeNode(attr);
        div.onkeydown = (event) => this._key_event_hander(event, x, y);

        return div;
    }

    /**
     * Event handler for key events
     * 
     * @param {*} event Key event
     * @param {*} x x-coordinate as integer offset from left
     * @param {*} y y-coordinate as integer offset from top
     */
    _key_event_hander(event, x, y){
        if(event.which == 13){
            if(this.on_cell_modified){
                let dom = this._tbl.tBodies[0].rows[y];
                let data = dom.cells[x].firstChild.innerHTML;
                this._rows[y][x] = data;
                this.on_cell_modified(this._xindex[x], this._rows[y][this._yindex_column], data);
            }
            return false;
        }
        return true;
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
     * @param {function} onclick_handler Onclick event handler
     * @param {String} text Text to place onto the button
     */
    constructor(container, onclick_handler, text){
        this.button = document.createElement("button");
        if(text != null)
            this.button.innerHTML = text;
        if(container != null)
            container.appendChild(this.button);
        this.button.onclick = onclick_handler;
    }

    /**
     * Return outer HTML
     *
     * @returns {String} With outer html representation
     */
    outer_html(){
        return this.button.outerHTML;
    }

    dom(){
        return this.button;
    }

};
