# data.py

from fyers_apiv3 import fyersModel
from config import CLIENT_ID
import datetime


def fetch_data_from_fyers_api(symbol, interval):
    """ Fetch real-time data from Fyers API for the given symbol and interval """
    pass


class MarketData:
    def __init__(self, access_token):
        self.access_token = access_token
        self.fyers = fyersModel.FyersModel(client_id=CLIENT_ID, token=self.access_token, is_async=False, log_path="")

    def get_real_time_data(self, symbol, interval = "5m"):
        """Fetch real-time data at 5-minute intervals."""
        # Assuming a method that fetches the latest 5-minute data
        # Modify it according to the way data is fetched in your codebase
        data = fetch_data_from_fyers_api(symbol, interval)  # Your method here
        return data


    def get_history(self, data):
        return self.fyers.history(data = data)

    def get_quotes(self, data):
        return self.fyers.quotes(data = data)

    def get_depth(self, data):
        return self.fyers.depth(data = data)

    def option_chain(self, data):
        return self.fyers.optionchain(data = data)