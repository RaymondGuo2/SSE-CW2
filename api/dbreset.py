import psycopg as db
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
load_dotenv()


def resetTableItem():
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
        curs.execute("DELETE FROM item")
        curs.execute("DROP TABLE item")
        conn.commit()
        print("All Rows Deleted")
        print("Item Table Deleted")

    except db.Error as e:
        print(f"Error connecting to the database: {e}")

    finally:
        conn.close()


resetTableItem()
