#-------------------------------------------------------------------------------
# ACCESS TO RASTER
#-------------------------------------------------------------------------------

#importing module
import arcpy

#raster to array conversion
#C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sagunto\sagtm1.tif
#Also : C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sagunto\sagtm1.tif\Band_1
#C:\asignaturas\sig1\2013-2014\cuatrimestreB\teoria\MT9\elevgrd (grid's have not extension)
raster = arcpy.Raster(r'E:\Asignaturas\DAS\2016-2017\datos\sagunto\sagtm1.tif')
#Getting raster properties
extent = raster.extent
name = raster.name
format_type = raster.format
number_of_bands = raster.bandCount
spatial_reference = raster.spatialReference
pixel_type = raster.pixelType
cell_size = raster.meanCellHeight
number_of_pixels_x = raster.width
number_of_pixels_y = raster.height
#In some cases, statistical values can be "None".
#So you have to run firstly the tool CalculateStatistics_management
minimum = raster.minimum
maximum = raster.maximum
mean = raster.mean
if minimum == None:
    arcpy.CalculateStatistics_management(raster)
    minimum = raster.minimum
    maximum = raster.maximum
    mean = raster.mean
#Equivalent: mean = arcpy.GetRasterProperties_management(raster,'MEAN')
#Output
print('Name: ' + name)
print ("XMin:" +str(extent.XMin)+" ; YMin: "+str(extent.YMin))
print('Format: ' + format_type)
print('Number of bands: '+ str(number_of_bands))
print('Spatial reference: '+ spatial_reference.name)
print('Type of data: ' + pixel_type)
print('Cell size: ' + str(cell_size))
print('Width: ' + str(number_of_pixels_x))
print('Heigh: ' + str(number_of_pixels_y))
print('Minimum value: ' + str(minimum))
print('Maximum value: ' + str(maximum))
print('Mean value: ' + str(mean))

#-------------------------------------------------------------------------------
# RASTER TO NUMPY
#-------------------------------------------------------------------------------
#importing modules
import arcpy
import numpy as np

#Access to raster
raster = arcpy.Raster(r'E:\Asignaturas\DAS\2016-2017\datos\sagunto\sagtm1.tif')
#raster to numpy array conversion
raster_matrix = arcpy.RasterToNumPyArray(raster)
#array size
height,width = raster_matrix.shape
print height,width
#sum of all values in the matrix
matrix_sum = np.sum(raster_matrix)
#Computation of mean value in matrix
mean = matrix_sum/(float(height)*float(width))
#Output
print mean

#-------------------------------------------------------------------------------
# RASTER MEAN FILTER
#-------------------------------------------------------------------------------
#importing modules
import arcpy
#output overwrite
arcpy.env.overwriteOutput = True

#kernel components
kernel = [1,1,1,1,1,1,1,1,1]

#raster properties
raster = arcpy.Raster(r'E:\Asignaturas\DAS\2016-2017\datos\sagunto\sagtm1.tif')
size = raster.meanCellHeight
width = raster.width
height = raster.height
extent = raster.extent
esquina_ii = arcpy.Point(extent.XMin,extent.YMin)

#raster to array conversion
raster1 = arcpy.RasterToNumPyArray(raster)
raster2 = arcpy.RasterToNumPyArray(raster)
rows,columns = height,width
#filter application
for row in range(1,rows-1):
    for column in range(1,columns-1):
        value1 = raster1.item(row-1,column-1)* kernel[0]
        value2 = raster1.item(row-1,column)* kernel[1]
        value3 = raster1.item(row-1,column+1)* kernel[2]
        value4 = raster1.item(row,column-1)* kernel[3]
        value5 = raster1.item(row,column)* kernel[4]
        value6 = raster1.item(row,column+1)* kernel[5]
        value7 = raster1.item(row+1,column-1)* kernel[6]
        value8 = raster1.item(row+1,column)* kernel[7]
        value9 = raster1.item(row+1,column+1)* kernel[8]
        value = (value1+value2+value3+value4+value5+value6+value7+value8+value9)/9
        raster2[row,column] = value

#array to raster conversion
res = arcpy.NumPyArrayToRaster(raster2,esquina_ii,size,size)
#save the raster
res.save(r'E:\Asignaturas\DAS\2016-2017\datos\sagunto\sagtm1_m.tif')


#-------------------------------------------------------------------------------
# RASTER BLOCK PROCESSING
#-------------------------------------------------------------------------------
#http://resources.arcgis.com/en/help/main/10.1/index.html#//00p600000003000000

#importing modules
import arcpy
from arcpy.sa import * #!!!WATCH OUT!!!

matrix = arcpy.Raster(r'E:\Asignaturas\DAS\2016-2017\datos\DEM\mde1.asc')
#We must check the extension license
#If the extension is available...
if arcpy.CheckExtension("Spatial") == "Available": #!!!OJO!!!
    #take a license
    arcpy.CheckOutExtension("Spatial")
    #Arithmetic calculus example (land relief exaggerated)
    res = matrix * 5
    #we apply two hillshade operations (map algebra expressions)
    hillshade1 = Hillshade(matrix,315,45)
    hillshade2 = Hillshade(res,315,45)
    #Save the outputs
    hillshade1.save(r'E:\Asignaturas\DAS\2016-2017\datos\output\hs1')
    hillshade2.save(r'E:\Asignaturas\DAS\2016-2017\datos\output\hs2')
    #release the license
    arcpy.CheckInExtension("Spatial")
else:
    print ('Spatial Analyst license not available')

#-------------------------------------------------------------------------------
# OPEN CV IMAGE SEGMENTATION
#-------------------------------------------------------------------------------
#importing modules
import cv2
from matplotlib import pyplot as plt

#open the image
img = cv2.imread('imagenes\\bolas.png',1)
#draw the image using matplotlib
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
#open a window to view the image
plt.show()


#-------------------------------------------------------------------------------
# RASTER TO NUMPY
#-------------------------------------------------------------------------------
import cv2
import numpy as np
from matplotlib import pyplot as plt

#open the image
path = 'imagenes\\bolas.png'
image = cv2.imread(path,0) #0: grayscale mode
#segmentation threshold
threshold = 128
#segmentation function with Opencv
vret,processed = cv2.threshold(image,threshold,255,cv2.THRESH_BINARY)
#matplotlib settings
plt.subplot(1,2,1) #two subplots (rows: 1; columns: 2)
plt.imshow(image,cmap = 'gray')
plt.title('Original')
plt.subplot(1,2,2)
plt.imshow(processed,cmap = 'gray')
plt.title('Threshold: {0}'.format(threshold))
#open a window to view the image
plt.show()

