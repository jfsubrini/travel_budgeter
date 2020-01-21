# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Connection to the Currency Converter Restful API to get the currencies exchange rates."""

import requests

from .config import CURRCONV_API_KEY


class CurrencyConverter:
    """
    Getting the currency exchange rate by requesting the Currency Converter Restful API.
    """

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
        rate = curr_conv[currencies][str(self.date)]
        return rate
