from flask import Blueprint, request, jsonify, abort
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def get_model(model, my_id):
    """Return the model to be used."""
    obj = storage.get(model, my_id)
    if obj:
        return jsonify(obj.to_dict()), 200
    abort(404)


def delete(model, my_id):
    """Delete a model if it exists."""
    obj = storage.get(model, my_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


def post(model, p_model, p_id, data):
    """Create a new model.(post request)"""
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")
    if p_model:
        parent = storage.get(p_model, p_id)
        if not parent:
            abort(404)
        key = p_model.__name__.lower() + "_id"
        json_data[key] = p_id
    for key, value in data.items():
        if key not in json_data:
            abort(400, "Missing {}".format(key))
        if type(value) is not str:
            json_data[key] = value(json_data[key])
    obj = model(**json_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


def put(model, my_id, data):
    """update (put request)"""
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")
    obj = storage.get(model, my_id)
    if not obj:
        abort(404)
    for key, val in json_data.items():
        if key not in data:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200


if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.amenities import *
    from api.v1.views.cities import *
    from api.v1.views.users import *
