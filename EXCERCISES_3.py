#-------------------------------------------------------------------------------
# CENTROIDS
#-------------------------------------------------------------------------------
import arcpy
import math

# ap.env.Workspace = "D:\\vyuka\\II - SKRI\\Cviceni\\Database\\Redlands.mdb"
path = "C:\Users\laboratorios\ELVLC\castilla-leon\castilla-leon\provincia.shp"
fields = ["SHAPE@TRUECENTROID"]

cursor = arcpy.da.SearchCursor(path, fields)

#create an empty point
point = arcpy.Point()
points = []
for row in cursor:
    centroid = row[0]
    # print centroid
    x = centroid[0]
    y = centroid[1]
    point.X = x
    point.Y = y

    #konverze z Point na PoinGeometry
    pointGeom = arcpy.PointGeometry(point)

    #create a list of point geometry objects
    points.append(pointGeom)


#create a new feature layer from the list of pointGeometry objects
arcpy.CopyFeatures_management(points, r"C:\Users\laboratorios\ELVLC\castilla-leon\castilla-leon\prov_centroids.shp")

#-------------------------------------------------------------------------------
# ADD FIELD
#-------------------------------------------------------------------------------
import arcpy

path = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon\municipio.shp"

fields = arcpy.ListFields(path)

arcpy.AddField_management(path, "POBDEN", "FLOAT", "15", "3")


#-------------------------------------------------------------------------------
# ARCPY DA
#-------------------------------------------------------------------------------
import arcpy
import math

# ap.env.Workspace = "D:\\vyuka\\II - SKRI\\Cviceni\\Database\\Redlands.mdb"

path = "C:\Users\laboratorios\ELVLC\castilla-leon\castilla-leon\provincia.shp"

fields = ["SHAPE@AREA","SHAPE@LENGTH","NOMBRE"]

cursor = arcpy.da.SearchCursor(path, fields)
for row in cursor:
    area = row[0]
    perimeter = row[1]
    name = row[2]

    print name, area, perimeter

#-------------------------------------------------------------------------------
# FIELD NAME
#-------------------------------------------------------------------------------
import arcpy

path = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon\municipio.shp"

fields = arcpy.ListFields(path)
print fields

for field in fields:
    print field.name, field.type, field.length, field.required


#-------------------------------------------------------------------------------
# NAME FIELDS
#-------------------------------------------------------------------------------
import arcpy
import math

path = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon\provincia.shp"

fields = arcpy.ListFields(path)
print fields

name_fields = []

for field in fields:
    name_fields.append(field.name)
##print name_list

if not "CR" in name_fields:
    arcpy.AddField_management(path, "CR", "FLOAT", "15", "3")

try:
    cursor = arcpy.UpdateCursor(path)
    for row in cursor:
        area = row.AREA
        perimeter = row.PERIMETER

        cr = (4 * math.pi * area) / (perimeter ** 2)

        row.setValue("CR", cr)
        #IMPORTANTE!!!!!!!!
        cursor.updateRow(row)
    del cursor
except:
    del cursor

#-------------------------------------------------------------------------------
# NAME LIST
#-------------------------------------------------------------------------------
import arcpy

path = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon\municipio.shp"

fields = arcpy.ListFields(path)
print fields

name_list = []

for field in fields:
    name_list.append(field.name)
print name_list

#-------------------------------------------------------------------------------
# SEARCH CURSOR
#-------------------------------------------------------------------------------
import arcpy

path = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon\municipio.shp"

whereClause = """ "POB95" > 5000 """
cursor = arcpy.SearchCursor(path, whereClause, "", "", "NOMBRE")


for row in cursor:
    print row.NOMBRE

#-------------------------------------------------------------------------------
# UPDATE CURSOR
#-------------------------------------------------------------------------------
import arcpy
import math

path = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon\provincia.shp"

fields = arcpy.ListFields(path)
print fields

name_fields = []

for field in fields:
    name_fields.append(field.name)
##print name_list

if not "CR" in name_fields:
    arcpy.AddField_management(path, "CR", "FLOAT", "15", "3")



try:
    cursor = arcpy.UpdateCursor(path)
    for row in cursor:
        area = row.AREA
        perimeter = row.PERIMETER

        cr = (4 * math.pi * area) / (perimeter ** 2)

        row.setValue("CR", cr)
        #IMPORTANTE!!!!!!!!
        cursor.updateRow(row)
    del cursor
except:
    del cursor


#-------------------------------------------------------------------------------
# EXCERSICE
#-------------------------------------------------------------------------------
import arcpy
import math
from arcpy import mapping


arcpy.env.Workspace = "C:\Users\laboratorios\ELVLC\DATA\results"
file = open("report.txt", "w")
path = "C:\Users\laboratorios\ELVLC\DATA\castilla-leon\provincia.shp"
fields = ["SHAPE@AREA", "SHAPE@XY", "SHAPE@AREA", "NOMBRE", "PERIMETER", "CR"]


# POPIS DAT #
desc = arcpy.Describe(path)
print "INFORMATION OF THE LAYER"
print "NAME:  " + desc.name
print "PATH:  " + desc.path
####print "Feature Type:  " + desc.featureType
####print "Shape Type :   " + desc.shapeType
####print "Spatial Index: " + str(desc.hasSpatialIndex)
file.write("CIRCULARITY COEFICIENT ANALYSIS" + "\n" + "************************" + "\n\n")
file.write("INFORMATION OF THE LAYER\n" + "NAME:  " + desc.name + "\n" + "PATH:  " + desc.path)

cursor = arcpy.da.SearchCursor(path, fields)
for row in cursor:
    # areaKm = (row[3] / 1000000)
    print(u'{0}, {1}, {2}, {3}'.format(row[2], row[0], row[4], row[5]))

# AVERAGE
sum_area = 0
count = 0
with arcpy.da.SearchCursor(path, "SHAPE@AREA") as cursor:
    for row in cursor:
        sum_area = sum_area + row[0]
        count += 1
# print count, sum_area
average = sum_area/count
print average




##radek = cur.Next()
##while radek:
##    print "Adresa je " + radek.NOMBRE
##    radek = cur.Next()


if not "CR" in name_fields:
    arcpy.AddField_management(path, "CR", "FLOAT", "15", "3")
try:
    cursor = arcpy.da.SearchCursor(path, ["SHAPE@XY"])
    for row in cursor:
        area = row.AREA
        perimeter = row.PERIMETER
        cr = (4 * math.pi * area) / (perimeter ** 2)
        row.setValue("CR", cr)
        #IMPORTANTE!!!!!!!!
        cursor.updateRow(row)
    del cursor
except:
    del cursor
file.close()


#-------------------------------------------------------------------------------
# NAME LIST
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# NAME LIST
#-------------------------------------------------------------------------------

