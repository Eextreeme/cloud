from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.recoveryprotocol import RecoveryProtocol

class RecoveryProtocolDAO(GeneralDAO):
    _domain_type = RecoveryProtocol

    def create(self, protocol: RecoveryProtocol) -> None:
        self._session.add(protocol)
        self._session.commit()

    def find_all(self) -> List[RecoveryProtocol]:
        return self._session.query(RecoveryProtocol).all()

    def find_by_id(self, protocol_id: int) -> RecoveryProtocol:
        return self._session.query(RecoveryProtocol).filter(RecoveryProtocol.recovery_protocol_id == protocol_id).first()