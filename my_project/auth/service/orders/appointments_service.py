from typing import List
from my_project.auth.dao import appointments_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.appointments import Appointments

class AppointmentsService(GeneralService):
    _dao = appointments_dao

    def create(self, appointment: Appointments) -> None:
        self._dao.create(appointment)

    def update(self, appointment_id: int, appointment: Appointments) -> None:
        self._dao.update(appointment_id, appointment)

    def get_all_appointments(self) -> List[Appointments]:
        return self._dao.find_all()

    def get_appointment_by_id(self, appointment_id: int) -> Appointments:
        return self._dao.find_by_id(appointment_id)