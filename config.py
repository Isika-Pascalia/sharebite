import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return None

def init_database():
    try:
        connection = get_db_connection()
        if not connection:
            print("❌ Cannot initialize database: No connection.")
            return
        
        cursor = connection.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create food_donations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_donations (
                id INT PRIMARY KEY AUTO_INCREMENT,
                food_name VARCHAR(100) NOT NULL,
                quantity VARCHAR(50),
                location VARCHAR(255),
                contact_info VARCHAR(255),
                donor_id INT,
                is_claimed BOOLEAN DEFAULT FALSE,
                claimed_by INT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (donor_id) REFERENCES users(id)
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Database initialized successfully.")
    except Error as e:
        print(f"❌ Failed to initialize database: {e}")
