from typing import List
from my_project.auth.service import appointments_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.appointments import Appointments


class AppointmentsController(GeneralController):
    _service = appointments_service

    def create_appointment(self, appointment: Appointments) -> None:
        self._service.create(appointment)

    def find_all(self) -> List[Appointments]:
        return self._service.get_all_appointments()

    def find_by_id(self, appointment_id: int) -> Appointments:
        return self._service.get_appointment_by_id(appointment_id)

    def update_appointment(self, appointment_id: int, appointment: Appointments) -> None:
        self._service.update(appointment_id, appointment)

    def delete_appointment(self, appointment_id: int) -> None:
        self._service.delete(appointment_id)