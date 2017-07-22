'''Here actually both the inputs are  taken from the user(reference map and the one one that has to be transformed ).
But sir asked to take one as a shapefile and then coordinate click and the other one manually so the other half part of the code has to be changed to mapviewer(reference shapefile has to be changed)
'''
import sys
from qgis.core import *
from qgis.gui import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import affine_transform

class inputshapefile1(QWidget):
    Mx = []
    My =  []

    def __init__(self, parent=None):
        super(inputshapefile1, self).__init__(parent)

        j=0
        flo = QFormLayout()
        self.setLayout(flo)
        self.setWindowTitle("coordinates of the 1st shapefile")

        e1 = QLineEdit(raw_input("enter the x coordinate of point 1:"))
        self.Mx.append(e1.text())
        flo.addRow("X-coordinate1", e1)

        e2 = QLineEdit(raw_input("enter the y coordinate of point1:"))
        self.My.append(e2.text())
        flo.addRow("Y-coordinate1", e2)


        e3 = QLineEdit(raw_input("enter the x coordinate of point2:"))
        self.Mx.append(e3.text())
        flo.addRow("X-coordinate2", e3)

        e4 = QLineEdit(raw_input("enter the y coordinate of point2:"))
        self.My.append(e4.text())
        flo.addRow("Y-coordinate2", e4)


        e5 = QLineEdit(raw_input("enter the x coordinate of point3:"))
        self.Mx.append(e5.text())
        flo.addRow("X-coordinate3", e5)

        e6 = QLineEdit(raw_input("enter the y coordinate of point3:"))
        self.My.append(e6.text())
        flo.addRow("Y-coordinate3", e6)


        e7 = QLineEdit(raw_input("enter the x coordinate of point4:"))
        self.Mx.append(e7.text())
        flo.addRow("X-coordinate4", e7)

        e8 = QLineEdit(raw_input("enter the y coordinate of point4:"))
        self.My.append(e8.text())
        flo.addRow("Y-coordinate4", e8)

        e9 = QLineEdit(raw_input("enter the x coordinate of point5:"))
        self.Mx.append(e9.text())
        flo.addRow("X-coordinate5", e9)

        e10 = QLineEdit(raw_input("enter the y coordinate of point5:"))
        self.My.append(e10.text())
        flo.addRow("Y-coordinate5", e10)

        e11 = QLineEdit(raw_input("enter the x coordinate of point6:"))
        self.Mx.append(e11.text())
        flo.addRow("X-coordinate6", e11)

        e12 = QLineEdit(raw_input("enter the y coordinate of point6:"))
        self.My.append(e12.text())
        flo.addRow("Y-coordinate6", e12)

        e13 = QLineEdit(raw_input("enter the x coordinate of point7:"))
        self.Mx.append(e13.text())
        flo.addRow("X-coordinate7", e13)

        e14 = QLineEdit(raw_input("enter the y coordinate of point7:"))
        self.My.append(e14.text())
        flo.addRow("Y-coordinate7", e14)

        e15 = QLineEdit(raw_input("enter the x coordinate of point8:"))
        self.Mx.append(e15.text())
        flo.addRow("X-coordinate8", e15)

        e16 = QLineEdit(raw_input("enter the y coordinate of point8:"))
        self.My.append(e16.text())
        flo.addRow("Y-coordinate8", e16)
        self.Mx = [float(i) for i in self.Mx]
        self.My = [float(i) for i in self.My]

class inputshapefile2(QWidget):
    Mrx = []
    Mry =  []


    def __init__(self, parent=None):
        super(inputshapefile2, self).__init__(parent)

        j=0
        flo = QFormLayout()
        self.setLayout(flo)
        self.setWindowTitle("coordinates of the 2nd shapefile")

        e1 = QLineEdit(raw_input("enter the x coordinate of point 1:"))
        self.Mrx.append(e1.text())
        flo.addRow("X-coordinate1", e1)

        e2 = QLineEdit(raw_input("enter the y coordinate of point1:"))
        self.Mry.append(e2.text())
        flo.addRow("Y-coordinate1", e2)


        e3 = QLineEdit(raw_input("enter the x coordinate of point2:"))
        self.Mrx.append(e3.text())
        flo.addRow("X-coordinate2", e3)

        e4 = QLineEdit(raw_input("enter the y coordinate of point2:"))
        self.Mry.append(e4.text())
        flo.addRow("Y-coordinate2", e4)


        e5 = QLineEdit(raw_input("enter the x coordinate of point3:"))
        self.Mrx.append(e5.text())
        flo.addRow("X-coordinate3", e5)

        e6 = QLineEdit(raw_input("enter the y coordinate of point3:"))
        self.Mry.append(e6.text())
        flo.addRow("Y-coordinate3", e6)


        e7 = QLineEdit(raw_input("enter the x coordinate of point4:"))
        self.Mrx.append(e7.text())
        flo.addRow("X-coordinate4", e7)

        e8 = QLineEdit(raw_input("enter the y coordinate of point4:"))
        self.Mry.append(e8.text())
        flo.addRow("Y-coordinate4", e8)

        e9 = QLineEdit(raw_input("enter the x coordinate of point5:"))
        self.Mrx.append(e9.text())
        flo.addRow("X-coordinate5", e9)

        e10 = QLineEdit(raw_input("enter the y coordinate of point5:"))
        self.Mry.append(e10.text())
        flo.addRow("Y-coordinate5", e10)

        e11 = QLineEdit(raw_input("enter the x coordinate of point6:"))
        self.Mrx.append(e11.text())
        flo.addRow("X-coordinate6", e11)

        e12 = QLineEdit(raw_input("enter the y coordinate of point6:"))
        self.Mry.append(e12.text())
        flo.addRow("Y-coordinate6", e12)

        e13 = QLineEdit(raw_input("enter the x coordinate of point7:"))
        self.Mrx.append(e13.text())
        flo.addRow("X-coordinate7", e13)

        e14 = QLineEdit(raw_input("enter the y coordinate of point7:"))
        self.Mry.append(e14.text())
        flo.addRow("Y-coordinate7", e14)

        e15 = QLineEdit(raw_input("enter the x coordinate of point8:"))
        self.Mrx.append(e15.text())
        flo.addRow("X-coordinate8", e15)

        e16 = QLineEdit(raw_input("enter the y coordinate of point8:"))
        self.Mry.append(e16.text())
        flo.addRow("Y-coordinate8", e16)
        self.Mrx=[float(i) for i in self.Mrx]
        self.Mry = [float(i) for i in self.Mry]

def main():
    app = QApplication(sys.argv)
    ex1 = inputshapefile1()
    print "input the next shapefile"
    ex2 = inputshapefile2()
    ex1.show()
    ex2.show()
    # print ex1.Mx,ex1.My,ex2.Mx,ex2.My

    flg1, flg2, error = affine_transform.main(ex1.Mx, ex1.My, ex2.Mrx, ex2.Mry)
    layout = QGridLayout()
    table = QTableWidget()
    tableItem = QTableWidgetItem()
    print ex1.Mx,ex1.My, ex2.Mrx,ex2.Mry, flg1,flg2, error
    # initiate table
    table.setWindowTitle("Main affine transforms table")
    table.resize(400, 300)
    table.columnWidth(4000)
    table.setRowCount(9)
    table.setColumnCount(6)
    # set data row1
    table.setItem(0, 0, QTableWidgetItem("point num"))
    table.setItem(0, 1, QTableWidgetItem("Mx"))
    table.setItem(0, 2, QTableWidgetItem("My"))
    table.setItem(0, 3, QTableWidgetItem("Mrx"))
    table.setItem(0, 4, QTableWidgetItem("Mry"))
    table.setItem(0, 5, QTableWidgetItem("Error"))
    table.setItem(1, 0, QTableWidgetItem("1"))
    table.setItem(2, 0, QTableWidgetItem("2"))
    table.setItem(3, 0, QTableWidgetItem("3"))
    table.setItem(4, 0, QTableWidgetItem("4"))
    table.setItem(5, 0, QTableWidgetItem("5"))
    table.setItem(6, 0, QTableWidgetItem("6"))
    table.setItem(7, 0, QTableWidgetItem("7"))
    table.setItem(8, 0, QTableWidgetItem("8"))
    j=1
    for i in range(1,9):
        table.setItem(i, j, QTableWidgetItem(str(ex1.Mx[i-1])))
    j=2
    for i in range(1,9):
        table.setItem(i, j, QTableWidgetItem(str(ex1.My[i-1])))
    j=3
    for i in range(1,9):
        table.setItem(i, j, QTableWidgetItem(str(ex2.Mrx[i-1])))
    j=4
    for i in range(1,9):
        table.setItem(i, j, QTableWidgetItem(str(ex2.Mry[i-1])))

    j=5
    for i in range(1,9):
        table.setItem(i, j, QTableWidgetItem(str(error[i-1])))
    i=flg1+1
    for j in range(6):
        table.item(i, j).setBackground(QColor(100, 100, 150))
    i = flg2+1
    for j in range(6):
        table.item(i, j).setBackground(QColor(100, 100, 150))

    table.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



'''
enter the x coordinate of point 1:-0.5096
enter the y coordinate of point1:0.4664
enter the x coordinate of point2:-0.2453
enter the y coordinate of point2: 0.6144
enter the x coordinate of point3:0.0591
enter the y coordinate of point3:0.6187
enter the x coordinate of point4:0.3319
enter the y coordinate of point4:0.3966
enter the x coordinate of point5:0.3504
enter the y coordinate of point5:0.0435
enter the x coordinate of point6:0.1289
enter the y coordinate of point6:-0.2102
enter the x coordinate of point7:-0.2178
enter the y coordinate of point7:-0.2123
enter the x coordinate of point8:-0.4906
enter the y coordinate of point8:0.09216
input the next shapefile
enter the x coordinate of point 1:-1.4803
enter the y coordinate of point1:-0.0122
enter the x coordinate of point2:-1.3629
enter the y coordinate of point2: 0.3634
enter the x coordinate of point3:-1.0987
enter the y coordinate of point3:0.6267
enter the x coordinate of point4:-0.6693
enter the y coordinate of point4: -0.6619
enter the x coordinate of point5:-0.3691
enter the y coordinate of point5: 0.4104
enter the x coordinate of point6:-0.3154
enter the y coordinate of point6:0.0525
enter the x coordinate of point7:-0.6366
enter the y coordinate of point7:-0.3451
enter the x coordinate of point8:-1.0811
enter the y coordinate of point8:-0.2571

'''
