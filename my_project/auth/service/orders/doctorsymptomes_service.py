from typing import List
from my_project.auth.dao import doctorsymptomes_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.doctorsymptomes import DoctorSymptomes

class DoctorSymptomesService(GeneralService):
    _dao = doctorsymptomes_dao

    def create(self, doctor_symptome: DoctorSymptomes) -> None:

        self._dao.create(doctor_symptome)

    def get_all_relations(self) -> List[DoctorSymptomes]:

        return self._dao.find_all()

    def get_symptomes_by_doctor(self, doctor_id: int) -> List[DoctorSymptomes]:

        return self._dao.find_by_doctor_id(doctor_id)

    def get_doctors_by_symptome(self, symptome_id: int) -> List[DoctorSymptomes]:

        return self._dao.find_by_symptome_id(symptome_id)

    def delete_relation(self, doctor_id: int, symptome_id: int) -> None:

        self._dao.delete_relation(doctor_id, symptome_id)

    def find_with_details(self):
        return self._dao.find_with_details()