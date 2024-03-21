from DBconnection import connection
from products import Product
from datetime import datetime
from usersManager import UsersManager

class InventoryManager():
    #Get Categories from the database
    def get_categories(self):
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM categories')
            rows = cursor.fetchall()

            return rows
        except Exception as e:
            return f"ERROR: {e}"
        finally:
            conn.close()
    
    #Get Products from the database
    def get_products(self):
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT p.name, p.description, c.name , p.stock FROM products as p JOIN categories AS c ON category=c.id WHERE stock > 0")
            rows = cursor.fetchall()

            return rows
        except Exception as e:
            return f"ERROR: {e}"
        finally:
            conn.close()
    
    #Get Product from the database
    def get_product(self, id: int):
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT p.name, p.description, c.name , p.stock FROM products as p JOIN categories AS c ON category=c.id WHERE p.id = '{id}'")
            row = cursor.fetchone()

            return row
        except Exception as e:
            return f"ERROR: {e}"
        finally:
            conn.close()
    
    #search for a product
    def search(self, query: str):
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT p.name, p.description, c.name , p.stock FROM products as p JOIN categories AS c ON category=c.id WHERE p.name LIKE '%{query}%' or p.description LIKE '%{query}%' or c.name LIKE '%{query}%'")
            rows = cursor.fetchall()

            return rows
        except Exception as e:
            return f"ERROR: {e}"
        finally:
            conn.close()
    
    #Add Product to the database
    def add_product(self, item: Product, user: str):
        conn = connection()
        um = UsersManager()
        res = "Product Added Successfully"
        try:
            if not um.exists(user): raise Exception("User Does Not Exist")
            if self.exists(item.name): raise Exception("Product Already Exists")
            if (not conn): raise Exception("Database Connection Error")
            if item.stock <= 0: raise Exception("Stock cannot be minor to one")
            if item.category < 1: raise Exception("Category cannot be minor to one")
            
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO products (name, description, stock, category) VALUES ('{item.name}', '{item.description}', {item.stock}, '{item.category}')")
            conn.commit()
            
            um.create_log(f"Product {item.name} added added", user)
        except Exception as e:
            res = f"ERROR: {e}"
        finally:
            conn.close()
            return res
        
    def update_product(self, item: Product, user: str):
        conn = connection()
        um = UsersManager()
        res = "Product Updated Successfully"
        try:
            if not um.exists(user): raise Exception("User Does Not Exist")
            if not self.exists(item.name): raise Exception("Product Does Not Exist")
            if (not conn): raise Exception("Database Connection Error")
            if item.stock <= 0: raise Exception("Stock cannot be minor to one")
            if item.category < 1: raise Exception("Category cannot be minor to one")
            cursor = conn.cursor()
            cursor.execute(f"UPDATE products SET description = '{item.description}', stock = {item.stock}, category = '{item.category}' WHERE name = '{item.name}'")
            conn.commit()
            
            um.create_log(f"Product {item.name} updated", user)
        except Exception as e:
            res = f"ERROR: {e}"
        finally:
            conn.close()
            return res
        
    def delete_product(self, name: str, user: str):
        conn = connection()
        um = UsersManager()
        res = "Product Deleted Successfully"
        try:
            if not um.exists(user): raise Exception("User Does Not Exist")
            if not self.exists(name): raise Exception("Product Does Not Exist")
            if (not conn): raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM products WHERE name = '{name}'")
            conn.commit()
            
            um.create_log(f"Product {name} deleted", user)
        except Exception as e:
            res = f"ERROR: {e}"
        finally:
            conn.close()
            return res
        
    def exists(self, name: str):
        conn = connection()
        try:
            if (not conn): raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM products WHERE name = '{name}'")
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