from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.symptomes import Symptomes

class SymptomesDAO(GeneralDAO):
    _domain_type = Symptomes

    def create(self, symptome: Symptomes) -> None:
        self._session.add(symptome)
        self._session.commit()

    def find_all(self) -> List[Symptomes]:
        return self._session.query(Symptomes).all()

    def find_by_id(self, symptome_id: int) -> Symptomes:
        return self._session.query(Symptomes).filter(Symptomes.symptome_id == symptome_id).first()