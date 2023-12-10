from app import app as flask_app


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


def form_test(client):
    response = client.post("/thankyou", data={
        "name": "Alan Smith",
        "email": "asmith@gmail.com",
        "message": "Fantastic Service!"
    })
    assert response.status_code == 200
    assert b"Expected response" in response.data


def search_test(client):
    search_query = "shoes"
    response = client.get(f"/search?query={search_query}")
    assert response.status_code == 200
    assert search_query.encode() in response.data


def currency_convert_test(client):
    original_price = "10"
    currency = "GBP"
    response = client.get(f"/convert_currency?price={original_price}&currency={currency}")
    assert response.status_code == 200
    assert "Price converted" in response.json

