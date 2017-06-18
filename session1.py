# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# -------- ACCESS PROJECT -------
#-------------------------------------------------------------------------------

#importing modules
import arcpy
import arcpy.mapping as map # renaming module


try:
    #definition of variables
    ruta = r'E:\DAS\2016-2017\temario_ingles\session1\theory\scripts\test.mxd'
    if arcpy.Exists(ruta): #checking if the file exists
        mxd = map.MapDocument(ruta)
    else:
        raise IOError

    # How to use some properties (title, author and summary)
    print "Title: " + mxd.title + " Author:" + mxd.author
    print mxd.summary

    #memory releasing
    del mxd
    # raw_imput: keyboard input. Only makes sense if we run the script on console mode
    raw_input()
except IOError:
    print "file doesn't exist"
    raw_input()

#-------------------------------------------------------------------------------
# -------- Accessing to the project from ArcMap python console window -------
#-------------------------------------------------------------------------------

#In order to run the script properly, we firstly need write these two lines

#import os
#os.system(r'c:\python\script.py parametro1')

#Import modules
import arcpy
import arcpy.mapping as map #change the module name
import sys

try:
    #Definition of variables
    ruta = sys.argv[1] #'Current' doesn't work
    print ruta
    if arcpy.Exists(ruta): #check if path exists
        mxd = map.MapDocument(ruta)
    else:
        raise IOError

    #Using some properties (title, author and summary)
    print "Titulo: " + mxd.title + " Autor:" + mxd.author
    print mxd.summary
    #keyboard input. Only makes sense if we run the script on console mode
    raw_input()
except IOError:
    print "File doesn't exists"
    raw_input() #hace que la ventana de comandos no se cierre para ver el print

#-------------------------------------------------------------------------------
# -------- access to the current project from arcmap python console window -------
#-------------------------------------------------------------------------------

# This only works if you copy the whole code into the command line and then press
# enter.

import arcpy
import arcpy.mapping as map # renaming module

#Definiction of variables
ruta = 'CURRENT' #reference to the current project
mxd = map.MapDocument(ruta)
#Using some properties (title, author and summary)
print "Titulo: " + mxd.title + " Autor:" + mxd.author
print mxd.summary

#-------------------------------------------------------------------------------
# -------- showing how to refresh the map after adding a new layer -------
#-------------------------------------------------------------------------------

import arcpy
import arcpy.mapping as map

#Definiction of variables
ruta = 'CURRENT' #reference to the current project
mxd = map.MapDocument(ruta) #returns the MapDocument
mapa = map.ListDataFrames(mxd)[0] #returns the first dataframe within the MapDocument
#Layer reference accordind a specific path
capa = map.Layer(r'E:\DAS\2016-2017\datos\castilla-leon\MUNICIPIO.shp')
#Add the new layer
map.AddLayer(mapa,capa)
#Refreshing of the TOC and the active view
arcpy.RefreshActiveView
arcpy.RefreshTOC

#-------------------------------------------------------------------------------
# -------- dataframe access -------
#-------------------------------------------------------------------------------

#Import modules
import arcpy
import arcpy.mapping as map

try:
    #Definition of variables
    ruta = r'E:\DAS\2016-2017\temario_ingles\session1\theory\scripts\test.mxd'
    if arcpy.Exists(ruta): #checks if the file exists
        mxd = map.MapDocument(ruta)
    else:
        raise IOError
    mapa = map.ListDataFrames(mxd)[0] #first dataframe
    #some dataframe's properties (name, units and scale)
    print 'Name of the data frame (0): ' + mapa.name
    print 'Units: ' + mapa.mapUnits
    print 'Scale: 1:' + str(mapa.scale)
except IOError:
    print "file doesn't exist"

	#Exercise: make a tool (in ArcToolBox) to shift the data frame extent.
    #Hint: look at the EXTENT data frame property

#-------------------------------------------------------------------------------
# -------- ACCESS DATAFRAME FUNCTION -------
#-------------------------------------------------------------------------------
#Import modules
import arcpy
import arcpy.mapping as map
import language as lang #access to the external module

try:
    #Definition of variables
    ruta = r'E:\DAS\2016-2017\temario_ingles\session1\theory\scripts\test.mxd'
    if arcpy.Exists(ruta):
        mxd = map.MapDocument(ruta)
    else:
        raise IOError
    df = map.ListDataFrames(mxd)[0]
    print 'Unidades: ' + df.mapUnits
    #calling changeUnits function
    print 'Unidades: ' + lang.changeUnits(df.mapUnits)

except IOError:
    print "file doesn't exist"

#-------------------------------------------------------------------------------
# -------- shows how to access to a layer within a data frame -------
#-------------------------------------------------------------------------------
#import modules
import arcpy
import arcpy.mapping as map

try:
    #Definition of variables
    ruta =  r'E:\DAS\2016-2017\temario_ingles\session1\theory\scripts\test.mxd'
    if arcpy.Exists(ruta): #checks if the file exists
        mxd = map.MapDocument(ruta)
    else:
        raise IOError
    df = map.ListDataFrames(mxd)[0] #first data frame
    capa = map.ListLayers(mxd,"",df)[0] #first layer within a data frame
    caja = capa.getExtent() #returns the layer's extent
    #print the name and the coordinates of the extent
    print capa.name, caja.XMin, caja.YMin, caja.XMax, caja.YMax
    #get the name of all layers within the data frame
    for c in map.ListLayers(mxd,"",df):
        print c.name

except IOError:
    print "file doesn't exist"

#EXERCISE. GET THE CENTROID FOR EACH LOADED LAYER