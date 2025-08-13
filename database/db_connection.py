import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

def connect():
    try:
        conn_str = (
            f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
            "Trusted_Connection=no;"
        )
        connection = pyodbc.connect(conn_str)
        print("✅ Database connection successful!")
        return connection
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        raise
