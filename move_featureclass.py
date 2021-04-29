# Name: move_featureclass.py
# Description: Moves feature class from file geodatabase to
#              SDE connection.

# Import system modules
import arcpy
import getopt
import os
import sys

def main(argv):
    HELP = 'move_featureclass.py -g <geodatabase> -s <sdefilename> -p <platform>'

    geodatabase = ''
    sdefilename = ''
    platform = 'DBO.'

    try:
        opts, args = getopt.getopt(argv, "hg:s:p:", ["geodatabase=", "sdefilename=", "platform="])
    except getopt.GetoptError:
        print(HELP)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(HELP)
            sys.exit()
        elif opt in ("-g", "--geodatabase"):
            geodatabase = arg
        elif opt in ("-s", "--sdefilename"):
            sdefilename = arg
        elif opt in ("-i", "--platform"):
            inputplat = arg
            if inputplat != '':
                platform = 'SDE.'
            elif inputplat == 'ORACLE':
                platform = 'SDE.'

    try:
        arcpy.env.workspace = geodatabase
        featureclasslist = arcpy.ListFeatureClasses()

        # arcpy.env.workspace = sdefilename
        # arcpy.env.overwriteOutput=True

        for dataitem in featureclasslist:
            # arcpy.CopyFeatures_management(os.path.join(geodatabase, dataitem), platform + dataitem)
            attributelist = arcpy.ListFields(os.path.join(geodatabase, dataitem))

            for attribute in attributelist:
                print 'Field : ' + attribute.name
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])

        # If using this code within a script tool, AddError can be used to return messages 
        #   back to a script tool. If not, AddError will have no effect.
        arcpy.AddError(e.args[0])
        sys.exit(2)

    # print 'Geodatabase path is ' + geodatabase
    # print 'SDE filename is ' + sdefilename

if __name__ == "__main__":
    main(sys.argv[1:])