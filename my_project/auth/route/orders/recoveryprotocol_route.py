from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import recovery_protocol_controller
from my_project.auth.domain.orders.recoveryprotocol import RecoveryProtocol

recovery_protocol_bp = Blueprint('recovery_protocol', __name__, url_prefix='/recovery_protocol')

@recovery_protocol_bp.get('')
def get_all_recovery_protocols() -> Response:
    protocols = recovery_protocol_controller.find_all()
    protocols_dto = [protocol.put_into_dto() for protocol in protocols]
    return make_response(jsonify(protocols_dto), HTTPStatus.OK)

@recovery_protocol_bp.post('')
def create_recovery_protocol() -> Response:
    content = request.get_json()
    protocol = RecoveryProtocol.create_from_dto(content)
    recovery_protocol_controller.create_recovery_protocol(protocol)
    return make_response(jsonify(protocol.put_into_dto()), HTTPStatus.CREATED)

@recovery_protocol_bp.get('/<int:protocol_id>')
def get_recovery_protocol(protocol_id: int) -> Response:
    protocol = recovery_protocol_controller.find_by_id(protocol_id)
    if protocol:
        return make_response(jsonify(protocol.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Recovery Protocol not found"}), HTTPStatus.NOT_FOUND)

@recovery_protocol_bp.put('/<int:protocol_id>')
def update_recovery_protocol(protocol_id: int) -> Response:
    content = request.get_json()
    protocol = RecoveryProtocol.create_from_dto(content)
    recovery_protocol_controller.update_recovery_protocol(protocol_id, protocol)
    return make_response("Recovery Protocol updated", HTTPStatus.OK)

@recovery_protocol_bp.delete('/<int:protocol_id>')
def delete_recovery_protocol(protocol_id: int) -> Response:
    recovery_protocol_controller.delete_recovery_protocol(protocol_id)
    return make_response("Recovery Protocol deleted", HTTPStatus.NO_CONTENT)