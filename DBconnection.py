import os
import mysql.connector
from dotenv import load_dotenv

#env variables
load_dotenv()
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "inventory")

def connection():
    try:
        # Establish the connection
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='inventory'
        )
        
        return conn
    except mysql.connector.Error as e:
        return False
    