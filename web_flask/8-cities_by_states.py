#!/usr/bin/python3
""" a script that starts a Flask web application """

from flask import Flask
from flask import render_template

from models.state import State
from models import storage

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def get_cities():
    """get the states list"""
    states = storage.all(State)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """close the storage session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
