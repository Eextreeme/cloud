from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import symptomes_controller
from my_project.auth.domain.orders.symptomes import Symptomes

symptomes_bp = Blueprint('symptomes', __name__, url_prefix='/symptomes')

@symptomes_bp.get('')
def get_all_symptomes() -> Response:
    symptomes = symptomes_controller.find_all()
    symptomes_dto = [symptome.put_into_dto() for symptome in symptomes]
    return make_response(jsonify(symptomes_dto), HTTPStatus.OK)

@symptomes_bp.post('')
def create_symptome() -> Response:
    content = request.get_json()
    symptome = Symptomes.create_from_dto(content)
    symptomes_controller.create_symptome(symptome)
    return make_response(jsonify(symptome.put_into_dto()), HTTPStatus.CREATED)

@symptomes_bp.get('/<int:symptome_id>')
def get_symptome(symptome_id: int) -> Response:
    symptome = symptomes_controller.find_by_id(symptome_id)
    if symptome:
        return make_response(jsonify(symptome.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Symptome not found"}), HTTPStatus.NOT_FOUND)

@symptomes_bp.put('/<int:symptome_id>')
def update_symptome(symptome_id: int) -> Response:
    content = request.get_json()
    symptome = Symptomes.create_from_dto(content)
    symptomes_controller.update_symptome(symptome_id, symptome)
    return make_response("Symptome updated", HTTPStatus.OK)

@symptomes_bp.delete('/<int:symptome_id>')
def delete_symptome(symptome_id: int) -> Response:
    symptomes_controller.delete_symptome(symptome_id)
    return make_response("Symptome deleted", HTTPStatus.NO_CONTENT)