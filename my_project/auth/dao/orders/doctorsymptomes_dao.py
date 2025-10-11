from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.doctorsymptomes import DoctorSymptomes
from my_project.auth.domain.orders.doctors import Doctors
from my_project.auth.domain.orders.symptomes import Symptomes
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased
from sqlalchemy.sql import select



class DoctorSymptomesDAO(GeneralDAO):
    _domain_type = DoctorSymptomes

    def create(self, doctor_symptome: DoctorSymptomes) -> None:

        self._session.add(doctor_symptome)
        self._session.commit()

    def find_all(self) -> List[DoctorSymptomes]:

        return self._session.query(DoctorSymptomes).all()

    def find_by_doctor_id(self, doctor_id: int) -> List[DoctorSymptomes]:

        return (
            self._session.query(DoctorSymptomes)
            .filter(DoctorSymptomes.doctor_id == doctor_id)
            .options(joinedload(DoctorSymptomes.symptome))
            .all()
        )

    def get_doctor_symptome_details(self):
        results = (
            self._session.query(
                DoctorSymptomes.doctor_id,
                Doctors.first_name.label("doctor_name"),
                Symptomes.symptome_name
            )
            .join(Doctors, DoctorSymptomes.doctor_id == Doctors.doctor_id)
            .join(Symptomes, DoctorSymptomes.symptome_id == Symptomes.symptome_id)
            .all()
        )
        return results
    def find_by_symptome_id(self, symptome_id: int) -> List[DoctorSymptomes]:

        return (
            self._session.query(DoctorSymptomes)
            .filter(DoctorSymptomes.symptome_id == symptome_id)
            .options(joinedload(DoctorSymptomes.doctor))
            .all()
        )

    def find_with_details(self):

        Doctor = aliased(Doctors)
        Symptome = aliased(Symptomes)

        return (
            self._session.query(
                DoctorSymptomes.doctor_id,
                Doctor.first_name.label("doctor_name"),
                Symptome.symptome_name.label("symptome_name")
            )
            .join(Doctor, DoctorSymptomes.doctor_id == Doctor.doctor_id)
            .join(Symptome, DoctorSymptomes.symptome_id == Symptome.symptome_id)
            .all()
        )