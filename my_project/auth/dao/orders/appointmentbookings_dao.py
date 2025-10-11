from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders import appointmentbookings
from my_project.auth.domain.orders.appointmentbookings import AppointmentBookings


class AppointmentBookingsDAO(GeneralDAO):
    _domain_type = appointmentbookings

    def create(self, booking: AppointmentBookings) -> None:
        self._session.add(booking)
        self._session.commit()

    def find_all(self) -> List[AppointmentBookings]:
        return self._session.query(AppointmentBookings).all()

    def find_by_id(self, booking_id: int) -> AppointmentBookings:
        return self._session.query(AppointmentBookings).filter(AppointmentBookings.booking_id == booking_id).first()