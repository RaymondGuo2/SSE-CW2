import psycopg as db
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
load_dotenv()

def resetTableItem():
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
    curs.execute("DELETE FROM item")
    curs.execute("DROP TABLE item")
    conn.commit()
    conn.close()
    print(DBNAME)
    print(HOST)
    print(PORT)
    print(USER)
    print(PASSWORD)
    print(CLIENT_ENCODING)


resetTableItem()
