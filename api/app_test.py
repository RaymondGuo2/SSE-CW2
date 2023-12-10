import pytest
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


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == (
        "Dinosaurs ruled the Earth 200 million years ago"
    )

