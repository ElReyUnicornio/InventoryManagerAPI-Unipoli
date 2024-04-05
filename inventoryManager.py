from DBconnection import connection
from products import Product
from datetime import datetime
from usersManager import UsersManager

class InventoryManager():
    """
    A class that manages the inventory of products.

    Methods:
    - get_categories: Get categories from the database.
    - get_products: Get products from the database.
    - get_product: Get a specific product from the database.
    - search: Search for products based on a query.
    - add_product: Add a new product to the database.
    - update_product: Update an existing product in the database.
    - delete_product: Delete a product from the database.
    - exists: Check if a product exists in the database.
    """

    def get_categories(self):
        """
        Get categories from the database.

        Returns:
        - A list of category names.
        - If an error occurs, returns a dictionary with the error message.
        """
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM categories')
            rows = cursor.fetchall()

            return rows
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def get_products(self):
        """
        Get products from the database.

        Returns:
        - A list of products with their name, description, category, and stock.
        - If an error occurs, returns a dictionary with the error message.
        """
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT p.name, p.description, c.name , p.stock FROM products as p JOIN categories AS c ON category=c.id WHERE stock > 0")
            rows = cursor.fetchall()

            return rows
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def get_product(self, name: str):
        """
        Get a specific product from the database.

        Args:
        - name: The name of the product to retrieve.

        Returns:
        - The product with its name, description, category, and stock.
        - If an error occurs, returns a dictionary with the error message.
        """
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT p.name, p.description, c.name , p.stock FROM products as p JOIN categories AS c ON category=c.id WHERE p.name = '{name}'")
            row = cursor.fetchone()

            return row
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def search(self, query: str):
        """
        Search for products based on a query.

        Args:
        - query: The search query.

        Returns:
        - A list of products that match the query, with their name, description, category, and stock.
        - If an error occurs, returns a dictionary with the error message.
        """
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT p.name, p.description, c.name , p.stock FROM products as p JOIN categories AS c ON category=c.id WHERE p.name LIKE '%{query}%' or p.description LIKE '%{query}%' or c.name LIKE '%{query}%'")
            rows = cursor.fetchall()

            return rows
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def add_product(self, item: Product, user: str):
        """
        Add a new product to the database.

        Args:
        - item: The product to add.
        - user: The user performing the action.

        Returns:
        - A success message if the product is added successfully.
        - If an error occurs, returns a dictionary with the error message.
        """
        conn = connection()
        um = UsersManager()
        res = "Product Added Successfully"
        try:
            if self.exists(item.name): raise Exception("Product Already Exists")
            if (not conn): raise Exception("Database Connection Error")
            if item.stock <= 0: raise Exception("Stock cannot be less than one")
            if item.category < 1: raise Exception("Category cannot be less than one")

            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO products (name, description, stock, category) VALUES ('{item.name}', '{item.description}', {item.stock}, '{item.category}')")
            conn.commit()

            um.create_log(f"Product {item.name} added added", user)
        except Exception as e:
            res = {"error": str(e)}
        finally:
            conn.close()
            return res

    def update_product(self, item: Product, user: str):
        """
        Update an existing product in the database.

        Args:
        - item: The updated product.
        - user: The user performing the action.

        Returns:
        - A success message if the product is updated successfully.
        - If an error occurs, returns a dictionary with the error message.
        """
        conn = connection()
        um = UsersManager()
        res = "Product Updated Successfully"
        try:
            if not self.exists(item.name): raise Exception("Product Does Not Exist")
            if (not conn): raise Exception("Database Connection Error")
            if item.stock <= 0: raise Exception("Stock cannot be less than one")
            if item.category < 1: raise Exception("Category cannot be less than one")
            cursor = conn.cursor()
            cursor.execute(f"UPDATE products SET description = '{item.description}', stock = {item.stock}, category = '{item.category}' WHERE name = '{item.name}'")
            conn.commit()

            um.create_log(f"Product {item.name} updated", user)
        except Exception as e:
            res = {"error": str(e)}
        finally:
            conn.close()
            return res

    def delete_product(self, name: str, user: str):
        """
        Delete a product from the database.

        Args:
        - name: The name of the product to delete.
        - user: The user performing the action.

        Returns:
        - A success message if the product is deleted successfully.
        - If an error occurs, returns a dictionary with the error message.
        """
        conn = connection()
        um = UsersManager()
        res = "Product Deleted Successfully"
        try:
            if not self.exists(name): raise Exception("Product Does Not Exist")
            if (not conn): raise Exception("Database Connection Error")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM products WHERE name = '{name}'")
            conn.commit()

            um.create_log(f"Product {name} deleted", user)
        except Exception as e:
            res = {"error": str(e)}
        finally:
            conn.close()
            return res

    def exists(self, name: str):
        """
        Check if a product exists in the database.

        Args:
        - name: The name of the product to check.

        Returns:
        - True if the product exists in the database.
        - False if the product does not exist in the database.
        - If an error occurs, returns False.
        """
        conn = connection()
        try:
            if (not conn): raise Exception("Database Connection Error")
            cursor = conn.cursor()
            print(name)
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