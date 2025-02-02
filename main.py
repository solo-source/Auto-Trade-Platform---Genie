# main.py
from cProfile import Profile

from auth import Auth
from order import Order
from data import MarketData
from utils import log_error, log_info
from user_api import Profile


def main():
    # Step 1: Authenticate the user and get access token
    auth = Auth()
    auth.generate_auth_code()
    auth_code = input("Enter the generated auth code: ")
    access_token = auth.generate_access_token(auth_code)

    if not access_token:
        log_error("Failed to get access token", "")
        return

    # # Step 2: Place orders and fetch data
    # order = Order(access_token)
    # data = {
    #     "symbol": "NSE:ONGC-EQ",
    #     "qty": 1,
    #     "type": 1,
    #     "side": 1,
    #     "productType": "INTRADAY",
    #     "limitPrice": 0,
    #     "stopPrice": 0,
    #     "validity": "DAY",
    #     "disclosedQty": 0,
    #     "offlineOrder": "False",
    #     "stopLoss": 0,
    #     "takeProfit": 0
    # }
    # order_response = order.place_single_order(data)
    # log_info(f"Order Response: {order_response}")

    # # Fetch market data
    # market_data = MarketData(access_token)
    # historical_data = market_data.get_history({"symbol": "NSE:NIFTY50-INDEX", "resolution": "D", "date_format": "0"})
    # log_info(f"Historical Data: {historical_data}")

    #get user profile
    userProfile = Profile(access_token)
    userProfile.generate_profile()
    userProfile.get_available_funds()
    userProfile.get_user_holdings()


    orders = Order(access_token)
    orders.retrieve_all_order()



if __name__ == "__main__":
    main()
