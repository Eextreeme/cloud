from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto


class Symptomes(db.Model):
    __tablename__ = "symptomes"

    symptome_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symptome_name = db.Column(db.String(100), nullable=False)

    doctors = db.relationship("DoctorSymptomes", back_populates="symptome", cascade="all, delete")

    def __repr__(self) -> str:
        return f"Symptomes({self.symptome_id}, '{self.symptome_name}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "symptome_id": self.symptome_id,
            "symptome_name": self.symptome_name,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Symptomes:
        return Symptomes(**dto_dict)