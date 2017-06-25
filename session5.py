#-------------------------------------------------------------------------------
# PROJECT ACCESS
#-------------------------------------------------------------------------------

from PyQt4.QtGui import QMessageBox
from qgis.core import QgsProject
#access to the project
project = QgsProject.instance()
#access to some properties
#path
path = project.fileName()
#title (see project properties in the menu)
title = project.title()
#output
print path
print title
QMessageBox.information(None, 'Message','Project path is: ' +path+'\n'+title)

#-------------------------------------------------------------------------------
# LAYER ACCESS
#-------------------------------------------------------------------------------
from qgis.core import QgsMapLayerRegistry
#layer registry access
registry = QgsMapLayerRegistry.instance()
#layer list
layers = registry.mapLayers()
#output
for key in layers:
    layer = layers[key]
    print layer.name()

#-------------------------------------------------------------------------------
# SELECT
#-------------------------------------------------------------------------------
registry = QgsMapLayerRegistry.instance()
layer_list = registry.mapLayers()
for key in layer_list:
    layer = layer_list[key]
    if layer.name()=="PROVINCIA":
        query = "NOMBRE = 'SORIA'"
        rows = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        for row in rows:
            #acces to geometry
            geom_prov = row.geometry()
            # bounding box of geometry
            bb = geom_prov.boundingBox()

for key in layer_list:
    layer = layer_list[key]
    if layer.name()=="ESTACIONES":
        #selection by bounding box (QgsRectangle)
        layer.select(bb,True)

#-------------------------------------------------------------------------------
# PLOT CHART
#-------------------------------------------------------------------------------
from PyQt4.QtCore import QVariant
from math import *
import matplotlib.pyplot as plt

def plotChart(names,ccs):
    labels = range(0,len(names))
    plt.bar(labels,ccs,width=0.5,align='center')
    plt.xticks(labels,names)
    plt.show()

registry = QgsMapLayerRegistry.instance()
layer_list = registry.mapLayers()
for key in layer_list:
    layer = layer_list[key]
    if layer.name()=="PROVINCIA":
        fields = layer.pendingFields()
        if fields.fieldNameIndex("CC") == -1:
             field = QgsField("CC",QVariant.Double)
             layer.startEditing()
             layer.dataProvider().addAttributes([field])
             layer.commitChanges()
        rows = layer.getFeatures()
        names = []
        ccs = []
        for row in rows:
            name = row.attribute("NOMBRE")
            names.append(name)
            area = row.attribute("AREA")
            perimeter = row.attribute("PERIMETER")
            cc = 0.282*(perimeter/sqrt(area))
            ccs.append(cc)
            field_id = row.fieldNameIndex("CC")
            row_id = row.id()
            attributes = {field_id:cc}
            layer.dataProvider().changeAttributeValues({row_id:attributes})
plotChart(names,ccs)


#-------------------------------------------------------------------------------
# COUNT LENGTH OF ROADS
#-------------------------------------------------------------------------------
import numpy as np

registry = QgsMapLayerRegistry.instance()
layer_list = registry.mapLayers()
lengths = []
for key in layer_list:
    layer = layer_list[key]
    if layer.name()=="CARRETERA":
        rows = layer.getFeatures()
        for row in rows:
            geom = row.geometry()
            if geom != None:
                lengths.append(geom.length())

    print "Total length: {} km".format(np.sum(lengths)/1000)
    print "Mean length: {} km".format(np.mean(lengths)/1000)
    print "Standard deviation: {} km".format(np.std(lengths)/1000)


#-------------------------------------------------------------------------------
# COORDINATES CREATING
#-------------------------------------------------------------------------------
from PyQt4.QtCore import QVariant
registry = QgsMapLayerRegistry.instance()

def openCSV(path_csv):
    ids=[]
    points = []
    skip = 1
    with open(path_csv) as csv:
        for line in csv:
            if skip > 1:
                parts = line.split(";")
                id = int(parts[0])
                ids.append(id)
                cx = float(parts[1])
                cy = float(parts[2])
                point = QgsPoint(cx,cy)
                points.append(point)
            skip += 1
    return ids,points

def transformPoints(points,source_crs,target_crs):
    tps = []
    t_matrix = QgsCoordinateTransform(source_crs,target_crs)
    for source_point in points:
        tp = t_matrix.transform(source_point)
        tps.append(tp)
    return tps

def createSHP(shp_path,points,ids,crs):
    fields = QgsFields()
    fields.append(QgsField("Id",QVariant.Int))
    shp_writer = QgsVectorFileWriter(shp_path,"CP1250",fields,QGis.WKBPoint,crs,"ESRI Shapefile")
    if shp_writer.hasError() != QgsVectorFileWriter.NoError: #if there is any error
        print "Error when creeting the layer: ", shp_writer.hasError(), shp_writer.errorMessage()
        del shp_writer
        return False
    else:
        for i in range(0,len(points)):
            point = points[i]
            id = ids[i]
            geom = QgsGeometry.fromPoint(point)
            n_row = QgsFeature()
            n_row.setGeometry(geom)
            n_row.setAttributes([id])
            shp_writer.addFeature(n_row)
        del shp_writer
        return True

ids_30,points_30 = openCSV(r"C:\DAS\SESSION7\LAB\huso30.csv")
ids_31,points_31 = openCSV(r"C:\DAS\SESSION7\LAB\huso31.csv")
source_crs = QgsCoordinateReferenceSystem(23031,QgsCoordinateReferenceSystem.EpsgCrsId)
target_crs = QgsCoordinateReferenceSystem(23030,QgsCoordinateReferenceSystem.EpsgCrsId)
points_31_30 = transformPoints(points_31,source_crs,target_crs)
ids = ids_30+ids_31
points = points_30+points_31_30
shp_path = r'C:\DAS\SESSION7\LAB\results\vertices.shp'
flag = createSHP(shp_path,points,ids,source_crs)
if flag:
    shp_layer = QgsVectorLayer(shp_path,"Vertices","ogr")
    registry.addMapLayer(shp_layer)
#-------------------------------------------------------------------------------
# PROJECT ACCESS
#-------------------------------------------------------------------------------