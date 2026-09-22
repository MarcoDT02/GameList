from marshmallow import Schema, fields, validate

VALID_GAME_STATUSES = ["backlog", "playing", "completed"]

class UserRegisterSchema(Schema):
  username = fields.String(
      required=True,
      validate=validate.Length(
          min=3,
          max=80,
          error="Username must be between 3 and 80 characters long.",
      ),
  )
  password = fields.String(
      required=True,
      validate=validate.Length(
          min=6, error="Password must be at least 6 characters long."
      ),
  )

class UserLoginSchema(Schema):
  username = fields.String(
      required=True,
      error_messages={"required": "The 'username' field is required."},
  )
  password = fields.String(
      required=True,
      error_messages={"required": "The 'password' field is required."},
  )

class GameCreateSchema(Schema):
  id = fields.Integer(dump_only=True)
  user_id = fields.Integer(dump_only=True)
  title = fields.String(
      required=True,
      validate=validate.Length(
          min=1,
          max=150,
          error="Title must be between 1 and 150 characters long.",
      ),
  )
  status = fields.String(
      required=True,
      validate=validate.OneOf(
          VALID_GAME_STATUSES,
          error=(
              "Invalid status. Allowed values are: 'backlog', 'playing',"
              " 'completed'."
          ),
      ),
  )
  rating = fields.Integer(
      allow_none=True,
      load_default=None,
      validate=validate.Range(
          min=1, max=10, error="Rating must be an integer between 1 and 10."
      ),
  )

class GameUpdateSchema(Schema):
  status = fields.String(
      validate=validate.OneOf(
          VALID_GAME_STATUSES,
          error=(
              "Invalid status. Allowed values are: 'backlog', 'playing',"
              " 'completed'."
          ),
      )
  )
  rating = fields.Integer(
      allow_none=True,
      validate=validate.Range(
          min=1, max=10, error="Rating must be an integer between 1 and 10."
      ),
  )