from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto


class Billing(db.Model, IDto):
    __tablename__ = "billing"

    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'))
    total_amount = db.Column(db.Float)
    payment_status = db.Column(db.String(20))
    payment_method = db.Column(db.String(50))
    billing_date = db.Column(db.Date)

    def __repr__(self) -> str:
        return f"Billing({self.bill_id}, {self.appointment_id}, {self.total_amount}, '{self.payment_status}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "bill_id": self.bill_id,
            "appointment_id": self.appointment_id,
            "total_amount": self.total_amount,
            "payment_status": self.payment_status,
            "payment_method": self.payment_method,
            "billing_date": self.billing_date,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Billing:
        return Billing(**dto_dict)