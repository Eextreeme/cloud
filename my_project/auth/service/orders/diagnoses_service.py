from typing import List
from my_project.auth.dao import diagnoses_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.diagnoses import Diagnoses

class DiagnosesService(GeneralService):
    _dao = diagnoses_dao

    def create(self, diagnosis: Diagnoses) -> None:
        self._dao.create(diagnosis)

    def update(self, diagnosis_id: int, diagnosis: Diagnoses) -> None:
        self._dao.update(diagnosis_id, diagnosis)

    def get_all_diagnoses(self) -> List[Diagnoses]:
        return self._dao.find_all()

    def get_diagnosis_by_id(self, diagnosis_id: int) -> Diagnoses:
        return self._dao.find_by_id(diagnosis_id)