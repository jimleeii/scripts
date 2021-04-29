# This file runs under ~\Python27\ArcGIS10.5\python.exe
# Version: 2.7.13

import arcpy

# Set parameters
fp = r'D:\Test\key\work\KEY_IRASV5_PROD.mxd'
lf = r'D:\Test\key\layers'

# Delete files in folder
arcpy.env.workspace = lf
fileList = arcpy.ListFiles('*.*')
for fl in fileList:
    arcpy.Delete_management(fl)

# # Map document
mxd = arcpy.mapping.MapDocument(fp)

# Process by layer
lyrs = arcpy.mapping.ListLayers(mxd) 
for lyr in lyrs:  
    if lyr.isFeatureLayer:
        try:  
            if lyr.dataSource.endswith('StationSeries'):
                lyr.saveACopy('%s\\%s.lyrx' % (lf, lyr.name))

        except:  
            print('Unable to retrieve [' + lyr.name + '] information')