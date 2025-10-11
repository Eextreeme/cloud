from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto


class Specialties(db.Model, IDto):
    __tablename__ = "specialties"

    specialty_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialty_name = db.Column(db.String(100), nullable=False)

    doctors = db.relationship('Doctors', back_populates="specialty")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "specialty_id": self.specialty_id,
            "specialty_name": self.specialty_name,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Specialties:
        """
        Creates a Specialties instance from a DTO (dictionary).
        :param dto_dict: DTO object
        :return: Specialties instance
        """
        return Specialties(**dto_dict)