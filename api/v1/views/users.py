#!/usr/bin/python3
"""Uses API to create and update users"""

from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def users(user_id=None):
    """Returns all users by ID"""
    if user_id:
        obj = storage.get(User, user_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    else:
        users = storage.all(User)
        userlist = []
        for user in users.values():
            userlist.append(user.to_dict())
        return jsonify(userlist)


app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """deletes a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def post_user():
    """add user using POST"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update user using PUT"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    notThese = ["id", "email", "created_at", "updated_at"]
    data = request.get_json()
    for key, value in data.items():
        if key not in notThese:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
