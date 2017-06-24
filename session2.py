#-------------------------------------------------------------------------------
# LAYERS ON OFF
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map #cambio el nombre del modulo

#Definicion de variables
ruta_mxd = 'CURRENT'
estado = arcpy.GetParameter(0) #parametro de tipo booleano (devuelve 0-1)
arcpy.AddMessage(estado) #muestra el valor de estado en la caja de mensajes
mxd = map.MapDocument(ruta_mxd) #acceso al proyecto
df = map.ListDataFrames(mxd)[0] #acceso al primer mapa de la lista (dataframe)
#Acceso a todas las capas y cambio de su estado de visibilidad
for c in map.ListLayers(mxd,"",df):
    c.visible = estado

#Refresco de la vista y de la TOC
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

#liberacion de memoria
del mxd
del df
del c

#-------------------------------------------------------------------------------
# MOVE LAYERS
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map #cambio el nombre del modulo

#Definicion de variables
ruta_mxd = 'c:\proyecto\proyecto.mxd'
mxd = map.MapDocument(ruta_mxd) #acceso al proyecto
df = map.ListDataFrames(mxd)[0] #acceso al primer mapa de la lista (dataframe)
#Acceso a la primera y ultima capa de la lista
lista_capas = map.ListLayers (mxd,"",df) #acceso a la lista de capas
n = len(lista_capas) #numero de capas
primera = lista_capas[0] #primera capa (la de arriba)
ultima = lista_capas[n-1] #ultima capa (la de abajo)

#Desplazamiento de la capa
map.MoveLayer(df,primera,ultima,'BEFORE')

#Refresco de la vista y de la TOC (solo si mxd = 'CURRENT'
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

#Exportar mapa a pdf
map.ExportToPDF(mxd, "C:/Projecto/Output/mapa.pdf")

#liberacion de memoria
del mxd, df, primera, ultima

#-------------------------------------------------------------------------------
# DESCRIBE LAYERS
#-------------------------------------------------------------------------------
import arcpy
import arcpy.mapping as map #cambio el nombre del modulo

#Definicion de variables
ruta_mxd = r'C:\asignaturas\sig1\2013-2014\cuatrimestre B\teoria\MT2\2_acceso_mapa\castilla_leon.mxd'
mxd = map.MapDocument(ruta_mxd) #acceso al proyecto
df = map.ListDataFrames(mxd)[0] #acceso al primer mapa de la lista (dataframe)
#Acceso a la primera y ultima capa de la lista
lista_capas = map.ListLayers (mxd,"",df) #acceso a la lista de capas
primera = lista_capas[0] #primera capa (la de arriba)
print primera.dataSource #ruta del fichero
#Acceso a la descripcion de la capa
#Describe funciona con rutas o capas (vectoriales). Por eso es mejor usar dataSource
desc = arcpy.Describe(primera.dataSource)

#Comprobacion de la existencia de atributos y su impresion
if hasattr(desc, "name"):
    print "Name:        " + desc.name
if hasattr(desc, "dataType"):
    print "DataType:    " + desc.dataType
if hasattr(desc, "catalogPath"):
    print "CatalogPath: " + desc.catalogPath
if hasattr(desc, "baseName"):
    print "BaseName:        " + desc.baseName
if hasattr(desc, "extent"):
    print "Extent:        " + str(desc.extent)
if hasattr(desc, "extension"):
    print "Extension:        " + desc.extension
if hasattr(desc, "dataElementType"):
    print "DataElementType:    " + desc.dataElementType
if hasattr(desc, "file"):
    print "File: " + desc.file
if desc.extension == 'shp':
    desc2 = arcpy.Describe(primera)
    print 'Tipo de shp: ' + desc2.featureClass.shapeType

#liberacion de memoria
del mxd, df, primera

#-------------------------------------------------------------------------------
# SELECT BY ATTRIBUTES
#-------------------------------------------------------------------------------
#importacion de modulos
import arcpy


#Asignacion de variables
#Establecimiento del workspace
arcpy.env.workspace = r'I:\tutorial_gvsig\carto\datos\castilla-leon'
#permitir la sobreescritura de resultados.
arcpy.env.overwriteOutput = True

try:
    #Capa shp a procesar
    fc = 'municipio.shp'
     #Carga en memoria del shp mediante la herramienta MakeFeatureLayer
    fl = 'mun_leon' #nombre de la capa en memoria (es una referencia)
    arcpy.MakeFeatureLayer_management(fc,fl) #creacion de la capa
    #creacion de la consulta
    consulta = '"CODPROV" = \'24\'' #OJO CON LA SINTAXIS!!!!
    arcpy.SelectLayerByAttribute_management(fl,'NEW_SELECTION',consulta)
    #consulta del numero de registros seleccionados
    res = arcpy.GetCount_management(fl)
    print 'Numero de entidades seleccionadas en ' + fl + ': ' + str(res)
    #crear un nuevo shp con las filas seleccionadas
    arcpy.CopyFeatures_management(fl,r'I:\tutorial_gvsig\carto\datos\castilla-leon\salida\mun_24.shp')

except:
    print arcpy.GetMessages()

#-------------------------------------------------------------------------------
# SELECT BY LOCATION
#-------------------------------------------------------------------------------
#importacion de modulos
import arcpy

#Asignacion de variables
#Establecimiento del workspace
arcpy.env.workspace = r'I:\tutorial_gvsig\carto\datos\castilla-leon'
#permitir la sobreescritura de resultados.
arcpy.env.overwriteOutput = True

try:
    #Capa shp a procesar
    fc = 'municipio.shp'
    #Carga en memoria del shp mediante la herramienta MakeFeatureLayer
    fl = 'capa_sel' #nombre de la capa en memoria (es una referencia)
    arcpy.MakeFeatureLayer_management(fc,fl) #creacion de la capa
    arcpy.SelectLayerByLocation_management(fl,'INTERSECT','estaciones.shp')
    #consulta del numero de registros seleccionados
    res = arcpy.GetCount_management(fl) #devuelve un objeto result (no un entero)
    print 'Numero de entidades seleccionadas en ' + fl + ': ' + str(res)
    #crear un nuevo shp con las filas seleccionadas
    if res > 0: #si hay entidades seleccionadas creas la capa de salida
        arcpy.CopyFeatures_management(fl,r'I:\tutorial_gvsig\carto\datos\castilla-leon\salida\consulta_loc.shp')
except:
    print arcpy.GetMessages()

#-------------------------------------------------------------------------------
# MAKE POINT
#-------------------------------------------------------------------------------
#Directorio de salida
arcpy.env.workspace = r'I:\asignaturas\sig-I\2012-2013\cuatrimestreB\python\ejemplos\8_geometrias\salida'

#Sobreescritura de resultados
arcpy.env.overwriteOutput = True

#capa de salida
capa_salida = 'Puntos.shp'

#creacion de un punto
punto = arcpy.Point(431031.973,4575534.885)
geometria = arcpy.PointGeometry(punto)

#creacion del shp
arcpy.CopyFeatures_management(gometria,capa_salida)

#-------------------------------------------------------------------------------
# AVERAGE AREA
#-------------------------------------------------------------------------------
#importacion de modulos
import arcpy

#Directorio de salida
arcpy.env.workspace = r'I:\tutorial_gvsig\carto\datos\castilla-leon'

#capa de entrada
capa_entrada = 'PROVINCIA.shp'

#Acceso a la geometria de los poligonos mediante un cursor de arcpy.da.
#Los "tokens" permiten en alcceso a propiedades geometricas de forma mas
#rapida y eficiente

#creacion de un cursor de solo lectura (search)
cursor = arcpy.da.SearchCursor(capa_entrada,'SHAPE@AREA')
#inicializacion de las variables
area = 0
conta = 0

#Recorrido del cursor
for fila in cursor:
    conta = conta + 1
    area = area + fila[0]

print 'Area media {0} Km2'.format ((area/conta)/1000000)