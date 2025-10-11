from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.specialities import Specialties

class SpecialtiesDAO(GeneralDAO):
    _domain_type = Specialties

    def create(self, specialty: Specialties) -> None:
        self._session.add(specialty)
        self._session.commit()

    def find_all(self) -> List[Specialties]:
        return self._session.query(Specialties).all()

    def find_by_id(self, specialty_id: int) -> Specialties:
        return self._session.query(Specialties).filter(Specialties.specialty_id == specialty_id).first()