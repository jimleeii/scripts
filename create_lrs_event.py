import arcpy
import options_reader
import os

params = []
params.append(options_reader.Parameters(short='-w', long='--workspace', variable={'workspace': None}, descrption="Workspace geodatabase file path or SDE file path."))
params.append(options_reader.Parameters(short='-p', long='--parent_network', variable={'parent_network': None}, descrption="Network fullname in LRS."))
params.append(options_reader.Parameters(short='-i', long='--in_feature_class', variable={'in_feature_class': None}, descrption="Input feature class full name will be registared in LRS."))
params.append(options_reader.Parameters(short='-e', long='--event_id_field', variable={'event_id_field': 'EventId'}, descrption="Event ID field name in input feature class."))
params.append(options_reader.Parameters(short='-r', long='--route_id_field', variable={'route_id_field': 'RouteId'}, descrption="Route ID field name in input feature class."))
params.append(options_reader.Parameters(short='-f', long='--from_date_field', variable={'from_date_field': 'EffectiveStartDate'}, descrption="From date field name in input feature class."))
params.append(options_reader.Parameters(short='-t', long='--to_date_field', variable={'to_date_field': 'EffectiveEndDate'}, descrption="To date field name in input feature class."))
params.append(options_reader.Parameters(short='-l', long='--loc_error_field', variable={'loc_error_field': 'LocError'}, descrption="Location error field name in input feature class."))
params.append(options_reader.Parameters(short='-m', long='--measure_field', variable={'measure_field': 'FromMeasure'}, descrption="From measure field name in input feature class."))
params.append(options_reader.Parameters(short='-o', long='--to_measure_field', variable={'to_measure_field': None}, descrption="To measure field name in input feature class."))

HELP = [""]
HELP.append("This is a script to help create LRS from existing featureclass.")
HELP.append("")
for hp in params:
    HELP.append("%s, %s\t\t%s" %(hp.short, hp.long, hp.description))    
HELP.append("")
HELP.append("")

# Tool variables
workspace = None
parent_network = None
in_feature_class = None
event_id_field = "EventId"
route_id_field = "RouteId"
from_date_field = "EffectiveStartDate"
to_date_field = "EffectiveEndDate"
loc_error_field = "LocError"
measure_field = "FromMeasure"
to_measure_field = None

event_spans_routes = "NO_SPANS_ROUTES"
to_route_id_field = None
store_route_name = "NO_STORE_ROUTE_NAME"
route_name_field = None
to_route_name_field = None

try:
    opts = options_reader.Options(version='1.0.0.0', help=HELP, 
        parameters={
            '-w': '--workspace', 
            '-p': '--parent_network', 
            '-i': '--in_feature_class', 
            '-e': '--event_id_field',
            '-r': '--route_id_field',
            '-f': '--from_date_field',
            '-t': '--to_date_field',
            '-l': '--loc_error_field',
            '-m': '--measure_field',
            '-o': '--to_measure_field'})

    readin = options_reader.read(opts)

    for rin in readin:
        if rin in ('-w', '--workspace'):
            workspace = readin[rin]
        elif rin in ('-p', '--parent_network'):
            parent_network = readin[rin]
        elif rin in ('-i', '--in_feature_class'):
            in_feature_class = readin[rin]
        elif rin in ('-e', '--event_id_field'):
            event_id_field = readin[rin]
        elif rin in ('-r', '--route_id_field'):
            route_id_field = readin[rin]
        elif rin in ('-f', '--from_date_field'):
            from_date_field = readin[rin]
        elif rin in ('-t', '--to_date_field'):
            to_date_field = readin[rin]
        elif rin in ('-l', '--loc_error_field'):
            loc_error_field = readin[rin]
        elif rin in ('-m', '--measure_field'):
            measure_field = readin[rin]
        elif rin in ('-o', '--to_measure_field'):
            to_measure_field = readin[rin]

    parent_network = os.path.join(workspace, parent_network)
    in_feature_class = os.path.join(workspace, in_feature_class)
    
    # Check out license
    arcpy.CheckOutExtension("LocationReferencing")

    # Set current workspace
    arcpy.env.workspace = workspace

    # Execute the tool
    arcpy.CreateLRSEventFromExistingDataset_locref(parent_network, in_feature_class, event_id_field, route_id_field,
                                                from_date_field, to_date_field, loc_error_field, measure_field,
                                                to_measure_field, event_spans_routes, to_route_id_field,
                                                store_route_name, route_name_field, to_route_name_field)
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

    # Check in license
    arcpy.CheckInExtension('LocationReferencing')

