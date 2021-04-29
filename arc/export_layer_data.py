# This file runs under ~\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
# Version: 3.7.9

import arcpy

# Join check
def joinCheck(lyr):
    fList = arcpy.Describe(lyr).fields
    for f in fList:
        print(f.name)
        if f.name.find(lyr.datasetName) > -1:
            return True
    return False

# Varables
folderPath = r'D:\Test\key\layers'

# Connect to layer folder
arcpy.env.workspace = folderPath
filelist = arcpy.ListFiles('*.*')

# Process by layer
for lyrFile in filelist:  
    try:
        # ArcDesktop syntex: lyr = arcpy.mapping.Layer(r'D:\Test\key\layers' + '\\' + lyrFile)
        # Load map file
        lyr = arcpy.mp.LayerFile('%s\\%s' % (folderPath, lyrFile))
        for l in lyr.listLayers():
            connectionProperties = l.connectionProperties
            source = connectionProperties['source']
            destination = connectionProperties['destination']
            srConInfo = source['connection_info']
            dtConInfo = destination['connection_info']

            # Open geodatabase
            arcpy.env.workspace = srConInfo['database']
            arcpy.env.qualifiedFieldNames = False

            # Prepare join information
            inFeatures = source['dataset']
            inField = connectionProperties['foreign_key']
            joinTable = destination['dataset']
            joinField = connectionProperties['primary_key']
            expression = l.definitionQuery
            outFeature = l.name.replace(' ', '').replace('-', '')

            # Load all feature class
            featureclasslist = arcpy.ListFeatureClasses()
            if outFeature not in featureclasslist:
                print('Exporting ... %s' % (l.name))

                data_joined_table = arcpy.AddJoin_management(inFeatures, inField, joinTable, joinField)
                arcpy.SelectLayerByAttribute_management(data_joined_table, "NEW_SELECTION", expression)
                arcpy.CopyFeatures_management(data_joined_table, outFeature)
    except:
        print('Unable to retrieve [' + lyrFile + '] information')