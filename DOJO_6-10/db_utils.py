''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
import mysql.connector as mysql                   # Used for interacting with the MySQL database
import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
import bcrypt
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
load_dotenv()                 # Read in the environment variables for MySQL
db_config = {
    "host": os.environ['MYSQL_HOST'],
    "user": os.environ['MYSQL_USER'],
    "password": os.environ['MYSQL_PASSWORD'],
    "database": os.environ['MYSQL_DATABASE']
}
session_config = {
    'session_key': os.environ['SESSION_KEY']
}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations
# CREATE SQL query
def create_user(username:str, password:str, email:str, first_name:str, last_name:str) -> int:
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db = mysql.connect(**db_config)
    cursor = db.cursor()
    query = "insert into users (username, hashed_password, email, first_name, last_name) values (%s, %s, %s, %s, %s)"
    values = (username, password, email, first_name, last_name)
    try:
        cursor.execute(query, values)
        db.commit()
    finally:

        db.close()
        return cursor.lastrowid

# SELECT SQL query
def select_users(user_id:int=None) -> list:
    db = mysql.connect(**db_config)
    cursor = db.cursor()
    if user_id == None:
        query = f"select id, username, email, first_name, last_name from users;"
        cursor.execute(query)
        result = cursor.fetchall()
    else:
        query = f"select id, username, email, first_name, last_name from users where id={user_id};"
        cursor.execute(query)
        result = cursor.fetchone()
    db.close()
    return result

# UPDATE SQL query
def update_user(user_id:int, username:str, password:str, email:str) -> bool:
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db = mysql.connect(**db_config)
    cursor = db.cursor()
    query = "update users set username=%s, hashed_password=%s, email=%s where id=%s;"
    values = (username, password, email, user_id)
    cursor.execute(query, values)
    db.commit()
    db.close()
    return True if cursor.rowcount == 1 else False

# DELETE SQL query
def delete_user(user_id:int) -> bool:
    db = mysql.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f"delete from users where id={user_id};")
    db.commit()
    db.close()
    return True if cursor.rowcount == 1 else False

# SELECT query to verify hashed password of users
def check_user_password(username:str, password:str) -> bool:
    db = mysql.connect(**db_config)
    cursor = db.cursor()
    query = 'select hashed_password from users where username=%s'
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if result is not None:
        return bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8'))
    return False

def get_user_id(username: str) -> int:
    db = mysql.connect(**db_config)
    cursor = db.cursor()
    query = 'select id from users where username=%s'
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result is not None:
        return result[0]
    else:
        return 0