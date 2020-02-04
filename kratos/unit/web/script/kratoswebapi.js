
class KratosWebApi {
    constructor(url){
        this._url = url;
        this._cbs = {};
    }

    start(){
        console.debug("Starting websocket communication");
        this._wsock = new WebSocket(this._url);
        this._wsock.onopen = (event) => {this._wsock_onopen(event);};
        this._wsock.onmessage = (event) => {this._wsock_onmessage(event)};
    }

    debug_websocket(){
        this._wsock;
    }
    table_event_handler(table, event, callback){
        console.debug("Registering callback for table: "
                       + table + " and event: " + event);
        if(!(table in this._cbs)){
            this._cbs[table] = {};
        }
        if(!(event in this._cbs[table])){
            this._cbs[table][event] = callback;
            return;
        }
        throw "Event handler already registered";
    }

    send_table_event(obj){
        this._wsock.send(JSON.stringify(obj));
    }

    _wsock_onopen(event){
        console.debug("WebSocket connection connected");
        for(let key of Object.keys(this._cbs)){
            let obj = {event: "getTable", target: key};
            this._wsock.send(JSON.stringify(obj));
        }
    }

    _wsock_onmessage(event) {
        console.debug("WebSocket event received");
        let obj = JSON.parse(event.data);
        if(obj.target in this._cbs && obj.event in this._cbs[obj.target]){
            this._cbs[obj.target][obj.event](obj);
        }
        else {
            console.info("Unhandled message: " + JSON.stringify(obj));
        }
    }
};