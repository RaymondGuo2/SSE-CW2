import psycopg as db
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
load_dotenv()


def connectDB():
    try:
        DBNAME = os.environ.get('DBNAME')
        HOST = os.environ.get('HOST')
        PORT = os.environ.get('PORT')
        USER = os.environ.get('USER')
        PASSWORD = os.environ.get('PASSWORD')
        CLIENT_ENCODING = os.environ.get('CLIENT_ENCODING')

        server_params = {
            'dbname': DBNAME,
            'host': HOST,
            'port': PORT,
            'user': USER,
            'password': PASSWORD,
            'client_encoding': CLIENT_ENCODING
        }

        conn = db.connect(**server_params)
        curs = conn.cursor()

    except db.Error as e:
        print(f"Error connecting to the database: {e}")
        conn = None
        curs = None

    finally:
        return conn, curs


def setupTableItem():
    conn, curs = connectDB()
    curs.execute("""
CREATE TABLE item (
item_id SERIAL PRIMARY KEY,
item_name VARCHAR(50) NOT NULL,
price NUMERIC(10,2) NOT NULL,
type VARCHAR(20) NOT NULL,
stock INTEGER NOT NULL,
color VARCHAR(20) NOT NULL,
size VARCHAR(2) NOT NULL,
url VARCHAR(400) NOT NULL,
link VARCHAR(400) NOT NULL
)
""")
    conn.commit()
    conn.close()
    print("Item Table Setup Complete")


def insertItem(
        name: str,
        price: float,
        itemType: str,
        stock: int,
        color: str,
        size: str,
        url: str,
        link: str):
    conn, curs = connectDB()
    curs.execute("""
INSERT INTO item (item_name, price, type, stock, color, size, url, link)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (name, price, itemType, stock, color, size, url, link))
    conn.commit()
    conn.close()
    print("Item Added to Item Table: ", (name), " Size: ", (size))


def setupDB():
    setupTableItem()
    insertItem('Northface Black Beanie',
               12,
               'Hat',
               0,
               'Black',
               'M',
               'https://www.footasylum.com/images/products/medium/127357.jpg',
               'blackbeanie')
    insertItem('Northface Green Beanie',
               12,
               'Hat',
               10,
               'Green',
               'M',
               ('https://i.pinimg.com/736x/45/'
                '98/86/4598863f4b9d99b8c26cdc1684a36466.jpg'),
               'greenbeanie')
    insertItem('Hugo Boss Jumper',
               60,
               'Jumper',
               10,
               'Grey',
               'M',
               ('https://brandrunner.co.uk/wp-content/uploads/2021/01/'
                'Hugo-Boss-Jumper-Boys-1.jpg'),
               'hugojumper')
    insertItem('Uniqlo Jumper',
               40,
               'Jumper',
               10,
               'Green',
               'M',
               ('https://www.uniqlo.com/jp/ja/contents/feature/masterpiece/'
                'common_22fw/img/item_12_01.jpg'),
               'uniqlojumper')
    insertItem('Air Force 1s',
               60,
               'Shoe',
               10,
               'White',
               '11',
               ('https://d2ob0iztsaxy5v.cloudfront.net/product/270104/'
                '2701041020_zm.jpg'),
               'airforce')
    insertItem('Vans',
               50,
               'Shoe',
               10,
               'Black',
               '11',
               ('https://i8.amplience.net/t/jpl/sz_product_list?plu=sz_'
                '284146_a&qlt=85&qlt=92&w=363&h=281&v=1&fmt'
                '=auto&fmt=auto'),
               'vans')
    insertItem('Northface Black Beanie',
               12,
               'Hat',
               8,
               'Black',
               'S',
               'https://www.footasylum.com/images/products/medium/127357.jpg',
               'blackbeanie')
    insertItem('Northface Black Beanie',
               12,
               'Hat',
               15,
               'Black',
               'L',
               'https://www.footasylum.com/images/products/medium/127357.jpg',
               'blackbeanie')
    insertItem('Air Force 1s',
               60,
               'Shoe',
               4,
               'White',
               '3',
               ('https://d2ob0iztsaxy5v.cloudfront.net/product/270104/'
                '2701041020_zm.jpg'),
               'airforce')
    insertItem('Air Force 1s',
               60,
               'Shoe',
               6,
               'White',
               '5',
               ('https://d2ob0iztsaxy5v.cloudfront.net/product/270104/'
                '2701041020_zm.jpg'),
               'airforce')
    insertItem('Air Force 1s',
               60,
               'Shoe',
               7,
               'White',
               '7',
               ('https://d2ob0iztsaxy5v.cloudfront.net/product/270104/'
                '2701041020_zm.jpg'),
               'airforce')
    insertItem('Air Force 1s',
               60,
               'Shoe',
               8,
               'White',
               '9',
               ('https://d2ob0iztsaxy5v.cloudfront.net/product/270104/'
                '2701041020_zm.jpg'),
               'airforce')
    insertItem('Vans',
               50,
               'Shoe',
               10,
               'Black',
               '3',
               ('https://i8.amplience.net/t/jpl/sz_product_list?plu=sz_'
                '284146_a&qlt=85&qlt=92&w=363&h=281&v=1&fmt'
                '=auto&fmt=auto'),
               'vans')
    insertItem('Vans',
               50,
               'Shoe',
               10,
               'Black',
               '5',
               ('https://i8.amplience.net/t/jpl/sz_product_list?plu=sz_'
                '284146_a&qlt=85&qlt=92&w=363&h=281&v=1&fmt'
                '=auto&fmt=auto'),
               'vans')
    insertItem('Vans',
               50,
               'Shoe',
               10,
               'Black',
               '7',
               ('https://i8.amplience.net/t/jpl/sz_product_list?plu=sz_'
                '284146_a&qlt=85&qlt=92&w=363&h=281&v=1&fmt'
                '=auto&fmt=auto'),
               'vans')
    insertItem('Vans',
               50,
               'Shoe',
               10,
               'Black',
               '9',
               ('https://i8.amplience.net/t/jpl/sz_product_list?plu=sz_'
                '284146_a&qlt=85&qlt=92&w=363&h=281&v=1&fmt'
                '=auto&fmt=auto'),
               'vans')
    insertItem('Northface Green Beanie',
               12,
               'Hat',
               10,
               'Green',
               'S',
               ('https://i.pinimg.com/736x/45/'
                '98/86/4598863f4b9d99b8c26cdc1684a36466.jpg'),
               'greenbeanie')
    insertItem('Northface Green Beanie',
               12,
               'Hat',
               10,
               'Green',
               'L',
               ('https://i.pinimg.com/736x/45/'
                '98/86/4598863f4b9d99b8c26cdc1684a36466.jpg'),
               'greenbeanie')
    insertItem('Hugo Boss Jumper',
               60,
               'Jumper',
               10,
               'Grey',
               'S',
               ('https://brandrunner.co.uk/wp-content/uploads/2021/01/'
                'Hugo-Boss-Jumper-Boys-1.jpg'),
               'hugojumper')
    insertItem('Hugo Boss Jumper',
               60,
               'Jumper',
               10,
               'Grey',
               'L',
               ('https://brandrunner.co.uk/wp-content/uploads/2021/01/'
                'Hugo-Boss-Jumper-Boys-1.jpg'),
               'hugojumper')
    insertItem('Uniqlo Jumper',
               40,
               'Jumper',
               10,
               'Green',
               'S',
               ('https://www.uniqlo.com/jp/ja/contents/feature/masterpiece/'
                'common_22fw/img/item_12_01.jpg'),
               'uniqlojumper')
    insertItem('Uniqlo Jumper',
               40,
               'Jumper',
               10,
               'Green',
               'L',
               ('https://www.uniqlo.com/jp/ja/contents/feature/masterpiece/'
                'common_22fw/img/item_12_01.jpg'),
               'uniqlojumper')
    print('Full Setup Complete')


setupDB()
