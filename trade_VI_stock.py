from fyers_apiv3.FyersWebsocket import data_ws
from config import CLIENT_ID
from order import Order  # Import the Order class to place orders
import numpy as np
import logging
import pytz
from datetime import datetime, time
import sys

# Global list to store historical closing prices
historical_prices = []

# Set up logging for better traceability.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logger.addHandler(handler)

# Set IST time zone
IST = pytz.timezone('Asia/Kolkata')

# Market Open and Close Timings
MARKET_OPEN = time(9, 15)  # 9:15 AM IST
MARKET_CLOSE = time(15, 30)  # 3:30 PM IST

BUY_THRESHOLD = 48
SELL_THRESHOLD = 70


def is_market_open():
    """
    Checks if the current time is within Indian market hours.
    :return: True if market is open, False otherwise.
    """
    current_time = datetime.now(IST).time()
    return MARKET_OPEN <= current_time <= MARKET_CLOSE


def calculate_rsi(prices, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given list of prices.
    :param prices: List of historical closing prices.
    :param period: Period for RSI calculation (default is 14).
    :return: RSI value or None if not enough data.
    """
    if len(prices) < period + 1:
        return None

    gains, losses = [], []
    for i in range(1, period + 1):
        change = prices[-i] - prices[-(i + 1)]
        gains.append(max(0, change))
        losses.append(max(0, -change))
    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def place_order(side, access_token):
    """
    Helper function to place a buy or sell order.
    :param side: 1 for Buy, -1 for Sell (API requires -1 for selling)
    :param access_token: Access token in the format "CLIENT_ID:access_token"
    :return: Response from the order placement.
    """
    order_data = {
        "symbol": "NSE:IDEA-EQ",  # Ensure this symbol is correct for your API.
        "qty": 1,                       # Quantity as an integer.
        "type": 2,                      # Market order type = 2
        "side": side,                   # 1 for buy, -1 for sell.
        "productType": "INTRADAY",       # Verify this string exactly matches the expected value.
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,          # Use a Boolean value.
        "stopLoss": 0,
        "takeProfit": 0,
    }

    order = Order(access_token)
    try:
        response = order.place_single_order(order_data)
    except Exception as e:
        logger.error(f"Order placement exception: {e}")
        return {"error": str(e)}
    return response



def onmessage(message, fyers_instance, access_token):
    """
    Callback function to handle incoming messages from the WebSocket.
    """
    if not is_market_open():
        logger.info("Market is closed. Disconnecting WebSocket.")
        fyers_instance.disconnect()
        return

    print("Received WebSocket Message:",
          "Symbol:", message.get("symbol"),
          "Last Traded Price:", message.get("ltp"),
          "High Price:", message.get("high_price"),
          "Low Price:", message.get("low_price"),
          "DateTime:", datetime.fromtimestamp(message["timestamp"]) if "timestamp" in message else "N/A",
          flush=True)

    if isinstance(message, dict) and 'ltp' in message:
        try:
            close_price = float(message['ltp'])
        except (ValueError, TypeError):
            logger.error("Invalid LTP data format.")
            return

        historical_prices.append(close_price)
        if len(historical_prices) > 15:
            historical_prices.pop(0)
        rsi = calculate_rsi(historical_prices)
        if rsi is not None:
            logger.info(f"RSI: {rsi}")
            print(f"RSI: {rsi}", flush=True)
            if rsi < BUY_THRESHOLD:
                logger.info("RSI below 30 - Placing Buy Order!")
                order_response = place_order(side=1, access_token=access_token)
                logger.info(f"Buy Order Response: {order_response}")
                print(f"Buy Order Response: {order_response}", flush=True)
            elif rsi > SELL_THRESHOLD:
                logger.info("RSI above 70 - Placing Sell Order!")
                order_response = place_order(side=-1, access_token=access_token)
                logger.info(f"Sell Order Response: {order_response}")
                print(f"Sell Order Response: {order_response}", flush=True)
    else:
        print("Unexpected Message Format:", message, flush=True)


def onerror(message):
    logger.error(f"WebSocket Error: {message}")
    print(f"WebSocket Error: {message}", flush=True)


def onclose(message):
    logger.info(f"Connection Closed: {message}")
    print(f"Connection Closed: {message}", flush=True)


def onopen(fyers_instance, access_token):
    data_type = "SymbolUpdate"
    symbols = ["NSE:IDEA-EQ"]
    fyers_instance.subscribe(symbols=symbols, data_type=data_type)
    logger.info("WebSocket connection opened and subscription successful.")
    print("WebSocket connection opened and subscription successful.", flush=True)


def connect_fyers_websocket_stock_VI(full_access_token, access_token):
    """
    Connect to the Fyers WebSocket and subscribe to the required symbols.
    """
    try:
        fyers_instance = data_ws.FyersDataSocket(
            access_token=full_access_token,  # Access token in the format "appid:accesstoken"
            log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
            litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
            write_to_file=False,  # Save response in a log file instead of printing it.
            reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
            on_connect=lambda: onopen(fyers_instance, full_access_token),  # Callback function to subscribe to data upon connection.
            on_close=onclose,  # Callback function to handle WebSocket connection close events.
            on_error=onerror,  # Callback function to handle WebSocket errors.
            on_message=lambda message: onmessage(message, fyers_instance, access_token)  # Callback function to handle incoming messages from the WebSocket.
        )

        fyers_instance.connect()
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {e}")
        print(f"Error in WebSocket connection: {e}", flush=True)

# If this module is imported, connect_fyers_websocket_nifty can be called.
