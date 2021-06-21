# This file runs under ~\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
# Version: 3.7.9

import sys
import arcpy

HELP = []
HELP.append('extract_geometry_part.py workspace featureclass <identifyfield>')
HELP.append('')
HELP.append('   workspace     - SDE connection file or File Geodatabase path')
HELP.append('   featureclass  - FeatureClass name, include schema for SDE connection')
HELP.append('   identifyfield - [Option] identify field from featureclass')
HELP.append('')

ID = 'Id'
BEGINSTATIONNUM = 'BeginStationNum'
ENDSTATIONNUM = 'EndStationNum'
SHAPE = 'SHAPE@'
IGNORELIST = ['OBJECTID','Shape_Length','Shape','PointCollection']

seed = 10156

#Is empty
def isEmpty(arg):
    if arg == None or arg == '':
        return True
    else:
        False

#Has Z
def hasZ(pnt):
    if pnt.Z == None:
        return None
    else:
        return True

#Has M
def hasM(pnt):
    if pnt.M == None:
        return None
    else:
        return True

#Get arguments
workspacename = arcpy.GetParameterAsText(0) #e.x r'D:\Test\sde\KEY_IRASV5_Upstream.sde', r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb'
featureclassname = arcpy.GetParameterAsText(1) #e.x 'dbo.STATIONSERIES', 'Centreline'
identifyfieldname = arcpy.GetParameterAsText(2)

if isEmpty(workspacename) or isEmpty(featureclassname):
    for h in HELP:
        print(h)
    sys.exit(2)

#Set source could be SDE, File Geodatabase
arcpy.env.workspace = workspacename
fc = featureclassname

#Get all fields
fields = []
for field in arcpy.ListFields(fc):
    fields.append(field.name)
#Add SHAPE@ field
fields.append(SHAPE)

existids = []
newrows = []
#Go through every row in featureclass
for row in arcpy.da.SearchCursor(fc, fields):
    geometry = row[fields.index(SHAPE)]
    if type(geometry) == type(None):
        continue

    if not geometry.isMultipart:
        continue

    #Print ID
    if not isEmpty(identifyfieldname):
        id = row[fields.index(identifyfieldname)]
        if id == 0:
            continue
        else:
            existids.append(id)
            print('%s %s' % (identifyfieldname, id))

    columns = []
    newrow = []
    for field in fields:
        if field in IGNORELIST:
            continue
        columns.append(field)
        newrow.append(row[fields.index(field)])

    partnum = 0

    for part in geometry:
        # print('Part %s' % (partnum))

        #Create new line
        line = arcpy.Polyline(part, geometry.spatialReference, hasZ(geometry.firstPoint), hasM(geometry.firstPoint))

        newrow[columns.index(SHAPE)] = line
        newrow[columns.index(ID)] = seed
        newrow[columns.index(BEGINSTATIONNUM)] = line.firstPoint.M
        newrow[columns.index(ENDSTATIONNUM)] = line.lastPoint.M

        newtuple = tuple(newrow)
        newrows.append(newtuple)
        seed += 1

        # for pointcollection in line:
        #     for pnt in pointcollection:
        #         print('X: %s, Y: %s, M: %s, Z: %s' % (pnt.X, pnt.Y, pnt.M, pnt.Z))

        partnum += 1

#Insert new lines seperated from parts
if len(newrows) > 0:
    #Open an InsertCursor
    cursor = arcpy.da.InsertCursor(fc, columns)

    for row in newrows:
        cursor.insertRow(row)

    #Delete cursor object
    del cursor

    print('Insert Completed')

#Delete existing lines after inserted new lines
if len(existids) > 0:
    idstring = ','.join(map(str, existids)) 
    whereclause = 'Id IN (%s)' % (idstring)

    # Create update cursor for feature class 
    with arcpy.da.UpdateCursor(fc, columns, whereclause) as cursor:
        for row in cursor:
            print(row[columns.index(ID)])
            
            cursor.deleteRow()

        print('Delete Completed')    