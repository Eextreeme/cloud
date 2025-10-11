from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.scedules import Schedules

class SchedulesDAO(GeneralDAO):
    _domain_type = Schedules

    def create(self, schedule: Schedules) -> None:
        self._session.add(schedule)
        self._session.commit()

    def find_all(self) -> List[Schedules]:
        return self._session.query(Schedules).all()

    def find_by_id(self, schedule_id: int) -> Schedules:
        return self._session.query(Schedules).filter(Schedules.schedule_id == schedule_id).first()