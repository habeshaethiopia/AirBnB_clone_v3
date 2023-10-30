#!/usr/bin/python3
"""Defines the Review class."""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def notFound(error):
    """Return the status of the API."""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage."""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
