import pyodbc
import pandas as pd

server = 'CGY-M920S-0008' 
database = 'KEY_IRASV5_Upstream' 
#username = 'test' 
#password = 'test'  
#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=True;')
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT DisplayFieldCode, TableName, ColumnName FROM AppDisplayField;"
df = pd.read_sql(query, cnxn)
print(df.head(-1))