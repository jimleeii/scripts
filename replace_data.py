import arcpy

prj = arcpy.mp.ArcGISProject(r"D:\Test\project\Working APR\Working APR.aprx")
con_pro = {}
for mxd in prj.listMaps():
    if mxd.name == 'Map tra':
        for l in mxd.listLayers():
            if not(l.isGroupLayer or l.isBasemapLayer):
                con_pro = l.connectionProperties['connection_info']
                break

for mxd in prj.listMaps():
    if mxd.name == 'Map':
        for l in mxd.listLayers():
            if not(l.isGroupLayer or l.isBasemapLayer):
                print('Updating %s' %(l.name))
                for p in l.connectionProperties['connection_info']:
                    print('%s : %s' %(p, l.connectionProperties['connection_info'][p]))
                l.connectionProperties['connection_info'] = con_pro
                #print(l.connectionProperties['connection_info'])
                break

for c in con_pro:
    print('%s :: %s' %(c, con_pro[c]))
#prj.saveACopy(r"D:\Test\project\Working APR\Working APR Update.aprx")
#print(con_pro)
#print('Done')

# mxd = prj.listMaps('Map')[0]
# lry = mxd.listLayers()
# for l in lry:
#     # Get the layer's CIM definition
#     lyrCIM = l.getDefinition('V2')         

#     if type(lyrCIM) is not arcpy.cim.CIMLayer.CIMGroupLayer:
#         # Get the data connection properties for the layer
#         dc = lyrCIM.featureTable.dataConnection

#         if type(dc) is not arcpy.cim.CIMVectorLayers.CIMRelQueryTableDataConnection:
#             print(dc.workspaceConnectionString)
#         else:
#             # Get the first relate on the layer
#             relate = lyrCIM.featureTable.relates
#             print(type(lyrCIM.featureTable))
            # Get the data connection properties for the relate
            #dc = relate.dataConnection
            #print(dc.workspaceConnectionString)
# mxd.findAndReplaceWorkspacePaths(r"C:\Project\Connection to Default.sde", 
#                                  r"C:\Project\Connection to Version1.sde")
# mxd.saveACopy(r"D:\Test\lrs\new lrs\Map1.mapx")