import pytest
from app import create_app
from models import db


@pytest.fixture()
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user_id(client):
    response = client.post(
        "/api/register",
        json={"username": "gamer_one", "password": "password123"},
    )
    return response.get_json()["user_id"]