#!/usr/bin/python3
"""
Place reviews view
"""

from api.v1.views import *
from flask import Flask, jsonify
from models import storage
from models.review import Review
from models.place import Place


@app_views.route("/place/<place_id>/review", strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """
        GET Request for reviews on a place
    """
    return parent_model(Place, place_id, "reviews")


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """
        GET Request for a review
    """
    return get_model(Review, review_id)


@app_views.route("/review/<review_id>",
                 methods=["DELETE"] ,strict_slashes=False)
def delete_review(review_id):
    """
        DELETE Request for a review
    """
    return delete(Review, review_id)


@app_views.route("/place/<place_id>/review",
                 strict_slashes=False,
                 methods=["POST"])
def post_review(place_id):
    """
        POST Request for a review
    """
    return post(Review, Place, place_id, {"text", "user_id"})


@app_views.route("/review/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def put_review(review_id):
    """
        PUT Request for a review
    """
    return put(Review, review_id, ["id", "created_at", "updated_at", "user_id",
               "place_id"])