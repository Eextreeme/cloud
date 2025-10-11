from typing import List
from my_project.auth.service import diagnoses_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.diagnoses import Diagnoses


class DiagnosesController(GeneralController):
    _service = diagnoses_service

    def create_diagnosis(self, diagnosis: Diagnoses) -> None:
        self._service.create(diagnosis)

    def find_all(self) -> List[Diagnoses]:
        return self._service.get_all_diagnoses()

    def find_by_id(self, diagnosis_id: int) -> Diagnoses:
        return self._service.get_diagnosis_by_id(diagnosis_id)

    def update_diagnosis(self, diagnosis_id: int, diagnosis: Diagnoses) -> None:
        self._service.update(diagnosis_id, diagnosis)

    def delete_diagnosis(self, diagnosis_id: int) -> None:
        self._service.delete(diagnosis_id)