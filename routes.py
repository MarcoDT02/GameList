from flask import Blueprint, abort, jsonify, request
from models import Game, User, db
from schemas import (
    GameCreateSchema,
    GameUpdateSchema,
    UserLoginSchema,
    UserRegisterSchema,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
game_create_schema = GameCreateSchema()
game_update_schema = GameUpdateSchema()
games_list_schema = GameCreateSchema(many=True)

@api_bp.route("/register", methods=["POST"])
def register():
  data = user_register_schema.load(request.get_json() or {})

  if User.query.filter_by(username=data["username"]).first():
    return (
        jsonify({
            "error": "Conflict",
            "message": "Username is already taken.",
        }),
        409,
    )

  new_user = User(username=data["username"])
  new_user.set_password(data["password"])

  db.session.add(new_user)
  db.session.commit()

  return (
      jsonify({
          "message": "User registered successfully!",
          "user_id": new_user.id,
      }),
      201,
  )

@api_bp.route("/login", methods=["POST"])
def login():
  data = user_login_schema.load(request.get_json() or {})

  user = User.query.filter_by(username=data["username"]).first()

  if not user or not user.check_password(data["password"]):
    return (
        jsonify({
            "error": "Unauthorized",
            "message": "Invalid credentials.",
        }),
        401,
    )

  return (
      jsonify({
          "message": "Login successful!",
          "user_id": user.id,
          "username": user.username,
      }),
      200,
  )

@api_bp.route("/users/<int:user_id>/games", methods=["GET"])
def get_games(user_id):
  user = db.session.get(User, user_id)
  if not user:
    abort(404, description=f"User with id {user_id} was not found.")

  return (
      jsonify({
          "count": len(user.games),
          "games": games_list_schema.dump(user.games),
      }),
      200,
  )

@api_bp.route("/users/<int:user_id>/games", methods=["POST"])
def add_game(user_id):
  user = db.session.get(User, user_id)
  if not user:
    abort(404, description=f"User with id {user_id} was not found.")

  data = game_create_schema.load(request.get_json() or {})

  new_game = Game(
      user_id=user.id,
      title=data["title"],
      status=data["status"],
      rating=data.get("rating"),
  )

  db.session.add(new_game)
  db.session.commit()

  return (
      jsonify({
          "message": "Game added successfully!",
          "game": game_create_schema.dump(new_game),
      }),
      201,
  )

@api_bp.route("/users/<int:user_id>/games/<int:game_id>", methods=["PUT"])
def update_game(user_id, game_id):
  game = Game.query.filter_by(id=game_id, user_id=user_id).first()
  if not game:
    abort(
        404,
        description=(
            f"Game with id {game_id} for user {user_id} was not found."
        ),
    )

  data = game_update_schema.load(request.get_json() or {})

  if "status" in data:
    game.status = data["status"]

  if "rating" in data:
    game.rating = data["rating"]

  db.session.commit()

  return (
      jsonify({
          "message": "Game updated successfully!",
          "game": game_create_schema.dump(game),
      }),
      200,
  )

@api_bp.route("/users/<int:user_id>/games/<int:game_id>", methods=["DELETE"])
def delete_game(user_id, game_id):
  game = Game.query.filter_by(id=game_id, user_id=user_id).first()
  if not game:
    abort(
        404,
        description=(
            f"Game with id {game_id} for user {user_id} was not found."
        ),
    )

  db.session.delete(game)
  db.session.commit()

  return jsonify({"message": "Game deleted successfully!"}), 200