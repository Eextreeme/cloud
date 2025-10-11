from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import schedules_controller
from my_project.auth.domain.orders.scedules import Schedules

schedules_bp = Blueprint('schedules', __name__, url_prefix='/schedules')

@schedules_bp.get('')
def get_all_schedules() -> Response:
    schedules = schedules_controller.find_all()
    schedules_dto = [schedule.put_into_dto() for schedule in schedules]
    return make_response(jsonify(schedules_dto), HTTPStatus.OK)

@schedules_bp.post('')
def create_schedule() -> Response:
    content = request.get_json()
    schedule = Schedules.create_from_dto(content)
    schedules_controller.create_schedule(schedule)
    return make_response(jsonify(schedule.put_into_dto()), HTTPStatus.CREATED)

@schedules_bp.get('/<int:schedule_id>')
def get_schedule(schedule_id: int) -> Response:
    schedule = schedules_controller.find_by_id(schedule_id)
    if schedule:
        return make_response(jsonify(schedule.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Schedule not found"}), HTTPStatus.NOT_FOUND)

@schedules_bp.put('/<int:schedule_id>')
def update_schedule(schedule_id: int) -> Response:
    content = request.get_json()
    schedule = Schedules.create_from_dto(content)
    schedules_controller.update_schedule(schedule_id, schedule)
    return make_response("Schedule updated", HTTPStatus.OK)

@schedules_bp.delete('/<int:schedule_id>')
def delete_schedule(schedule_id: int) -> Response:
    schedules_controller.delete_schedule(schedule_id)
    return make_response("Schedule deleted", HTTPStatus.NO_CONTENT)