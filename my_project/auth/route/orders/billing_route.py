from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import billing_controller
from my_project.auth.domain.orders.billing import Billing

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')
@billing_bp.get('')
def get_all_bills() -> Response:
    bills = billing_controller.find_all()
    bills_dto = [bill.put_into_dto() for bill in bills]
    return make_response(jsonify(bills_dto), HTTPStatus.OK)

@billing_bp.post('')
def create_bill() -> Response:
    content = request.get_json()
    bill = Billing.create_from_dto(content)
    billing_controller.create_bill(bill)
    return make_response(jsonify(bill.put_into_dto()), HTTPStatus.CREATED)

@billing_bp.get('/<int:bill_id>')
def get_bill(bill_id: int) -> Response:
    bill = billing_controller.find_by_id(bill_id)
    if bill:
        return make_response(jsonify(bill.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Bill not found"}), HTTPStatus.NOT_FOUND)

@billing_bp.put('/<int:bill_id>')
def update_bill(bill_id: int) -> Response:
    content = request.get_json()
    bill = Billing.create_from_dto(content)
    billing_controller.update_bill(bill_id, bill)
    return make_response("Bill updated", HTTPStatus.OK)

@billing_bp.delete('/<int:bill_id>')
def delete_bill(bill_id: int) -> Response:
    billing_controller.delete_bill(bill_id)
    return make_response("Bill deleted", HTTPStatus.NO_CONTENT)