#!/usr/bin/python3
"""the flask app"""
from flask import Flask, render_template, url_for
from models import storage
from models.amenity import Amenity
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    """Displays an HTML page with a list of all State objects in DBStorage."""
    states = storage.all("State").values()
    return render_template("8-cities_by_states.html", states=states, id=id)


@app.teardown_appcontext
def teardown_db(self):
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays an HTML page with a list of all State objects in DBStorage."""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
