# Name: create_feature_class.py
# Description: Creates feature class and save it to file geodatabase.
# Environment: arcpy version 3.7.9
# Reference: https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/create-feature-class.htm


import arcpy

out_path = input('file geodatabase: ')
out_name = input('feature class name: ')
# POINT—The geometry type will be point.
# MULTIPOINT—The geometry type will be multipoint.
# POLYGON—The geometry type will be polygon.
# POLYLINE—The geometry type will be polyline.
# MULTIPATCH—The geometry type will be multipatch.
geometry_type = input('geometry type: ')
template = input('template path: ')
spatial_reference = arcpy.Describe(template).spatialReference

arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type, template, 'ENABLED', 'ENABLED', spatial_reference)