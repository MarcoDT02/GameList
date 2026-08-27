from flask import Blueprint, request, jsonify
from models import db, User, Game

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 400

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered!", "user_id": new_user.id}), 201


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "user_id": user.id}), 200

@api_bp.route("/users/<int:user_id>/games", methods=["GET"])
def get_games(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_games = [game.to_dict() for game in user.games]
    return jsonify(user_games), 200


@api_bp.route("/users/<int:user_id>/games", methods=["POST"])
def add_game(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    title = data.get("title")
    status = data.get("status")
    rating = data.get("rating")

    if not title or not status:
        return jsonify({"error": "Title and status are required"}), 400

    valid_statuses = ["backlog", "playing", "completed"]
    if status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    new_game = Game(
        user_id=user_id,
        title=title,
        status=status,
        rating=rating
    )

    db.session.add(new_game)
    db.session.commit()

    return jsonify(new_game.to_dict()), 201


@api_bp.route("/users/<int:user_id>/games/<int:game_id>", methods=["PUT"])
def update_game(user_id, game_id):
    game = Game.query.filter_by(id=game_id, user_id=user_id).first()
    if not game:
        return jsonify({"error": "Game not found"}), 404

    data = request.get_json() or {}

    if "status" in data:
        if data["status"] not in ["backlog", "playing", "completed"]:
            return jsonify({"error": "Invalid status"}), 400
        game.status = data["status"]

    if "rating" in data:
        game.rating = data["rating"]

    db.session.commit()
    return jsonify(game.to_dict()), 200


@api_bp.route("/users/<int:user_id>/games/<int:game_id>", methods=["DELETE"])
def delete_game(user_id, game_id):
    game = Game.query.filter_by(id=game_id, user_id=user_id).first()
    if not game:
        return jsonify({"error": "Game not found"}), 404

    db.session.delete(game)
    db.session.commit()

    return jsonify({"message": "Game deleted successfully"}), 200