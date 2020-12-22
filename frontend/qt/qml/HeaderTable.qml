import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0
import MutableHeaderTableModel 0.1

Rectangle{

    id: headerTableRoot
    signal itemModified(row: int, column: int, value: string)

    /*
    TableView{
	    anchors.top: parent.top
	    anchors.left: parent.left
	    anchors.right: parent.right
	    height: 40
	    id: headerRow
	    columnSpacing: 1
	    rowSpacing: 1
	    
	    model: TableModel {
		TableModelColumn{display: "first_name"}
		TableModelColumn{display: "last_name"}
		rows: [
		    {
			last_name: "Last Name",
			first_name: "First Name"
		    }
		]
	    }
	    delegate: TextField{
		    text: model.display
		    padding: 12
		    readOnly: true
	    }
    }
    */
    TableView{
		
        anchors.top: horizontalHeaderView.bottom
	anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
	
        columnSpacing: 1
        rowSpacing: 1
	objectName: "as"
	id: tableView
	
	model: MutableHeaderTableModel{
		objectName: "asd"
	}

        delegate: TextInput{
            text: model.display
            padding: 12
            selectByMouse: true
            Rectangle{
                anchors.fill: parent
                color: "#efefef"
                z: -1
            }
	    onAccepted: headerTableRoot.itemModified(row, column, text)
        }
    }
    HorizontalHeaderView{
	anchors.top: parent.top
	anchors.left: parent.left
	anchors.right: parent.right
	height: 40
	columnSpacing: 1
	rowSpacing: 1
	id: horizontalHeaderView
	
	objectName: "asHeader"
	syncView: tableView

	delegate: TextField{
		text: model.display
		padding: 12
		readOnly: true
	}

    }
}
