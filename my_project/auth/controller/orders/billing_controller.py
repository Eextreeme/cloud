from typing import List
from my_project.auth.service import billing_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain.orders.billing import Billing


class BillingController(GeneralController):
    _service = billing_service

    def create_bill(self, bill: Billing) -> None:
        self._service.create(bill)

    def find_all(self) -> List[Billing]:
        return self._service.get_all_bills()

    def find_by_id(self, bill_id: int) -> Billing:
        return self._service.get_bill_by_id(bill_id)

    def update_bill(self, bill_id: int, bill: Billing) -> None:
        self._service.update(bill_id, bill)

    def delete_bill(self, bill_id: int) -> None:
        self._service.delete(bill_id)