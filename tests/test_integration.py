def test_register_success(client):
    response = client.post(
        "/api/register",
        json={"username": "newgamer", "password": "password123"},
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "User registered successfully!"
    assert "user_id" in data


def test_register_duplicate_username(client):
    payload = {"username": "dupgamer", "password": "password123"}
    client.post("/api/register", json=payload)

    response = client.post("/api/register", json=payload)
    data = response.get_json()

    assert response.status_code == 409
    assert data["error"] == "Conflict"


def test_login_success(client):
    client.post(
        "/api/register",
        json={"username": "logingamer", "password": "password123"},
    )

    response = client.post(
        "/api/login",
        json={"username": "logingamer", "password": "password123"},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Login successful!"
    assert data["username"] == "logingamer"


def test_login_invalid_credentials(client):
    client.post(
        "/api/register",
        json={"username": "logingamer", "password": "password123"},
    )

    response = client.post(
        "/api/login",
        json={"username": "logingamer", "password": "wrongpassword"},
    )
    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Unauthorized"


def test_add_game_success(client, user_id):
    response = client.post(
        f"/api/users/{user_id}/games",
        json={"title": "The Witcher 3", "status": "completed", "rating": 10},
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Game added successfully!"
    assert data["game"]["title"] == "The Witcher 3"
    assert data["game"]["status"] == "completed"
    assert data["game"]["rating"] == 10
    assert data["game"]["user_id"] == user_id


def test_add_game_user_not_found(client):
    response = client.post(
        "/api/users/999/games",
        json={"title": "The Witcher 3", "status": "backlog"},
    )
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Not Found"


def test_add_game_validation_error(client, user_id):
    response = client.post(
        f"/api/users/{user_id}/games",
        json={"title": "Cyberpunk 2077", "status": "invalid_status", "rating": 12},
    )
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Validation Error"


def test_get_games_success(client, user_id):
    client.post(
        f"/api/users/{user_id}/games",
        json={"title": "Hades", "status": "playing", "rating": 9},
    )

    response = client.get(f"/api/users/{user_id}/games")
    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 1
    assert data["games"][0]["title"] == "Hades"


def test_get_games_user_not_found(client):
    response = client.get("/api/users/999/games")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Not Found"


def test_update_game_success(client, user_id):
    create_res = client.post(
        f"/api/users/{user_id}/games",
        json={"title": "Celeste", "status": "backlog"},
    )
    game_id = create_res.get_json()["game"]["id"]

    response = client.put(
        f"/api/users/{user_id}/games/{game_id}",
        json={"status": "completed", "rating": 9},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Game updated successfully!"
    assert data["game"]["status"] == "completed"
    assert data["game"]["rating"] == 9


def test_update_game_not_found(client, user_id):
    response = client.put(
        f"/api/users/{user_id}/games/999",
        json={"status": "playing"},
    )
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Not Found"


def test_delete_game_success(client, user_id):
    create_res = client.post(
        f"/api/users/{user_id}/games",
        json={"title": "Doom Eternal", "status": "playing"},
    )
    game_id = create_res.get_json()["game"]["id"]

    delete_res = client.delete(f"/api/users/{user_id}/games/{game_id}")
    assert delete_res.status_code == 200
    assert delete_res.get_json()["message"] == "Game deleted successfully!"

    get_res = client.get(f"/api/users/{user_id}/games")
    assert get_res.get_json()["count"] == 0


def test_delete_game_not_found(client, user_id):
    response = client.delete(f"/api/users/{user_id}/games/999")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Not Found"