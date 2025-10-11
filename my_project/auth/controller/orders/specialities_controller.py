from typing import List
from my_project.auth.service import specialties_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.specialities import Specialties


class SpecialtiesController(GeneralController):
    _service = specialties_service

    def create_specialty(self, specialty: Specialties) -> None:
        self._service.create(specialty)

    def find_all(self) -> List[Specialties]:
        return self._service.get_all_specialties()

    def find_by_id(self, specialty_id: int) -> Specialties:
        return self._service.get_specialty_by_id(specialty_id)

    def update_specialty(self, specialty_id: int, specialty: Specialties) -> None:
        self._service.update(specialty_id, specialty)

    def delete_specialty(self, specialty_id: int) -> None:
        self._service.delete(specialty_id)