import os
import pyodbc
import arcpy

# Percentage in decimal from geometry M 
def toPercentage(geo, dist):
    #length = geo.getLength('GEODESIC', 'METERS')
    length = geo.lastPoint.M
    return dist / length

workspacename = arcpy.GetParameterAsText(0) #e.x r'D:\Test\sde\KEY_IRASV5_Upstream.sde', r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb'
featureclassname = arcpy.GetParameterAsText(1) #e.x 'dbo.STATIONSERIES', 'Centreline'
destworkspacename = arcpy.GetParameterAsText(2) #e.x r'D:\Test\sde\KEY_IRASV5_Upstream.sde', r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb'
destdataset = arcpy.GetParameterAsText(3) #e.x 'LineReferenceSystem'
destfeatureclassname = arcpy.GetParameterAsText(4) #e.x 'dbo.STATIONSERIES', 'Centreline'

if len(workspacename) == 0:
    workspacename = r'D:\Test\sde\SQL2017.sde' #r'D:\Test\lrs\KeyeraEvent.gdb'

if len(featureclassname) == 0:
    featureclassname = 'STATIONSERIES'

if len(destworkspacename) ==0:
    destworkspacename = r'D:\Test\sde\SQL2017.sde'

if len(destdataset) == 0:
    destdataset = 'LineReferenceSystem'

if len(destfeatureclassname) == 0:
    destfeatureclassname = 'PIPESEGMENTFC'

arcpy.env.workspace = workspacename
fc = featureclassname

desc = arcpy.Describe(destworkspacename)
cp = desc.connectionProperties

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=%s;'
                      'Database=%s;'
                      'Trusted_Connection=yes;' %(cp.server, cp.database))

cursor = conn.cursor()
cursor.execute('SELECT DISTINCT BeginStationSeriesId FROM PipeSegment WHERE BeginStationSeriesId = EndStationSeriesId')

ssids = []
for row in cursor:
    ssids.append(str(row[0]))

seperator = ','
where = seperator.join(ssids)

data = []
cursor.execute('SELECT Id, BeginStationSeriesId, BeginStationNum, EndStationNum FROM PipeSegment WHERE BeginStationSeriesId = EndStationSeriesId ORDER BY BeginStationSeriesId, BeginStationNum, EndStationNum')
for row in cursor:
    data.append(row)

datasets = arcpy.ListDatasets(wild_card='*%s' %(destdataset))
for ds in datasets:
    for dsfc in arcpy.ListFeatureClasses(feature_dataset=ds, wild_card='*%s' %(fc)):
        fc = os.path.join(ds, dsfc)

geometries = {key:value for (key,value) in arcpy.da.SearchCursor(fc, ['Id', 'SHAPE@'], 'Id IN (%s)' %(where))} 

arcpy.env.workspace = destworkspacename
outfc = destfeatureclassname

datasets = arcpy.ListDatasets(wild_card='*%s' %(destdataset))
for ds in datasets:
    for dsfc in arcpy.ListFeatureClasses(feature_dataset=ds, wild_card='*%s' %(outfc)):
        outfc = os.path.join(ds, dsfc)

notfound = []

for id in geometries:
    geometry = geometries[id]
    if type(geometry) == type(None):
        continue

    print('StationSeries ID: %s and length: %s' %(id, geometry.lastPoint.M))

    for d in data:
        if id == d[1]:
            print('Processing ... %s to %s' %(d[2], d[3]))
            seg = geometry.segmentAlongLine(toPercentage(geometry, float(d[2])), toPercentage(geometry, float(d[3])), True)

            with arcpy.da.UpdateCursor(outfc, ['UpstreamPipesegmentId', 'SHAPE@'], 'UpstreamPipesegmentId = %s' %(str(d[0])))  as upcursor:
                for uprow in upcursor:
                    try:
                        uprow[1] = seg
                        upcursor.updateRow(uprow)
                    except:
                        notfound.append(uprow[0])
