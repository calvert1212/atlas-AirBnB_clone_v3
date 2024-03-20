#!/usr/bin/python3
"""
Provides a RESTful API for managing AirBnB clone data.
It includes CORS configuration to allow requests from any origin,
and a custom error handler for 404 errors.
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os
from os import getenv
from flask_cors import CORS

"""Creates a Flask application instance"""
app = Flask(__name__)

"""Registers the blueprint for the API views"""
app.register_blueprint(app_views)

"""Configure CORS to allow requests from any origin."""
"""Necessary for client-side web applications to interact with the API."""
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """Closes storage when the application context is torn down."""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """Return a JSON response for 404 errors."""
    return (jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    """Use environment variables for host and port, with defaults if not set."""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    """Run the Flask server with the specified host and port, using threaded mode for better performance."""
    app.run(host=host, port=port, threaded=True)
