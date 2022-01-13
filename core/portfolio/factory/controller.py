from core.portfolio.factory.protocol import OrderProtocol
from dataclasses import dataclass, field
from rest_framework import exceptions

class OrderController:
    def process(self, protocol: OrderProtocol):
        protocol.validator.validate()
        try:
            protocol.execute()
        except Exception as e:
            raise exceptions.APIException({"detail": str(e)})
        return protocol.response
    
OrderProcessor: dict = {
    "buy": BuyOrderProcessor,
    "sell": SellOrderProcessor,
    "action": ActionProcessor,
}