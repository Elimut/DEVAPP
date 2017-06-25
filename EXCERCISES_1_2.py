#-------------------------------------------------------------------------------
# MXD DESCRIPTION
#-------------------------------------------------------------------------------

import arcpy
from arcpy import mapping

mxd_path2 = "C:\Users\laboratorios\ELVLC\session1\session1.mxd"

if arcpy.Exists(mxd_path2):
    mxd = mapping.MapDocument(mxd_path2)
    title = mxd.title
    description = mxd.description
    author = mxd.author
    print "title:", title, "description is:", description, author
    print mxd.filePath.split("\\") [-1]
else:
    print "document doesn?t exist"

#-------------------------------------------------------------------------------
# DESCRIPTION REPORT
#-------------------------------------------------------------------------------
import arcpy
from arcpy import mapping


file = open("report.txt", "w")
mxd = mapping.MapDocument(r"C:\Users\laboratorios\ELVLC\session1\session1.mxd")

mxd_name = mxd.filePath.split("\\")[-1]
file.write(mxd_name+"\n\n")
list_df = mapping.ListDataFrames(mxd)

for df in list_df:
    num_lyr = len(mapping.ListLayers(mxd, "", df))
    file.write(df.name+ ": " + str(num_lyr) + " layers\nn")
    for lyr in mapping.ListLayers(mxd, "", df):
       file.write(df.name + " + " + lyr.name + "\n")
       ext = lyr.getExtent()

       if lyr.isFeatureLayer:
        file.write(lyr.name + " VECTOR\n ")
        file.write((str(((str(ext)).split(" ")[0:4]))) + " \n")
        file.write(lyr.dataSource + " \n\n")
       else:
        file.write(lyr.name + " RASTR\n ")
        file.write(" does not have extent  \n ")
        file.write(lyr.dataSource + " \n\n")
file.close()

#-------------------------------------------------------------------------------
# DESCRIPTION DATA
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
from arcpy import mapping

env.workspace = "C:\Users\laboratorios\ELVLC\session1\castilla-leon"

## vypise seznam vrstev ##
list_shp = arcpy.ListFeatureClasses()
## print list_shp

# mxd_path = mapping.MapDocument(r"C:\Users\laboratorios\ELVLC\session1\session1.mxd")
list_df = mapping.ListDataFrames(mxd_path)
##print list_df

## vzpise dataframy a layers uvnitr nich ##
for df in list_df:
    #print df.name
    # list_layers = mapping.ListLayers(mxd_path, "", df)
    for shp in df:
        #print shp.name

mxd_path2 = "C:\Users\laboratorios\ELVLC\session1\session1.mxd"

if arcpy.Exists(mxd_path2):
    mxd = mapping.MapDocument(mxd_path2)
    title = mxd.title
    description = mxd_path.description
    author = mxd_path.author
    print title, description, author
else:
    print "document doesn?t exist"

#-------------------------------------------------------------------------------
# ADD LAYER
#-------------------------------------------------------------------------------
import arcpy
from arcpy import mapping

mxd = mapping.MapDocument('CURRENT')

df = mapping.ListDataFrames(mxd)[0]

layer_path = mapping.ListLayers(mxd, "", df)
layer = mapping.Layer(layer_path)
layer = arcpy.GetParameter(0)
position = arcpy.GetParameter(1)

mapping.AddLayer(df, layer, position)

#-------------------------------------------------------------------------------
# DESCRIBE
#-------------------------------------------------------------------------------
import arcpy
from arcpy import mapping

## layer_path = r"C:\Users\laboratorios\ELVLC\session1\castilla-leon\ALTIMETRIA.shp"

layer_path = arcpy.GetParameter(0)
desc = arcpy.Describe(layer_path)

print desc.name
print desc.dataType
print desc.path
print desc.catalogPath


#-------------------------------------------------------------------------------
# DESCRIBE RASTER
#-------------------------------------------------------------------------------
import arcpy

# Set the current workspace
arcpy.env.workspace = "C:\Users\laboratorios\ELVLC\DATA\sagunto"

desc = arcpy.Describe(arcpy.env.workspace)

# Get and print a list of GRIDs from the workspace
rasters = arcpy.ListRasters("*", "ALL")

for raster in rasters:
    i = arcpy.Raster(raster)
    print(raster)
    print "Name: ", i.name
    if hasattr(desc, "name"):
        print "Name:        " + desc.name
    if hasattr(desc, "dataType"):
        print "DataType:    " + desc.dataType
    if hasattr(desc, "catalogPath"):
        print "CatalogPath: " + desc.catalogPath

#-------------------------------------------------------------------------------
# Extract features to a new feature class based on a Location and an attribute query
#-------------------------------------------------------------------------------
# Import arcpy and set path to data
import arcpy
arcpy.env.workspace = r"C:\Users\laboratorios\ELVLC\DATA\castilla-leon"
arcpy.env.overwriteOutput = True
arcpy.MakeFeatureLayer_management('MUNICIPIO.shp', 'municipio_lyr')
arcpy.SelectLayerByAttribute_management('municipio_lyr',
                                        'NEW_SELECTION', '"POB95" > 5000')
arcpy.CopyFeatures_management("municipio_lyr", 'scriptFIN_municipio.shp')
# SelectLayerByLocation_management (in_layer, {overlap_type}, {select_features}, {search_distance}, {selection_type})
arcpy.MakeFeatureLayer_management('ESTACIONES.shp', 'estaciones_lyr')
arcpy.MakeFeatureLayer_management('EMBALSES.shp', 'embalses_lyr')
#distance = 40000 # your distance here (could be a string as well)
#linearUnit = distance + "Meters" # use any of the above provided measurement keywords
arcpy.SelectLayerByLocation_management("estaciones_lyr", 'WITHIN_A_DISTANCE', "embalses_lyr","40000")
arcpy.CopyFeatures_management("estaciones_lyr", 'scriptFIN_estaciones.shp')
arcpy.MakeFeatureLayer_management('scriptFIN_estaciones.shp', 'script_estaciones_lyr')
arcpy.MakeFeatureLayer_management('scriptFIN_municipio.shp', 'script_municipio_lyr')
arcpy.SelectLayerByLocation_management('script_municipio_lyr', 'intersect', 'script_estaciones_lyr')
arcpy.CopyFeatures_management("script_municipio_lyr", 'scriptFIN_FINAL.shp')


#-------------------------------------------------------------------------------
# SELECTIONS
#-------------------------------------------------------------------------------
# Import system modules
import arcpy

# Set the workspace
arcpy.env.workspace = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon"
fl_municipality = "municipality"
# Make a layer from the feature class
layer_path = "municipio.shp"
arcpy.MakeFeatureLayer_management(layer_path, fl_municipality)

# Select all cities which overlap the chihuahua polygon
arcpy.SelectLayerByLocation_management("municipio.shp", "intersect", "carretera.shp", 0, "new_selection")

# Within selected features, further select only those cities which have a population > 10,000
arcpy.SelectLayerByAttribute_management(fl_municipality, "NEW_SELECTION", ' "ODPROV" = \'24\' ')
print arcpy.GetCount_management(fl_municipality)
# Write the selected features to a new featureclass
# arcpy.CopyFeatures_management("municipality", "muniplus")

arcpy.env.workspace = r"C:\Users\laboratorios\ELVLC\DATA\results"
#arcpy.CopyFeatures_management(fl_municipality, "cod_24.shp")


#-------------------------------------------------------------------------------
# SWITCH OFF ON
#-------------------------------------------------------------------------------
import arcpy
from arcpy import mapping

mxd = mapping.MapDocument(r"C:\Users\laboratorios\ELVLC\session2\session2.mxd")

df = mapping.ListDataFrames(mxd)[0]

layers = mapping.ListLayers(mxd, "", df)

parameter = arcpy.GetParameter(0)
for layer in layers:
    layer.visible = parameter

arcpy.RefreshActiveView()
arcpy.RefreshTOC()

#-------------------------------------------------------------------------------
# ADD LAYER
#-------------------------------------------------------------------------------