# Name: FeatureClassToFeatureClass_Example2.py
# Description: Use FeatureClassToFeatureClass with an expression to create a subset
#  of the original feature class.  
 
# Import system modules
import os
import sys
import arcpy

print(arcpy.GetParameterAsText(0))
print(arcpy.GetParameterAsText(1))
print(arcpy.GetParameterAsText(2))
# Get input arguments
#print(sys.argv)
# os.remove("D:\\Test\\sde\\test.sde")
# arcpy.CreateDatabaseConnection_management("D:\\Test\\sde", "test.sde", "SQL_SERVER", "SQL2017", "OPERATING_SYSTEM_AUTH", "#", "#", "#", "KEY_IRASV5_Upstream", "#", "#", "dbo.DEFAULT")

# Set environment settings
#arcpy.env.workspace = "C:/Users/wei_li/OneDrive - dynamicrisk.net/Desktop/KeyeraUpdate_20210218.gdb"
#arcpy.FeatureClassToFeatureClass_conversion("KEY_LINES", "C:/output/output.gdb",  "KEY_LINES")

# Set local variables
#inFeatures = "KEY_LINES"
#outLocation = "C:/output/output.gdb"
#outFeatureClass = "postoffices"
#delimitedField = arcpy.AddFieldDelimiters(arcpy.env.workspace, "NAME")
#print(delimitedField)
#expression = delimitedField + " = 'Post Office'"
 
# Execute FeatureClassToFeatureClass
#arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)