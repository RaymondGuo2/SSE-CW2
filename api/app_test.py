from app import app as flask_app
from app import process_query


def app():
    yield flask_app


def client(app):
    return app.test_client()


def home_page_test(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Expected content on home page" in response.data


def form_test(client):
    response = client.post("/submit", data={
        "name": "Alan Smith",
        "email": "asmith@gmail.com",
        "message": "Fantastic Service!"
    })
    assert response.status_code == 200
    assert b"Expected response" in response.data


def basket_test(client):
    with client.session_transaction() as se:
        se['cart'] = [{'itemName': 'Adidas', 'quantity': 2, 'price': 10}]
    response = client.get("/basket")
    assert response.status_code == 200
    assert b"Adidas" in response.data


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == (
        "Dinosaurs ruled the Earth 200 million years ago"
    )
