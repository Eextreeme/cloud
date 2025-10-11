from typing import List
from my_project.auth.dao import doctors_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.doctors import Doctors

class DoctorsService(GeneralService):
    _dao = doctors_dao

    def create(self, doctor: Doctors) -> None:
        self._dao.create(doctor)

    def update(self, doctor_id: int, doctor: Doctors) -> None:
        self._dao.update(doctor_id, doctor)

    def get_all_doctors(self) -> List[Doctors]:
        return self._dao.find_all()

    def get_doctor_by_id(self, doctor_id: int) -> Doctors:
        return self._dao.find_by_id(doctor_id)