#!/usr/bin/python3
"""
Handling Ammenity objects via Flask
"""

from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenities(amenity_id=None):
    """Returns all amenities or an amenity by specific ID"""
    if amenity_id:
        obj = storage.get(Amenity, amenity_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    else:
        amenities = storage.all(Amenity)
        amenitylist = []
        for amenity in amenities.values():
            amenitylist.append(amenity.to_dict())
        return jsonify(amenitylist)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """deletes an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def post_amenity():
    """add amenity using POST"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing Name"}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update an amenity using PUT"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    notThese = ["id", "created_at", "updated_at"]
    data = request.get_json()
    for key, value in data.items():
        if key not in notThese:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
