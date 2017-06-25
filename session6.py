
#-------------------------------------------------------------------------------
# TEMPLATE REGISTRY
#-------------------------------------------------------------------------------
provReg = QgsProviderRegistry.instance()
provList = prov.Reg.ProviderList()
for provider in provList:
    print provider

#-------------------------------------------------------------------------------
# ACTIVE LAYER
#-------------------------------------------------------------------------------
layer = iface.activeLayer()
if layer != None:
    print layer.name()
    print layer.featureCount()
else:
    print "There is no anay active layer"

#-------------------------------------------------------------------------------
# SOMETHING....
#-------------------------------------------------------------------------------
import glob
#list of shp files in a folder
file_list = glob.glob(r"C:\DAS\DATA\castilla-leon\*.shp")
#convert file path to uppercase
upper_case = []
for file in file_list:
    upper_case.append(file.upper())
#sort descending
upper_case.sort(reverse=True)
#add each layer
for file in upper_case:
    name = file.split("\\")[-1].split(".")[0]
    iface.addVectorLayer(file,name,"ogr")

#-------------------------------------------------------------------------------
# REPORT QGIS
#-------------------------------------------------------------------------------
def makeReport(txt_file,name,path,type,extent):
    if type == 0:
        type_geom = "Point"
    if type == 1:
        type_geom = "Line"
    if type == 2:
        type_geom = "Polygon"
    extension = str(extent.xMinimum())+","+str(extent.yMinimum())+","+str(extent.xMaximum())+","+str(extent.yMaximum())
    line = name.ljust(40)+path.ljust(80)+type_geom.ljust(20)+extension.ljust(50)+"\n"
    txt_file.write(line)

txt_file = open(r"C:\DAS\SESSION6\THEORY\lab\report.txt","w")
header = "NAME".ljust(40)+"PATH".ljust(80)+"TYPE".ljust(20)+"EXTENT".ljust(50)+"\n"
txt_file.write(header)

registry = QgsMapLayerRegistry.instance()
layer_list = registry.mapLayers()
for key in layer_list:
    layer = layer_list[key]
    name =  layer.name()
    path = layer.source()
    type = layer.geometryType()
    extent = layer.extent()
    makeReport(txt_file,name,path,type,extent)

txt_file.close()