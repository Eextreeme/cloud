from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.billing import Billing

class BillingDAO(GeneralDAO):
    _domain_type = Billing

    def create(self, bill: Billing) -> None:
        self._session.add(bill)
        self._session.commit()

    def find_all(self) -> List[Billing]:
        return self._session.query(Billing).all()

    def find_by_id(self, bill_id: int) -> Billing:
        return self._session.query(Billing).filter(Billing.bill_id == bill_id).first()