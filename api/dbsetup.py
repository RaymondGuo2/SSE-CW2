import psycopg as db
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
load_dotenv()


def setupTableItem():
    DBNAME = os.environ.get('DBNAME')
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    CLIENT_ENCODING = os.environ.get('CLIENT_ENCODING')
    server_params = {'dbname': DBNAME,
                     'host': HOST,
                     'port': PORT,
                     'user': USER,
                     'password': PASSWORD,
                     'client_encoding': CLIENT_ENCODING}
    conn = db.connect(**server_params)
    curs = conn.cursor()
    curs.execute("""
CREATE TABLE item (
item_id SERIAL PRIMARY KEY,
item_name VARCHAR(20) NOT NULL,
price DECIMAL(10,2) NOT NULL,
type VARCHAR(20) NOT NULL,
stock INTEGER NOT NULL,
color VARCHAR(20) NOT NULL,
size VARCHAR(2) NOT NULL
)
""")
    conn.commit()
    conn.close()
    print("Item Table Setup Complete")


def insertItem(
        name: str,
        price: int,
        itemType: str,
        stock: int,
        color: str,
        size: str):
    DBNAME = os.environ.get('DBNAME')
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    CLIENT_ENCODING = os.environ.get('CLIENT_ENCODING')
    server_params = {'dbname': DBNAME,
                     'host': HOST,
                     'port': PORT,
                     'user': USER,
                     'password': PASSWORD,
                     'client_encoding': CLIENT_ENCODING}
    conn = db.connect(**server_params)
    curs = conn.cursor()
    curs.execute("""
INSERT INTO item (item_name, price, type, stock, color, size)
VALUES (%s, %s, %s, %s, %s, %s)
""", (name, price, itemType, stock, color, size))
    conn.commit()
    conn.close()
    print("Item Added to Item Table: ", (name))


def setupDB():
    setupTableItem()
    insertItem('Black Beanie', 12, 'Hat', 10, 'Black', 'M')
    insertItem('Green Beanie', 12, 'Hat', 10, 'Green', 'M')
    insertItem('Hugo Boss Jumper', 60, 'Jumper', 10, 'Grey', 'M')
    insertItem('Uniqlo Jumper', 40, 'Jumper', 10, 'Green', 'M')
    insertItem('Air Force 1s', 60, 'Shoe', 10, 'White', '11')
    insertItem('Vans', 50, 'Shoe', 10, 'Black', '11')
    print('Full Setup Complete')


setupDB()
