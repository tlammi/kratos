import QtQuick 2.0
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13


Page {
    background: Rectangle {
        color: "black"
    }

    ColumnLayout {
        anchors.fill: parent

        spacing: 2

        Rectangle {
            Layout.alignment: Qt.AlignLeft
            Layout.preferredHeight: parent.height * 0.6
            Layout.preferredWidth: parent.width

            color: "black"

            ColumnLayout {
                anchors.fill: parent

                spacing: 2

                Rectangle {
                    Layout.alignment: Qt.AlignLeft
                    Layout.preferredHeight: parent.height*0.4
                    Layout.preferredWidth: parent.width

                    color: "black"

                    Text {
                        id: lastnameText
                        anchors.fill: parent

                        text: applicationData.lastname
                        renderType: Text.NativeRendering
                        wrapMode: Text.Wrap

                        fontSizeMode: Text.Fit
                        minimumPixelSize: 10
                        font.pixelSize: 1000
                        font.bold: true
                        color: "white"
                    }
                }

                Rectangle {
                    Layout.alignment: Qt.AlignLeft
                    Layout.preferredHeight: parent.height*0.4
                    Layout.preferredWidth: parent.width

                    color: "black"

                    RowLayout {
                        anchors.fill: parent

                        spacing: 2

                        Rectangle {
                            Layout.preferredHeight: parent.height
                            Layout.preferredWidth: parent.width - parent.height - parent.spacing
                            Layout.alignment: Qt.AlignLeft

                            color: "black"

                            Text {
                                anchors.fill: parent
                                
                                text: applicationData.firstname
                                renderType: Text.NativeRendering
                                wrapMode: Text.Wrap

                                fontSizeMode: Text.Fit
                                minimumPixelSize: 10
                                font.pixelSize: lastnameText.fontInfo.pixelSize
                                color: "white"
                            }
                        }

                        Rectangle {
                            Layout.preferredHeight: parent.height
                            Layout.preferredWidth: parent.height
                            Layout.alignment: Qt.AlignRight

                            color: "black"
                            border {
                                width: 2
                                color: "white"
                            }

                            Text {
                                anchors.fill: parent

                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter

                                text: applicationData.lot_number
                                renderType: Text.NativeRendering
                                wrapMode: Text.Wrap

                                fontSizeMode: Text.Fit
                                minimumPixelSize: 10
                                font.pixelSize: lastnameText.fontInfo.pixelSize
                                color: "white"
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.alignment: Qt.AlignLeft
                    Layout.preferredHeight: parent.height*0.2
                    Layout.preferredWidth: parent.width

                    color: "black"

                    Text {
                        anchors.fill: parent

                        text: applicationData.team
                        renderType: Text.NativeRendering
                        wrapMode: Text.Wrap

                        fontSizeMode: Text.Fit
                        minimumPixelSize: 10
                        font.pixelSize: lastnameText.fontInfo.pixelSize
                        color: "white"
                    }
                }
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignLeft
            Layout.preferredHeight: parent.height * 0.4
            Layout.preferredWidth: parent.width

            StackLayout {
                id: bottom_stack
                anchors.fill: parent

                currentIndex: 0

                Rectangle {
                    color: "black"

                    RowLayout {
                        anchors.fill: parent

                        spacing: 2

                        Rectangle {
                            Layout.preferredHeight: parent.height
                            Layout.preferredWidth: parent.width / 2

                            color: "black"

                            ColumnLayout {
                                anchors.fill: parent

                                spacing: 2

                                Rectangle {
                                    Layout.alignment: Qt.AlignLeft
                                    Layout.preferredHeight: parent.height * 0.5
                                    Layout.preferredWidth: parent.width

                                    color: "black"

                                    Text {
                                        anchors.fill: parent

                                        text: applicationData.attempt_num + " att."
                                        renderType: Text.NativeRendering

                                        fontSizeMode: Text.Fit
                                        minimumPixelSize: 10
                                        font.pixelSize: 1000
                                        color: "yellow"
                                    }
                                }

                                Rectangle {
                                    Layout.alignment: Qt.AlignLeft
                                    Layout.preferredHeight: parent.height * 0.5
                                    Layout.preferredWidth: parent.width

                                    color: "black"

                                    Text {
                                        anchors.fill: parent

                                        text: applicationData.weight + " kg"
                                        renderType: Text.NativeRendering

                                        fontSizeMode: Text.Fit
                                        minimumPixelSize: 10
                                        font.pixelSize: 1000
                                        color: "yellow"
                                    }
                                }
                            }
                        }

                        Rectangle {
                            Layout.preferredHeight: parent.height
                            Layout.preferredWidth: parent.width / 2

                            color: "black"

                            Text {
                                anchors.fill: parent

                                text: applicationData.minutes + ":" + applicationData.seconds
                                renderType: Text.NativeRendering

                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter

                                fontSizeMode: Text.Fit
                                minimumPixelSize: 10
                                font.pixelSize: 1000
                                font.bold: true
                                color: "red"
                            }
                        }
                    }
                }

                Rectangle {
                    color: 'black'

                    RowLayout {
                        anchors.fill: parent

                        Rectangle {
                            id: rightJudgeDecision

                            Layout.preferredHeight: parent.height / 2
                            Layout.preferredWidth: parent.width / 4
                            Layout.margins: 10
                            Layout.alignment: Qt.AlignLeft

                            color: "black"
                        }

                        Rectangle {
                            id: middleJudgeDecision

                            Layout.preferredHeight: parent.height / 2
                            Layout.preferredWidth: parent.width / 4
                            Layout.margins: 10
                            Layout.alignment: Qt.AlignHCenter

                            color: "black"
                        }

                        Rectangle {
                            id: leftJudgeDecision

                            Layout.preferredHeight: parent.height / 2
                            Layout.preferredWidth: parent.width / 4
                            Layout.margins: 10
                            Layout.alignment: Qt.AlignRight

                            color: "black"
                        }

                        Connections {
                            target: applicationData

                            onJudgingSet: {
                                leftJudgeDecision.color =
                                    judging[0] === "NA" ? "black" : judging[0]
                                middleJudgeDecision.color =
                                    judging[1] === "NA" ? "black" : judging[1]
                                rightJudgeDecision.color =
                                    judging[2] === "NA" ? "black" : judging[2]

                                bottom_stack.currentIndex = 1
                            }

                            onJudgingCleared: {
                                bottom_stack.currentIndex = 0

                                leftJudgeDecision.color = "black"
                                middleJudgeDecision.color = "black"
                                rightJudgeDecision.color = "black"
                            }
                        }
                    }
                }
            }
        }
    }
}
