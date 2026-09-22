from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
  @app.errorhandler(ValidationError)
  def handle_validation_error(err):
    return (
        jsonify({
            "error": "Validation Error",
            "message": "Invalid input data.",
            "details": err.messages,
        }),
        400,
    )

  @app.errorhandler(HTTPException)
  def handle_http_exception(err):
    return (
        jsonify({"error": err.name, "message": err.description}),
        err.code,
    )

  @app.errorhandler(Exception)
  def handle_unexpected_exception(err):
    return (
        jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        }),
        500,
    )