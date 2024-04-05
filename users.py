from pydantic import BaseModel
from typing import Union

class User(BaseModel):
    name: str
    enrollment: str
    password: str
    role: str

class Admin(User):
    position: Union[str, None]
    
class Student(User):
    carreer: Union[str, None]
    quarter: Union[int, None]
    
class Login_data(BaseModel):
    enrollment: str
    password: str