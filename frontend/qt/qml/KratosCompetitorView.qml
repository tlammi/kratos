import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0

Rectangle{
    anchors.fill: parent

    Rectangle{
        id: tlAlign
        anchors.top: parent.top
        anchors.left: parent.left
        height: 10
        width: 10
        color: "blue"
    }

    HeaderTable{
	    id: headerTable
	    anchors.top: tlAlign.bottom
	    anchors.left: tlAlign.right
	    objectName: "asdf"
	    height: parent.height-300
	    width: parent.width-300
    }

    Rectangle{
	    id: middleAlign
	    anchors.top: headerTable.bottom
	    height: 10
    }
    Button {
	    id: addButton
	    anchors.top: middleAlign.bottom
	    anchors.left: tlAlign.right
	    onClicked: headerTable.model.appendRow()
	    text: "Add"
    }
    Rectangle{
	    id: buttonAlign1
	    anchors.left: addButton.right
	    width: 10
    }
    Button {
	    id: phButton1
	    anchors.top: middleAlign.bottom
	    anchors.left: buttonAlign1.right
	    text: "Sort"
	    onClicked: headerTable.model.sort()
    }
    Rectangle{
	    id: buttonAlign2
	    anchors.left: phButton1.right
	    width: 10
    }
    Button {
	    anchors.top: middleAlign.bottom
	    anchors.left: buttonAlign2.right
	    text: "Placeholder Button"
    }
    
}
