#!/usr/bin/python3
"""Uses API to interact with cities"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    """Retrieves all cities in a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Gets a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Creates a city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    city = City(**request.json)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
