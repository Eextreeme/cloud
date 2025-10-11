from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.doctors import Doctors
from sqlalchemy.orm import joinedload


class DoctorsDAO(GeneralDAO):
    _domain_type = Doctors

    def create(self, doctor: Doctors) -> None:
        self._session.add(doctor)
        self._session.commit()

    def find_all(self) -> List[Doctors]:
        return self._session.query(Doctors).all()

    def find_with_specialty(self):
        return (
            self._session.query(Doctors)
            .options(
                joinedload(Doctors.specialty),
            )
            .all()
        )
    def find_by_id(self, doctor_id: int) -> Doctors:
        return self._session.query(Doctors).filter(Doctors.doctor_id == doctor_id).first()