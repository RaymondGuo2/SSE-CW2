from flask import Flask, render_template, request
import requests

app = Flask(__name__)


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


@app.route("/returngitname", methods=["GET", "POST"])
def returngithub():
    input_username = request.form.get("username")
    repos = []

    response = requests.get(
        f"https://api.github.com/users/{input_username}/repos"
    )

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            commits_url = repo["commits_url"].split("{")[0]
            commits_response = requests.get(commits_url)
            if commits_response.status_code == 200:
                commits = commits_response.json()
                latest_commit = commits[0] if commits else None

                repo_data = {
                    "full_name": repo["full_name"],
                    "html_url": repo["html_url"],
                    "language": repo["language"],
                    "created_at": repo["created_at"],
                    "updated_at": repo["updated_at"],
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

    return render_template(
        "returngitname.html", username=input_username, repos=repos
    )
