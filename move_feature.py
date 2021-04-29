# Import system modules
import arcpy
import os
import sys
try:
        ParcelSAMNo = arcpy.GetParameterAsText(0)
        ModeofQuery = arcpy.GetParameterAsText(1)
        TransactionNo= arcpy.GetParameterAsText(2)
        if ParcelSAMNo:
            print(ParcelSAMNo)
        if ModeofQuery:
            print(ModeofQuery)
        if TransactionNo:
            print(TransactionNo)
        arcpy.env.workspace = r"D:\Test\sde\KEY_IRASV5_Upstream.sde" #"C:\Users\chenna.kishore\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\LIC.sde\LIC.LandPlan"
        #arcpy.env.overwriteOutput = True 
        fc = "dbo.STATIONSERIES"
        where_clause = "Id in (" + ParcelSAMNo + ")"
        s_cursor = arcpy.da.SearchCursor(fc, ("SHAPE@", "Id", "StationSeriesName"), where_clause)
        for s_row in s_cursor:
            print(s_row[2])


        #arcpy.env.workspace = r"C:\Users\chenna.kishore\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\SDE@REGEO.sde\SDE.Parcels"
        #outFc="SDE.RPAR_PD_Parcels"
        #with arcpy.da.InsertCursor(outFc,["PIN", "PAR_AREA", "SAM_NO", "TRANS_NO", "SHAPE@"]) as rowInserter:
            #for s_row in s_cursor:
                    # Insert the new row into the Parcel Layer
                    #geom = s_row[0]
                    #row_values = [str(s_row[1]), s_row[2], 0, int(TransactionNo), geom]
                    #print row_values
                    #rowInserter.insertRow(row_values)
                    #rowInserter.insertRow([str(s_row[1]), s_row[2], 0, int(TransactionNo), geom])
        # Clean up the cursor
        #del rowInserter
        del s_cursor
        del s_row
except Exception as e:
    print(e.message)
print("Success Full..!")
