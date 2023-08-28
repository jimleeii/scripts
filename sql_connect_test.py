# import pandas as pd
import pyodbc
import os

server = input('sql server: ')
database = input('database: ')
filename = input('sql file: ')

script = []
with open(filename) as f:
    for line in f:
        script.append(line.strip())
    # lines = f.readlines()
    # script = os.linesep.join(lines)

connect = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=' + server + ';Database=' + database+ ';Trusted_Connection=yes;')
# connect.timeout = 0
cursor = connect.cursor()

# sql = """\
# SET NOCOUNT ON;
# EXEC sp_InsertSingleParts;
# """

try:
    cursor.execute(os.linesep.join(script))
except Exception as e:
    print(e)
finally:
    cursor.close()
    connect.commit()