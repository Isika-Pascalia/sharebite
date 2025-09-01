import mysql.connector
from mysql.connector import Error

class Config:
    # Database configuration - UPDATE THESE WITH YOUR MySQL CREDENTIALS
    DB_HOST = 'localhost'
    DB_USER = 'root'  # Your MySQL username (usually 'root')
    DB_PASSWORD = '1234567890'  # CHANGE THIS to your MySQL password
    DB_NAME = 'sharebite_db'
    
    # Flask configuration
    SECRET_KEY = 'sharebite-secret-key-change-in-production'

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    """Initialize the database and create tables"""
    try:
        # First, create the database if it doesn't exist
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        connection.commit()
        cursor.close()
        connection.close()
        print("Database 'sharebite_db' created successfully!")
        
        # Now connect to the database and create tables
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Users table created successfully!")
        
        # Create food_donations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_donations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                food_name VARCHAR(200) NOT NULL,
                quantity VARCHAR(100) NOT NULL,
                location VARCHAR(255) NOT NULL,
                contact_info VARCHAR(255) NOT NULL,
                donor_id INT NOT NULL,
                is_claimed BOOLEAN DEFAULT FALSE,
                claimed_by INT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (donor_id) REFERENCES users(id),
                FOREIGN KEY (claimed_by) REFERENCES users(id)
            )
        """)
        print("Food donations table created successfully!")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("All database tables created successfully!")
        
    except Error as e:
        print(f"Error creating database: {e}")
        print("Make sure MySQL is running and your credentials are correct!")

# Test database connection when this file is run
if __name__ == "__main__":
    print("Testing database connection...")
    init_database()