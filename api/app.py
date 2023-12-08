from flask import Flask, render_template, request, jsonify
import psycopg as db
import requests
import logging
import os

app = Flask(__name__, static_folder='static')


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


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/basket")
def basket():
    basket_items = session.get('cart', [])
    return render_template("basket.html", basket_items=basket_items)


@app.route("/place_order", methods=["POST"])
def place_order():
    input_name = request.form.get("name")
    input_email = request.form.get("email")
    input_message = request.form.get("message")
    return render_template(
        "thankyou.html",
        name=input_name,
        email=input_email,
        message=input_message
    )


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
        f'https://api.frankfurter.app/latest?from=USD&to={currency}'
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
    curs.execute("SELECT* FROM item ORDER BY item_id")
    unformatted_response = curs.fetchall()
    response = [
        (item[0],
         item[1].strip("'"),
         f"{item[2]:.2f}",
         item[3].strip("'"),
         str(item[4]),
         item[5].strip("'"),
         item[6].strip("'"),
         item[7])
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
    Attributes = selectAttribute(3)
    Id = Attributes[0]
    Item_Name = Attributes[1]
    Price = Attributes[2]
    Type = Attributes[3]
    Stock = Attributes[4]
    Color = Attributes[5]
    Size = Attributes[6]
    Url = Attributes[7]
    return render_template(
        "database.html",
        response=Sql,
        response_id=Id,
        response_name=Item_Name,
        response_price=Price,
        response_type=Type,
        response_stock=Stock,
        response_color=Color,
        response_size=Size,
        response_url=Url
    )


@app.route('/airforce')
def airforce():
    Attributes = selectAttribute(5)
    Id = Attributes[0]
    Item_Name = Attributes[1]
    Price = Attributes[2]
    _Type = Attributes[3]
    Stock = Attributes[4]
    Color = Attributes[5]
    Size = Attributes[6]
    Url = Attributes[7]
    return render_template(
        'airforce.html',
        ID=Id,
        item_name=Item_Name,
        price=Price,
        Type=_Type,
        stock=Stock,
        color=Color,
        size=Size,
        url=Url
    )


@app.route('/vans')
def vans():
    Attributes = selectAttribute(6)
    Id = Attributes[0]
    Item_Name = Attributes[1]
    Price = Attributes[2]
    _Type = Attributes[3]
    Stock = Attributes[4]
    Color = Attributes[5]
    Size = Attributes[6]
    Url = Attributes[7]
    return render_template(
        'vans.html',
        ID=Id,
        item_name=Item_Name,
        price=Price,
        Type=_Type,
        stock=Stock,
        color=Color,
        size=Size,
        url=Url
    )


@app.route('/blackbeanie')
def blackbeanie():
    Attributes = selectAttribute(1)
    IdM = Attributes[0]
    Item_Name = Attributes[1]
    Price = Attributes[2]
    _Type = Attributes[3]
    StockM = Attributes[4]
    Color = Attributes[5]
    SizeM = Attributes[6]
    Url = Attributes[7]
    AttributesL = selectAttribute(8)
    IdL = AttributesL[0]
    StockL = AttributesL[4]
    SizeL = AttributesL[6]
    AttributesS = selectAttribute(7)
    IdS = AttributesS[0]
    StockS = AttributesS[4]
    SizeS = AttributesS[6]
    return render_template(
        'blackbeanie.html',
        IDM=IdM,  # M
        item_name=Item_Name,
        price=Price,
        Type=_Type,
        stockM=StockM,
        color=Color,
        sizeM=SizeM,
        url=Url,
        IDL=IdL,  # L
        stockL=StockL,
        sizeL=SizeL,
        IDS=IdS,  # S
        stockS=StockS,
        sizeS=SizeS
    )


@app.route('/greenbeanie')
def greenbeanie():
    Attributes = selectAttribute(2)
    Id = Attributes[0]
    Item_Name = Attributes[1]
    Price = Attributes[2]
    _Type = Attributes[3]
    Stock = Attributes[4]
    Color = Attributes[5]
    Size = Attributes[6]
    Url = Attributes[7]
    return render_template(
        'greenbeanie.html',
        ID=Id,
        item_name=Item_Name,
        price=Price,
        Type=_Type,
        stock=Stock,
        color=Color,
        size=Size,
        url=Url
    )


@app.route('/hugojumper')
def hugojumper():
    Attributes = selectAttribute(3)
    Id = Attributes[0]
    Item_Name = Attributes[1]
    Price = Attributes[2]
    _Type = Attributes[3]
    Stock = Attributes[4]
    Color = Attributes[5]
    Size = Attributes[6]
    Url = Attributes[7]
    return render_template(
        'hugojumper.html',
        ID=Id,
        item_name=Item_Name,
        price=Price,
        Type=_Type,
        stock=Stock,
        color=Color,
        size=Size,
        url=Url
    )


@app.route('/uniqlojumper')
def uniqlojumper():
    Attributes = selectAttribute(4)
    Id = Attributes[0]
    Item_Name = Attributes[1]
    Price = Attributes[2]
    _Type = Attributes[3]
    Stock = Attributes[4]
    Color = Attributes[5]
    Size = Attributes[6]
    Url = Attributes[7]
    return render_template(
        'uniqlojumper.html',
        ID=Id,
        item_name=Item_Name,
        price=Price,
        Type=_Type,
        stock=Stock,
        color=Color,
        size=Size,
        url=Url
    )


"""
def process_query(query):
    return search_results
"""


@app.route('/add-to-cart')
def add_to_cart():
    unique_id = request.args.get('id')
    quantity = int(request.args.get('quantity'))
    size = request.args.get('size')

    product_name, price = get_product_details(unique_id) 

    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({'product_id':unique_id, 'product_name':product_name, 'size': size, 'quantity':quantity, 'price':price})
    return jsonify({"status": "success", "id": unique_id})


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if query == "What is your name?":
        return "SSE_LEGENDS"
    if "plus" in query:
        return add(query)
    if "multiplied" in query:
        return multiply(query)
    if "minus" in query:
        return subtract(query)
    else:
        return "Unknown"


def add(query):
    numbers = []
    current_number = ""
    for char in query:
        if char.isdigit():
            current_number += char
        elif current_number:
            numbers.append(int(current_number))
            current_number = ""
    if current_number:
        numbers.append(int(current_number))

    num1 = numbers[0]
    num2 = numbers[1]
    result = num1 + num2
    return str(result)


def multiply(query):
    numbers = []
    current_number = ""
    for char in query:
        if char.isdigit():
            current_number += char
        elif current_number:
            numbers.append(int(current_number))
            current_number = ""
    if current_number:
        numbers.append(int(current_number))

    num1 = numbers[0]
    num2 = numbers[1]
    result = num1 * num2
    return str(result)


def subtract(query):
    numbers = []
    current_number = ""
    for char in query:
        if char.isdigit():
            current_number += char
        elif current_number:
            numbers.append(int(current_number))
            current_number = ""
    if current_number:
        numbers.append(int(current_number))

    num1 = numbers[0]
    num2 = numbers[1]
    result = num1 - num2
    return str(result)


@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("q")
    result = process_query(query)
    return result


@app.route("/githubuname")
def githubuname():
    return render_template("githubuname.html")


logging.basicConfig(level=logging.INFO)


def get_commit_counts(owner, repo):
    commit_count = 0
    page = 1
    while True:
        response = (
            requests.get(
                f"https://api.github.com/repos/{owner}/{repo}/commits",
                params={'per_page': 100, 'page': page}
            )
            )
        commits = response.json()
        commit_count += len(commits)
        if 'next' not in response.links:
            break
        page += 1
    return commit_count


@app.route("/returngitname", methods=["GET", "POST"])
def returngithub():
    input_username = request.form.get("username")
    repos = []
    repo_names = []
    error_message = None

    try:
        response = requests.get(
            f"https://api.github.com/users/{input_username}/repos"
        )
        response.raise_for_status()

        repos_json = response.json()
        for repo in repos_json:
            commits_url = repo["commits_url"].split("{")[0]
            commits_response = requests.get(commits_url)
            commits_response.raise_for_status()

            repo_name = repo["name"]
            commit_counts = get_commit_counts(input_username, repo_name)

            commits = commits_response.json()
            latest_commit = commits[0] if commits else None

            repo_data = {
                "repo_name": repo["name"],
                "full_name": repo["full_name"],
                "html_url": repo["html_url"],
                "language": repo["language"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "commit_counts": commit_counts,
                "latest_commit": {
                    "hash": (
                        latest_commit["sha"]
                        if latest_commit
                        else "N/A"
                    ),
                    "author": (
                        latest_commit["commit"]["author"]["name"]
                        if latest_commit
                        else "N/A"
                    ),
                    "date": (
                        latest_commit["commit"]["author"]["date"]
                        if latest_commit
                        else "N/A"
                    ),
                    "message": (
                        latest_commit["commit"]["message"]
                        if latest_commit
                        else "N/A"
                    ),
                },
            }
            repos.append(repo_data)
            repo_names.append(repo_name)
    except requests.RequestException as req_err:
        logging.error(
            f"HTTP request error for user {input_username}: {req_err}"
        )
        error_message = (
            "Failed to fetch repositories. "
            "Please try again later."
        )

    if error_message:
        return render_template("error.html", error_message=error_message), 500

    return render_template(
        "returngitname.html",
        username=input_username,
        repos=repos,
        repo_names=repo_names
    )


"""
app.run(debug=True)
"""
