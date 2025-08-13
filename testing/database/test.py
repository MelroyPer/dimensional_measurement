import pyodbc

# Update these with your actual details
server = 'ALVS-INTSQL02'     # e.g. '192.168.1.100' or 'sql.mycompany.com'
database = 'TND_QI'       # e.g. 'quality_db'
username = 'TND_QI_Admin'            # e.g. 'dbuser'
password = 'hpa!VTeq04h!k9FSvwKc'            # e.g. 'mypassword'


conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

try:
    conn = pyodbc.connect(conn_str, timeout=5)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)



# try:
#     conn = pyodbc.connect(conn_str)
#     cursor = conn.cursor()
#     cursor.execute("SELECT TOP 5 * FROM your_table_name")  # Change table name
#     rows = cursor.fetchall()

#     for row in rows:
#         print(row)

#     conn.close()
# except Exception as e:
#     print("Connection failed:", e)
