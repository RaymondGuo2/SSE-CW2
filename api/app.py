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
    return render_template("basket.html")


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


@app.route('/add-to-cart')
def add_to_cart():  
    unique_id = request.args.get('id')
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
