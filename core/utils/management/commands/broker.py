from django.core.management.base import BaseCommand
from brokerage.rest import Broker

from datetime import datetime
main_id = 'a234caae-b645-4486-876f-306c709e4b4c'
class Command(BaseCommand):
    def handle(self, *args, **options):
        clearing_data = {
  "account_owner_name": "Rede Akbar",
  "bank_account_type": "SAVINGS",
  "bank_account_number": "32131231abc",
  "bank_routing_number": "121000358",
  "nickname": "Bank BNI"
}
        create_data = {
            "contact": {
    "email_address": "ribonred@gmail.com",
    "phone_number": "555-666-7788",
    "street_address": ["20 N San Mateo Dr"],
    "unit": "Apt 1A",
    "city": "San Mateo",
    "state": "CA",
    "postal_code": "94401",
    "country": "USA"
  },
  "identity": {
    "given_name": "Rede",
    "middle_name": "akbar",
    "family_name": "wijaya",
    "date_of_birth": "1988-08-12",
    "tax_id": "666-55-4321",
    "tax_id_type": "USA_SSN",
    "country_of_citizenship": "USA",
    "country_of_birth": "USA",
    "country_of_tax_residence": "USA",
    "funding_source": ["employment_income"]
  },
  "disclosures": {
    "is_control_person": False,
    "is_affiliated_exchange_or_finra": False,
    "is_politically_exposed": False,
    "immediate_family_exposed": False
  },
  "agreements": [
    {
      "agreement": "margin_agreement",
      "signed_at": datetime.utcnow().isoformat() + "Z",
      "ip_address": "185.13.21.99",
      "revision": "16.2021.05"
    },
    {
      "agreement": "account_agreement",
      "signed_at": datetime.utcnow().isoformat() + "Z",
      "ip_address": "185.13.21.99",
      "revision": "16.2021.05"
    },
    {
      "agreement": "customer_agreement",
      "signed_at": datetime.utcnow().isoformat() + "Z",
      "ip_address": "185.13.21.99",
      "revision": "16.2021.05"
    }
  ],
        }
        broker = Broker()
        # resp = broker.get_account(main_id)
        resp = broker.get_trading_account('9485782d-40d7-3365-aaf5-f5f44d78e755')
        
        # resp = broker.create_account(create_data)
        # resp = broker.get_transfer_data_all('5e20df35-bbd0-41ee-be48-d809673bf0a0')
        # resp = broker.delete_transfer_data_id('9485782d-40d7-3365-aaf5-f5f44d78e755','7ac5ee81-2bb5-4a4b-bdc1-aee92741c6ec')
        # resp =broker.create_clearing_house_relationship(main_id,clearing_data)
        # resp =  broker.deposit_account(main_id,"50000")
        print(resp)

        
        # 2020-09-11T18:09:33Z