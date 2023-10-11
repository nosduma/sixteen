import sqlite3

def show_table_structure(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Query the schema information from the sqlite_master table
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")

    # Fetch and print the results
    tables = cursor.fetchall()
    for table in tables:
        table_name, create_table_sql = table
        print(f"Table Name: {table_name}")
        print("Table Schema:")
        print(create_table_sql)
        print()

    conn.close()

# Replace 'database.db' with your actual database file name
show_table_structure('database.db')
