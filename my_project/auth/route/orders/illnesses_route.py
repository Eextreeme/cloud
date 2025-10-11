from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import illnesses_controller
from my_project.auth.domain.orders.illnesses import Illnesses

illnesses_bp = Blueprint('illnesses', __name__, url_prefix='/illnesses')

@illnesses_bp.get('')
def get_all_illnesses() -> Response:
    illnesses = illnesses_controller.find_all()
    illnesses_dto = [illness.put_into_dto() for illness in illnesses]
    return make_response(jsonify(illnesses_dto), HTTPStatus.OK)

@illnesses_bp.post('')
def create_illness() -> Response:
    content = request.get_json()
    illness = Illnesses.create_from_dto(content)
    illnesses_controller.create_illness(illness)
    return make_response(jsonify(illness.put_into_dto()), HTTPStatus.CREATED)

@illnesses_bp.get('/<int:illness_id>')
def get_illness(illness_id: int) -> Response:
    illness = illnesses_controller.find_by_id(illness_id)
    if illness:
        return make_response(jsonify(illness.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Illness not found"}), HTTPStatus.NOT_FOUND)

@illnesses_bp.put('/<int:illness_id>')
def update_illness(illness_id: int) -> Response:
    content = request.get_json()
    illness = Illnesses.create_from_dto(content)
    illnesses_controller.update_illness(illness_id, illness)
    return make_response("Illness updated", HTTPStatus.OK)

@illnesses_bp.delete('/<int:illness_id>')
def delete_illness(illness_id: int) -> Response:
    illnesses_controller.delete_illness(illness_id)
    return make_response("Illness deleted", HTTPStatus.NO_CONTENT)