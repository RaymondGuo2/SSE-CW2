from flask import Flask, render_template, request

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
    else:
        return "Unknown"


def add(query):
    words = query.split()
    index_plus = words.index("plus")
    num1 = int(words[index_plus - 1])
    num2 = int(words[index_plus + 1])
    result = num1 + num2
    result = str(result)
    return result


@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("q")
    result = process_query(query)
    return result
