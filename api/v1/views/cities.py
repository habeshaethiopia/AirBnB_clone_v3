#!/usr/bin/python3
"""
cities view
"""

from api.v1.views import *
from flask import Flask, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["GET"])
def get_cities(state_id):
    """
    GET Request all cities in a State
    """
    all_cities = storage.get(City, state_id)
    if all_cities:
        return jsonify([p.to_dict() for p in getattr(City, "cities")]), 200
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """
    GET Request for a city
    """
    return get_model(City, city_id)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    DELETE Request for a city
    """
    return delete(City, city_id)


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["POST"])
def post_city(state_id):
    """
    POST Request for a city
    """
    return post(City, State, state_id, {"name"})


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """
    PUT Request for a city
    """
    return put(City, city_id, ["id", "created_at", "updated_at"])
