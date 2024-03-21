#!/usr/bin/python3
"""
Provides a RESTful API for managing AirBnB clone data.
It includes CORS configuration to allow requests from any origin,
and a custom error handler for 404 errors.
"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS
import os

"""Creates Flask instance"""
app = Flask(__name__)
"""Configures CORS to allow requests, needed"""
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

"""Sets up Flask environment variables"""
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

"""Registers Blueprint for app_views"""
app.register_blueprint(app_views)


"""Tears down Flask"""
@app.teardown_appcontext
def teardown_db(exception):
    """Tears down and closes Flask"""
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """Handler for 404 error (Not Found)"""
    code = exception.__str__().split()[0]
    description = "Not found"
    message = {'error': description}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    """MAIN Flask App"""
    # start Flask app
    app.run(host=host, port=port)
