import requests
import json
from config import keys


class ConversionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConversionException(f"Нет смысла переводить {keys[quote]} в {keys[base]}...")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {quote}...")
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {base}...")
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f"Не удалось высчитать количество {amount}...")

        req = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        price = json.loads(req.content)[keys[base]]

        return price
