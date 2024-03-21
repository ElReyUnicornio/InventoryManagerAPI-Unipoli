from DBconnection import connection
from datetime import datetime
from typing import Union

#Users base Class
class UsersManager():
    #register the user
    def register(self, name: str, enrollment: str, password: str, role: str, carreer: Union[str,None], quarter: Union[int,None], position: Union[str,None]):
        conn = connection()
        res = "User Registered Successfully"
        try:
            if self.exists(enrollment): raise Exception("User Already Exists")
            if (not conn): raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO users (name, enrollment, password, role) VALUES ('{name}', '{enrollment}', '{password}', '{role}', '{carreer}', '{quarter}', '{position}')")
            conn.commit()
            
            self.create_log(f"User {name}({enrollment}) registered correctly", enrollment)
            res = {"name": name, "enrollment": enrollment, "role": role, "carreer": carreer, "quarter": quarter, "position": position}
        except Exception as e:
            res = f"ERROR: {str(e)}"
        finally:
            conn.close()
            return res
        
    #login the user
    def login(self, enrollment: str, password: str):
        conn = connection()
        try:
            if not conn: raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE enrollment = '{enrollment}' AND password = '{password}'")
            row = cursor.fetchone()
            if not row: raise Exception("Invalid Credentials")
            
            description = (f"User {row[0]}({row[1]}) logged in")
            self.create_log(description, row[1])
            return {"name": row[0], "enrollment": row[1], "role": row[3], "carreer": row[4], "quarter": row[5], "position": row[6]}
        except Exception as e:
            
            return f"ERROR: {str(e)}"
        finally:
            conn.close()
    
    #check if user Already exists
    def exists(self, user: str):
        conn = connection()
        try:
            if (not conn): raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE enrollment = '{user}'")
            row = cursor.fetchone()
            conn.close()
            if row:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()
    
    def create_log(self, description: str, user: str):
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
        