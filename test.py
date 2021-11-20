# Name: FeatureClassToFeatureClass_Example2.py
# Description: Use FeatureClassToFeatureClass with an expression to create a subset
#  of the original feature class.  
 
# Import system modules
import os
import sys
#import arcpy
import cx_Oracle
import time

#print(arcpy.GetParameterAsText(0))
#print(arcpy.GetParameterAsText(1))
#print(arcpy.GetParameterAsText(2))
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

q = ['SELECT B.Id, B.StationSeriesId, SS.LineLoopId AS LineLoopId, B.StationNum, SS.BeginStationNum, SS.EndStationNum, LL.LineName, ',
'	LL.LineName AS FeatureName, ',
'	MLVS1.UpstreamCompressorName UpCompressorName, MLVS2.DownstreamCompressorName DownCompressorName, ',
'	MLVS1.MLVSectionName StartMLVSectionName, MLVS2.MLVSectionName EndMLVSectionName, ',
'	(B.StationNum * MLV1.MultiplierNum + MLV1.FactorNum) AS Chainage, ',
'	(SS.BeginStationNum * MLV1.MultiplierNum + MLV1.FactorNum) AS StartChainage, ',
'	(SS.EndStationNum * MLV2.MultiplierNum + MLV2.FactorNum) AS EndChainage, ',
'	(SS.EndStationNum * MLV2.MultiplierNum + MLV2.FactorNum) - (SS.BeginStationNum * MLV1.MultiplierNum + MLV1.FactorNum) AS Length, ',
'	BendLatitude, BendLongitude ',
'FROM Bend B ',
'INNER JOIN StationSeries SS ON B.StationSeriesId = SS.Id ',
'INNER JOIN MLVCorrection MLV1 ON (SS.Id = MLV1.StationSeriesId) AND ((SS.BeginStationNum BETWEEN MLV1.BeginStationNum AND MLV1.EndStationNum) OR (SS.BeginStationNum BETWEEN MLV1.EndStationNum AND MLV1.BeginStationNum)) ',
'INNER JOIN MLVCorrection MLV2 ON (SS.Id = MLV2.StationSeriesId) AND ((SS.EndStationNum BETWEEN MLV2.BeginStationNum AND MLV2.EndStationNum) OR (SS.EndStationNum BETWEEN MLV2.EndStationNum AND MLV2.BeginStationNum)) ',
'INNER JOIN LineLoop LL ON SS.LineLoopId = LL.Id ',
'INNER JOIN MLVSection MLVS1 ON MLV1.MLVSectionId = MLVS1.Id ',
'INNER JOIN MLVSection MLVS2 ON MLV2.MLVSectionId = MLVS2.Id ',
'WHERE SS.EffectiveEndDate IS NULL AND B.EffectiveEndDate IS NULL AND SS.LineLoopID = 11960 ',
'ORDER BY SS.LineLoopId, SS.SeriesValueNumber, Chainage ']
query = os.linesep.join(q)
print(query)

conn = cx_Oracle.connect(dsn='ETP',user='ETP_IRASV6_STAGE_OWNR',password='etp')
cursor = conn.cursor()

# cursor.prefetchrows = 1000
# cursor.arraysize = 1000

query = 'select * from bend where StationSeriesId = 87492'

start = time.time()
cursor.execute(query)
elapsed = time.time() - start
print("Time for", elapsed, "seconds")

for row in cursor:
    print(row)