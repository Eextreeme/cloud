from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import doctors_controller
from my_project.auth.domain.orders.doctors import Doctors

doctors_bp = Blueprint('doctors', __name__, url_prefix='/doctors')

@doctors_bp.get('')
def get_all_doctors() -> Response:
    doctors = doctors_controller.find_all()
    doctors_dto = [doctor.put_into_dto() for doctor in doctors]
    return make_response(jsonify(doctors_dto), HTTPStatus.OK)

@doctors_bp.post('')
def create_doctor() -> Response:
    content = request.get_json()
    doctor = Doctors.create_from_dto(content)
    doctors_controller.create_doctor(doctor)
    return make_response(jsonify(doctor.put_into_dto()), HTTPStatus.CREATED)

@doctors_bp.get('all')
def get_all_employees_with() -> Response:
    doctors = doctors_controller.find_with_specialty()
    doctors_dto = [employee.put_into_large_dto() for employee in doctors]
    return make_response(jsonify(doctors_dto), HTTPStatus.OK)

@doctors_bp.get('/<int:doctor_id>')
def get_doctor(doctor_id: int) -> Response:
    doctor = doctors_controller.find_by_id(doctor_id)
    if doctor:
        return make_response(jsonify(doctor.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Doctor not found"}), HTTPStatus.NOT_FOUND)

@doctors_bp.put('/<int:doctor_id>')
def update_doctor(doctor_id: int) -> Response:
    content = request.get_json()
    doctor = Doctors.create_from_dto(content)
    doctors_controller.update_doctor(doctor_id, doctor)
    return make_response("Doctor updated", HTTPStatus.OK)

@doctors_bp.delete('/<int:doctor_id>')
def delete_doctor(doctor_id: int) -> Response:
    doctors_controller.delete_doctor(doctor_id)
    return make_response("Doctor deleted", HTTPStatus.NO_CONTENT)