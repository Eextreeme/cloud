from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto

class Patients(db.Model, IDto):
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"Patients({self.patient_id}, '{self.first_name}', '{self.last_name}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Patients:
        return Patients(**dto_dict)