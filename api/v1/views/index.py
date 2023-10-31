#!/usr/bin/python3
"""Defines the index"""
from models import storage
from api.v1.views import app_views, Amenity, City, Place, Review, State, User
from flask import Flask, jsonify


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"}), 200

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """Return the stats of the API."""
    counts = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(counts), 200
