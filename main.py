from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import sys


class GraphFrame(QtWidgets.QFrame):
    def __init__(self, mainwindow, parent):
        super(GraphFrame, self).__init__(parent=parent)
        # parent storage
        self.mainWindow = mainwindow
        # set the design
        self.setMinimumSize(QtCore.QSize(300, 0))
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("graphFrame")
        # the graph frame has a white background and black border
        self.setStyleSheet(
            "QFrame {background-color: rgb(255, 255, 255);"
            "border-width: 1;"
            "border-radius: 3;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)}"
            )

        # stores vertices
        self.points = []

    def mousePressEvent(self, event):
        current_mode = self.mainWindow.modeComboBox.currentText()
        if current_mode == "Create Vertices":
            # get click position
            self.points.append((event.x(), event.y()))
        # update display
        self.update()

    def paintEvent(self, event):
        # create the painter and pen
        painter = QPainter(self)
        pen = QPen(Qt.red, 5)
        painter.setPen(pen)
        # draw all the points
        for point in self.points:
            painter.drawEllipse(point[0], point[1], 10, 10)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 428)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        # central widget to hold everything
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        # group for the stats widgets
        self.statsBox = QtWidgets.QGroupBox(self.centralwidget)
        self.statsBox.setMinimumSize(QtCore.QSize(200, 220))
        self.statsBox.setMaximumSize(QtCore.QSize(200, 220))
        self.statsBox.setObjectName("statsBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.statsBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # labels for how many of each colour there is
        self.colour1Label = QtWidgets.QLabel(self.statsBox)
        self.colour1Label.setObjectName("colour1Label")
        self.verticalLayout_2.addWidget(self.colour1Label)
        self.colour2Label = QtWidgets.QLabel(self.statsBox)
        self.colour2Label.setObjectName("colour2Label")
        self.verticalLayout_2.addWidget(self.colour2Label)
        self.colour3Label = QtWidgets.QLabel(self.statsBox)
        self.colour3Label.setObjectName("colour3Label")
        self.verticalLayout_2.addWidget(self.colour3Label)
        self.colour4Label = QtWidgets.QLabel(self.statsBox)
        self.colour4Label.setObjectName("colour4Label")
        self.verticalLayout_2.addWidget(self.colour4Label)
        self.gridLayout.addWidget(self.statsBox, 0, 0, 1, 1)
        # group to hold the colouring widgets
        self.colouringBox = QtWidgets.QGroupBox(self.centralwidget)
        self.colouringBox.setMinimumSize(QtCore.QSize(200, 125))
        self.colouringBox.setMaximumSize(QtCore.QSize(200, 125))
        self.colouringBox.setObjectName("colouringBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.colouringBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        # random colour check box
        self.randomCheckBox = QtWidgets.QCheckBox(self.colouringBox)
        self.randomCheckBox.setObjectName("randomCheckBox")
        self.verticalLayout_3.addWidget(self.randomCheckBox)
        # colour the vertices button
        self.colourButton = QtWidgets.QPushButton(self.colouringBox)
        self.colourButton.setObjectName("colourButton")
        self.verticalLayout_3.addWidget(self.colourButton)
        self.gridLayout.addWidget(self.colouringBox, 1, 0, 1, 1)
        # spacer so the above groups don't stretch, instead the spacer will
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        # line at the bottom
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 1)
        # group for holding the graph widgets
        self.graphBox = QtWidgets.QGroupBox(self.centralwidget)
        self.graphBox.setMinimumSize(QtCore.QSize(0, 0))
        self.graphBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.graphBox.setObjectName("graphBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.graphBox)
        self.verticalLayout.setObjectName("verticalLayout")
        # widget to hold settings for making the vertex graph
        self.graphOptionsWidget = QtWidgets.QWidget(self.graphBox)
        self.graphOptionsWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.graphOptionsWidget.setMaximumSize(QtCore.QSize(300, 50))
        self.graphOptionsWidget.setObjectName("graphOptionsWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.graphOptionsWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # mode combo box
        self.modeComboBox = QtWidgets.QComboBox(self.graphOptionsWidget)
        self.modeComboBox.setObjectName("modeComboBox")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.modeComboBox.addItem("")
        self.horizontalLayout.addWidget(self.modeComboBox)
        # clear button
        self.clearButton = QtWidgets.QPushButton(self.graphOptionsWidget)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.clearButton.clicked.connect(self.button_clear_all)
        self.verticalLayout.addWidget(self.graphOptionsWidget)
        # graph frame to draw vertices and their connections
        self.graphFrame = GraphFrame(self, self.graphBox)
        # window layout
        self.verticalLayout.addWidget(self.graphFrame)
        self.gridLayout.addWidget(self.graphBox, 0, 1, 4, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        # window menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 570, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # window statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Four Colouring"))
        # update all widgets
        self.statsBox.setTitle(_translate("MainWindow", "Stats"))
        self.colour1Label.setText(_translate("MainWindow", "Red: 0"))
        self.colour2Label.setText(_translate("MainWindow", "Yellow: 0"))
        self.colour3Label.setText(_translate("MainWindow", "Green: 0"))
        self.colour4Label.setText(_translate("MainWindow", "Blue: 0"))
        self.colouringBox.setTitle(_translate("MainWindow", "Colouring"))
        self.randomCheckBox.setText(_translate("MainWindow", "Random Colour Order"))
        self.colourButton.setText(_translate("MainWindow", "Colour"))
        self.graphBox.setTitle(_translate("MainWindow", "Graph"))
        self.modeComboBox.setItemText(0, _translate("MainWindow", "Create Vertices"))
        self.modeComboBox.setItemText(1, _translate("MainWindow", "Create Connections"))
        self.modeComboBox.setItemText(2, _translate("MainWindow", "Erase Vertices"))
        self.clearButton.setText(_translate("MainWindow", "Clear All"))

    def paintEvent(self, event):
        # use the main window paint event to cause the graph frame paint
        # event to trigger
        self.graphFrame.update()

    def button_clear_all(self):
        # remove all vertices
        self.graphFrame.points.clear()
        # update the graph frame by repainting it
        self.graphFrame.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
