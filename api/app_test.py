from app import app as flask_app, dbQuery, reduceStock, selectAttribute


def app():
    flask_app.config['TESTING'] = True
    return flask_app


def client(app):
    return app.test_client()


def home_page_test(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Expected content on home page" in response.data


def shoes_page_test(client):
    response = client.get("/shoes")
    assert response.status_code == 200


def hats_page_test(client):
    response = client.get("/hat")
    assert response.status_code == 200


def jumper_page_test(client):
    response = client.get("/jumper")
    assert response.status_code == 200


def airforce_page_test(client):
    response = client.get("/airforce")
    assert response.status_code == 200


def vans_page_test(client):
    response = client.get("/vans")
    assert response.status_code == 200


def uniqlojumper_page_test(client):
    response = client.get("/uniqlojumper")
    assert response.status_code == 200


def hugoboss_page_test(client):
    response = client.get("/hugojumper")
    assert response.status_code == 200


def greenbeanie_page_test(client):
    response = client.get("/greenbeanie")
    assert response.status_code == 200


def blackbeanie_page_test(client):
    response = client.get("/blackbeanie")
    assert response.status_code == 200


def contact_page_test(client):
    response = client.get("/contact")
    assert response.status_code == 200


def basket_page_test(client):
    response = client.get("/basket")
    assert response.status_code == 200


def checkout_page_test(client):
    response = client.get("/checkout")
    assert response.status_code == 200


def database_page_test(client):
    response = client.get("/database")
    assert response.status_code == 200


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


def search_test(client):
    search_query = "shoes"
    response = client.get(f"/search?query={search_query}")
    assert response.status_code == 200
    assert search_query.encode() in response.data


def currency_convert_test(client):
    original_price = "10"
    currency = "GBP"
    response = client.get(("/convert_currency?price="
                           f"{original_price}&currency={currency}"))
    assert response.status_code == 200
    assert "Price converted" in response.json


def mock_db_connection(mocker):
    mock_connect = mocker.patch('app.connectDB')
    mock_conn = mocker.MagicMock()
    mock_curs = mocker.MagicMock()
    mock_connect.return_value = (mock_conn, mock_curs)
    return mock_conn, mock_curs


def test_db_query(mock_db_connection):
    _, mock_curs = mock_db_connection
    mock_curs.fetchall.return_value = [
        (1, "'Product1'", 20.0, "'Hat'", 5, "'Red'", "'M'", 'URL1'),
    ]
    result = dbQuery()
    assert result == [
        (1, "'Product1'", 20.0, "'Hat'", 5, "'Red'", "'M'", 'URL1')
    ]


def test_reduce_stock(mock_db_connection):
    mock_conn, mock_curs = mock_db_connection
    item_id, reduce_by = 1, 2

    reduceStock(item_id, reduce_by)
    mock_curs.execute.assert_called_with("""
        UPDATE item
        SET stock = GREATEST(stock - %s, 0)
        WHERE item_id = %s
    """, (reduce_by, item_id))
    mock_conn.commit.assert_called_once()


def test_select_attribute(mock_db_connection):
    _, mock_curs = mock_db_connection
    mock_curs.fetchone.side_effect = [[5], (
        1, 
        "'Product1'", 
        20.0, 
        "'Hat'", 
        5, 
        "'Red'", 
        "'M'", 
        'URL1'
    )]

    item_id = 1
    result = selectAttribute(item_id)
    assert result == [1, "Product1", "20.00", "Hat", "5", "Red", "M", 'URL1']
