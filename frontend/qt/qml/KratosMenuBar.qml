
import QtQuick.Controls 2.15


MenuBar{
    height: 30
    MenuBarItem{
        height: parent.height
        menu: Menu {
            title: "File"
            MenuItem{
                text: "New"
            }
            MenuItem{
                text: "Open"
            }
            MenuItem{
                text: "Save"
            }
            MenuItem{
                text: "Exit"
            }
        }
    }
    MenuBarItem{
        height: parent.height
        menu: Menu {
            title: "Edit"
        }
    }
    MenuBarItem{
        height: parent.height
        menu: Menu {
            title: "View"
        }
    }
}