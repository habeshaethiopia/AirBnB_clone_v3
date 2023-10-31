#!/usr/bin/python3
"""the user view"""

from api.v1.views import *
from flask import Flask, jsonify
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id=None):
    """
    GET Request for users
    """
    if user_id:
        return get_model(User, user_id)

    return jsonify([obj.to_dict() for obj in storage.all("User").values()])


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    DELETE Request for user
    """
    return delete(User, user_id)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """
    POST Request for States
    """
    return post(User, None, None, {"email", "password"})


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """
    PUT Request for States
    """
    return put(User, user_id, ["id", "email", "created_at", "updated_at"])
