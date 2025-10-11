# """
# 2022
# apavelchak@gmail.com
# © Andrii Pavelchak
# """

from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto


class Appointments(db.Model, IDto):
    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    consultation_fee = db.Column(db.Float)

    def __repr__(self) -> str:
        return f"Appointments({self.appointment_id}, {self.doctor_id}, {self.patient_id}, '{self.appointment_date}', '{self.appointment_time}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "appointment_id": self.appointment_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "appointment_date": self.appointment_date,
            "appointment_time": self.appointment_time,
            "consultation_fee": self.consultation_fee,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Appointments:
        return Appointments(**dto_dict)
