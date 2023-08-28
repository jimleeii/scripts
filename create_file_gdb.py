# Name: create_file_gdb.py
# Description: Creates file geodatabase wth file path and file name.
# Environment: arcpy version 3.7.9
# Reference: https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/create-file-gdb.htm


import arcpy

out_folder_path = input('file path: ')
out_name = input('file geodatabase name: ')

arcpy.management.CreateFileGDB(out_folder_path, out_name)