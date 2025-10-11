from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto

class Doctors(db.Model, IDto):
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialties.specialty_id"))
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(100))

    symptomes = db.relationship("DoctorSymptomes", back_populates="doctor", cascade="all, delete")

    specialty = db.relationship('Specialties', back_populates="doctors")

    def put_into_large_dto(self) -> Dict[str, Any]:
        return {
            "doctor_id": self.doctor_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialty": self.specialty.put_into_dto() if self.specialty else None,
            "phone_number": self.phone_number,
            "email": self.email,
        }

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "doctor_id": self.doctor_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialty_id": self.specialty_id,
            "phone_number": self.phone_number,
            "email": self.email,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Doctors:
        return Doctors(**dto_dict)