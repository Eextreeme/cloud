from typing import List
from my_project.auth.dao import illnesses_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.illnesses import Illnesses

class IllnessesService(GeneralService):
    _dao = illnesses_dao

    def create(self, illness: Illnesses) -> None:
        self._dao.create(illness)

    def update(self, illness_id: int, illness: Illnesses) -> None:
        self._dao.update(illness_id, illness)

    def get_all_illnesses(self) -> List[Illnesses]:
        return self._dao.find_all()

    def get_illness_by_id(self, illness_id: int) -> Illnesses:
        return self._dao.find_by_id(illness_id)