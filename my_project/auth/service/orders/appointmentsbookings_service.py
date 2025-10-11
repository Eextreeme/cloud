from typing import List
from my_project.auth.dao import appointment_bookings_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.appointmentbookings import AppointmentBookings

class AppointmentBookingsService(GeneralService):
    _dao = appointment_bookings_dao

    def create(self, booking: AppointmentBookings) -> None:
        self._dao.create(booking)

    def update(self, booking_id: int, booking: AppointmentBookings) -> None:
        self._dao.update(booking_id, booking)

    def get_all_appointment_bookings(self) -> List[AppointmentBookings]:
        return self._dao.find_all()

    def get_appointment_booking_by_id(self, booking_id: int) -> AppointmentBookings:
        return self._dao.find_by_id(booking_id)