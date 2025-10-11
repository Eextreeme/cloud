from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import appointments_controller
from my_project.auth.domain.orders.appointments import Appointments

appointments_bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointments_bp.get('')
def get_all_appointments() -> Response:
    appointments = appointments_controller.find_all()
    appointments_dto = [appointment.put_into_dto() for appointment in appointments]
    return make_response(jsonify(appointments_dto), HTTPStatus.OK)

@appointments_bp.post('')
def create_appointment() -> Response:
    content = request.get_json()
    appointment = Appointments.create_from_dto(content)
    appointments_controller.create_appointment(appointment)
    return make_response(jsonify(appointment.put_into_dto()), HTTPStatus.CREATED)

@appointments_bp.get('/<int:appointment_id>')
def get_appointment(appointment_id: int) -> Response:
    appointment = appointments_controller.find_by_id(appointment_id)
    if appointment:
        return make_response(jsonify(appointment.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Appointment not found"}), HTTPStatus.NOT_FOUND)

@appointments_bp.put('/<int:appointment_id>')
def update_appointment(appointment_id: int) -> Response:
    content = request.get_json()
    appointment = Appointments.create_from_dto(content)
    appointments_controller.update_appointment(appointment_id, appointment)
    return make_response("Appointment updated", HTTPStatus.OK)

@appointments_bp.delete('/<int:appointment_id>')
def delete_appointment(appointment_id: int) -> Response:
    appointments_controller.delete_appointment(appointment_id)
    return make_response("Appointment deleted", HTTPStatus.NO_CONTENT)