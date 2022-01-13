from core.user.models import User
from core.portfolio.models import BotOptionType
from core.universe.models import Universe
from dataclasses import dataclass
from core.services.convert import ConvertMoney
@dataclass
class BotCreateProps(BaseDatavalidation):
    ticker: str
    spot_date: datetime.date
    created: datetime
    expiry: datetime.date
    investment_amount: float
    price: float
    margin: int
    currency: str
    bot: BotOptionType
    bot_id: str

    def __init__(
        self,
        ticker: str,
        spot_date: datetime,
        investment_amount: float,
        price: float,
        bot_id: str,
        margin: int = 1,
    ):
        self.ticker = ticker
        self.spot_date = spot_date.date()
        self.created = spot_date
        self.investment_amount = investment_amount * margin
        self.price = price
        self.bot_id = bot_id
        self.currency = self.get_ticker_currency()
        self.margin = margin

    def get_ticker_currency(self) -> str:
        try:
            ticker = Universe.objects.get(ticker=self.ticker)
        except Universe.DoesNotExist:
            raise ValueError(f"Ticker {self.ticker} not found in Universe")
        return ticker.currency_code.currency_code

    def validate(self):
        self.validate_ticker_is_active(self.ticker)
        self.get_bot(self.bot_id)
        self.set_time_to_exp(self.bot.time_to_exp)
        self.set_expiry_date()
    
@dataclass
class SellPayload:
    setup: dict
    side: str
    ticker: Universe
    user_id: User
    margin:int


@dataclass
class BuyPayload:
    amount: float
    bot_id: str
    price: float
    side: str
    ticker: str
    user_id: str
    margin: int

    @property
    def c_amount(self):
        converter = ConvertMoney(self.user_id.user_balance.currency_code, self.ticker.currency_code)
        return converter.convert(self.amount)