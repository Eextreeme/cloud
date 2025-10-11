from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders import illnesses

class IllnessesDAO(GeneralDAO):
    _domain_type = illnesses.Illnesses

    def create(self, illness: illnesses.Illnesses) -> None:
        self._session.add(illness)
        self._session.commit()

    def find_all(self) -> List[illnesses.Illnesses]:
        return self._session.query(illnesses.Illnesses).all()

    def find_by_id(self, illness_id: int) -> illnesses.Illnesses:
        return self._session.query(illnesses.Illnesses).filter(illnesses.Illnesses.illness_id == illness_id).first()