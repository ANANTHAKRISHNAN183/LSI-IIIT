import sys, os

from Tkinter import *
from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *


import  affine_transform


def main():
    app = QApplication(sys.argv)
    ex1 = Window()
    ex1.show()
    sys.exit(app.exec_())

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        w = QWidget()
        b = QLabel(w)
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Geo Registration!")


        self.b1 = QPushButton(self)
        self.b1.setText("Shape_File1")
        self.b1.move(75, 150)
        self.b1.clicked.connect(self.b1_clicked)


        self.b2 = QPushButton(self)
        self.b2.setText("Shape_File2")
        self.b2.move(300, 150)
        self.b2.clicked.connect(self.b2_clicked)



        self.b3 = QPushButton(self)
        self.b3.setText("Table")
        self.b3.move(200, 400)
        self.b3.clicked.connect(self.b3_clicked)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()


    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 225, 500, 225)
        qp.drawLine(250, 0, 250, 225)

    def b2_clicked(self):
        print "Button 2 clicked"
        self.b2.layout = QHBoxLayout(self)
        self.b2.layout.addWidget(self.b2)

        QgsApplication.setPrefixPath("/usr", True)
        QgsApplication.initQgis()
        self.viewer1 = MapViewer("shapefiles/other_polygon.shp")
        self.viewer1.show()


    def b3_clicked(self):
        print "Table is clicked"
        self.b3.layout = QGridLayout(self)
        self.b3.layout.addWidget(self.b3)
        self.GridLayout = MyGrid(self)

    def b1_clicked(self):
        print "Button 1 clicked"
        self.b1.layout = QHBoxLayout(self)
        self.b1.layout.addWidget(self.b1)

        QgsApplication.setPrefixPath("/usr", True)
        QgsApplication.initQgis()
        self.viewer = MapViewer("shapefiles/Vindhya algo testDXF_segmentedCenterLines.shp")
        self.viewer.show()

class MyGrid(QTableView):
    def __init__(self, parent=None):
        self.table = QTableWidget()
        self.tableItem = QTableWidgetItem()

        # initiate table
        self.table.setWindowTitle("Main affine transforms table")
        self.table.resize(400, 300)
        self.table.columnWidth(4000)
        self.table.setRowCount(9)
        self.table.setColumnCount(6)

        # set data row1
        if __name__ == '__main__':
            Mx, My, Mrx, Mry, flg1, flg2, error=affine_transform.main()
        self.table.setItem(0, 0, QTableWidgetItem("point num"))
        self.table.setItem(0, 1, QTableWidgetItem("Mx"))
        self.table.setItem(0, 2, QTableWidgetItem("My"))
        self.table.setItem(0, 3, QTableWidgetItem("Mrx"))
        self.table.setItem(0, 4, QTableWidgetItem("Mry"))
        self.table.setItem(0, 5, QTableWidgetItem("Error"))
        self.table.setItem(1, 0, QTableWidgetItem("1"))
        self.table.setItem(2, 0, QTableWidgetItem("2"))
        self.table.setItem(3, 0, QTableWidgetItem("3"))
        self.table.setItem(4, 0, QTableWidgetItem("4"))
        self.table.setItem(5, 0, QTableWidgetItem("5"))
        self.table.setItem(6, 0, QTableWidgetItem("6"))
        self.table.setItem(7, 0, QTableWidgetItem("7"))
        self.table.setItem(8, 0, QTableWidgetItem("8"))
        j=1
        for i in range(1,9):
                self.table.setItem(i, j, QTableWidgetItem(str(Mx[i-1])))
        j=2
        for i in range(1,9):
                self.table.setItem(i, j, QTableWidgetItem(str(My[i-1])))
        j=3
        for i in range(1,9):
                self.table.setItem(i, j, QTableWidgetItem(str(Mrx[i-1])))
        j=4
        for i in range(1,9):
                self.table.setItem(i, j, QTableWidgetItem(str(Mry[i-1])))
        j=5
        for i in range(1,9):
                self.table.setItem(i, j, QTableWidgetItem(str(error[i-1])))
        i=flg1+1
        for j in range(6):
            self.table.item(i, j).setBackground(QColor(100, 100, 150))
        i = flg2+1
        for j in range(6):
            self.table.item(i, j).setBackground(QColor(100, 100, 150))

        # show table
        self.table.show()


class MapViewer(QMainWindow):
    root = Tk()
    def __init__(self, shapefile):
        QMainWindow.__init__(self)
        self.setWindowTitle("Map Viewer")



        canvas = QgsMapCanvas()
        canvas.useImageToRender(False)
        canvas.setCanvasColor(Qt.white)
        canvas.show()


        layer = QgsVectorLayer(shapefile, "large", "ogr")
        if not layer.isValid():
            return IOError("Invalid Shapefile")

        QgsMapLayerRegistry.instance().addMapLayer(layer)
        canvas.setExtent(layer.extent())
        canvas.setLayerSet([QgsMapCanvasLayer(layer)])

        self.setCentralWidget(canvas)

    def key(event):
        print "pressed", repr(event.char)

    def callback(event):
        print "clicked at", event.x, event.y

    canvas = Canvas(root, width=100, height=100)
    canvas.bind("<Key>", key)
    canvas.bind("<Button-1>", callback)
    canvas.pack()



if __name__ == '__main__':
   main()