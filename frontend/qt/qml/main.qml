import QtQuick 2.3
import QtQuick.Controls 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.15


ApplicationWindow{
    id: root
    visible: true

    height: 600
    width: 800

    menuBar: KratosMenuBar {}
    //header: KratosToolBar {}

    contentData: [
        Rectangle{
            anchors.fill: parent
            TabBar{
                id: tabBar
                width: 400
                TabButton{ text: "Configuration"
                font.pixelSize: 12 }
                TabButton{ text: "Competitors" }
                TabButton{ text: "Competition" }
            }
            StackLayout {
                anchors.right: parent.right
                anchors.left: parent.left
                anchors.bottom: parent.bottom
                anchors.top: tabBar.bottom
                currentIndex: tabBar.currentIndex
                Item{
                    KratosConfigView{}
                }
                Item{
			KratosCompetitorView{
			}
                }

                Item{
                    Rectangle{
                        anchors.fill: parent 
                        color: "blue"
                    }
                }
            }
        }
    ]

    footer: TabBar{
    }
    
    StackView {
        anchors.fill: parent
    }

}
