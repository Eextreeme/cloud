from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.patients import Patients

class PatientsDAO(GeneralDAO):
    _domain_type = Patients

    def create(self, patient: Patients) -> None:
        self._session.add(patient)
        self._session.commit()

    def find_all(self) -> List[Patients]:
        return self._session.query(Patients).all()

    def find_by_id(self, patient_id: int) -> Patients:
        return self._session.query(Patients).filter(Patients.patient_id == patient_id).first()