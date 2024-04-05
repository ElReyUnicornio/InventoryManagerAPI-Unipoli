import os
from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from users import Admin, Student, User, Login_data
from usersManager import UsersManager
from DBconnection import connection
from inventoryManager import InventoryManager
from products import Product
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt

app = FastAPI()
origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://localhost:8100",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
usersManager = UsersManager()
inventoryManager = InventoryManager()

class Token(BaseModel):
    user_token: str

# ENVIRONMENT VARIABLES
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "1357924680")
TOKEN_EXPIRE_MINUTES = float(os.getenv("TOKEN_EXPIRE_MINUTES", 1))

@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Root endpoint of the API.

    Returns:
        str: HTML response with a link to the API documentation page.
    """
    return """<html><p>Go to <a href='http://127.0.0.1:8000/docs'>Documentation page</a> to see the API documentation</p></html>"""

@app.delete("/delete_item/")
def delete_item(item: Product):
    """
    Delete an item from the inventory.

    Args:
        item (Product): The item to be deleted.

    Returns:
        dict: The result of the deletion operation.
    """
    token = Token(user_token=(item.user_token.replace('"', '')))
    user = verify_token(token)
    return inventoryManager.delete_product(item.name, user)

@app.patch("/update_item/")
def update_item(item: Product):
    """
    Update an item in the inventory.

    Args:
        item (Product): The item to be updated.

    Returns:
        dict: The result of the update operation.
    """
    token = Token(user_token=(item.user_token.replace('"', '')))
    user = verify_token(token)
    return inventoryManager.update_product(item, user)

@app.post("/add_item/")
def add_item(item: Product):
    """
    Add a new item to the inventory.

    Args:
        item (Product): The item to be added.

    Returns:
        dict: The result of the addition operation.
    """
    print(item)
    token = Token(user_token=(item.user_token.replace('"', '')))
    user = verify_token(token)
    return inventoryManager.add_product(item, user)

@app.get("/get_item/{item_id}")
def read_item(item_id: str):
    """
    Get a specific item from the inventory.

    Args:
        item_id (str): The ID of the item to retrieve.

    Returns:
        dict: The retrieved item.
    """
    return inventoryManager.get_product(item_id)

@app.get("/get_items/")
def read_items(q: Union[str, None] = None):
    """
    Get all items from the inventory.

    Args:
        q (Union[str, None], optional): The search query. Defaults to None.

    Returns:
        list: The retrieved items.
    """
    if q:
        return inventoryManager.search(q)
    else:
        return inventoryManager.get_products()

@app.get("/categories/")
def get_categories():
    """
    Get all categories from the inventory.

    Returns:
        list: The retrieved categories.
    """
    return inventoryManager.get_categories()

@app.post("/register/")
def register(user: Union[Admin, Student]):
    """
    Register a new user.

    Args:
        user (Union[Admin, Student]): The user to be registered.

    Returns:
        str: The authentication token for the registered user.
    
    Raises:
        HTTPException: If there is an error during the registration process.
    """
    if user.role == "Admin":
        position = user.position
        carreer = ''
        quarter = 0
    elif user.role == "Student":
        position = ''
        carreer = user.carreer
        quarter = user.quarter
        
    res = usersManager.register(user.name, user.enrollment, user.password, user.role, carreer, quarter, position)
    if "error" not in res:
        expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({**res, "exp": expire}, SECRET_KEY, algorithm="HS256")
        return token
    else:
        raise HTTPException(status_code=401, detail=res["error"])


@app.post("/login/")
def login(user: Login_data):
    """
    Log in a user.

    Args:
        user (User): The user to log in.

    Returns:
        str: The authentication token for the logged-in user.
    
    Raises:
        HTTPException: If there is an error during the login process.
    """
    res = usersManager.login(user.enrollment, user.password)
    if "error" not in res:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({**res, "exp": expire}, SECRET_KEY, algorithm="HS256")
        return token
    else:
        raise HTTPException(status_code=401, detail=res["error"])

@app.post('/verify_token/')
def verify_token(token: Token):
    """
    Verify the authenticity of a token.

    Args:
        token (str): The token to be verified.

    Returns:
        dict: The payload of the token.

    Raises:
        HTTPException: If the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token.user_token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))