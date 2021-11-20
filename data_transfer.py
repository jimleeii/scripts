import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQL2012;'
                      'Database=WGL_IRASv6_STAGE;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute("SELECT * FROM SystemPreferences WHERE ParameterName = 'MapWorkspaceVersion'")

for i in cursor:
    print(i)