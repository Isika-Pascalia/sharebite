# import mysql.connector
# from mysql.connector import Error

# class Config:
#     SECRET_KEY = "your_super_secret_key"  # Change to something strong!
#     DB_HOST = "localhost"
#     DB_USER = "root"       # Change if different
#     DB_PASSWORD = "1234567890"  # Set your MySQL password
#     DB_NAME = "sharebite"

# def get_db_connection():
#     """Establish MySQL database connection"""
#     try:
#         connection = mysql.connector.connect(
#             host=Config.DB_HOST,
#             user=Config.DB_USER,
#             password=Config.DB_PASSWORD,
#             database=Config.DB_NAME
#         )
#         return connection
#     except Error as e:
#         print(f"Database connection failed: {e}")
#         return None

# def init_database():
#     """Initialize tables if they don't exist"""
#     connection = get_db_connection()
#     if connection:
#         cursor = connection.cursor()

#         # Create users table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 username VARCHAR(100) UNIQUE NOT NULL,
#                 email VARCHAR(150) UNIQUE NOT NULL,
#                 password VARCHAR(255) NOT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)

#         # Create food donations table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS food_donations (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 food_name VARCHAR(200) NOT NULL,
#                 quantity VARCHAR(50) NOT NULL,
#                 location VARCHAR(255) NOT NULL,
#                 contact_info VARCHAR(255) NOT NULL,
#                 donor_id INT NOT NULL,
#                 is_claimed BOOLEAN DEFAULT FALSE,
#                 claimed_by INT DEFAULT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 FOREIGN KEY (donor_id) REFERENCES users(id)
#             )
#         """)

#         connection.commit()
#         cursor.close()
#         connection.close()
import os
import mysql.connector
from mysql.connector import Error


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key")

    # Database configuration from environment variables
    # e.g., mysql-<service-name>.onrender.com
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")      # e.g., render user
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")


def get_db_connection():
    """Establish MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None


def init_database():
    """Initialize tables if they don't exist"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create food donations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_donations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                food_name VARCHAR(200) NOT NULL,
                quantity VARCHAR(50) NOT NULL,
                location VARCHAR(255) NOT NULL,
                contact_info VARCHAR(255) NOT NULL,
                donor_id INT NOT NULL,
                is_claimed BOOLEAN DEFAULT FALSE,
                claimed_by INT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (donor_id) REFERENCES users(id)
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
