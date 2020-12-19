
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Styles 1.4

Rectangle{
    anchors.top: parent.top
    anchors.left: parent.left
    width: 400
    height: 120
    Rectangle{
        id: topAlign
        height: 10
        anchors.top: parent.top
    }
    Rectangle{
        id: leftAlign
        width: 10
        anchors.left: parent.left
    }
    TextField {
        id: textField
        anchors.top: topAlign.bottom
        anchors.left: leftAlign.right
        anchors.right: parent.right
        height: 60
        placeholderText: "Event Name"
        font.pixelSize: 20
    }
    Rectangle{
        id: middleAlign
        height: 10
        anchors.top: textField.bottom

    }
    ComboBox{
        width: parent.width
        model: ["Weightlifting", "Power lifting <not working>"]
        anchors.top: middleAlign.bottom
        anchors.left: leftAlign.right
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        font.pixelSize: 18
    }
}