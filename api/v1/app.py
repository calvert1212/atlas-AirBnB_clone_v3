#!/usr/bin/python3
"""
Provides a RESTful API for managing AirBnB clone data.
It includes CORS configuration to allow requests from any origin,
and a custom error handler for 404 errors.
"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template
from models import storage
import os
from flask_cors import CORS

"""Creates a Flask application instance"""
app = Flask(__name__)

"""Configure CORS to allow requests from any origin."""
"""Necessary for client-side web applications to interact with the API."""
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

"""Registers the blueprint for the API views"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage when the application context is torn down."""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """Return a JSON response for 404 errors."""
    code = exception.__str__().split()[0]
    description = "Not found"
    message = {'error': description}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    """Use environment variables for host and port, with defaults if not set."""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    """Run the Flask server with the specified host and port, using threaded mode for better performance."""
    app.run(host=host, port=port, threaded=True)
