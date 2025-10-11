from typing import List
from my_project.auth.dao import recovery_protocol_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.recoveryprotocol import RecoveryProtocol

class RecoveryProtocolService(GeneralService):
    _dao = recovery_protocol_dao

    def create(self, protocol: RecoveryProtocol) -> None:
        self._dao.create(protocol)

    def update(self, protocol_id: int, protocol: RecoveryProtocol) -> None:
        self._dao.update(protocol_id, protocol)

    def get_all_recovery_protocols(self) -> List[RecoveryProtocol]:
        return self._dao.find_all()

    def get_recovery_protocol_by_id(self, protocol_id: int) -> RecoveryProtocol:
        return self._dao.find_by_id(protocol_id)