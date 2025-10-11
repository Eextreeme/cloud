from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto


class DoctorSymptomes(db.Model, IDto):
    __tablename__ = "doctor_symptomes"

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id", ondelete="CASCADE"), primary_key=True)
    symptome_id = db.Column(db.Integer, db.ForeignKey("symptomes.symptome_id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    doctor = db.relationship("Doctors", back_populates="symptomes")
    symptome = db.relationship("Symptomes", back_populates="doctors")

    def __repr__(self) -> str:
        return f"DoctorSymptomes(doctor_id={self.doctor_id}, symptome_id={self.symptome_id})"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "doctor_id": self.doctor_id,
            "symptome_id": self.symptome_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> DoctorSymptomes:
        return DoctorSymptomes(**dto_dict)