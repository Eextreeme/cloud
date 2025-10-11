from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto


class AppointmentBookings(db.Model, IDto):
    __tablename__ = "appointment_bookings"

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'))
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)

    def __repr__(self) -> str:
        return f"AppointmentBookings({self.booking_id}, {self.appointment_id})"


    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "booking_id": self.booking_id,
            "appointment_id": self.appointment_id,
            "booking_date": self.booking_date,
            "booking_time": self.booking_time,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> AppointmentBookings:
        return AppointmentBookings(**dto_dict)