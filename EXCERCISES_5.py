#-------------------------------------------------------------------------------
# SELECT RASTER PIX
#-------------------------------------------------------------------------------
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
# MY CREATE TIN
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\ELVLC\DATA\results"

#output folder
output_folder = r'C:\ELVLC\DATA\results'
input_folder = r"C:\ELVLC\DATA\64032"

peaks = r"C:\ELVLC\DATA\64032\64032puntos_cota.shp"
water = r"C:\ELVLC\DATA\64032\64032hidrog_lin.shp"
contourline = r"C:\ELVLC\DATA\64032\64032curvas_nivel.shp"

param_peak = peaks +  " elevation <none> masspoints false"
param_water = water + " <none> <none> hardline false"
param_contourline = contourline +  " elevation <none> softline false"
parameters = param_peak+";"+param_water+";"+param_contourline
##
##inFCs = [[peaks, "elevation", "<None>", "masspoints", False],
##             [param_water, "<None>", "<None>", "hardline", False],
##             [param_contourline, "elevation", "<None>", "softline", False]]
##params = [[param_peak],[param_water],[param_contourline]]

#checking license availability
if arcpy.CheckExtension("3D") == "Available":
    #Take a license
    arcpy.CheckOutExtension("3D")
    #Create a new empty TIN
    arcpy.CreateTin_3d("tin2")
    #Edit TIN
    arcpy.EditTin_3d("tin2",parameters)
##    arcpy.EditTin_3d("tin2", inFCs)
    #Tin to raster
    data_type = "FLOAT"
    interp_method = "LINEAR"
    samp_method = "CELLSIZE 10"
    factor = 1
    arcpy.TinRaster_3d(output_folder+"\\tin2",output_folder+"\\grid", interp_method, samp_method, factor)

    #release the license
    arcpy.CheckInExtension("3D")
else:
    print ('License not available')

#-------------------------------------------------------------------------------
# CHECKING LICENSES
#-------------------------------------------------------------------------------
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\ELVLC\DATA\castilla-leon"

#output folder
output = 'C:\ELVLC\DATA\results'

#checking license availability
if arcpy.CheckExtension("3D") == "Available":

    #Take a license
    arcpy.CheckOutExtension("3D")


    #release the license
    arcpy.CheckInExtension("3D")

else:
    print ('License not available')
