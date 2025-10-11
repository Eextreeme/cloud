from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto


class RecoveryProtocol(db.Model, IDto):
    __tablename__ = "recovery_protocol"

    recovery_protocol_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    recovery_plan = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"RecoveryProtocol({self.recovery_protocol_id}, {self.doctor_id}, {self.patient_id})"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "recovery_protocol_id": self.recovery_protocol_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "recovery_plan": self.recovery_plan,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> RecoveryProtocol:
        return RecoveryProtocol(**dto_dict)