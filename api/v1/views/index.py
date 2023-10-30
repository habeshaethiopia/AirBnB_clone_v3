#!/usr/bin/python3
"""Defines the State class."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})
