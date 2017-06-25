#-------------------------------------------------------------------------------
# GRAPHS
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map
import arcgisscripting

path = r"C:\Users\laboratorios\ELVLC\session6\session6.mxd"
mxd = map.MapDocument(path)
graphic_list = map.ListLayoutElements(mxd, "TEXT_ELEMENT")
df = map.ListDataFrames(mxd)[0]
layer = map.ListLayers(mxd, "", df)[0]
layer_muni = map.ListLayers(mxd, "", df)[1]
cur = arcpy.SearchCursor(layer)
row = cur.next()
while row:
    name = row.getValue("NOMBRE")
    code = row.getValue("PROVI")
    area = row.getValue("AREA")/1000000
    perimeter = row.getValue("PERIMETER")/1000
    name = row.getValue("NOMBRE")
    query = '"NOMBRE" = '+"'" +name+"'"
    arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)
    df.zoomToSelectedFeatures()
    graphic_list = map.ListLayoutElements(mxd, "TEXT_ELEMENT")
    for graphic in graphic_list:
        if graphic.name == "txt_name":
            graphic.text == name
        if graphic.name == "txt_vode":
            graphic.text = str(cod)
        if graphic.name == "txt_area":
            graphic.text = str('% .2f' % area)+" KM2"
        if graphic.name == "txt_perimeter":
            graphic.text = str('% .2f' % perimeter)+" KM"
    graphic_list2 = map.ListLayoutElements(mxd, "GRAPHIC_ELEMENT")
    graph_width1a = 15
    graph_width1b = 0
    graph_width2a = 15
    graph_width2b = 0
##    for graph in graphic_list2:
##        if graphic.name == "graph1_pop1":
##            graphic.width =

    map.ExportToPDF(mxd,"C:\Users\laboratorios\ELVLC\session6" + name + ".pdf")
    row = cur.next()

#-------------------------------------------------------------------------------
# GRAPHIC ELEMENT
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map

path = r"C:\Users\laboratorios\ELVLC\session6\session6.mxd"
mxd = map.MapDocument(path)

graphic_list = map.ListLayoutElements(mxd, "TEXT_ELEMENT")

for graphic in graphic_list:
##    if graphic.name !="":
##        print graphic.type
    if graphic.name== "txt_population":
        print graphic.text
        graphic.text = "2000"

map.ExportToPDF(mxd,r"C:\Users\laboratorios\ELVLC\DATA\results\printmap.pdf")

#-------------------------------------------------------------------------------
# 3D CHART
#-------------------------------------------------------------------------------

from GChartWrapper import *
g = Pie3D([1,2,3,4])
g.label('A','B','C','D')
g.color('00dd00')
image = g.image()
image.save('chart.jpg','JPEG')

#-------------------------------------------------------------------------------
# NECO
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map

path = r"C:\Users\laboratorios\ELVLC\session6\session6.mxd"
mxd = map.MapDocument(path)
graphic_list = map.ListLayoutElements(mxd, "TEXT_ELEMENT")
df = map.ListDataFrames(mxd)[0]
layer = map.ListLayers(mxd, "", df)[0]

### find a layer by name
##layers = map.ListLayers(mxd,"",df)
##
##for layer in layers:
##    if layer.name == "Municipio":
##        my_layer = layer

query = '"NOMBRE" = \'Posada de Valdeon\''
# query =''' "NOMBRE"' = 'Posada de Valdeion' '''
arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)
df.zoomToSelectedFeatures()
cursor = arcpy.SearchCursor(layer)
name = ''
pop95 = 0

for row in cursor:
    name = row.getValue("NOMBRE")
    pop95 = row.getValue("POB95")

graphic_list = map.ListLayoutElements(mxd, "TEXT_ELEMENT")
for graphic in graphic_list:
    if graphic.name== "txt_name":
        graphic.text = name
    if graphic.name== "txt_population":
        graphic.text = pop95


map.ExportToPDF(mxd,r"C:\Users\laboratorios\ELVLC\DATA\results\pop95.pdf")
#-------------------------------------------------------------------------------
# GRAPHS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# GRAPHS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# GRAPHS
#-------------------------------------------------------------------------------