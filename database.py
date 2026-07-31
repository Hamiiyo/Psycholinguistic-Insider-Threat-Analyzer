import pyodbc

# Connect to SentinelDB for centralized incident tracking
conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.\SQLEXPRESS;'
                              'Database=SentinelDB;'
                              'Trusted_Connection=yes;')

cursor = conn.cursor()

with open('schema.sql', 'r') as file:
    sql_script = file.read()

try:
    cursor.execute(sql_script)
    conn.commit()
    print("[+] Database tables successfully created.")
except Exception as e:
    print(f"[!] Error creating tables: {e}")
finally:
    cursor.close()
    conn.close()