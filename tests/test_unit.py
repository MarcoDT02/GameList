import pytest
from marshmallow import ValidationError
from models import User
from schemas import (
    GameCreateSchema,
    GameUpdateSchema,
    UserLoginSchema,
    UserRegisterSchema,
)


def test_password_hashing():
    user = User(username="player1")
    user.set_password("secretpass")

    assert user.password_hash != "secretpass"
    assert user.check_password("secretpass") is True
    assert user.check_password("wrongpass") is False


def test_user_register_schema_valid():
    schema = UserRegisterSchema()
    data = schema.load({"username": "valid_gamer", "password": "password123"})

    assert data["username"] == "valid_gamer"
    assert data["password"] == "password123"


def test_user_register_schema_invalid():
    schema = UserRegisterSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({"username": "ab", "password": "123"})

    errors = exc_info.value.messages
    assert "username" in errors
    assert "password" in errors


def test_user_login_schema_missing_fields():
    schema = UserLoginSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({})

    errors = exc_info.value.messages
    assert "username" in errors
    assert "password" in errors


def test_game_create_schema_valid():
    schema = GameCreateSchema()
    data = schema.load({
        "title": "Elden Ring",
        "status": "completed",
        "rating": 10,
    })

    assert data["title"] == "Elden Ring"
    assert data["status"] == "completed"
    assert data["rating"] == 10


def test_game_create_schema_default_rating():
    schema = GameCreateSchema()
    data = schema.load({"title": "Hollow Knight", "status": "backlog"})

    assert data["title"] == "Hollow Knight"
    assert data["status"] == "backlog"
    assert data["rating"] is None


def test_game_create_schema_invalid_status_and_rating():
    schema = GameCreateSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({
            "title": "",
            "status": "dropped",
            "rating": 15,
        })

    errors = exc_info.value.messages
    assert "title" in errors
    assert "status" in errors
    assert "rating" in errors


def test_game_update_schema_valid():
    schema = GameUpdateSchema()
    data = schema.load({"status": "playing", "rating": 8})

    assert data["status"] == "playing"
    assert data["rating"] == 8


def test_game_update_schema_invalid():
    schema = GameUpdateSchema()

    with pytest.raises(ValidationError) as exc_info:
        schema.load({"status": "paused", "rating": 0})

    errors = exc_info.value.messages
    assert "status" in errors
    assert "rating" in errors