from typing import List
from my_project.auth.service import symptomes_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.symptomes import Symptomes


class SymptomesController(GeneralController):
    _service = symptomes_service

    def create_symptome(self, symptome: Symptomes) -> None:
        self._service.create(symptome)

    def find_all(self) -> List[Symptomes]:
        return self._service.get_all_symptomes()

    def find_by_id(self, symptome_id: int) -> Symptomes:
        return self._service.get_symptome_by_id(symptome_id)

    def update_symptome(self, symptome_id: int, symptome: Symptomes) -> None:
        self._service.update(symptome_id, symptome)

    def delete_symptome(self, symptome_id: int) -> None:
        self._service.delete(symptome_id)