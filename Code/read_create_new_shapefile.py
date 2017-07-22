#Open the cvs file create the cvs file using qgis initially and then use that cvs file to read all the coordinatesthen now return those values to shapefile now using the best A_F values calculate the new coordinates
from osgeo import ogr
import os
import csv
def main():
     Total_id = 0
     shapex = []
     shapey = []
     with open('shapefiles/Vindhya algo testDXF_segmentedCenterLines.csv', 'rb') as csvfile:
          spamreader = csv.reader(csvfile)
          count=0
          lis=[]

          for row in spamreader:
               if (count == 0):
                    count = 1
                    continue
               row = row[0][12:]
               length = len(row)
               row = row[0:length - 1]
               lis = row.split(',', 2)
               for i in lis:
                    lis1 = i.split(' ', 1)
                    shapex.append(lis1[0])
                    shapey.append(lis1[1])
               Total_id=Total_id+1
     shapex=[float(i) for i in shapex]
     shapey=[float(i) for i in shapey]
     shapex_length=len(shapex)
     return shapex,shapey,shapex_length,Total_id

#This module is used to generate a new shapefile with the new coordinates 
def transformed_shapefile(new_shapex,new_shapey,Total_id):

     driver = ogr.GetDriverByName('ESRI Shapefile')
     shapefile_name = "shapefiles/generated_shapefile.shp"
     if os.path.exists(shapefile_name):
          os.remove(shapefile_name)

     out_data_source = driver.CreateDataSource(shapefile_name)

     out_layer = out_data_source.CreateLayer('cleaned', geom_type=ogr.wkbLineString)

     out_layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
     out_layer_defn = out_layer.GetLayerDefn()
     j=0
     for i in range(Total_id):
          line = ogr.Geometry(ogr.wkbLineString)
          line.AddPoint(new_shapex[j], new_shapey[j])
          line.AddPoint(new_shapex[j+1],new_shapey[j+1])
          feature = ogr.Feature(out_layer_defn)
          feature.SetField('id',i)
          feature.SetGeometry(line)
          out_layer.CreateFeature(feature)
          feature.Destroy()
          j=j+2
     out_data_source.Destroy()


if __name__ == '__main__':
    shapex,shapey,shapex_length=main()
