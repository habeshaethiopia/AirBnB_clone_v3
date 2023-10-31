#!/usr/bin/python3
"""Defines the State class."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def all_states():
    """Return the list of all State objects."""
    states = storage.all("State")
    states = [state.to_dict() for state in states.values()]
    return jsonify(states), 200


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def state(state_id=None):
    """return a single statr"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id=None):
    """delete a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """create a state"""
    state = request.get_json()
    if state is None:
        abort(400, "Not a JSON")
    if "name" not in state:
        abort(400, "Missing name")
    state = State(**state)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state_dict = request.get_json()
    if state_dict is None:
        abort(400, "Not a JSON")
    for key, value in state_dict.items():
        if key in ["name"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200