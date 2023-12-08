from flask import Flask, render_template, request, jsonify, redirect, session
import psycopg as db
import requests
import logging
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__, static_folder='static')

dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
load_dotenv()

app.secret_key = os.environ.get('FLASK_SECRET_KEY')

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_email = request.form.get("email")
    input_address = request.form.get("address")
    return render_template(
        "form.html", name=input_name, email=input_email, address=input_address
    )


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/basket")
def basket():
    cart_items = session.get('cart', [])
    return render_template("basket.html", basket_items=cart_items)



""" @app.route("/search")
def search():
    query = request.args.get("query")
    search_results = process_query(query)
    return render_template("search_results.html", results=search_results)
"""


@app.route('/convert_currency')
def convert_currency():
    original_price = float(request.args.get('price'))
    currency = request.args.get('currency')

    response = requests.get(
        'https://api.frankfurter.app/latest?from=USD&to={currency}'
    )
    data = response.json()
    exchange_rate = data['rates'][currency]

    converted_price = original_price * exchange_rate
    return jsonify(convertedPrice=converted_price)


@app.route("/contact")
def contact_page():
    return render_template("contact.html", api_key=os.environ.get(
        'GOOGLE_MAPS_API_KEY'))


@app.route("/hat")
def hat_page():
    return render_template("hat.html")


@app.route("/shoes")
def shoes_page():
    return render_template("shoes.html")


@app.route("/jumper")
def jumper_page():
    return render_template("jumper.html")


def connectDB():
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
    return conn, curs


def dbQuery():
    conn, curs = connectDB()
    curs.execute("SELECT* FROM item ORDER BY item_id")
    unformatted_response = curs.fetchall()
    response = [
        (item[0],
         item[1].strip("'"),
         f"{item[2]:.2f}",
         item[3].strip("'"),
         str(item[4]),
         item[5].strip("'"),
         item[6].strip("'"))
        for item in unformatted_response
    ]
    conn.close()
    return response


def reduceStock(itemID: int, reduceBy: int):
    conn, curs = connectDB()
    curs.execute("""
        UPDATE item
        SET stock = GREATEST(stock - %s, 0)
        WHERE item_id = %s
    """, (reduceBy, itemID))
    conn.commit()
    conn.close


def selectAttribute(itemID: int, attribute: str):
    # attribute = "item_name", "price", "type", "stock", "color", "size"
    conn, curs = connectDB()
    curs.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'item'
        """)
    columnNames = [row[0] for row in curs.fetchall()]
    if attribute not in columnNames:
        raise ValueError("Invalid Attribute")
    curs.execute("""
        SELECT {attribute}
        FROM item
        WHERE item_id = %s
    """.format(attribute=attribute), (itemID,))
    unformatted_response = curs.fetchone()
    if unformatted_response:
        unformatted_response = unformatted_response[0]
        if attribute == "price":
            response = f"{unformatted_response:.2f}"
        elif attribute in ["stock", "item_id"]:
            response = int(unformatted_response)
        else:
            response = unformatted_response.strip("'")
    else:
        response = "Attribute Not Found"
    conn.close()
    return response


@app.route("/database")
def database_page():
    Sql = dbQuery()
    Name = selectAttribute(3, "item_name")
    Price = selectAttribute(3, "price")
    Type = selectAttribute(3, "type")
    Stock = selectAttribute(3, "stock")
    Color = selectAttribute(3, "color")
    Size = selectAttribute(3, "size")
    reduceStock(3, 1)
    return render_template(
        "database.html",
        response=Sql,
        response_name=Name,
        response_price=Price,
        response_type=Type,
        response_stock=Stock,
        response_color=Color,
        response_size=Size
    )


@app.route('/airforce')
def airforce():
    return render_template('airforce.html')


@app.route('/vans')
def vans():
    return render_template('vans.html')


@app.route('/blackbeanie')
def blackbeanie():
    return render_template('blackbeanie.html')


@app.route('/greenbeanie')
def greenbeanie():
    return render_template('greenbeanie.html')


@app.route('/hugojumper')
def hugojumper():
    return render_template('hugojumper.html')


@app.route('/uniqlojumper')
def uniqlojumper():
    Stock = selectAttribute(3, "stock")
    return render_template(
        'uniqlojumper.html',
        stock=Stock
    )


"""
def process_query(query):
    return search_results
"""


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json

    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(data)
    session.modified = True
    return jsonify(success=True)



"""
app.run(debug=True)
"""
