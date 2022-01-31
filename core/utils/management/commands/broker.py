from django.core.management.base import BaseCommand
from brokerage.rest import Broker,MarketData

from datetime import datetime
main_id = '2e5b32c8-2282-436c-ab25-a950903666d0'
firm_id ='a64482a3-7647-3ccc-bd9e-e77f500f78e8'
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
    "email_address": "ribonred@hotmail.com",
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
    "middle_name": "zora",
    "family_name": "widodo",
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
        exchange =MarketData()
        # print(exchange.get_quote("AAPL"))
        # resp = broker.get_account(main_id)
        # resp = broker.get_trading_account(firm_id)
        
        # resp = broker.create_account(create_data)
        # resp = broker.get_transfer_data_all('5e20df35-bbd0-41ee-be48-d809673bf0a0')
        # resp = broker.delete_transfer_data_id('9485782d-40d7-3365-aaf5-f5f44d78e755','7ac5ee81-2bb5-4a4b-bdc1-aee92741c6ec')
        # resp =broker.create_clearing_house_relationship(main_id,clearing_data)
        # resp =broker.get_related_clearing_house(main_id)
        # resp =  broker.deposit_account(firm_id,"10000")
        # resp =  broker.is_open()
        # resp =  broker.transfer(firm_id,main_id,"250")
        # resp =  broker.buy_order_direct(main_id,'AAL',"250")
        # resp =  broker.sell_order_direct(main_id,'AAL',300)
        resp =  broker.retrive_transfer_data('51fcf60f-fc3f-4b10-8e25-08104d118be1')
        
        # resp =  broker.create_order_with_setup('5e20df35-bbd0-41ee-be48-d809673bf0a0',"AAPL",5,172.2,175.75,159)
        print(resp)

        
        # 2020-09-11T18:09:33Z