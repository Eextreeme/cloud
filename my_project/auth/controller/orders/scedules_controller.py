from typing import List
from my_project.auth.service import schedules_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.scedules import Schedules


class SchedulesController(GeneralController):
    _service = schedules_service

    def create_schedule(self, schedule: Schedules) -> None:
        self._service.create(schedule)

    def find_all(self) -> List[Schedules]:
        return self._service.get_all_schedules()

    def find_by_id(self, schedule_id: int) -> Schedules:
        return self._service.get_schedule_by_id(schedule_id)

    def update_schedule(self, schedule_id: int, schedule: Schedules) -> None:
        self._service.update(schedule_id, schedule)

    def delete_schedule(self, schedule_id: int) -> None:
        self._service.delete(schedule_id)