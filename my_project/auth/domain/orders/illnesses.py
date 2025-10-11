# """
# 2022
# apavelchak@gmail.com
# © Andrii Pavelchak
# """

from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto


class Illnesses(db.Model, IDto):
    __tablename__ = "illneses"

    illness_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    illness_name = db.Column(db.String(100), nullable=False)
    treatment_plan = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"Illnesses({self.illness_id}, '{self.illness_name}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "illness_id": self.illness_id,
            "illness_name": self.illness_name,
            "treatment_plan": self.treatment_plan,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Illnesses:
        return Illnesses(**dto_dict)