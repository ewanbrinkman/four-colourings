from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
import sys
from math import sqrt

PENSIZE = 5
VERTEX_DIAMETER = 20
VERTEX_COLOURS = ["red", "yellow", "green", "blue"]


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

        # graph vertices stores all the vertex positions on the graph frame
        self.graph_vertices = {}
        # vertex data stores the colour and connections of the vertices
        self.vertex_data = {}
        # current vertex is the vertex id to use next
        self.current_vertex = 1

        # the vertex currently selected to make a connection
        self.selected_vertex = None

    def get_pos_distance(self, pos1, pos2):
        # get the distance between two points
        return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    def get_closest_vertex(self, mouse_pos, vertices):
        # get the distances from the position clicked to the positions
        # of all the vertices
        smallest_distance = (None, 0)
        for vertex, pos in vertices.items():
            # find the distance to the point
            distance = self.get_pos_distance((mouse_pos.x(), mouse_pos.y()),
                                             (pos[0], pos[1]))

            # no smallest distance yet, this distance will become the
            # smallest distance
            if not smallest_distance[1]:
                smallest_distance = (vertex, distance)
            # make the new distance the smallest distance, if it is smaller
            else:
                if distance < smallest_distance[1]:
                    smallest_distance = (vertex, distance)

        return smallest_distance

    def mousePressEvent(self, event):
        # get the current mode of the graph
        current_mode = self.mainWindow.modeComboBox.currentText()
        # create a vertex at the clicked position
        if current_mode == "Create Vertices":
            # create a new vertex at the clicked position
            self.graph_vertices[self.current_vertex] = (event.x(), event.y())
            self.vertex_data[self.current_vertex] = {
                "colour": 0,
                "connections:": []
            }
            self.current_vertex += 1

        # connect vertices with a line
        elif current_mode == "Create Connections":
            # get the closest vertex to the mouse click
            closest_vertex = self.get_closest_vertex(event,
                                                     self.graph_vertices)

            # the closest vertex must be within a certain distance
            if closest_vertex[0] and closest_vertex[1] <= VERTEX_DIAMETER:
                self.selected_vertex = closest_vertex[0]

        # erase a vertex
        elif current_mode == "Erase Vertices":
            # list to hold vertices to be removed
            erase_vertices = []
            # get the distances from the position clicked to the positions
            # of all the vertices
            for vertex, pos in self.graph_vertices.items():
                # find the distance to the point
                distance = self.get_pos_distance((event.x(), event.y()),
                                                 (pos[0], pos[1]))
                # add the vertex to a list of vertices to be erased
                # don't erase the vertex in the loop, as that will change
                # the size the dictionary during iteration
                if distance <= VERTEX_DIAMETER:
                    erase_vertices.append(vertex)

            # erase any vertices in the erase list
            if erase_vertices:
                for vertex in erase_vertices:
                    del self.graph_vertices[vertex]
                    del self.vertex_data[vertex]

        # update display
        self.update()

    def get_qt_colour(self, qt_colour):
        if qt_colour == "red":
            return Qt.red
        elif qt_colour == "yellow":
            return Qt.yellow
        elif qt_colour == "green":
            return Qt.green
        elif qt_colour == "blue":
            return Qt.blue
        elif qt_colour == "black":
            return Qt.black

    def colour_painter(self, painter, pen_colour, brush_colour):
        # create the pen and brush with the correct colours
        pen = QPen(self.get_qt_colour(pen_colour), PENSIZE)
        brush = QBrush(self.get_qt_colour(brush_colour))
        # set the pen and brush to the painter
        painter.setPen(pen)
        painter.setBrush(brush)

        return painter

    def paintEvent(self, event):
        # create the painter
        painter = QPainter(self)

        print(self.selected_vertex)

        # draw all the vertices
        for vertex in self.graph_vertices:
            # get the position of the vertex on the graph
            pos = self.graph_vertices[vertex]
            x_pos, y_pos = pos[0], pos[1]

            # create the painter to match the vertex's current colour
            vertex_colour = self.vertex_data[vertex]['colour']

            if vertex_colour == 0:
                painter = self.colour_painter(painter, "black", "yellow")
            else:
                painter = self.colour_painter(painter,
                    VERTEX_COLOURS[vertex_colour-1],
                    VERTEX_COLOURS[vertex_colour-1])

            # draw the vertex
            painter.drawEllipse(x_pos - VERTEX_DIAMETER / 2,
                                y_pos - VERTEX_DIAMETER / 2,
                                VERTEX_DIAMETER, VERTEX_DIAMETER)


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
        self.graphFrame.graph_vertices.clear()
        self.graphFrame.vertex_data.clear()
        self.graphFrame.selected_vertex = None
        # update the graph frame by repainting it
        self.graphFrame.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
