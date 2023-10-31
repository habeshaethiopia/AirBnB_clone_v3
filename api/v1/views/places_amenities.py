#!/usr/bin/python3
"""place_aminity view"""
from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["GET", "POST", "DELETE"],
    strict_slashes=False,
)
def handle_request(place_id, amenity_id):
    """
    Handle GET, POST, and DELETE requests for a amenity
    """
    if request.method == "GET":
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity or amenity not in place.amenities:
            abort(404)
        return jsonify(amenity.to_dict()), 200

    elif request.method == "DELETE":
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity or amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    elif request.method == "POST":
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if not place or not amenity:
            abort(404)
        if not request.get_json():
            abort(400, "Not a JSON")
        if "user_id" not in request.get_json():
            abort(400, "Missing user_id")
        if "text" not in request.get_json():
            abort(400, "Missing text")
        amenity = amenity(**request.get_json())
        amenity.place_id = place_id
        amenity.save()
        return jsonify(amenity.to_dict()), 201
