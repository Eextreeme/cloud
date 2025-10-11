from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import specialties_controller
from my_project.auth.domain.orders.specialities import Specialties

specialties_bp = Blueprint('specialties', __name__, url_prefix='/specialties')

@specialties_bp.get('')
def get_all_specialties() -> Response:
    specialties = specialties_controller.find_all()
    specialties_dto = [specialty.put_into_dto() for specialty in specialties]
    return make_response(jsonify(specialties_dto), HTTPStatus.OK)

@specialties_bp.post('')
def create_specialty() -> Response:
    content = request.get_json()
    specialty = Specialties.create_from_dto(content)
    specialties_controller.create_specialty(specialty)
    return make_response(jsonify(specialty.put_into_dto()), HTTPStatus.CREATED)

@specialties_bp.get('/<int:specialty_id>')
def get_specialty(specialty_id: int) -> Response:
    specialty = specialties_controller.find_by_id(specialty_id)
    if specialty:
        return make_response(jsonify(specialty.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Specialty not found"}), HTTPStatus.NOT_FOUND)

@specialties_bp.put('/<int:specialty_id>')
def update_specialty(specialty_id: int) -> Response:
    content = request.get_json()
    specialty = Specialties.create_from_dto(content)
    specialties_controller.update_specialty(specialty_id, specialty)
    return make_response("Specialty updated", HTTPStatus.OK)

@specialties_bp.delete('/<int:specialty_id>')
def delete_specialty(specialty_id: int) -> Response:
    specialties_controller.delete_specialty(specialty_id)
    return make_response("Specialty deleted", HTTPStatus.NO_CONTENT)