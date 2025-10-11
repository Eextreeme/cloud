from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import doctorsymptomes_controller
from my_project.auth.domain.orders.doctorsymptomes import DoctorSymptomes

doctor_symptomes_bp = Blueprint('doctor_symptomes', __name__, url_prefix='/doctor_symptomes')

@doctor_symptomes_bp.get('')
def get_all_relations() -> Response:
    """
    Отримати всі зв'язки між лікарями і симптомами.
    """
    relations = doctorsymptomes_controller.find_all_relations()
    relations_dto = [relation.put_into_dto() for relation in relations]
    return make_response(jsonify(relations_dto), HTTPStatus.OK)

@doctor_symptomes_bp.post('')
def create_relation() -> Response:
    """
    Створити новий зв'язок між лікарем і симптомом.
    """
    content = request.get_json()
    relation = DoctorSymptomes.create_from_dto(content)
    doctorsymptomes_controller.create_relation(relation)
    return make_response(jsonify(relation.put_into_dto()), HTTPStatus.CREATED)

@doctor_symptomes_bp.get('/by_doctor/<int:doctor_id>')
def get_symptomes_by_doctor(doctor_id: int) -> Response:
    """
    Отримати всі симптоми, пов'язані з конкретним лікарем.
    """
    relations = doctorsymptomes_controller.find_symptomes_by_doctor(doctor_id)
    if not relations:
        return make_response(jsonify({"error": "No symptomes found for this doctor"}), HTTPStatus.NOT_FOUND)
    symptomes_dto = [relation.symptome.put_into_dto() for relation in relations]
    return make_response(jsonify(symptomes_dto), HTTPStatus.OK)

@doctor_symptomes_bp.get('/by_symptome/<int:symptome_id>')
def get_doctors_by_symptome(symptome_id: int) -> Response:
    """
    Отримати всіх лікарів, пов'язаних із конкретним симптомом.
    """
    relations = doctorsymptomes_controller.find_doctors_by_symptome(symptome_id)
    if not relations:
        return make_response(jsonify({"error": "No doctors found for this symptome"}), HTTPStatus.NOT_FOUND)
    doctors_dto = [relation.doctor.put_into_dto() for relation in relations]
    return make_response(jsonify(doctors_dto), HTTPStatus.OK)

@doctor_symptomes_bp.delete('/<int:doctor_id>/<int:symptome_id>')
def delete_relation(doctor_id: int, symptome_id: int) -> Response:
    """
    Видалити зв'язок між лікарем і симптомом.
    """
    doctorsymptomes_controller.delete_relation(doctor_id, symptome_id)
    return make_response("Relation deleted", HTTPStatus.NO_CONTENT)

@doctor_symptomes_bp.get('/all')
def get_all_details() -> Response:
    """
    Отримати всі зв'язки між лікарями і симптомами з іменами лікарів і назвами симптомів.
    """
    details = doctorsymptomes_controller.find_with_details()
    # Перетворення кожного рядка у словник
    details_dto = [row._asdict() for row in details]
    return make_response(jsonify(details_dto), HTTPStatus.OK)