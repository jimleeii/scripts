import pyodbc
import pandas as pd

tables = [
'MLVCorrection'
]

for table in tables:
    try:
        schema_query = f"""
        select COLUMN_NAME 
        from INFORMATION_SCHEMA.COLUMNS 
        where TABLE_NAME = '{table}' 
        and COLUMN_NAME not in ('LastModByUserId','LastModDateTime','CreatedDate','CreatedUser')
        ;"""

        base_server = 'SQL2019'
        base_database = 'EEC_US_TRANS_IRASv6_STAGE_OLD'
        base_cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+base_server+';DATABASE='+base_database+';Trusted_Connection=True;')
        base_cursor = base_cnxn.cursor()
        base_cursor.execute(schema_query)
        columns = [str(row[0]) for row in base_cursor]

        query = f"""
        select 
        {','.join(columns)}
        from {table}
        ;"""

        # select rows from SQL table to insert in dataframe.
        base_df = pd.read_sql(query, base_cnxn)

        if len(base_df) == 0:
            raise Exception(f'Table has no data on {base_database}@{base_server}. Count:[{len(base_df)}]')

        server = 'SQL-ENBRIDGE' 
        database = 'EEC_US_TRANS_IRASv6_STAGE' 
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=True;')
        cursor = cnxn.cursor()
        # select rows from SQL table to insert in dataframe.
        df = pd.read_sql(query, cnxn)

        if len(df) == 0:
            raise Exception(f'Table has no data on {database}@{server}. Count:[{len(df)}]')

        print(list(base_df['Id']) == list(df['Id']))

        #rdf = df.compare(base_df)
        #rdf.to_excel(fr'D:\data\{table}.xlsx')
    except Exception as e:
        print(f'Error on {table}.')
        print(f'Exception: {str(e)}')
