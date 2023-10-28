#!/usr/bin/python3
"""start flask and set a route"""

from flask import Flask, render_template
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.teardown_appcontext
def close(self):
    """Closes sessions"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """returns the Airbnb Project"""
    places = storage.all(Place).values()
    amenities = storage.all(Amenity).values()
    states = storage.all(State).values()
    _all = {}
    for p, u in storage._DBStorage__session.query(Place, User).\
            filter(Place.user_id == User.id):
        _all[p.user_id] = "{} {}".format(u.first_name, u.last_name)
    return render_template('100-hbnb.html', **locals())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
