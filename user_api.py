from fyers_apiv3 import fyersModel
from config import CLIENT_ID


class Profile:
    def __init__(self, access_token):
        self.access_token = access_token

    def generate_profile(self):
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        self.fyers = fyersModel.FyersModel(
            client_id=CLIENT_ID, is_async=False, token=self.access_token, log_path=""
        )

        # Make a request to get the user profile information
        response = self.fyers.get_profile()

        # Print the response received from the Fyers API
        if response["code"] == 200 and response["s"] == "ok":
            user_data = response["data"]
            print(
                "##########################################################################################################"
            )
            print("Fyers Client ID: " + user_data["fy_id"])
            print("Name: " + user_data["name"])
            print("Email: " + user_data["email_id"])
            print(
                "##########################################################################################################"
            )
        else:
            print("Error: \n" + response["code"] + " -  " + response["message"])

    def get_available_funds(self):
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        self.fyers = fyersModel.FyersModel(
            client_id=CLIENT_ID, is_async=False, token=self.access_token, log_path=""
        )

        # Make a request to get the funds information
        response = self.fyers.funds()

        if response["code"] == 200 and response["s"] == "ok":
            fund_limits = response["fund_limit"]
            print(
                "\n\n===================================================USER FUNDS======================================================="
            )
            for fund_limit in fund_limits:
                # print(f"\nFund ID: {fund_limit['id']}")
                print(f"\n--------", fund_limit["title"], "--------")
                print("Equity Amount:", fund_limit["equityAmount"])
                print("Commodity Amount:", fund_limit["commodityAmount"])
        else:
            print("Error: \n" + response["code"] + " -  " + response["message"])

    def get_user_holdings(self):
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        self.fyers = fyersModel.FyersModel(
            client_id=CLIENT_ID, is_async=False, token=self.access_token, log_path=""
        )

        response = self.fyers.holdings()

        if response["code"] == 200 and response["s"] == "ok":
            overall = response["overall"]

            print(
                "\n\n================================================= HOLDINGS ==================================================="
            )
            print("Total No. of Holdings: ", overall["count_total"])
            print("Total Investment: ", overall["total_investment"])
            print("Present Value of Holdings: ", overall["total_current_value"])
            print("Total Profit/Loss Made: ", overall["total_pl"])
            print("PNL Percentage: ", overall["pnl_perc"])
            print("\n")

            print(
                "----------------------------------------------HOLDINGS DETAILS------------------------------------------------"
            )
            holdings = response["holdings"]

            if not holdings:
                print("Empty Holdings List.")
            else:
                for holding in holdings:
                    print("f\n--------", holding["symbol"], "--------")
                    if holding["holdingType"] == "HLD":
                        print(
                            "Holding Type: ",
                            holding["holdingType"],
                            "(Purchased and available in Demat Account)",
                        )
                    else:
                        print(
                            "Holding Type: ",
                            holding["holdingType"],
                            "(Purchased but not yet delivered in Demat Account)",
                        )
                    print("Quantity: ", holding["quantity"])
                    print("Remaining Quantity: ", holding["remainingQuantity"])
                    print("Profit/Loss Made: ", holding["pl"])
                    print("Cost Price: ", holding["costPrice"])
                    print("Market Value: ", holding["marketVal"])
                    print("LTP: ", holding["ltp"])

                    if holding["exchange"] == 10:
                        print("Exchange: NSE(National Stock Exchange)")
                    elif holding["exchange"] == 11:
                        print("Exchange: MCX(Multi Commodity Exchange)")
                    else:
                        print("Exchange: BSE(Bombay Stock Exchange)")

                    if holding["segment"] == 10:
                        print("Segment: Capital Market")
                    elif holding["segment"] == 11:
                        print("Segment: Equity Derivatives")
                    elif holding["segment"] == 12:
                        print("Segment: Currency Derivatives")
                    else:
                        print("Segment: Commodity Derivatives)")

                    print("Pledged Quantity: ", holding["collateralQuantity"])
                    print("Remaining Pledged Quantity: ", holding["remainingPledgedQuantity"])
        else:
            print("Error: \n" + response["code"] + " -  " + response["message"])

    def get_user_positions(self):
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        self.fyers = fyersModel.FyersModel(
            client_id=CLIENT_ID, is_async=False, token=self.access_token, log_path=""
        )

        response = self.fyers.positions()

        if response["code"] == 200 and response["s"] == "ok":
            netPositions = response["netPositions"]
            overall = response["overall"]
