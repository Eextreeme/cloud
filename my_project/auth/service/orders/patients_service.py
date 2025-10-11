from typing import List
from my_project.auth.dao import patients_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.patients import Patients

class PatientsService(GeneralService):
    _dao = patients_dao

    def create(self, patient: Patients) -> None:
        self._dao.create(patient)

    def update(self, patient_id: int, patient: Patients) -> None:
        self._dao.update(patient_id, patient)

    def get_all_patients(self) -> List[Patients]:
        return self._dao.find_all()

    def get_patient_by_id(self, patient_id: int) -> Patients:
        return self._dao.find_by_id(patient_id)