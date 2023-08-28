import arcpy
from os import path

def ListFolders(rootfolder, folders):
    arcpy.env.workspace = rootfolder
    workspaces = arcpy.ListWorkspaces("*")
    
    if len(workspaces) == 0:
        return
    
    for workspace in workspaces:
        # print(workspace)
        folders.append(workspace)
        ListFolders(workspace, folders)

def ListFiles(filefolder, allfiles):
    arcpy.env.workspace = filefolder
    files = arcpy.ListFiles("*")

    for file in files:
        # print(path.join(filefolder, file))
        allfiles.append(path.join(filefolder, file))
    
folders = []
ListFolders("C:\Temp", folders)

files = []
for folder in folders:
    # print(folder)
    ListFiles(folder, files)

for file in files:
    print(file)