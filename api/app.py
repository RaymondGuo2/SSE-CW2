from flask import Flask, render_template, request, jsonify, session
import psycopg as db
import requests
import os
import json
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__, static_folder='static')

dotenv_path = find_dotenv(filename='.env')
load_dotenv()

secret_key = os.urandom(24)
app.secret_key = secret_key


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_email = request.form.get("email")
    input_message = request.form.get("message")
    return render_template(
        "form.html", name=input_name, email=input_email, message=input_message
    )


@app.route("/basket")
def basket():
    cart_items = session.get('cart', [])
    return render_template("basket.html", basket_items=cart_items)


def send_simple_message(to_email, name, address):
    mail_api_key = os.environ.get('mailAPIKEY2')
    email_subject = f"Thank You for Your Order, {name}!"
    email_body = (
        f"Dear {name},\n\n"
        "Thank you for your order! It will be shipped to: "
        f"{address}.\n\nBest regards,\nYour Team"
    )

    return requests.post(
        "https://api.eu.mailgun.net/v3/notesqa.com/messages",
        auth=("api", mail_api_key),
        data={
            "from": "Excited User <mailgun@notesqa.com>",
            "to": [to_email],
            "subject": email_subject,
            "text": email_body
        })


@app.route("/search")
def search():
    query = request.args.get("query")
    search_results = search_db(query)
    return render_template(
        "searchresults.html",
        response=search_results,
        query=query
    )


def search_db(search_query):
    if not search_query:
        return []

    conn, curs = connectDB()
    curs.execute("""
    SELECT DISTINCT ON (item_name) *
    FROM item
    WHERE item_name ILIKE %s
    """, ('%' + search_query + '%',)
    )

    response = curs.fetchall()
    conn.close()
    return response


@app.route('/convert_currency')
def convert_currency():
    original_price = float(request.args.get('price'))
    currency = request.args.get('currency')

    response = requests.get(
        f'https://api.frankfurter.app/latest?from=GBP&to={currency}'
    )
    data = response.json()

    if currency in data['rates']:
        exchange_rate = data['rates'][currency]
        converted_price = original_price * exchange_rate
        return jsonify(convertedPrice=converted_price)
    else:
        return jsonify(error="Currency not found"), 404


@app.route("/contact")
def contact_page():
    return render_template("contact.html", api_key=os.environ.get(
        'GOOGLE_MAPS_API_KEY'))


@app.route("/hat")
def hat_page():
    bbAttributes = selectAttribute(1)
    gbAttributes = selectAttribute(2)
    return render_template(
        "hat.html",
        bb_attributes=bbAttributes,
        gb_attributes=gbAttributes
    )


@app.route("/shoes")
def shoes_page():
    afAttributes = selectAttribute(5)
    vAttributes = selectAttribute(6)
    return render_template(
        "shoes.html",
        af_attributes=afAttributes,
        v_attributes=vAttributes
    )


@app.route("/jumper")
def jumper_page():
    hbjAttributes = selectAttribute(3)
    ujAttributes = selectAttribute(4)
    return render_template(
        "jumper.html",
        hbj_attributes=hbjAttributes,
        uj_attributes=ujAttributes
    )


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
    curs.execute("SELECT* FROM item ORDER BY  item_name, size DESC")
    unformatted_response = curs.fetchall()
    response = [
        (
         item[0].strip("'"),
         item[1].strip("'"),
         f{item[2]:.2f},
         item[3].strip("'"),
         str(item[4]),
         item[5].strip("'"),
         item[6].strip("'"),
         item[7].strip("'")
        )
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
    conn.close()


def selectAttribute(itemID: int):
    # attribute = "item_name" "price" "type" "stock" "color" "size" "url"
    conn, curs = connectDB()
    curs.execute("""
        SELECT COUNT(*)
        FROM item
        """)
    MaxId = int(curs.fetchone()[0])
    if itemID < 0 or itemID > MaxId:
        raise ValueError("Invalid Item ID")
    curs.execute("""
        SELECT *
        FROM item
        WHERE item_id = %s
    """, (itemID,))
    _r = curs.fetchone()
    response = [
        _r[0],
        _r[1].strip("'"),
        f"{_r[2]:.2f}",
        _r[3].strip("'"),
        str(_r[4]),
        _r[5].strip("'"),
        _r[6].strip("'"),
        _r[7]
    ]
    conn.close()
    return response


@app.route("/database")
def database_page():
    Sql = dbQuery()
    return render_template(
        "database.html",
        response=Sql,
    )


@app.route('/airforce')
def airforce():
    _3_Attributes = selectAttribute(9)
    _5_Attributes = selectAttribute(10)
    _7_Attributes = selectAttribute(11)
    _9_Attributes = selectAttribute(12)
    _11_Attributes = selectAttribute(5)
    return render_template(
        'airforce.html',
        _3_attributes=_3_Attributes,
        _5_attributes=_5_Attributes,
        _7_attributes=_7_Attributes,
        _9_attributes=_9_Attributes,
        _11_attributes=_11_Attributes
    )


@app.route('/vans')
def vans():
    _3_Attributes = selectAttribute(13)
    _5_Attributes = selectAttribute(14)
    _7_Attributes = selectAttribute(15)
    _9_Attributes = selectAttribute(16)
    _11_Attributes = selectAttribute(6)
    return render_template(
        'vans.html',
        _3_attributes=_3_Attributes,
        _5_attributes=_5_Attributes,
        _7_attributes=_7_Attributes,
        _9_attributes=_9_Attributes,
        _11_attributes=_11_Attributes
    )


@app.route('/blackbeanie')
def blackbeanie():
    _M_Attributes = selectAttribute(1)
    _S_Attributes = selectAttribute(7)
    _L_Attributes = selectAttribute(8)
    return render_template(
        'blackbeanie.html',
        _S_attributes=_S_Attributes,
        _M_attributes=_M_Attributes,
        _L_attributes=_L_Attributes
    )


@app.route('/greenbeanie')
def greenbeanie():
    _M_Attributes = selectAttribute(2)
    _S_Attributes = selectAttribute(17)
    _L_Attributes = selectAttribute(18)
    return render_template(
        'greenbeanie.html',
        _S_attributes=_S_Attributes,
        _M_attributes=_M_Attributes,
        _L_attributes=_L_Attributes
    )


@app.route('/hugojumper')
def hugojumper():
    _M_Attributes = selectAttribute(3)
    _S_Attributes = selectAttribute(19)
    _L_Attributes = selectAttribute(20)
    return render_template(
        'hugojumper.html',
        _S_attributes=_S_Attributes,
        _M_attributes=_M_Attributes,
        _L_attributes=_L_Attributes
    )


@app.route('/uniqlojumper')
def uniqlojumper():
    _M_Attributes = selectAttribute(4)
    _S_Attributes = selectAttribute(21)
    _L_Attributes = selectAttribute(22)
    return render_template(
        'uniqlojumper.html',
        _S_attributes=_S_Attributes,
        _M_attributes=_M_Attributes,
        _L_attributes=_L_Attributes
    )


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json

    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(data)
    session.modified = True
    return jsonify(success=True)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/thankyou", methods=["POST"])
def place_order():
    input_name = request.form.get("name")
    input_email = request.form.get("email")
    input_address = request.form.get("address")

    # Call the function to send an email
    response = send_simple_message(input_email, input_name, input_address)

    # Handle the email response (Optional)
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Email sending failed. Status code:", response.status_code)

    basket_items_json = request.form.get("basketItems")
    basket_items = json.loads(basket_items_json)
    for item in basket_items:
        reduceStock(item['itemId'], item['quantity'])

    return render_template(
        "thankyou.html",
        name=input_name,
        email=input_email,
        address=input_address
    )
