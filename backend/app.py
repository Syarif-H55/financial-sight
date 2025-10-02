from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    
    from .api import main_blueprint
    app.register_blueprint(main_blueprint)

    return app


if __name__ == "__main__":
    # Allow running as `python backend/app.py`
    from flask_cors import CORS
    app = create_app()
    CORS(app)
    app.run(host="127.0.0.1", port=5000, debug=True)


