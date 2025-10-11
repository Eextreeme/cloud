from typing import List
from my_project.auth.service import recovery_protocol_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.recoveryprotocol import RecoveryProtocol


class RecoveryProtocolController(GeneralController):
    _service = recovery_protocol_service

    def create_recovery_protocol(self, protocol: RecoveryProtocol) -> None:
        self._service.create(protocol)

    def find_all(self) -> List[RecoveryProtocol]:
        return self._service.get_all_recovery_protocols()

    def find_by_id(self, protocol_id: int) -> RecoveryProtocol:
        return self._service.get_recovery_protocol_by_id(protocol_id)

    def update_recovery_protocol(self, protocol_id: int, protocol: RecoveryProtocol) -> None:
        self._service.update(protocol_id, protocol)

    def delete_recovery_protocol(self, protocol_id: int) -> None:
        self._service.delete(protocol_id)