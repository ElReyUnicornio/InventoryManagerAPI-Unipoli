from DBconnection import connection
from datetime import datetime
from typing import Union
from users import Admin, Student
import bcrypt

#Users base Class
class UsersManager():
    """
    This class provides methods for user registration, login, and log creation.
    """

    def register(self, name: str, enrollment: str, password: str, role: str, carreer: str, quarter: str, position: str):
        """
        Registers a new user in the database.

        Args:
            name (str): The name of the user.
            enrollment (str): The enrollment number of the user.
            password (str): The password of the user.
            role (str): The role of the user.
            carreer (str): The career of the user.
            quarter (str): The quarter of the user.
            position (str): The position of the user.

        Returns:
            dict: A dictionary containing the result of the registration process. If successful, the dictionary will contain a "message" key with the value "User Registered Successfully". If an error occurs, the dictionary will contain an "error" key with the error message.
        """
        conn = connection()
        try:
            if not conn: raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE enrollment = %s", (enrollment,))
            row = cursor.fetchone()
            if row: raise Exception("User Already Exists")

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            cursor.execute("INSERT INTO users (name, enrollment, password, role, carreer, quarter, position) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                        (name, enrollment, hashed_password, role, carreer, quarter, position))
            conn.commit()

            description = (f"User {name}({enrollment}) registered")
            self.create_log(description, enrollment)
            return {"message": "User Registered Successfully"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()
        
    def login(self, enrollment: str, password: str):
        """
        Logs in a user with the provided enrollment number and password.

        Args:
            enrollment (str): The enrollment number of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary containing the user information if the login is successful. The dictionary will contain the following keys: "name", "enrollment", "role", "carreer", "quarter", and "position". If an error occurs, the dictionary will contain an "error" key with the error message.
        """
        conn = connection()
        try:
            if not conn: raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE enrollment = %s", (enrollment,))
            row = cursor.fetchone()
            if not row: raise Exception("Invalid Credentials")

            # Verify hashed password
            hashed_password = row[2].encode('utf-8')
            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                raise Exception("Invalid Credentials")

            description = (f"User {row[0]}({row[1]}) logged in")
            self.create_log(description, row[1])
            return {"name": row[0], "enrollment": row[1], "role": row[3], "carreer": row[4], "quarter": row[5], "position": row[6]}
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()
    
    def create_log(self, description: str, user: str):
        """
        Creates a log entry in the database.

        Args:
            description (str): The description of the log entry.
            user (str): The user associated with the log entry.
        """
        conn = connection()
        try:
            if not conn: raise Exception("Database Connection Error")
            date = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO logs (date, description, user) VALUES ('{date}', '{description}', '{user}')")
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()
        