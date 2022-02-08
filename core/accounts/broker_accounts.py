from brokerage.rest import Broker
from core.user.models import User
from core.accounts.models import TradingAccounts, Agreements
from django.core.exceptions import ObjectDoesNotExist

from core.utils import utcisoformat


class AccountBrokerServices:
    brokerage = Broker()

    def __init__(self, user: User):
        self.user: User = user

    def check_user_credentials(self):
        for creds in self.user.trade_requirements_status:
            if not self.user.trade_requirements_status[creds] and not creds == 'bank':
                raise ValueError(f"please complete your {creds} credentials")

    def set_submit_payload(self):
        identity = self.user.user_detail_info.dict_fields()
        contact = self.user.user_contact_info.dict_fields()
        disclosures = self.user.user_disclosures_info.dict_fields()
        agreement = [
            {
                "agreement": agreement.get_agreement_display(),
                "signed_at": agreement.signed_at.replace(microsecond=0).isoformat() + "Z",
                "ip_address": agreement.ip_address,
                "revision": "16.2021.05"
            }
            for agreement in Agreements.objects.filter(user=self.user)
        ]
        payload = dict(
            identity=identity,
            contact=contact,
            disclosures=disclosures,
            agreements=agreement
        )
        print(payload)
        return payload

    def activate_account(self):
        payload = self.set_submit_payload()
        response =  self.brokerage.create_account(payload)
        response = response['account']
        TradingAccounts.objects.create(
            trading_account_id=response['id'],
            current_status=response['status']
        )

    def get_trading_accounts(self):
        self.check_user_credentials()
        try:
            trade_account = self.user.user_trading_account
            return trade_account
        except ObjectDoesNotExist:
            self.activate_account()
