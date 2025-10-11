from typing import List
from my_project.auth.service import doctorsymptomes_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.doctorsymptomes import DoctorSymptomes
from ...dao.orders.doctorsymptomes_dao import DoctorSymptomesDAO


class DoctorSymptomesController(GeneralController):
    _service = doctorsymptomes_service
    _dao = DoctorSymptomesDAO()

    def create_relation(self, doctor_symptome: DoctorSymptomes) -> None:
        self._service.create(doctor_symptome)

    def find_all_relations(self) -> List[DoctorSymptomes]:
        return self._service.get_all_relations()

    def find_symptomes_by_doctor(self, doctor_id: int) -> List[DoctorSymptomes]:

        return self._service.get_symptomes_by_doctor(doctor_id)

    def find_doctors_by_symptome(self, symptome_id: int) -> List[DoctorSymptomes]:

        return self._service.get_doctors_by_symptome(symptome_id)

    def delete_relation(self, doctor_id: int, symptome_id: int) -> None:

        self._service.delete_relation(doctor_id, symptome_id)

    def find_with_details(self):
        """
        Викликає сервіс для отримання зв'язків між лікарями і симптомами разом з деталями.
        """
        return self._service.find_with_details()