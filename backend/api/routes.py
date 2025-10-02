from flask import Blueprint, send_from_directory
import os

main_blueprint = Blueprint("main", __name__)

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "../../frontend/pages")

@main_blueprint.route("/")
def index():
    return send_from_directory(FRONTEND_PATH, "index.html")

@main_blueprint.route("/<path:filename>")
def static_pages(filename):
    return send_from_directory(FRONTEND_PATH, filename)
