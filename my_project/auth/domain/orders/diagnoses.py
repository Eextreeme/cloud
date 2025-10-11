from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto


class Diagnoses(db.Model, IDto):
    __tablename__ = "diagnoses"

    diagnosis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    illness_id = db.Column(db.Integer, db.ForeignKey('illneses.illness_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    diagnosis_date = db.Column(db.Date, nullable=False)

    def __repr__(self) -> str:
        return f"Diagnoses({self.diagnosis_id}, {self.illness_id}, {self.doctor_id}, {self.patient_id})"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "diagnosis_id": self.diagnosis_id,
            "illness_id": self.illness_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "diagnosis_date": self.diagnosis_date,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Diagnoses:
        return Diagnoses(**dto_dict)