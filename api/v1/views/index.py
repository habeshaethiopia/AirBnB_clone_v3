#!/usr/bin/python3
"""Defines the State class."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"}), 200


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    """Return the stats of the API."""
    classes = {
        "amenities": 47,
        "cities": 36,
        "places": 154,
        "reviews": 718,
        "states": 27,
        "users": 31,
    }

    return jsonify(classes), 200
