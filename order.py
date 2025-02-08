# order.py

from fyers_apiv3 import fyersModel
from config import CLIENT_ID

class Order:
    def __init__(self, access_token):
        self.access_token = access_token
        self.fyers = fyersModel.FyersModel(token=self.access_token, is_async=False, client_id=CLIENT_ID, log_path="")

    def retrieve_all_order(self):
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        global orderBooks
        fyers = fyersModel.FyersModel(client_id=CLIENT_ID, token=self.access_token, is_async=False, log_path="")

        response = fyers.orderbook()
        if response["code"] == 200 and response["s"] == "ok":
            orderBooks = response["orderBook"]
            print(
                "-------------------------------------------------ALL ORDERS---------------------------------------------------")
        else:
            print("Error: \n" + response["code"] + " -  " + response["message"])

        if not orderBooks:
            print("Empty Order List.")
        else:
            for orderBook in orderBooks:
                print("\n Order No: ", orderBook["slNo"])
                print("Order ID: ", orderBook["id"])  # Corrected here
                print("Symbol: ", orderBook["symbol"])
                print("Client ID: ", orderBook["clientId"])
                print("PAN: ", orderBook["pan"])

                if orderBook["exchange"] == 10:
                    print("Exchange: NSE(National Stock Exchange)")
                elif orderBook["exchange"] == 11:
                    print("Exchange: MCX(Multi Commodity Exchange)")
                else:
                    print("Exchange: BSE(Bombay Stock Exchange)")

                if orderBook["status"] == 1:
                    print("Status: Canceled")
                elif orderBook["status"] == 2:
                    print("Status: Traded/Filled")
                elif orderBook["status"] == 4:
                    print("Status: Transit")
                elif orderBook["status"] == 5:
                    print("Status: Rejected")
                else:
                    print("Status: Pending")

                if orderBook["segment"] == 10:
                    print("Segment: Capital Market")
                elif orderBook["segment"] == 11:
                    print("Segment: Equity Derivatives")
                elif orderBook["segment"] == 12:
                    print("Segment: Currency Derivatives")
                else:
                    print("Segment: Commodity Derivatives)")

                print("Limit Price: ", orderBook["limitPrice"])
                print("Stop Price: ", orderBook["stopPrice"])

                if orderBook["type"] == 1:
                    print("Limit Order")
                elif orderBook["type"] == 2:
                    print("Market Order")
                elif orderBook["type"] == 3:
                    print("Stop Order (SL-M)")
                else:
                    print("StopLimit Order (SL-L)")

                if orderBook["side"] == 1:
                    print("Order For: BUY")
                else:
                    print("Order For: SELL")

                print("Order Validity: ", orderBook["orderValidity"])
                print("Order Date & Time: ", orderBook["orderDateTime"])

                print("Quantity:", orderBook["qty"])
                print("Remaining Quantity: ", orderBook["remainingQuantity"])
                print("Filled Quantity: ", orderBook["filledQty"])
                print("Disclosed Quantity: ", orderBook["disclosedQty"])

    def place_single_order(self, data):
        fyers = fyersModel.FyersModel(client_id=CLIENT_ID, token=self.access_token,is_async=False, log_path="")
        response = fyers.place_order(data=data)
        return response["message"]

    def place_multi_orders(self, data):
        return self.fyers.place_basket_orders(data)

    def modify_order(self, data):
        return self.fyers.modify_order(data)

    def cancel_order(self, data):
        return self.fyers.cancel_order(data)

    def cancel_multi_orders(self, data):
        return self.fyers.cancel_basket_orders(data)

    def exit_position(self, data):
        return self.fyers.exit_positions(data)

    def convert_position(self, data):
        return self.fyers.convert_position(data)
