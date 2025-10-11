from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.appointments import Appointments

class AppointmentsDAO(GeneralDAO):
    _domain_type = Appointments

    def create(self, appointment: Appointments) -> None:
        self._session.add(appointment)
        self._session.commit()

    def find_all(self) -> List[Appointments]:
        return self._session.query(Appointments).all()

    def find_by_id(self, appointment_id: int) -> Appointments:
        return self._session.query(Appointments).filter(Appointments.appointment_id == appointment_id).first()