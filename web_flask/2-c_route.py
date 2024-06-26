#!/usr/bin/python3
""" a script that starts a Flask web application """

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """return Hello HBNB"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def route_hbnb():
    """return HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """dicplay c followed by text"""
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
