#-------------------------------------------------------------------------------
# ACCESS TO RASTER
#-------------------------------------------------------------------------------
#importing module
import arcpy

#raster to array conversion
#C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sagunto\sagtm1.tif
#Also : C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sagunto\sagtm1.tif\Band_1
#C:\asignaturas\sig1\2013-2014\cuatrimestreB\teoria\MT9\elevgrd (grid's have not extension)
raster = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm1.tif')
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
from matplotlib import pyplot as plt

#Access to raster
raster = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm1.tif')
matrix = arcpy.RasterToNumPyArray(raster)

plt.imshow(matrix,cmap='gray')
plt.show()

#-------------------------------------------------------------------------------
# RASTER KERNEL
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
# DESCRIBE RASTER
#-------------------------------------------------------------------------------
import arcpy

raster = arcpy.Raster(r"C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm1.tif")

print raster.extent
print raster.catalogPath
print raster.bandCount
print raster.height
print raster.width
print raster.meanCellHeight


arcpy.CalculateStatistics_management(raster)
print raster.minimum
print raster.maximum
print raster.mean

#-------------------------------------------------------------------------------
# BANDS RASTER
#-------------------------------------------------------------------------------
#importing modules
import arcpy
import numpy as np
from matplotlib import pyplot as plt

#Access to raster
r_red = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm4.tif')
r_green = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm3.tif')
r_blue = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm2.tif')

m_red = arcpy.RasterToNumPyArray(r_red)
m_green = arcpy.RasterToNumPyArray(r_green)
m_blue = arcpy.RasterToNumPyArray(r_blue)

rgb = np.dstack((m_red, m_green, m_blue))

plt.imshow(rgb)
plt.show()


#-------------------------------------------------------------------------------
# COMPOSITE BANDS
#-------------------------------------------------------------------------------
#importing modules
import arcpy
import numpy as np
from matplotlib import pyplot as plt

#Access to raster
r_red = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm4.tif')
r_green = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm3.tif')
r_blue = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm2.tif')

output = r'C:\Users\laboratorios\ELVLC\DATA\sagunto\fc2.tif'
arcpy.CompositeBands_management([r_red, r_green, r_blue], output)


#-------------------------------------------------------------------------------
# HILLSHADE
#-------------------------------------------------------------------------------
#http://resources.arcgis.com/en/help/main/10.1/index.html#//00p600000003000000

#importing modules
import arcpy
from arcpy.sa import * #!!!WATCH OUT!!!

dem = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\DEM\mde1.asc')

#We must check the extension license
#If the extension is available...
if arcpy.CheckExtension("Spatial") == "Available": #!!!OJO!!!
    #take a license
    arcpy.CheckOutExtension("Spatial")
    #Arithmetic calculus example (land relief exaggerated)
    res = dem * 5
    #we apply two hillshade operations (map algebra expressions)
    hillshade1 = Hillshade(dem,315,45)
    hillshade2 = Hillshade(res,315,45)
    #Save the outputs
    hillshade1.save(r'C:\Users\laboratorios\ELVLC\DATA\results\hs1')
    hillshade2.save(r'C:\Users\laboratorios\ELVLC\DATA\results\hs2')

    #release the license
    arcpy.CheckInExtension("Spatial")
else:
    print ('Spatial Analyst license not available')


#-------------------------------------------------------------------------------
# SAVE FC
#-------------------------------------------------------------------------------
#importing modules
import arcpy
import numpy as np
from matplotlib import pyplot as plt

#Access to raster
r_red = arcpy.Raster(r'C:\Users\laboratorios\ELVLC\DATA\sagunto\sagtm1.tif')

extent = r_red.extent
ll_corner = arcpy.Point(extent.XMin, extent.YMin)
cell_size = r_red.meanCellHeight

m_red = arcpy.RasterToNumPyArray(r_red)
n_matrix = m_red+50

r_fc = arcpy.NumPyArrayToRaster(n_matrix, ll_corner, cell_size, cell_size)
r_fc.save (r'C:\Users\laboratorios\ELVLC\DATA\sagunto\my_raster.tif')

#-------------------------------------------------------------------------------
# TRESHOLD IMAGE
#-------------------------------------------------------------------------------
import cv2
from matplotlib import pyplot as plt

img = cv2.imread(r"C:\Users\laboratorios\ELVLC\DATA\lena.png", 0) #grayscale mode


#set parameters of the treshold
threshold = 128
max_value = 255
threshold_mode = cv2.THRESH_BINARY
res, thr = cv2.threshold(img, threshold, max_value, threshold_mode)

#prepare display
#first display area
plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(img, cmap="gray")

plt.subplot(1,2,2)
plt.title("Treshold: " +str(threshold))
plt.imshow(thr, cmap="gray")

#open the window
plt.show()