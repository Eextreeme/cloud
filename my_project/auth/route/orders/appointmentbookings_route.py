from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import appointment_bookings_controller
from my_project.auth.domain.orders.appointmentbookings import AppointmentBookings

appointment_bookings_bp = Blueprint('appointment_bookings', __name__, url_prefix='/appointment_bookings')

@appointment_bookings_bp.get('')
def get_all_appointment_bookings() -> Response:
    bookings = appointment_bookings_controller.find_all()
    bookings_dto = [booking.put_into_dto() for booking in bookings]
    return make_response(jsonify(bookings_dto), HTTPStatus.OK)

@appointment_bookings_bp.post('')
def create_appointment_booking() -> Response:
    content = request.get_json()
    booking = AppointmentBookings.create_from_dto(content)
    appointment_bookings_controller.create_appointment_booking(booking)
    return make_response(jsonify(booking.put_into_dto()), HTTPStatus.CREATED)

@appointment_bookings_bp.get('/<int:booking_id>')
def get_appointment_booking(booking_id: int) -> Response:
    booking = appointment_bookings_controller.find_by_id(booking_id)
    if booking:
        return make_response(jsonify(booking.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Booking not found"}), HTTPStatus.NOT_FOUND)

@appointment_bookings_bp.put('/<int:booking_id>')
def update_appointment_booking(booking_id: int) -> Response:
    content = request.get_json()
    booking = AppointmentBookings.create_from_dto(content)
    appointment_bookings_controller.update_appointment_booking(booking_id, booking)
    return make_response("Booking updated", HTTPStatus.OK)

@appointment_bookings_bp.delete('/<int:booking_id>')
def delete_appointment_booking(booking_id: int) -> Response:
    appointment_bookings_controller.delete_appointment_booking(booking_id)
    return make_response("Booking deleted", HTTPStatus.NO_CONTENT)