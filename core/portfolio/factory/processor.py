class SellOrderProcessor:
    getter_price = RkdGetterPrice()

    def __init__(self, payload: dict, getterprice: GetPriceProtocol = None):
        self.payload: SellPayload = SellPayload(**payload)
        self.validator: ValidatorProtocol = SellValidator(self.payload)
        if getterprice:
            self.getter_price = getterprice

    def execute(self):
        self.payload.price = self.getter_price.get_price(
            [self.payload.ticker.ticker]
        )
        with db_transaction.atomic():
            position = self.validator.position
            bot = position.bot
            trading_day = timezone.now()
            if bot.is_ucdc():
                positions, self.response = ucdc_sell_position(self.payload.price, trading_day, position, apps=True)
            elif bot.is_uno():
                positions, self.response = uno_sell_position(self.payload.price, trading_day, position, apps=True)
            elif bot.is_classic():
                positions, self.response = classic_sell_position(self.payload.price, trading_day, position, apps=True)
            elif bot.is_stock():
                positions, self.response = user_sell_position(self.payload.price, trading_day, position, apps=True)


class BuyOrderProcessor:
    getter_price = RkdGetterPrice()
    response: Order

    def __init__(self, payload: dict, getterprice: GetPriceProtocol = None):
        self.raw_payload = payload
        self.payload = BuyPayload(**payload)
        self.validator: ValidatorProtocol = BuyValidator(self.payload)
        if getterprice:
            self.getter_price = getterprice

    def execute(self):
        self.raw_payload["price"] = self.getter_price.get_price(
            [self.payload.ticker.ticker]
        )
        with db_transaction.atomic():
            self.response = Order.objects.create(
                **self.raw_payload, order_type="apps", is_init=True
            )