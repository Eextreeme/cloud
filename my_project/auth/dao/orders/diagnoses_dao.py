from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.diagnoses import Diagnoses

class DiagnosesDAO(GeneralDAO):
    _domain_type = Diagnoses

    def create(self, diagnosis: Diagnoses) -> None:
        self._session.add(diagnosis)
        self._session.commit()

    def find_all(self) -> List[Diagnoses]:
        return self._session.query(Diagnoses).all()

    def find_by_id(self, diagnosis_id: int) -> Diagnoses:
        return self._session.query(Diagnoses).filter(Diagnoses.diagnosis_id == diagnosis_id).first()