from flask import Flask, render_template, request
import psycopg as db
import configparser
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


""" @app.route("/search")
def search():
    query = request.args.get("query")
    search_results = process_query(query)
    return render_template("search_results.html", results=search_results)
"""

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
"""


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/hat")
def hat_page():
    return render_template("hat.html")


@app.route("/shoes")
def shoes_page():
    return render_template("shoes.html")


@app.route("/jumper")
def jumper_page():

    return render_template("jumper.html")


config = configparser.ConfigParser()
config.read('dbtool.ini')


def testSQL():
    DBNAME = os.environ.get('DBNAME')
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    CLIENT_ENCODING = os.getenv('CLIENT_ENCODING')
    server_params = {'dbname': DBNAME,
                     'host': HOST,
                     'port': PORT,
                     'user': USER,
                     'password': PASSWORD,
                     'client_encoding': CLIENT_ENCODING}
    conn = db.connect(**server_params)
    curs = conn.cursor()
    curs.execute(config['query']['bigPopulation'],
                 [config['default']['bigPopulation']])
    response = ('There are %d big countries' % curs.rowcount)
    conn.close()
    print(DBNAME)
    print(HOST)
    print(PORT)
    print(USER)
    print(PASSWORD)
    print(CLIENT_ENCODING)
    return response


"""
testSQL()
"""


@app.route("/database")
def database_page():
    responsesql = testSQL()
    return render_template("database.html", response=responsesql)


"""
def process_query(query):
    return search_results
"""


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
app.run(debug=False)
"""
