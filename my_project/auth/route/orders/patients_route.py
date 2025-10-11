from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import patients_controller
from my_project.auth.domain.orders.patients import Patients

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

@patients_bp.get('')
def get_all_patients() -> Response:
    patients = patients_controller.find_all()
    patients_dto = [patient.put_into_dto() for patient in patients]
    return make_response(jsonify(patients_dto), HTTPStatus.OK)

@patients_bp.post('')
def create_patient() -> Response:
    content = request.get_json()
    patient = Patients.create_from_dto(content)
    patients_controller.create_patient(patient)
    return make_response(jsonify(patient.put_into_dto()), HTTPStatus.CREATED)

@patients_bp.get('/<int:patient_id>')
def get_patient(patient_id: int) -> Response:
    patient = patients_controller.find_by_id(patient_id)
    if patient:
        return make_response(jsonify(patient.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Patient not found"}), HTTPStatus.NOT_FOUND)

@patients_bp.put('/<int:patient_id>')
def update_patient(patient_id: int) -> Response:
    content = request.get_json()
    patient = Patients.create_from_dto(content)
    patients_controller.update_patient(patient_id, patient)
    return make_response("Patient updated", HTTPStatus.OK)

@patients_bp.delete('/<int:patient_id>')
def delete_patient(patient_id: int) -> Response:
    patients_controller.delete_patient(patient_id)
    return make_response("Patient deleted", HTTPStatus.NO_CONTENT)