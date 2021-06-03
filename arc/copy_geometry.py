# This file runs under ~\Python27\ArcGIS10.5\python.exe
# Version: 2.7.13

import arcpy

#Set source
arcpy.env.workspace = r"D:\Test\sde\KEY_IRASV5_Upstream.sde"
fc = "dbo.STATIONSERIES"

#Build a dictionary with IDs as keys and geometries as value
geometries = {key:value for (key,value) in arcpy.da.SearchCursor(fc, ['LineloopId', 'SHAPE@'])}

#Set destination
arcpy.env.workspace = r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb'
outfc = 'Centreline'

#Empty list to store ids in outfc not found in fc
notfound = []

#Update outfc with geometries from fc where ID:s match
with arcpy.da.UpdateCursor(outfc, ['LineloopId', 'SHAPE@']) as cursor:
    for row in cursor:
        try:
            print 'Processing ... ', row[0]
            row[1] = geometries[row[0]]
            cursor.updateRow(row)
        except:
            notfound.append(row[0])

print 'Found no id match and could not update geometry for IDs: ', notfound