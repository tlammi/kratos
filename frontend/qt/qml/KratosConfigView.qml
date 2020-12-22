
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Styles 1.4

Rectangle{
    id: config_root
    objectName: "Config"
    anchors.top: parent.top
    anchors.left: parent.left
    width: 400
    height: 120

    signal eventNameChanged(msg: string)

    Rectangle {
        id: tlAlign
        height: 10
	width: 10
        anchors.top: parent.top
	anchors.left: parent.left
    }
    TextField {
        id: textField
        anchors.top: tlAlign.bottom
        anchors.left: tlAlign.right
        anchors.right: parent.right
        height: 60
        placeholderText: "Event Name"
        font.pixelSize: 20
	onAccepted: config_root.eventNameChanged(text)
    }
    Rectangle{
        id: middleAlign
        height: 10
        anchors.top: textField.bottom

    }
    ComboBox{
	id: sportBox
        width: parent.width
        model: ["Weightlifting <not working>", "Power lifting <not working>"]
        anchors.top: middleAlign.bottom
        anchors.left: tlAlign.right
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        font.pixelSize: 18
    }
    Rectangle{
	    id: bottomAlign
	    height: 10
	    anchors.top: sportBox.bottom
    }
}
