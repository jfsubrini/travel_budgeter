# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods,unnecessary-comprehension
"""Connection to the Currency Converter Restful API to get the currencies exchange rates."""

import requests

from .config import CURRCONV_API_KEY


class CurrencyConverter:
    """ Class definition finding the coordinates of the place to find
    and returning the latitude, longitude and the address of that place.
    """  # TODO

    def __init__(self, currency_in, currency_out, date):
        self.currency_in = currency_in
        self.currency_out = currency_out
        self.date = date

    def exchange(self):
        """ Currency Converter REST API """
        currencies = f"{self.currency_in}_{self.currency_out}"
        payload = {
            "q": currencies,
            "compact": "ultra",
            "date": self.date,
            "apiKey": CURRCONV_API_KEY,
        }
        response = requests.get(
            "https://free.currconv.com/api/v7/convert?", params=payload
        )
        curr_conv = response.json()
        rate = curr_conv[currencies][self.date]
        return rate


if __name__ == "__main__":
    # CurrencyConverter instance creation.
    EXCHANGE_RATE = CurrencyConverter("EUR", "PEN", "2020-01-17")
    RATE = EXCHANGE_RATE.exchange()
    print("RATE = ", RATE)
    # /api/v7/currencies?apiKey=[YOUR_API_KEY]
    # /api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&date=[yyyy-mm-dd]&apiKey=[YOUR_API_KEY]
    # /api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&date=[yyyy-mm-dd]&endDate=[yyyy-mm-dd]&apiKey=[YOUR_API_KEY]
