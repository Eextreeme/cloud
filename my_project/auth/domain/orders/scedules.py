from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto



class Schedules(db.Model, IDto):
    __tablename__ = "schedules"

    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    day_of_week = db.Column(db.String(15))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __repr__(self) -> str:
        return f"Schedules({self.schedule_id}, {self.doctor_id}, '{self.day_of_week}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "schedule_id": self.schedule_id,
            "doctor_id": self.doctor_id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Schedules:
        return Schedules(**dto_dict)