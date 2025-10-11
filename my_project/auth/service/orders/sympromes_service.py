from typing import List
from my_project.auth.dao import symptomes_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.symptomes import Symptomes

class SymptomesService(GeneralService):
    _dao = symptomes_dao

    def create(self, symptome: Symptomes) -> None:
        self._dao.create(symptome)

    def update(self, symptome_id: int, symptome: Symptomes) -> None:
        self._dao.update(symptome_id, symptome)

    def get_all_symptomes(self) -> List[Symptomes]:
        return self._dao.find_all()

    def get_symptome_by_id(self, symptome_id: int) -> Symptomes:
        return self._dao.find_by_id(symptome_id)