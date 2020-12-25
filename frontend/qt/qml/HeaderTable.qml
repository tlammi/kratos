import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0
import MutableHeaderTableModel 0.1

Rectangle{

    id: headerTableRoot

    signal itemModified(row: int, column: int, value: string)
    readonly property TableView table_view: tableView
    readonly property HorizontalHeaderView header_view: horizontalHeaderView
    readonly property MutableHeaderTableModel model: mutableHeaderTableModel

    MutableHeaderTableModel{
	    id: mutableHeaderTableModel
    }

    TableView{	
	id: tableView

        anchors.top: horizontalHeaderView.bottom
	anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        columnSpacing: 1
        rowSpacing: 1

	model: parent.model

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
	
	syncView: tableView

	delegate: TextField{
		text: model.display
		padding: 12
		readOnly: true
	}
    }
}
