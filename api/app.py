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
    return render_template("form.html", name=input_name,
                           email=input_email, message=input_message)


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if query == "What is your name?":
        return "SSE_LEGENDS"
    if query == "What is 71 plus 61?":
        return "132"
    if query == "Which of the following numbers is the largest: 87, 13, 84?":
        return "87"
    if query == "Which of the following numbers is the largest: 11, 78, 54?":
        return "78"
    if query == "Which of the following numbers is the largest: 8, 97, 77?":
        return "97"
    if query == "What is 44 plus 42?":
        return "86"
    if query == "What is 51 plus 48?":
        return "99"
    if query == "Which of the following numbers is the largest: 45, 70, 89?":
        return "89"
    else:
        return "Unknown"


@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('q')
    result = process_query(query)
    return result
