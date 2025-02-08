# trade_VI_stock_listener.py
import sys
import threading
from os import access

from trade_VI_stock import connect_fyers_websocket_stock_VI

def run_websocket(full_access_token, access_token):
    """
    Function to run the WebSocket connection.
    """
    connect_fyers_websocket_stock_VI(full_access_token, access_token)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        #print("Usage: python trade_VI_stock_listener.py <full_access_token>")
        sys.exit(1)
    full_access_token = sys.argv[1]
    access_token = sys.argv[2]

    # Create a thread for the WebSocket listener
    websocket_thread = threading.Thread(target=run_websocket, args=(full_access_token,access_token))
    websocket_thread.daemon = True  # Optional: Make it a daemon thread if you want it to exit when main thread exits
    websocket_thread.start()

    # Optionally, you can join the thread if you want this script to block until the WebSocket thread finishes.
    # For long-running WebSocket connections, you may instead want to simply keep the process alive.
    websocket_thread.join()
