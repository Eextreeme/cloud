from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import diagnoses_controller
from my_project.auth.domain.orders.diagnoses import Diagnoses

diagnoses_bp = Blueprint('diagnoses', __name__, url_prefix='/diagnoses')

@diagnoses_bp.get('')
def get_all_diagnoses() -> Response:
    diagnoses = diagnoses_controller.find_all()
    diagnoses_dto = [diagnosis.put_into_dto() for diagnosis in diagnoses]
    return make_response(jsonify(diagnoses_dto), HTTPStatus.OK)

@diagnoses_bp.post('')
def create_diagnosis() -> Response:
    content = request.get_json()
    diagnosis = Diagnoses.create_from_dto(content)
    diagnoses_controller.create_diagnosis(diagnosis)
    return make_response(jsonify(diagnosis.put_into_dto()), HTTPStatus.CREATED)

@diagnoses_bp.get('/<int:diagnosis_id>')
def get_diagnosis(diagnosis_id: int) -> Response:
    diagnosis = diagnoses_controller.find_by_id(diagnosis_id)
    if diagnosis:
        return make_response(jsonify(diagnosis.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Diagnosis not found"}), HTTPStatus.NOT_FOUND)

@diagnoses_bp.put('/<int:diagnosis_id>')
def update_diagnosis(diagnosis_id: int) -> Response:
    content = request.get_json()
    diagnosis = Diagnoses.create_from_dto(content)
    diagnoses_controller.update_diagnosis(diagnosis_id, diagnosis)
    return make_response("Diagnosis updated", HTTPStatus.OK)

@diagnoses_bp.delete('/<int:diagnosis_id>')
def delete_diagnosis(diagnosis_id: int) -> Response:
    diagnoses_controller.delete_diagnosis(diagnosis_id)
    return make_response("Diagnosis deleted", HTTPStatus.NO_CONTENT)