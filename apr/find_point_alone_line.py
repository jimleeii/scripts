# Usage info:
# ~\python.exe find_point_alone_line.py <workspacename> <dataset> <featureclassname> <destworkspacename> <destdataset>
# workspacename: Full path of database connection.  e.x. D:\Test\sde\KEY_IRASV5_Upstream.sde
# dataset: Spatial dataset name in database. e.x. LineReferenceSystem
# featureclassname: Featureclass name in database. e.x. STATIONSERIES
# destworkspacename: Full path of export database connection. e.x. D:\Test\lrs\KeyeraPlay.gdb
# destdataset: Spatial dataset name in export database. e.x. LineReferenceSystem
# destfeatureclassname: Export featureclass name. e.x. PIPESEGMENTFC
# destFKname: Export FK field name. e.x. UpstreamPipeSegmentId


import arcpy
import os
import pyodbc
import time

# Get full path of featureclass
#   datasetname     : Dataset name
#   featureclassname: Featureclass name
def getFullPath(datasetname=None, featureclassname=None):
    if type(datasetname) == type(None):
        for fc in arcpy.ListFeatureClasses(wild_card='*%s' %(featureclassname)):
            return fc
    else:
        datasets = arcpy.ListDatasets(wild_card='*%s' %(datasetname))
        for ds in datasets:
            for fc in arcpy.ListFeatureClasses(feature_dataset=ds, wild_card='*%s' %(featureclassname)):
                return os.path.join(ds, fc)

# Percentage in decimal from geometry M 
#   geo : Input geomertry 
#   dist: Distance from start
def toPercentage(geo, dist):
    # This a function from ESRI, but not producing satisfy result
    # length = geo.getLength('GEODESIC', 'METERS')

    length = geo.lastPoint.M
    return dist / length

getDistinctAvailableSSID = 'SELECT DISTINCT BeginStationSeriesId FROM PipeSegment WHERE BeginStationSeriesId = EndStationSeriesId'
getSSInfoBySSID = 'SELECT Id, BeginStationSeriesId, BeginStationNum, EndStationNum FROM PipeSegment WHERE BeginStationSeriesId = EndStationSeriesId ORDER BY BeginStationSeriesId, BeginStationNum, EndStationNum'

# Workspace name for geodatabase (e.x. r'D:\Test\sde\KEY_IRASV5_Upstream.sde', r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb')
workspacename = r'D:\Test\sde\SQL2017_tra.sde' if len(arcpy.GetParameterAsText(0)) == 0 else arcpy.GetParameterAsText(0)

# [Optional] Dataset name in geodatabase (e.x. 'LineReferenceSystem'), provide empty string 
dataset = 'LineReferenceSystem' if len(arcpy.GetParameterAsText(1)) == 0 else arcpy.GetParameterAsText(1)

# Featureclass name for spatial table in geodatabase (e.x. 'dbo.STATIONSERIES', 'Centreline')
featureclassname = 'STATIONSERIES' if len(arcpy.GetParameterAsText(2)) == 0 else arcpy.GetParameterAsText(2)

# Workspace name for export geodatabase (e.x. r'D:\Test\sde\KEY_IRASV5_Upstream.sde', r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb')
destworkspacename = workspacename if len(arcpy.GetParameterAsText(3)) == 0 else arcpy.GetParameterAsText(3)

# [Optional] Dataset name within export geodatabase (e.x. 'LineReferenceSystem')
destdataset = dataset if len(arcpy.GetParameterAsText(4)) == 0 else arcpy.GetParameterAsText(4)

# Featureclass name for export geodatabase (e.x. 'dbo.STATIONSERIES', 'Centreline')
destfeatureclassname = 'PIPESEGMENTFC' if len(arcpy.GetParameterAsText(5)) == 0 else arcpy.GetParameterAsText(5)

# Featureclasse FK name for export geodatabase
destFKname = 'UpstreamPipeSegmentId' if len(arcpy.GetParameterAsText(6)) == 0 else arcpy.GetParameterAsText(6)

# Create connection from workspace
desc = arcpy.Describe(workspacename)
cp = desc.connectionProperties
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=%s;'
                      'Database=%s;'
                      'Trusted_Connection=yes;' %(cp.server, cp.database))
cursor = conn.cursor()

# Execute getDistinctAvailableSSID query and load into array
cursor.execute(getDistinctAvailableSSID)
ssids = [str(row[0]) for row in cursor]

# Execute getSSInfoBySSID query and load into array
cursor.execute(getSSInfoBySSID)
data = [row for row in cursor]

# Get featureclass full name from source workspace
arcpy.env.workspace = workspacename
fc = getFullPath(featureclassname=featureclassname)

if type(fc) == type(None):
    print('Cannot find %s' %(featureclassname))
    exit(0)

try:
    where = ','.join(ssids)
    geometries = {key:value for (key,value) in arcpy.da.SearchCursor(fc, ['Id', 'SHAPE@'], 'Id IN (%s)' %(where))} 
except arcpy.ExecuteError:
    print('Exception on SearchCursor')
    print(arcpy.GetMessages(2))
    exit(0)

arcpy.env.workspace = destworkspacename
outfc = getFullPath(destdataset, destfeatureclassname)

if type(outfc) == type(None):
    print('Cannot find %s' %(destfeatureclassname))
    exit(0)

start = time.process_time()

notfound = []

# Start an edit session. Must provide the workspace.
edit = arcpy.da.Editor(destworkspacename)
# Edit session is started without an undo/redo stack for versioned data (for second argument, use False for unversioned data)
edit.startEditing(False, True)
# Start an edit operation
edit.startOperation()

for id in geometries:
    geometry = geometries[id]
    if type(geometry) == type(None):
        continue

    print('%s ID: %s with length[%s]' %(featureclassname, id, geometry.lastPoint.M))

    for d in data:
        if id == d[1]:
            print('Processing ... %s to %s' %(d[2], d[3]))

            seg = geometry.segmentAlongLine(toPercentage(geometry, float(d[2])), toPercentage(geometry, float(d[3])), True)

            with arcpy.da.UpdateCursor(outfc, [destFKname, 'SHAPE@'], '%s = %s' %(destFKname, str(d[0])))  as upcursor:
                for uprow in upcursor:
                    try:
                        uprow[1] = seg
                        upcursor.updateRow(uprow)
                    except arcpy.ExecuteError:
                        notfound.append('ID: %s :: %s' %(uprow[0], arcpy.GetMessages(2)))

# Stop the edit operation.
edit.stopOperation()
# Stop the edit session and save the changes
edit.stopEditing(True)

elapsed_time = time.process_time() - start

if len(notfound) > 0:
    print(nf for nf in notfound)

print('Process finished in %s' %(elapsed_time))