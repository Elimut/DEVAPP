#-------------------------------------------------------------------------------
# EXTRACT ROADS
#-------------------------------------------------------------------------------
#importing modules
import arcpy

#enable output overwrite
arcpy.env.overwriteOutput = True

#input folder
arcpy.env.workspace = r'I:\tutorial_gvsig\carto\datos\castilla-leon'

#output folder
output = 'I:\\asignaturas\\sig-I\\2012-2013\\cuatrimestreB\\teoria\\MT7\\salida'

#layers
layer_towns = 'NUCLEOS.shp'
layer_roads = 'CARRETERA.shp'

#Analysis:******************
#Buffer
arcpy.Buffer_analysis(layer_towns,output+'\\buf_towns.shp',1000)
#Clip
arcpy.Clip_analysis(layer_roads,output+'\\buf_towns.shp',output+'\\clip_roads.shp')

#-------------------------------------------------------------------------------
# SELECT RASTER
#-------------------------------------------------------------------------------
#importing modules
import arcpy
from arcpy.sa import *


#enable output overwrite
arcpy.env.overwriteOutput = True

#imput folder
arcpy.env.workspace = r'C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sextante'

#layer
raster_layer = 'dem.asc' #asc file

#ckeking license availability
if arcpy.CheckExtension('Spatial') == 'Available':
    #Take a license
    arcpy.CheckOutExtension('Spatial')
    #run a SA tool
    output_layer = arcpy.sa.ExtractByAttributes(raster_layer,'"VALUE" >= 1000 AND "VALUE" <= 1500')
    #save the layer
    output_layer.save('DEM_sel')
    #release the license
    arcpy.CheckInExtension('Spatial')
else:
    print ('License not available')


#-------------------------------------------------------------------------------
# CREATE TIN
#-------------------------------------------------------------------------------
#importing module
import arcpy

#enable output overwrite
arcpy.env.overwriteOutput = True

#output folder
arcpy.env.workspace = 'I:\\asignaturas\\sig-I\\2012-2013\\cuatrimestreB\\teoria\\MT7\\salida'

#ckeking license availability
if arcpy.CheckExtension("3D") == "Available":
    #Take a license
    arcpy.CheckOutExtension("3D")
    #Create a new empty TIN
    arcpy.CreateTin_3d('tin')
    #release the license
    arcpy.CheckInExtension("3D")
else:
    print ('License not available')

#-------------------------------------------------------------------------------
# EDIT TIN
#-------------------------------------------------------------------------------
#importing module
import arcpy

#enable output overwrite
arcpy.env.overwriteOutput = True

#output folder
arcpy.env.workspace = 'I:\\asignaturas\\sig-I\\2012-2013\\cuatrimestreB\\teoria\\MT7\\salida'

#input folder
input_folder = 'I:\\64032'

#ckeking license availability
if arcpy.CheckExtension("3D") == "Available":
    #take the license
    arcpy.CheckOutExtension("3D")
    #Create a new empty TIN
    arcpy.CreateTin_3d('tin')
    #Edit the TIN
    arcpy.EditTin_3d('tin',input_folder+'\\64032puntos_cota.shp ELEVACI?N <none> masspoints true','true')
    #release the license
    arcpy.CheckInExtension("3D")
else:
    print ('License not available')

#-------------------------------------------------------------------------------
# TIN TO GRID
#-------------------------------------------------------------------------------
#importing module
import arcpy

#enable output overwrite
arcpy.env.overwriteOutput = True

#output folder
arcpy.env.workspace = 'I:\\asignaturas\\sig-I\\2012-2013\\cuatrimestreB\\teoria\\MT7\\salida'

#tool parameters
tin = 'tin'
grid = 'grid'
data_type = 'FLOAT'
interpolation_method = 'LINEAR'
sampling_method = 'CELLSIZE 10'
factor = 1

if arcpy.CheckExtension("3D") == "Available":
    arcpy.CheckOutExtension("3D")
    #TIN to GRID conversion
    arcpy.TinRaster_3d(tin,grid,data_type, interpolation_method, sampling_method,factor)
    arcpy.CheckInExtension("3D")
else:
    print ('Licencia 3D no disponible')

#-------------------------------------------------------------------------------
# SLOPE MAP
#-------------------------------------------------------------------------------
#importing module
import arcpy

#enable output overwrite
arcpy.env.overwriteOutput = True

#output folder
arcpy.env.workspace = 'I:\\asignaturas\\sig-I\\2012-2013\\cuatrimestreB\\teoria\\MT7\\salida'

#tool parameters
grid = 'grid'
output_layer = 'slopes'
units = 'DEGREE'
factor = 1

if arcpy.CheckExtension("3D") == "Available":
    arcpy.CheckOutExtension("3D")
    #slope tool
    arcpy.Slope_3d(grid,output_layer,units,factor)
    arcpy.CheckInExtension("3D")
else:
    print ('License not available')

#-------------------------------------------------------------------------------
# NDVI
#-------------------------------------------------------------------------------
#Info:
#https://en.wikipedia.org/wiki/Normalized_Difference_Vegetation_Index

#importing modules
import arcpy
from arcpy.sa import *

#Acceso a las variable de entorno
#enable output overwrite
arcpy.env.overwriteOutput = True
#input folder
arcpy.env.workspace = r'C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sagunto'
if arcpy.CheckExtension('Spatial') == 'Available':
    arcpy.CheckOutExtension('Spatial')
    #load the raster layer. Besides we convert the values from integer to float
    r = Float(Raster('sagtm3.tif')) #landsat red band
    irc = Float(Raster('sagtm4.tif')) #landsat near-infrared band
    #NDVI calculus
    ndvi = (irc-r)/(irc+r) #values between -1 and 1
    #raster reclassification from an ascii file (rmp extension)
    ndvi_reclass = ReclassByASCIIFile(ndvi,'ndvi.rmp')
    #save the result
    ndvi_reclass.save('ndvi_r')
    arcpy.CheckInExtension('Spatial')
else:
    print ('License not available')

#-------------------------------------------------------------------------------
# SELECT RASTER
#-------------------------------------------------------------------------------
#importing modules
import numpy as np
import arcpy

#enable output overwrite
arcpy.env.overwriteOutput = True

#dem path
path = r'C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sextante\dem.asc'

#access to raster layer (not to confuse with arcpy.sa.Raster)
raster = arcpy.Raster(path)

#raster properties
rows = raster.height #rows
columns = raster.width #columns
#lower left corner coordinates
llc = arcpy.Point()
llc.X = raster.extent.XMin
llc.Y = raster.extent.YMin
#Tama?o de celda
cel_x = raster.meanCellWidth
cel_y = raster.meanCellHeight
#NO Data value
no_data = raster.noDataValue

#raster to numpyArray conversion
matrix = arcpy.RasterToNumPyArray(path)

#matrix iteration and values manipulation
for i in range (0,rows):
    for j in range (0,columns):
        value = matrix[i][j]
        if value < 1000.0 or value > 1500.0:
            matrix[i][j] = -999.0

#numpyArray to Raster conversion
sel_dem = arcpy.NumPyArrayToRaster(mi_array,llc,cel_x,cel_y,no_data)
#Save the result
sel_dem.save(r'C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\sextante\sel_dem')

#-------------------------------------------------------------------------------
# ACCESS TEMPLATE ELEMENTS
#-------------------------------------------------------------------------------
#importing modules
import arcpy
import arcpy.mapping as map

mxd = map.MapDocument(r'E:\asignaturas\layout.mxd')
#listing all graphics elements within a layout
for graphic in map.ListLayoutElements(mxd):
    #get the graphic element type
    print(graphic.type)


#-------------------------------------------------------------------------------
# ACCESS TEMPLATE TEXT
#-------------------------------------------------------------------------------
#importing modules
import arcpy
import arcpy.mapping as map

mxd = map.MapDocument(r'I:\asignaturas\layout.mxd')
#filtering all graphic elements by type
for graphic in map.ListLayoutElements(mxd,'TEXT_ELEMENT'):
    #get a graphic object using its name
    if graphic.name == 'text_name':
        print(grafico.text)
    if graphic.name == 'text_population':
        print (graphic.text)

#-------------------------------------------------------------------------------
# ACCESS GRAPHIC ELEMENTS PROPERTIES
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map

mxd = map.MapDocument(r'E:\asignaturas\master\DAS\2016-2017\temario_ingles\session4\theory\layout.mxd')
name = ''
#listing all graphics elements within a layout
for graphic in map.ListLayoutElements(mxd):
    if graphic.name != '':
        name = graphic.name
    else:
        name = ''
    #access to each type of graphic element
    if graphic.type == 'TEXT_ELEMENT':
        print('Type: '+ graphic.type +' Text: '+ graphic.text +' X: '+ str(graphic.elementPositionX) + ' Y: ' + str(graphic.elementPositionY) + ' Name: ' + name)
    if graphic.type == 'GRAPHIC_ELEMENT':
        print('Type: ' + graphic.type + ' X: '+ str(graphic.elementPositionX) + ' Y: ' + str(graphic.elementPositionY) + ' Width: '+ str(graphic.elementWidth) + ' Height: ' + str(graphic.elementHeight) + ' Name: ' + name)
    if graphic.type == 'DATAFRAME_ELEMENT':
        print('Typo: ' + graphic.type + ' Width: '+ str(graphic.elementWidth) + ' Height: ' + str(graphic.elementHeight) + ' Name: ' + name)

#-------------------------------------------------------------------------------
# TEMPLATE PROCESSING
#-------------------------------------------------------------------------------
#importing modules
import arcpy
import arcpy.mapping as map

#mxd folder
mxd = map.MapDocument(r'E:\asignaturas\master\DAS\2016-2017\temario_ingles\session4\theory\layout.mxd')
#data frame access
df = map.ListDataFrames(mxd)[0]
#layer access (municipalities)
layer = map.ListLayers(mxd,'',df)[0]
#attribute query
query = '"NOMBRE" = \'Posada de Valdeon\'' #BE CAREFUL WITH THE SINTAX!!!!
arcpy.SelectLayerByAttribute_management(layer,'NEW_SELECTION',query)
#zoom to selected elements
df.zoomToSelectedFeatures()
#feature iteration (cursor)
cursor = arcpy.SearchCursor(layer,query)
name_mun = ''
population =0
for row in cursor:
    name_mun = row.getValue('NOMBRE')
    population = row.getValue('POB95')
#template processing
for graphic in map.ListLayoutElements(mxd):
    if graphic.name == 'txt_name':
        graphic.text = name_mun
    if graphic.name == 'txt_population':
        graphic.text = population
#export result to pdf file
map.ExportToPDF(mxd, r'E:\asignaturas\master\DAS\2016-2017\temario_ingles\session4\theory\map.pdf')

#-------------------------------------------------------------------------------
# DEM MANAGEMENT
#-------------------------------------------------------------------------------
import arcpy

arcpy.env.overwriteOutput = True
#workspace
input_folder = r"C:\DAS\DATA\64032"

#output_folder
output_folder = r"C:\DAS\DATA\64032\results"
spot = input_folder+"\\64032puntos_cota.shp ELEVACI?N <none> masspoints false"
contours = input_folder+"\\64032curvas_nivel.shp ELEVACI?N <none> softline false"
breaklines = input_folder+"\\64032hidrog_lin.shp <none> <none> hardline false"

if arcpy.CheckExtension('3D') == "Available":
    arcpy.CheckOutExtension('3D')
    #create empty TIN
    arcpy.CreateTin_3d(output_folder+"\\tin")
    #edit tin
    arcpy.EditTin_3d(output_folder+"\\tin",spot+";"+contours+";"+breaklines)
    #tin to raster conversion
    data_type = "FLOAT"
    interp_method = "LINEAR"
    samp_method = "CELLSIZE 10"
    factor = 1
    arcpy.TinRaster_3d(output_folder+"\\tin",output_folder+"\\grid",data_type,interp_method,samp_method,factor)
    #slope computation
    arcpy.Slope_3d(output_folder+"\\grid",output_folder+"\\slope","DEGREE",1)
    #hillshading
    arcpy.HillShade_3d()


    arcpy.CheckInExtension('3D')
else:
    print('Licence not available')

#-------------------------------------------------------------------------------
# PRINT MAPS
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map

path_mxd = r"C:\DAS\SESSION4\template2.mxd"
#mxd reference
mxd = map.MapDocument(path_mxd)

#access to the list of graphic elements
graphic_list = map.ListLayoutElements(mxd,"TEXT_ELEMENT")


df = map.ListDataFrames(mxd)[0]
layer = map.ListLayers(mxd,"",df)[0]
#iterate every feature in a layer
cursor = arcpy.SearchCursor(layer)
for row in cursor:
    name = row.getValue("NOMBRE")
    cod = row.getValue("PROVI")
    area = row.getValue("AREA")/1000000
    perimeter = row.getValue("PERIMETER")/1000
    query = '"NOMBRE" = '+"'"+name+"'"
    arcpy.SelectLayerByAttribute_management(layer,"NEW_SELECTION",query )
    df.zoomToSelectedFeatures()
    graphic_list = map.ListLayoutElements(mxd,"TEXT_ELEMENT")
    for graphic in graphic_list:
        if graphic.name == "txt_name":
            graphic.text = name
        if graphic.name == "txt_id":
            graphic.text = str(cod)
        if graphic.name == "txt_area":
            graphic.text = str('% .2f' % area)+" KM2"
        if graphic.name == "txt_perimeter":
            graphic.text = str('% .2f' % perimeter)+" KM"
        if graphic.name == "txt_title":
            graphic.text = "CASTILLA-LEON: "+name
        if graphic.name == "txt_scale":
            graphic.text = str('% .0f' % df.scale)
    map.ExportToPDF(mxd,"C:\\DAS\\SESSION4\\"+name+".pdf")
