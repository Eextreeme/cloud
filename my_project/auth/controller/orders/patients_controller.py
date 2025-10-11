from typing import List
from my_project.auth.service import patients_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.patients import Patients


class PatientsController(GeneralController):
    _service = patients_service

    def create_patient(self, patient: Patients) -> None:
        self._service.create(patient)

    def find_all(self) -> List[Patients]:
        return self._service.get_all_patients()

    def find_by_id(self, patient_id: int) -> Patients:
        return self._service.get_patient_by_id(patient_id)
    

    def update_patient(self, patient_id: int, patient: Patients) -> None:
        self._service.update(patient_id, patient)

    def delete_patient(self, patient_id: int) -> None:
        self._service.delete(patient_id)