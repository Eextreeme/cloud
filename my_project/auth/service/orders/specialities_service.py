from typing import List
from my_project.auth.dao import specialties_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.specialities import Specialties

class SpecialtiesService(GeneralService):
    _dao = specialties_dao

    def create(self, specialty: Specialties) -> None:
        self._dao.create(specialty)

    def update(self, specialty_id: int, specialty: Specialties) -> None:
        self._dao.update(specialty_id, specialty)

    def get_all_specialties(self) -> List[Specialties]:
        return self._dao.find_all()

    def get_specialty_by_id(self, specialty_id: int) -> Specialties:
        return self._dao.find_by_id(specialty_id)