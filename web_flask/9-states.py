#!/usr/bin/python3
"""the flask app"""
from flask import Flask, render_template
from models import storage

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
