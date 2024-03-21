from typing import Union
from fastapi import FastAPI
import mysql.connector
from fastapi.responses import HTMLResponse
from users import Admin, Student
from usersManager import UsersManager
from DBconnection import connection
from inventoryManager import InventoryManager
from products import Product

app = FastAPI()
usersManager = UsersManager()
inventoryManager = InventoryManager()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """<html><p>Go to <a href='http://127.0.0.1:8000/docs'>Documentation page</a> to see the API documentation</p></html>"""

@app.delete("/delete_item/{item_name}/{user}")
def delete_item(item_name: str, user: str):
    return inventoryManager.delete_product(item_name, user)

@app.patch("/update_item/{user}")
def update_item(item: Product, user: str):
    return inventoryManager.update_product(item, user)

#add a new product to the database
@app.post("/add_item/{user}")
def add_item(item: Product, user: str):
    return inventoryManager.add_product(item, user)

#Get Product from the database
@app.get("/get_item/{item_id}")
def read_item(item_id: int):
    return inventoryManager.get_product(item_id)

#Get Products from the database
@app.get("/get_items/")
def read_items(q: Union[str, None] = None):
    if q:
        return inventoryManager.search(q)
    else:
        return inventoryManager.get_products()

#Register a new user
@app.post("/register/")
def register(user: Union[Admin, Student]):
    return usersManager.register(user.name, user.enrollment, user.password, user.role, user.carreer, user.quarter, user.position)

#Login a user
@app.post("/login/")
def login(user: Union[Admin, Student]):
    return usersManager.login(user.enrollment, user.password)

#Get Categories from the database
@app.get("/categories/")
def get_categories():
    return inventoryManager.get_categories()