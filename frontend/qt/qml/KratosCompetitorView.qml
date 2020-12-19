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
    
    Row{
        id: headerRow
        anchors.top: tlAlign.bottom
        anchors.left: tlAlign.right
        spacing: 1
        Rectangle{
            color: "red"; width: 100; height: 50
            Text{
                text: "Last Name"
            }

            MouseArea{
                anchors.fill: parent
                cursorShape: Qt.SizeHorCursor
            }
        }
        Rectangle{
            color: "green"; width: 100; height: 50
            Text{
                text: "First Name"
            }
        }
    }
    TableView{
        anchors.top: headerRow.bottom
        anchors.left: tlAlign.right
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        columnSpacing: 1
        rowSpacing: 1

        model: TableModel{
            TableModelColumn{display: "last_name"}
            TableModelColumn{display: "first_name"}
            rows: [
                {
                    last_name: "Meikalainen",
                    first_name: "Matti"
                },
                {
                    last_name: "Esimerkki",
                    first_name: "Erkki"
                }
            ]
        }

        delegate: TextInput{
            text: model.display
            padding: 12
            selectByMouse: true
            onAccepted: model.display = text
            Rectangle{
                anchors.fill: parent
                color: "#efefef"
                z: -1
            }
        }
    }
}