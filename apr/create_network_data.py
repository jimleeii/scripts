# This file runs under ~\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
# Version: 3.7.9

import sys
import arcpy

HELP = []
HELP.append('create_network.py workspace featureclass lineidfield')
HELP.append('')
HELP.append('   workspace     - SDE connection file or File Geodatabase path')
HELP.append('   featureclass  - FeatureClass name, include schema for SDE connection')
HELP.append('   lineidfield - Line ID field name')
HELP.append('')

#Is empty
def isEmpty(arg):
    if arg == None or arg == '':
        return True
    else:
        False

#Get arguments
workspacename = arcpy.GetParameterAsText(0) #e.x r'D:\Test\sde\KEY_IRASV5_Upstream.sde', r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb'
featureclassname = arcpy.GetParameterAsText(1) #e.x 'dbo.STATIONSERIES', 'Centreline'
lineidfield = arcpy.GetParameterAsText(2)

outputlocation = r'D:\Test\lrs\Shapes\shapes.gdb'

if isEmpty(workspacename) or isEmpty(featureclassname) or isEmpty(lineidfield):
    for h in HELP:
        print(h)
    sys.exit(2)

#Set source could be SDE, File Geodatabase
arcpy.env.workspace = workspacename
fc = featureclassname

ids = []
for row in arcpy.da.SearchCursor(fc, [lineidfield]):
    ids.append(row[0])

ids = set(ids)
for id in ids:
    intid = int(id)
    print('Processing ... %s' % (intid))

    outfc = 'L%s' % (intid)
    whereclause = '%s = %s' % (lineidfield, intid)

    # Execute Select
    arcpy.FeatureClassToFeatureClass_conversion(fc, outputlocation, outfc, whereclause)
