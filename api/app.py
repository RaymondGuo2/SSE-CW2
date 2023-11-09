from flask import Flask, render_template, request
from datetime import datetime
import requests
import logging
import base64
from io import BytesIO
import matplotlib.pyplot as plt

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


def get_commit_dates(owner, repo):
    commit_dates = []
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/commits",
            params={'page': page}
        )
        response.raise_for_status()
        commits = response.json()
        if not commits:
            break
        for commit in commits:
            commit_date = datetime.strptime(
                commit['commit']['author']['date'],
                '%Y-%m-%dT%H:%M:%SZ'
            )
            commit_dates.append(commit_date)
        page += 1
    return commit_dates


def get_commit_counts(owner, repo):
    commit_dates = get_commit_dates(owner, repo)
    commit_counts = list(range(1, len(commit_dates) + 1))
    return commit_counts


def generate_commit_activity_plot(commit_dates, commit_counts):
    # Assume commit_dates is a list of datetime objects
    if not commit_dates:
        return None

    plt.figure(figsize=(10, 4))
    plt.plot(commit_dates, commit_counts, marker='o')
    plt.title('Commit Activity')
    plt.xlabel('Date')
    plt.ylabel('Number of Commits')
    plt.tight_layout()

    png_image = BytesIO()
    plt.savefig(png_image, format='png')
    plt.close()

    png_image.seek(0)
    base64_string = base64.b64encode(png_image.read()).decode('utf-8')

    return base64_string


@app.route("/returngitname", methods=["GET", "POST"])
def returngithub():
    input_username = request.form.get("username")
    repos = []
    # commit_counts = []
    # commit_dates = []
    error_message = None

    try:
        response = requests.get(
            f"https://api.github.com/users/{input_username}/repos"
        )
        response.raise_for_status()

        repos_json = response.json()
        for repo in repos_json:

            repo_name = repo["name"]

            commits_url = repo["commits_url"].split("{")[0]
            commits_response = requests.get(commits_url)
            commits_response.raise_for_status()
            commits = commits_response.json()
            latest_commit = commits[0] if commits else None

            try:
                commit_dates = get_commit_dates(input_username, repo_name)
                commit_counts = get_commit_counts(commit_dates)
                commit_activity_plot = generate_commit_activity_plot(
                    commit_dates, commit_counts
                 )
            except Exception as e:
                    logging.error(f"Error processing repo '{repo_name}': {e}")
                    commit_activity_plot = None

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
                "commit_activity": {
                    "dates": commit_dates,
                    "counts": commit_counts
                },
                "commit_activity_plot": commit_activity_plot,
                "total_commits": len(commit_dates) if commit_dates else 0
            }
            repos.append(repo_data)
            # commit_counts.append(indv_commit_counts)
            # commit_dates.append(indv_commit_dates)
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
        # commit_counts=commit_counts,
        # commit_dates=commit_dates
    )
