# Name: create_sde.py
# Description: Creates SDE file using database connection properties.

# Import system modules
import arcpy
import getopt
import os
import sys

def main(argv):
    HELP = 'create_sde.py -p <path> -f <filename> -s <platform> -i <instance> -a <authentication> -u <username> -d <password> -b <database> -v <version>'
    DEFAULT = '#'
    DATABASE = 'DATABASE_AUTH'
    OSA = 'OPERATING_SYSTEM_AUTH'

    path = ''
    filename = ''
    platform = ''
    instance = ''
    authentication = OSA
    username = DEFAULT
    password = DEFAULT
    database = ''
    version = 'dbo.DEFAULT'

    try:
        opts, args = getopt.getopt(argv, "hp:f:s:i:a:u:d:b:v:", ["path=", "filename=", "platform=", "instance=", "authentication=", "username=", "password=", "database=", "version="])
    except getopt.GetoptError:
        print(HELP)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(HELP)
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-f", "--filename"):
            filename = arg
        elif opt in ("-s", "--platform"):
            platform = arg
        elif opt in ("-i", "--instance"):
            instance = arg
        elif opt in ("-a", "--authentication"):
            inputauth = arg
            if inputauth == 'database':
                authentication = DATABASE
        elif opt in ("-u", "--username"):
            inputuser = arg
            if inputuser != '':
                username = inputuser
        elif opt in ("-d", "--password"):
            inputpass = arg
            if inputpass != '':
                password = inputpass
        elif opt in ("-b", "--database"):
            database = arg
        elif opt in ("-v", "--version"):
            inputversion = arg
            if inputversion != '':
                version = inputversion

    fullname = path + '\\' + filename

    # print 'SDE file is ', fullname
    # print 'Database Platform is ', platform
    # print 'Instance is ', instance
    # print 'Authentication is ', authentication
    # print 'Username is ', username
    # print 'Password is ', password
    # print 'Database is ', database
    # print 'Version is ', version
    
    if os.path.exists(fullname):
        os.remove(fullname)

    try:
        # Run the tool
        arcpy.CreateDatabaseConnection_management(path, filename, platform, instance, authentication, username, password, DEFAULT, database, DEFAULT, DEFAULT, version)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])

        # If using this code within a script tool, AddError can be used to return messages 
        #   back to a script tool. If not, AddError will have no effect.
        arcpy.AddError(e.args[0])
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])