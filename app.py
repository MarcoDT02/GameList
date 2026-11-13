import os
from errors import register_error_handlers
from flask import Flask
from models import db
from routes import api_bp

def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:PASSWORD@localhost:5432/gametracker_db",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    register_error_handlers(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)