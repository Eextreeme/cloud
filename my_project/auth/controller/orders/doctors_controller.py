from typing import List
from my_project.auth.service import doctors_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.doctors import Doctors
from ...dao.orders.doctors_dao import DoctorsDAO




class DoctorsController(GeneralController):
    _service = doctors_service
    _dao = DoctorsDAO()

    def find_with_specialty(self):
        return self._dao.find_with_specialty()
    def create_doctor(self, doctor: Doctors) -> None:
        self._service.create(doctor)

    def find_all(self) -> List[Doctors]:
        return self._service.get_all_doctors()
    
    def find_by_id(self, doctor_id: int) -> Doctors:
        return self._service.get_doctor_by_id(doctor_id)

    def update_doctor(self, doctor_id: int, doctor: Doctors) -> None:
        self._service.update(doctor_id, doctor)

    def delete_doctor(self, doctor_id: int) -> None:
        self._service.delete(doctor_id)