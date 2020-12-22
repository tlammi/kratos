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
	    objectName: "competitorConfigTable"
	    anchors.fill: parent
    }
    
}
