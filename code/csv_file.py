#when lines are present in a shapefile
'''
import csv
with open('shapefiles/Vindhya algo testDXF_segmentedCenterLines.csv', 'rb') as csvfile:
     spamreader = csv.reader(csvfile)
     count=0
     lis=[]
     Mx=[]
     My=[]
     for row in spamreader:
         if(count==0):
             count=1
             continue
         row = row[0][12:]
         length=len(row)
         row=row[0:length-1]
         lis=row.split(',', 2)
         for i in lis:
              lis1=i.split(' ',1)
              Mx.append(lis1[0])
              My.append(lis1[1])
print Mx
print My
'''
#when a polygon is ddirectly considered
import csv
def main():
     Mx,My=Mx_My()
     Mrx,Mry=Mrx_Mry()
     return Mx,My,Mrx,Mry

def Mx_My():
     lis = []
     lis1 = []
     Mx = [0 for u in range(9)]
     My = [0 for u in range(9)]
     k=0
     with open('shapefiles/my_polygon.csv', 'rb') as csvfile:
          spamreader = csv.reader(csvfile)
          count=0
          for row in spamreader:
               lis.append(row[0])
          lis=lis[1][10:]
          length = len(lis)
          lis = lis[0:length - 2]
          length=len(lis)
          lis1=lis.split(',', 8)
          for i in lis1:
               lis2=i.split(' ',1)
               Mx[k]=lis2[0]
               My[k]=lis2[1]
               k=k+1
     Mx = Mx[:8]
     My = My[:8]
     Mx=[float(i) for i in Mx]
     My = [float(i) for i in My]
     print Mx
     print My
     return Mx,My


def Mrx_Mry():
     lis = []
     lis1 = []
     Mrx = [0 for u in range(9)]
     Mry = [0 for u in range(9)]
     k=0
     with open('shapefiles/other_polygon.csv', 'rb') as csvfile:
          spamreader = csv.reader(csvfile)
          count = 0
          for row in spamreader:
               lis.append(row[0])
          lis = lis[1][10:]
          length = len(lis)
          lis = lis[0:length - 2]
          length = len(lis)
          lis1 = lis.split(',', 8)
          for i in lis1:
               lis2 = i.split(' ', 1)
               Mrx[k]=lis2[0]
               Mry[k]=lis2[1]
               k=k+1
     Mrx=Mrx[:8]
     Mry = Mry[:8]
     Mrx = [float(i) for i in Mrx]
     Mry = [float(i) for i in Mry]
     print Mrx
     print Mry
     return Mrx, Mry


if __name__ == '__main__':
    Mx, My, Mrx, Mry= main()
