from typing import List
from my_project.auth.service import appointment_bookings_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.appointmentbookings import AppointmentBookings


class AppointmentBookingsController(GeneralController):
    _service = appointment_bookings_service

    def create_appointment_booking(self, booking: AppointmentBookings) -> None:
        self._service.create(booking)

    def find_all(self) -> List[AppointmentBookings]:
        return self._service.get_all_appointment_bookings()

    def find_by_id(self, booking_id: int) -> AppointmentBookings:
        return self._service.get_appointment_booking_by_id(booking_id)

    def update_appointment_booking(self, booking_id: int, booking: AppointmentBookings) -> None:
        self._service.update(booking_id, booking)

    def delete_appointment_booking(self, booking_id: int) -> None:
        self._service.delete(booking_id)