#-------------------------------------------------------------------------------
# CURSOR READINGS
#-------------------------------------------------------------------------------
'''EXISTEN TRES TIPOS DE CURSORES:
- De lectura: arcpy.SearchCursor
- De creacion de nuevas entidades (filas): arcpy.InsertCursor
- De modificacion de entidades (valores de artibutos o geometrias): arcpy.UpdateCursor

Mas info:   http://resources.arcgis.com/es/help/main/10.1/index.html#/na/018z0000009r000000/
            http://resources.arcgis.com/es/help/main/10.1/index.html#//002z0000001q000000
'''

#importacion de modulos
import arcpy

try:
    #Capa de consulta
    capa_consulta = r'I:\tutorial_gvsig\carto\datos\castilla-leon\provincia.shp'
    #Nombre del campo a consultar
    campo_consulta = 'NOMBRE'
    #creacion de un cursor de solo lectura (search)
    cursor = arcpy.SearchCursor(capa_consulta)
    #lectura del cursor mediante bucle for
    print 'Lectura mediante bucle for:'
    for fila in cursor: #fila es un objeto row
        print fila.getValue(campo_consulta) #valor para el campo especificado

    #lectura del cursor mediante bucle while
    #como el cursor ya estaba creado y leido, debemos crearlo de nuevo
    cursor = arcpy.SearchCursor(capa_consulta)
    print 'Lectura mediante bucle while:'
    fila = cursor.next() #primera fila
    while fila:
        print fila.getValue(campo_consulta) #valor para el campo especificado
        fila = cursor.next() #siguiente fila (NO OLVIDAR -> BUCLE INFINITO)

    #liberar memoria
    del cursor
except:
    print arcpy.GetMessages()
    del cursor

#-------------------------------------------------------------------------------
# CURSOR READING FIELDS
#-------------------------------------------------------------------------------
#importacion de modulos
import arcpy

try:
    #Capa de consulta
    capa_consulta = r'C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\castilla-leon\municipio.shp'
    #acceso a los campos de la capa
    lista_campos = arcpy.ListFields(capa_consulta)
    #impresion de la cabecera (nombres de los campos)
    cabecera = ''
    for campo in lista_campos: #recorrido por los campos
        if campo.type != 'Geometry': #si el campo no es de geometria
            #justificado a la izquierda con 15 de ancho
            cabecera += campo.name.ljust(30)

    print cabecera

    #creacion de un cursor de solo lectura (search)
    cursor = arcpy.SearchCursor(capa_consulta)
    #impresion del resto de valores
    linea = ''
    for fila in cursor: #para cada fila
        for campo in lista_campos: #para cada campo
            if campo.type != 'Geometry': #si el campo no es de geometria
                #antes de imprimir los valores han de pasarse a string
                linea += str(fila.getValue(campo.name)).ljust(30)

        print linea
        linea = ''

    #liberar memoria
    del cursor, lista_campos, cabecera, linea, capa_consulta
except:
    print 'Se ha producido un error'
    del cursor, lista_campos, cabecera, linea, capa_consulta

#-------------------------------------------------------------------------------
# CURSOR WRITING
#-------------------------------------------------------------------------------
#MAS INFO: http://resources.arcgis.com/es/help/main/10.1/index.html#//002z0000001q000000

#importacion de modulos
import arcpy
import tablas
import math
import sys, traceback

try:
    #Capa de consulta
    capa_consulta = r'C:\asignaturas\sig1\2013-2014\cuatrimestreA\datos\castilla-leon\provincia.shp'
    #Acceso a la lista de campos
    lista_campos = arcpy.ListFields(capa_consulta)
    #Creacion de un campo nuevo (mediante una herramienta)
    #creacion de una lista con los nombres de los campos
    lista_nombres = [f.name for f in arcpy.ListFields(capa_consulta)]
    if not 'Compacidad' in lista_nombres: #si el campo no existe...
        #crea el campo
        arcpy.AddField_management(capa_consulta,'Compacidad','FLOAT', 10, 3)
    else:
        cabecera = tablas.imprimeCabecera(lista_campos,15)
        print cabecera
        #Creacion del cursor de actualizacion
        cursor = arcpy.UpdateCursor(capa_consulta)
        for fila in cursor:
            area = fila.getValue('AREA')
            perimetro = fila.getValue('PERIMETER')
            coeficiente = 0.282 * (perimetro / math.sqrt(area))
            fila.setValue('Compacidad', coeficiente)
            cursor.updateRow(fila)
        cursor = arcpy.SearchCursor(capa_consulta)
        datos = tablas.imprimeDatos(cursor,lista_campos,15)
        print datos

except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n     " +  str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"
    msgs = "ARCPY ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    arcpy.AddError(msgs)
    arcpy.AddError(pymsg)

    print msgs
    print pymsg

    arcpy.AddMessage(arcpy.GetMessages(1))
    print arcpy.GetMessages(1)
