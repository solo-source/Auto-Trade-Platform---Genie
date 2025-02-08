from fyers_apiv3.FyersWebsocket import data_ws
from config import CLIENT_ID
from order import Order  # Import the Order class to place orders
import numpy as np
import logging
import pytz
from datetime import datetime, time

# Global list to store historical closing prices
historical_prices = []

# Set up logging for better traceability
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Set IST time zone
IST = pytz.timezone('Asia/Kolkata')

# Market Open and Close Timings
MARKET_OPEN = time(9, 15)  # 9:15 AM IST
MARKET_CLOSE = time(15, 30)  # 3:30 PM IST


# Function to check if the current time is within market hours
def is_market_open():
    """
    Checks if the current time is within Indian market hours.
    :return: True if market is open, False otherwise.
    """
    current_time = datetime.now(IST).time()
    return MARKET_OPEN <= current_time <= MARKET_CLOSE


# RSI Calculation Function
def calculate_rsi(prices, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given list of prices.
    :param prices: List of historical closing prices.
    :param period: Period for RSI calculation (default is 14).
    :return: RSI value.
    """
    if len(prices) < period:
        return None  # Not enough data to calculate RSI

    gains, losses = [], []

    # Calculate price changes
    for i in range(1, period + 1):
        change = prices[-i] - prices[-(i + 1)]
        gains.append(max(0, change))
        losses.append(max(0, -change))

    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)

    if avg_loss == 0:  # Avoid division by zero
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def place_order(side, access_token):
    """
    Helper function to place a buy or sell order.
    :param side: 1 for Buy, 2 for Sell
    :param access_token: Access token in the format "CLIENT_ID:access_token"
    """
    order_data = {
        "symbol": "NSE:NIFTY50-INDEX",  # Adjust symbol as needed
        "qty": 1,  # Adjust quantity as needed
        "type": 1,  # Market order (1)
        "side": side,  # 1 for Buy, -1 for Sell
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0
    }

    order = Order(access_token)
    response = order.place_single_order(order_data)
    return response


def onmessage(message, fyers_instance, access_token):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.
    This function calculates RSI and places orders if thresholds are crossed.

    Parameters:
        message (dict): The received message from the WebSocket.
    """
    if not is_market_open():
        logger.info("Market is closed. Disconnecting WebSocket.")
        fyers_instance.disconnect()
        return

    logger.info(f"Received Message: {message}")

    # Extract the last traded price (ltp)
    if 'ltp' in message:
        close_price = message['ltp']
        historical_prices.append(close_price)

        # Keep the list size to the last 14 prices (for RSI calculation)
        if len(historical_prices) > 14:
            historical_prices.pop(0)

        # Calculate RSI once we have enough data
        rsi = calculate_rsi(historical_prices)

        if rsi is not None:
            logger.info(f"RSI: {rsi}")

            # Set the RSI thresholds (buy below 30, sell above 70)
            buy_threshold = 30
            sell_threshold = 70

            if rsi < buy_threshold:
                logger.info("RSI below 30 - Placing Buy Order!")
                order_response = place_order(side=1, access_token=access_token)
                logger.info(f"Buy Order Response: {order_response}")

            elif rsi > sell_threshold:
                logger.info("RSI above 70 - Placing Sell Order!")
                order_response = place_order(side=-1, access_token=access_token)
                logger.info(f"Sell Order Response: {order_response}")


def onerror(message):
    logger.error(f"WebSocket Error: {message}")


def onclose(message):
    logger.info(f"Connection Closed: {message}")


def onopen(fyers_instance, access_token):
    data_type = "SymbolUpdate"
    symbols = ["NSE:NIFTY50-INDEX"]
    fyers_instance.subscribe(symbols=symbols, data_type=data_type)


def connect_fyers_websocket_stock(access_token):
    """
    Connect to the Fyers WebSocket and subscribe to the required symbols for live data feed.
    """
    try:
        fyers_instance = data_ws.FyersDataSocket(access_token)
        fyers_instance.onopen = lambda: onopen(fyers_instance, access_token)
        fyers_instance.onmessage = lambda message: onmessage(message, fyers_instance, access_token)
        fyers_instance.onerror = onerror
        fyers_instance.onclose = onclose

        fyers_instance.connect()
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {e}")
