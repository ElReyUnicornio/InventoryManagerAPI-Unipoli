import mysql.connector

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
    