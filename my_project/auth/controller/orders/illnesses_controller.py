from typing import List
from my_project.auth.service import illnesses_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.illnesses import Illnesses


class IllnessesController(GeneralController):
    _service = illnesses_service

    def create_illness(self, illness: Illnesses) -> None:
        self._service.create(illness)

    def find_all(self) -> List[Illnesses]:
        return self._service.get_all_illnesses()

    def find_by_id(self, illness_id: int) -> Illnesses:
        return self._service.get_illness_by_id(illness_id)

    def update_illness(self, illness_id: int, illness: Illnesses) -> None:
        self._service.update(illness_id, illness)

    def delete_illness(self, illness_id: int) -> None:
        self._service.delete(illness_id)