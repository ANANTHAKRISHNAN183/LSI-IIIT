'''Opens up the shape file and then upon mouse click find out the coordinates this is done for both the
 shapefiles and this coordinates are sent to the affibe_transform module
'''

import sys
from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import affine_transform
import read_create_new_shapefile as rcs

Mx = []
My = []
Mrx = []
Mry = []

count = 0
count1 = 0

def main():
    app = QApplication(sys.argv)
    ex1 = Window()
    ex1.show()
    sys.exit(app.exec_())

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        w = QWidget()
        b = QLabel(w)
        w.move(200, 200)
        self.setGeometry(50, 50, 400, 100)
        self.setWindowTitle("Geo Referencing!")

        self.b1 = QPushButton(self)
        self.b1.setText("Mouse_click_inputs")
        self.b1.move(30, 50)
        self.b1.clicked.connect(self.b1_clicked)

        self.b2 = QPushButton(self)
        self.b2.setText("Manually_give_inputs")
        self.b2.move(220, 50)
        self.b2.clicked.connect(self.b2_clicked)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)

    def b1_clicked(self):
        print "Take inputs using mouse_click"
        # self.b1.clicked.connect(self.on_pushButton_clicked)
        ex1 = Window1(self)
        ex1.show()
        return

    def b2_clicked(self):
        print "Take coordinate inputs from the user"
        # here the inputs from the user has to be included which is the textbox module
        return

class Window1(QMainWindow):
    #creates a window
    def __init__(self, parent=None):
        super(Window1, self).__init__(parent)
        self.initUI()

    def initUI(self):
        w = QWidget()
        #b = QLabel(w)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("Mouse_click inputs!")

        #creates a button and upon clicking a shapefile is opened
        self.b1 = QPushButton(self)
        self.b1.setText("shape_File1")
        self.b1.move(45, 100)
        self.b1.clicked.connect(self.b1_clicked)

        #creates another button upon clicking another shapefile is opened
        self.b2 = QPushButton(self)
        self.b2.setText("shape_File2")
        self.b2.move(250, 100)
        self.b2.clicked.connect(self.b2_clicked)

        #this 3rd button is used to view the affine table
        self.b3 = QPushButton(self)
        self.b3.setText("affine table")
        self.b3.move(145, 250)
        self.b3.clicked.connect(self.b3_clicked)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(200, 0, 200, 200)
        qp.drawLine(0, 200, 400, 200)

    def b1_clicked(self):
        print "Button 1 clicked"
        QgsApplication.setPrefixPath("/usr", True)
        QgsApplication.initQgis()
        #open the shapefile
        self.viewer = MapViewer("shapefiles/Vindhya algo testDXF_segmentedCenterLines.shp")
        return

    def b2_clicked(self):
        print "Button 2 clicked"
        QgsApplication.setPrefixPath("/usr", True)
        QgsApplication.initQgis()
        #open another shapefile
        self.viewer1= MapViewer1("shapefiles/Vindhya algo testDXF_segmentedCenterLines.shp")
        return
    def b3_clicked(self):
        #opens up the table
        flg1, flg2, error,flag,A=affine_transform.main(Mx,My,Mrx,Mry)
        self.b3.layout = QGridLayout(self)
        self.b3.layout.addWidget(self.b3)
        length = len(Mx)
        self.GridLayout = MyGrid(flg1, flg2, error,length)
        #this list will contain only those points that are needed for transformation error points will be removed
        for i in range(length+1):
            if(i==flg1):
                Mx.remove(Mx[i])
                My.remove(My[i])
                Mrx.remove(Mrx[i])
                Mry.remove(Mry[i])
                error.remove(error[i])
                break
        length=len(Mx)
        for i in range(length+1):
            if(i==flg2):
                Mx.remove(Mx[i])
                My.remove(My[i])
                Mrx.remove(Mrx[i])
                Mry.remove(Mry[i])
                error.remove(error[i])
                break
        #the below method is used to generate the coordinates from the cvs file initally a cvs file has to be created
        shapex,shapey,shapex_length,Total_id=rcs.main()
        new_shapex = [0 for i in range(shapex_length)]
        new_shapey = [0 for i in range(shapex_length)]
        for i in range(shapex_length):
            q=0
            new_shapex[i]=A[flag][q][0]*shapex[i]+A[flag][q][1]*shapey[i]+A[flag][q][2]
            q=1
            new_shapey[i]=A[flag][q][0]*shapex[i]+A[flag][q][1]*shapey[i]+A[flag][q][2]
        #this below method us used to generate a new shapefile using the new coordinates produced..
        rcs.transformed_shapefile(new_shapex,new_shapey,Total_id)
        #if u wish to view that shapefile in the console itself then create another mapviewer class here to view
        #it here directly or it can be seen in qgis .

class MyGrid(QTableView):
    #for viewing the table
    def __init__(self,flg1,flg2,error,length):

        self.table = QTableWidget()
        self.tableItem = QTableWidgetItem()
        # initiate table
        self.table.setWindowTitle("Main affine transforms table")
        self.table.resize(400, 300)
        self.table.columnWidth(4000)
        self.table.setRowCount(length+1)
        self.table.setColumnCount(6)

        # set data row1
        self.table.setItem(0, 0, QTableWidgetItem("point num"))
        self.table.setItem(0, 1, QTableWidgetItem("Mx"))
        self.table.setItem(0, 2, QTableWidgetItem("My"))
        self.table.setItem(0, 3, QTableWidgetItem("Mrx"))
        self.table.setItem(0, 4, QTableWidgetItem("Mry"))
        self.table.setItem(0, 5, QTableWidgetItem("Error"))
        j=0
        for i in range(1,length+1):
            self.table.setItem(i, 0, QTableWidgetItem(str(i)))
        j=1
        for i in range(1,length+1):
                self.table.setItem(i, j, QTableWidgetItem(str(Mx[i-1])))
        j=2
        for i in range(1,length+1):
                self.table.setItem(i, j, QTableWidgetItem(str(My[i-1])))
        j=3
        for i in range(1,length+1):
                self.table.setItem(i, j, QTableWidgetItem(str(Mrx[i-1])))
        j=4
        for i in range(1,length+1):
                self.table.setItem(i, j, QTableWidgetItem(str(Mry[i-1])))

        j=5
        for i in range(1,length+1):
                self.table.setItem(i, j, QTableWidgetItem(str(error[i-1])))
        i=flg1+1
        for j in range(6):
            self.table.item(i, j).setBackground(QColor(100, 100, 150))
        i = flg2+1
        for j in range(6):
            self.table.item(i, j).setBackground(QColor(100, 100, 150))

        self.table.show()

class PointTool(QgsMapToolEmitPoint):
    #(for shapefile1)
    #here this is used for the clicking and picking the coordinates for the shapefile click the coordinates after zooming in
    #zoom can de done using mouse
    count = 0

    def __init__(self, canvas):
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasReleaseEvent(self, mouseEvent):
        if (self.count == 8):
            return
        qgsPoint = self.toMapCoordinates(mouseEvent.pos())
        print('x:', qgsPoint.x(), ', y:', qgsPoint.y())
        Mx.append(qgsPoint.x())
        My.append(qgsPoint.y())
        self.count = self.count + 1


class MapViewer(QMainWindow):
    #for shapefile1
    #This Mapviewer is used for viewing the shapefile on canvas
    def __init__(self, shapefile):
        QMainWindow.__init__(self)
        self.setWindowTitle("Map Viewer")
        self.canvas = QgsMapCanvas()
        self.canvas.useImageToRender(False)
        self.canvas.setCanvasColor(Qt.white)
        toolIdentify = PointTool(self.canvas)
        self.canvas.setMapTool(toolIdentify)
        layer = QgsVectorLayer(shapefile, "large", "ogr")
        if not layer.isValid():
            return IOError("Invalid Shapefile")

        QgsMapLayerRegistry.instance().addMapLayer(layer)
        self.canvas.setExtent(layer.extent())
        self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
        self.canvas.show()
        self.setupGui()
        self.setCentralWidget(self.canvas)



class PointTool1(QgsMapToolEmitPoint):
    # (for shapefile2)
    ''' here this is used for the clicking and picking the coordinates for the shapefile click the
    coordinates after zooming in'''
    # zoom can de done using mouse
    count1 = 0

    def __init__(self, canvas):
        QgsMapToolEmitPoint.__init__(self, canvas)

    def canvasReleaseEvent(self, mouseEvent):
        if (self.count1 == 8):
            return
        qgsPoint = self.toMapCoordinates(mouseEvent.pos())
        print('x:', qgsPoint.x(), ', y:', qgsPoint.y())
        Mrx.append(qgsPoint.x())
        Mry.append(qgsPoint.y())
        self.count1 = self.count1 + 1

class MapViewer1(QMainWindow):
    # for shapefile2
    # This Mapviewer is used for viewing the shapefile on canvas
    def __init__(self, shapefile):
        QMainWindow.__init__(self)
        self.setWindowTitle("Map Viewer")

        self.canvas = QgsMapCanvas()
        self.canvas.useImageToRender(False)

        self.canvas.setCanvasColor(Qt.white)
        toolIdentify = PointTool1(self.canvas)
        self.canvas.setMapTool(toolIdentify)


        layer = QgsVectorLayer(shapefile, "large", "ogr")
        if not layer.isValid():
            return IOError("Invalid Shapefile")

        QgsMapLayerRegistry.instance().addMapLayer(layer)
        self.canvas.setExtent(layer.extent())
        self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
        self.canvas.show()
        self.setupGui()
        self.setCentralWidget(self.canvas)

if __name__ == '__main__':
    main()
