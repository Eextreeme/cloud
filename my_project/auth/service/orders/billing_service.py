from typing import List
from my_project.auth.dao import billing_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain.orders.billing import Billing

class BillingService(GeneralService):
    _dao = billing_dao

    def create(self, bill: Billing) -> None:
        self._dao.create(bill)

    def update(self, bill_id: int, bill: Billing) -> None:
        self._dao.update(bill_id, bill)

    def get_all_bills(self) -> List[Billing]:
        return self._dao.find_all()

    def get_bill_by_id(self, bill_id: int) -> Billing:
        return self._dao.find_by_id(bill_id)