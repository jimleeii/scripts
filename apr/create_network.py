# This file runs under ~\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
# Version: 3.7.9

import sys
import arcpy

HELP = []
HELP.append('create_network.py workspace <skip>')
HELP.append('')
HELP.append('   workspace     - SDE connection file or File Geodatabase path')
HELP.append('   skip          - [Option] skip exporting')
HELP.append('')

#Is empty
def isEmpty(arg):
    if arg == None or arg == '':
        return True
    else:
        False

#Get arguments
workspacename = arcpy.GetParameterAsText(0) #e.x r'D:\Test\sde\KEY_IRASV5_Upstream.sde', r'D:\Test\key\0519\main\irascenterline\v101\irascentreline.gdb'
skip = arcpy.GetParameterAsText(1) 

if isEmpty(workspacename):
    for h in HELP:
        print(h)
    sys.exit(2)

#Set source could be SDE, File Geodatabase
arcpy.env.workspace = workspacename

networkfcs = []

if isEmpty(skip):
    for lfc in arcpy.ListFeatureClasses():
        print('Processing ... %s' % (lfc))
        infc = lfc
        rid = 'LineId'
        fromfield = 'BeginStationNum'
        tofield = 'EndStationNum'
        outroutes = 'Network%s' % (lfc)

        networkfcs.append(outroutes)

        # Execute CreateRoutes
        arcpy.CreateRoutes_lr(infc, rid, outroutes, "TWO_FIELDS", fromfield, tofield)

if not networkfcs:
    for lfc in arcpy.ListFeatureClasses('Network*'):
        networkfcs.append(lfc)

if len(networkfcs) > 0:
    finalnetwork = '%s\%s' % (workspacename, 'Network')
    arcpy.Merge_management(networkfcs, finalnetwork)

    print('Completed')