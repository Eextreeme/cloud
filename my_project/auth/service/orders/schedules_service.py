from typing import List
from my_project.auth.dao import schedules_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.scedules import Schedules

class SchedulesService(GeneralService):
    _dao = schedules_dao

    def create(self, schedule: Schedules) -> None:
        self._dao.create(schedule)

    def update(self, schedule_id: int, schedule: Schedules) -> None:
        self._dao.update(schedule_id, schedule)

    def get_all_schedules(self) -> List[Schedules]:
        return self._dao.find_all()

    def get_schedule_by_id(self, schedule_id: int) -> Schedules:
        return self._dao.find_by_id(schedule_id)