from config import get_db_connection

connection = get_db_connection()
if connection:
    print("✅ Database connection successful!")
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    print("Tables:", cursor.fetchall())
    connection.close()
else:
    print("❌ Database connection failed!")
