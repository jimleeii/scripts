# Name: create_feature.py
# Description: Creates feature and save it to feature class in the file geodatabase.
# Environment: arcpy version 3.7.9
# Reference: 


import arcpy
import pandas as pd
import pyodbc
import os

SHAPE = 'SHAPE@'
IGNORELIST = ['OBJECTID','Shape_Length','Shape']

lineloop_query = [
'SELECT DISTINCT SS.LineLoopId ',
'FROM Bend B',
'INNER JOIN StationSeries SS ON B.StationSeriesId = ss.Id ',
'INNER JOIN LineLoop LL ON SS.LineLoopId = LL.Id ',
'WHERE SS.EffectiveEndDate IS NULL AND B.EffectiveEndDate IS NULL ',
'ORDER BY SS.LineLoopId'
]

stationseries_query = [
'SELECT DISTINCT ss.LineLoopId, SS.Id ',
'FROM Bend B ',
'INNER JOIN StationSeries SS ON B.StationSeriesId = ss.Id ',
'INNER JOIN LineLoop LL ON SS.LineLoopId = LL.Id ',
'WHERE SS.EffectiveEndDate IS NULL AND B.EffectiveEndDate IS NULL ',
'ORDER BY SS.LineLoopId, SS.Id'
]

bend_query = [
'SELECT B.Id, B.StationSeriesId, SS.SourceId, SS.LineLoopId AS LineLoopId, B.StationNum, SS.BeginStationNum, SS.EndStationNum, LL.LineName, ',
    'LL.LineName AS FeatureName, ',
    'MLVS1.UpstreamCompressorName UpCompressorName, MLVS2.DownstreamCompressorName DownCompressorName, ',
    'MLVS1.MLVSectionName StartMLVSectionName, MLVS2.MLVSectionName EndMLVSectionName, ',
    '(B.StationNum * MLV1.MultiplierNum + MLV1.FactorNum) AS Chainage, ',
    '(SS.BeginStationNum * MLV1.MultiplierNum + MLV1.FactorNum) AS StartChainage, ',
    '(SS.EndStationNum * MLV2.MultiplierNum + MLV2.FactorNum) AS EndChainage, ',
    '(SS.EndStationNum * MLV2.MultiplierNum + MLV2.FactorNum) - (SS.BeginStationNum * MLV1.MultiplierNum + MLV1.FactorNum) AS Length, ',
    'BendLatitude, BendLongitude ',
'FROM Bend B ',
'INNER JOIN StationSeries SS ON B.StationSeriesId = SS.Id ',
'INNER JOIN MLVCorrection MLV1 ON (SS.Id = MLV1.StationSeriesId) AND ((SS.BeginStationNum BETWEEN MLV1.BeginStationNum AND MLV1.EndStationNum) OR (SS.BeginStationNum BETWEEN MLV1.EndStationNum AND MLV1.BeginStationNum)) ',
'INNER JOIN MLVCorrection MLV2 ON (SS.Id = MLV2.StationSeriesId) AND ((SS.EndStationNum BETWEEN MLV2.BeginStationNum AND MLV2.EndStationNum) OR (SS.EndStationNum BETWEEN MLV2.EndStationNum AND MLV2.BeginStationNum)) ',
'INNER JOIN LineLoop LL ON SS.LineLoopId = LL.Id ',
'INNER JOIN MLVSection MLVS1 ON MLV1.MLVSectionId = MLVS1.Id ',
'INNER JOIN MLVSection MLVS2 ON MLV2.MLVSectionId = MLVS2.Id ',
'WHERE SS.EffectiveEndDate IS NULL AND B.EffectiveEndDate IS NULL ', # use AND SS.LineLoopId = ? for parameter on cursor
'ORDER BY SS.LineLoopId, SS.SeriesValueNumber, Chainage'
]

server = input('sql server: ')
database = input('database: ')
feature_class = input('feature class: ')
# LINELOOP-The lineloop based.
# STATIONSERIES-The station series based.
segment_type = input('segment type: ')

spatial_reference = arcpy.Describe(feature_class).spatialReference
connect = pyodbc.connect('Driver={SQL Server};Server=' + server + ';Database=' + database+ ';Trusted_Connection=yes;')
lineloop_data = pd.read_sql(os.linesep.join(lineloop_query), connect)
stationseries_data = pd.read_sql(os.linesep.join(stationseries_query), connect)
bend_data = pd.read_sql(os.linesep.join(bend_query), connect)

fields = []
for field in arcpy.ListFields(feature_class):
    if field.name in IGNORELIST:
        continue
    fields.append(field.name)
print(tuple(fields) + (SHAPE,))

insert_cursor = arcpy.da.InsertCursor(feature_class, fields + [SHAPE])

for index, row in lineloop_data.iterrows():
    lineloopId = row['LineLoopId']
    print(f'LineloopId: {int(lineloopId)} [{index + 1} / {len(lineloop_data.index)}]')

    bend_data_by_lineloopId = bend_data[bend_data['LineLoopId'] == lineloopId]

    point_collection = arcpy.Array()

    if segment_type == 'STATIONSERIES':
        stationseries_by_lineloopId = stationseries_data[stationseries_data['LineLoopId'] == lineloopId]

        for sindex, ss_row in stationseries_by_lineloopId.iterrows():
            ssId = ss_row['Id']
            print(f'StationSeriesId: {int(ssId)} [{sindex + 1} / {len(stationseries_by_lineloopId.index)}]')

            bend_data_by_lineloopId_ssId = bend_data_by_lineloopId[bend_data_by_lineloopId['StationSeriesId'] == ssId]

            chainage = -1
            for idx, bend_row in bend_data_by_lineloopId_ssId.iterrows():
                point = arcpy.Point(bend_row["BendLongitude"], bend_row["BendLatitude"], None, bend_row["Chainage"])
                if chainage == point.M:
                    continue
                else:
                    chainage = point.M

                point_collection.add(point)

            polyline = arcpy.Polyline(point_collection, spatial_reference)

            bend_data_filtered = bend_data_by_lineloopId_ssId[fields]
            insert_data = bend_data_filtered.iloc[-1].tolist()
            insert_data.append(polyline)
            insert_cursor.insertRow(insert_data)
    elif segment_type == 'LINELOOP':
        chainage = -1
        for idx, bend_row in bend_data_by_lineloopId.iterrows():
            point = arcpy.Point(bend_row["BendLongitude"], bend_row["BendLatitude"], None, bend_row["Chainage"])
            if chainage == point.M:
                continue
            else:
                chainage = point.M

            point_collection.add(point)

        polyline = arcpy.Polyline(point_collection, spatial_reference)

        bend_data_filtered = bend_data_by_lineloopId[fields]
        insert_data = bend_data_filtered.iloc[-1].tolist()
        insert_data.append(polyline)
        insert_cursor.insertRow(insert_data)


    #bend_cursor = connect.cursor()
    #bend_cursor.execute(os.linesep.join(bend_query), lineloopId)
    #bend_row = bend_cursor.fetchone()
    #while bend_row:
    #    print(bend_row)
    #    bend_row = bend_cursor.fetchone()