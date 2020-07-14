from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
import sys
from math import sqrt
from fourcolourings import *

# all available colours to use are stored in this list. When choosing
# colours for vertices, vertices will be given numbers that represent a
# colour. 1 will represent the first colour in the list, 2 will represent
# the second colour in the list, and so on. A colour of 0 means no colour has
# been chosen yet
VERTEX_COLOURS = ["red", "yellow", "green", "blue", "magenta"]
# sizes for drawing wth the painter
VERTEX_PENSIZE = 5
CONNECTION_PENSIZE = 4
VERTEX_DIAMETER = 20


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

    def colour_vertices(self):
        # reset the colour of all the vertices
        for vertex in self.vertex_data:
            self.vertex_data[vertex]['colour'] = 0

        # if the vertices should be coloured in a random order
        random_colour_order = self.mainWindow.randomCheckBox.isChecked()

        # colour the vertices
        self.vertex_data, colour_total = colour_vertices(self.vertex_data, 5,
                                                         random_colour_order)
        # repaint with the new colours
        self.repaint()

        # update the main window labels to show how many of each colour
        print(colour_total)
        # there is
        self.mainWindow.update_colour_totals(colour_total[1], colour_total[2],
                                             colour_total[3], colour_total[4])

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
                "connections": []
            }
            self.current_vertex += 1

        # connect vertices with a line
        elif current_mode == "Create Edges":
            # get the closest vertex to the mouse click
            closest_vertex = self.get_closest_vertex(event,
                                                     self.graph_vertices)

            # the closest vertex must be within a certain distance
            if closest_vertex[0] and closest_vertex[1] <= VERTEX_DIAMETER:
                # a selected vertex already exists, connect the previously
                # selected vertex and the clicked vertex right now
                if self.selected_vertex:
                    # add the connection to each vertex if it hasn't been
                    # added already
                    if closest_vertex[0] not in self.vertex_data[self.selected_vertex]['connections']:
                        self.vertex_data[self.selected_vertex][
                            'connections'].append(closest_vertex[0])
                    if self.selected_vertex not in self.vertex_data[closest_vertex[0]]['connections']:
                        self.vertex_data[closest_vertex[0]][
                            'connections'].append(self.selected_vertex)
                    # remove the selected vertex
                    self.selected_vertex = None
                # make the clicked vertex the selected vertex
                else:
                    self.selected_vertex = closest_vertex[0]
            else:
                self.selected_vertex = None

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
                # the colour total labels will be updated
                colour_total = count_colours(self.vertex_data, 5)

                # erase the vertices
                for vertex in erase_vertices:
                    # subtract 1 from the colour total of the vertex if it
                    # is coloured
                    if self.vertex_data[vertex]['colour']:
                        colour_total = count_colours(self.vertex_data, 5)
                        colour_total[self.vertex_data[vertex]['colour']] -= 1

                    # remove all the vertex's connection
                    for conn in self.vertex_data[vertex]['connections']:
                        self.vertex_data[conn]['connections'].remove(vertex)
                    # remove this vertex from the vertex data dictionaries
                    del self.graph_vertices[vertex]
                    del self.vertex_data[vertex]

                # update the colour total labels
                self.mainWindow.update_colour_totals(colour_total[1],
                                                     colour_total[2],
                                                     colour_total[3],
                                                     colour_total[4])

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
        elif qt_colour == "magenta":
            return Qt.magenta
        else:
            return Qt.black

    def colour_painter(self, painter, pen_colour, pen_size, brush_colour,
                       alpha_brush=False):
        # create the pen and brush with the correct colours
        if alpha_brush:
            pen = QPen(self.get_qt_colour(pen_colour), 0)
        else:
            pen = QPen(self.get_qt_colour(pen_colour), pen_size)
        # only make a brush if required
        if brush_colour:
            # make the brush alpha if required
            if alpha_brush:
                brush = QBrush(self.get_qt_colour(brush_colour), 3)
            else:
                brush = QBrush(self.get_qt_colour(brush_colour))

        # set the pen and brush to the painter
        painter.setPen(pen)
        if brush_colour:
            painter.setBrush(brush)

        return painter

    def paintEvent(self, event):
        # create the painter
        painter = QPainter(self)

        # set the painter for the lines to connect vertices
        painter = self.colour_painter(painter, "black", CONNECTION_PENSIZE,
                                      False)
        # draw the connections between all vertices
        for vertex in self.graph_vertices:
            # get the position of the vertex on the graph
            pos = self.graph_vertices[vertex]
            x_pos, y_pos = pos[0], pos[1]

            # draw all its connections
            for conn in self.vertex_data[vertex]['connections']:
                painter.drawLine(x_pos, y_pos, self.graph_vertices[conn][0],
                                 self.graph_vertices[conn][1])

        # draw all the vertices
        for vertex in self.graph_vertices:
            # get the position of the vertex on the graph
            pos = self.graph_vertices[vertex]
            x_pos, y_pos = pos[0], pos[1]

            # colour the vertex transparent if it is selected
            if self.selected_vertex == vertex:
                painter = self.colour_painter(painter, "yellow",
                                              VERTEX_PENSIZE, "yellow", True)
                # draw the selection circle
                painter.drawEllipse(x_pos - VERTEX_DIAMETER,
                                    y_pos - VERTEX_DIAMETER,
                                    VERTEX_DIAMETER * 2, VERTEX_DIAMETER * 2)

            # create the painter to match the vertex's current colour
            vertex_colour = self.vertex_data[vertex]['colour']

            if vertex_colour == 0:
                painter = self.colour_painter(painter, "black", VERTEX_PENSIZE,
                                              "yellow")
            else:
                painter = self.colour_painter(painter,
                                              VERTEX_COLOURS[vertex_colour-1],
                                              VERTEX_PENSIZE,
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
        spacerItem = QtWidgets.QSpacerItem(0, 0,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
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

        # button connections
        self.clearButton.clicked.connect(self.button_clear_all)
        self.colourButton.clicked.connect(self.graphFrame.colour_vertices)

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
        self.randomCheckBox.setText(_translate("MainWindow", "Random Colour "
                                                             "Order"))
        self.colourButton.setText(_translate("MainWindow", "Colour"))
        self.graphBox.setTitle(_translate("MainWindow", "Graph"))
        self.modeComboBox.setItemText(0, _translate("MainWindow", "Create "
                                                                  "Vertices"))
        self.modeComboBox.setItemText(1, _translate("MainWindow", "Create "
                                                                  "Edges"))
        self.modeComboBox.setItemText(2, _translate("MainWindow", "Erase "
                                                                  "Vertices"))
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
        # update the colour totals
        self.update_colour_totals(0, 0, 0, 0)

    def update_colour_totals(self, colour1, colour2, colour3, colour4):
        self.colour1Label.setText(f"Red: {colour1}")
        self.colour1Label.repaint()
        self.colour2Label.setText(f"Yellow: {colour2}")
        self.colour2Label.repaint()
        self.colour3Label.setText(f"Green: {colour3}")
        self.colour3Label.repaint()
        self.colour4Label.setText(f"Blue: {colour4}")
        self.colour4Label.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
