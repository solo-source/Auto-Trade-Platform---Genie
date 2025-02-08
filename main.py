# main.py
from auth import Auth
from order import Order
from utils import log_error, log_info
from user_api import Profile
from config import CLIENT_ID, stockSymbols, indexSymbols, currencySymbols, commoditiesSymbols
from colorama import Fore, Style
from datetime import datetime, time
import pytz
import sys
import subprocess  # For launching a new terminal
from sys import executable  # To get the path of the current Python interpreter

# Define official market hours for India (9:15 AM to 3:30 PM IST)
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)
IST = pytz.timezone('Asia/Kolkata')


def is_market_open():
    """
    Check if the current time is within official market hours.
    """
    now = datetime.now(IST).time()
    return MARKET_OPEN <= now <= MARKET_CLOSE


def handle_market_close():
    """
    Handle actions when the market is closed.
    Display a message and stop the application.
    """
    print(Fore.RED + "Market is closed. Please check back tomorrow." + Style.RESET_ALL)
    sys.exit()  # Gracefully exit the application


def run_websocket_listener(full_access_token, access_token, filename):
    """
    Launch the WebSocket listener in a new terminal window.

    This function uses subprocess.Popen with the CREATE_NEW_CONSOLE flag (Windows)
    to open a new terminal that will run our dedicated listener script.
    """
    try:
        subprocess.Popen(
            [executable, filename, full_access_token, access_token],
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Windows-only flag
        )
    except Exception as e:
        print(Fore.RED + f"Error launching WebSocket listener: {e}" + Style.RESET_ALL)


def show_available_symbols(stock, index, currency, commodities):
    print(Fore.CYAN + "\n[Show Available Symbols]" + Style.RESET_ALL)
    # Example placeholder list of symbols. Replace with your actual data.
    print("Available Symbols:")
    for symbol in stock:
        print(" - ", symbol)
    print()

# # -------------------------
# # Placeholder functions
# # -------------------------
# def view_positions():
#     print(Fore.CYAN + "\n[View Positions]" + Style.RESET_ALL)
#     print("This functionality is not implemented yet.\n")
#
#
# def view_trades():
#     print(Fore.CYAN + "\n[View Trades]" + Style.RESET_ALL)
#     print("This functionality is not implemented yet.\n")
#
#
#
#
#
# def trade_nifty():
#     print(Fore.CYAN + "\n[Trade Nifty]" + Style.RESET_ALL)
#     # Placeholder for Trade Nifty functionality.
#     print("Trade Nifty functionality is not implemented yet.\n")
#
#
# def trade_fo():
#     print(Fore.CYAN + "\n[Trade F/O]" + Style.RESET_ALL)
#     # Placeholder for Futures & Options trading.
#     print("Trade F/O functionality is not implemented yet.\n")
#
#
# def trade_currency():
#     print(Fore.CYAN + "\n[Trade Currency]" + Style.RESET_ALL)
#     # Placeholder for Currency trading.
#     print("Trade Currency functionality is not implemented yet.\n")
#
#
# def trade_commodities():
#     print(Fore.CYAN + "\n[Trade Commodities]" + Style.RESET_ALL)
#     # Placeholder for Commodities trading.
#     print("Trade Commodities functionality is not implemented yet.\n")
#

# -------------------------
# Submenu functions for Trading
# -------------------------
def trade_index_menu(full_access_token, access_token):
    """
    Submenu for Trade Index.
    """
    while True:
        print(Fore.MAGENTA + "\nTrade Index Menu:" + Style.RESET_ALL)
        print("1. Trade Nifty")
        print("2. Previous Menu")
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
        if choice == "1":
            if not is_market_open():
                print(Fore.RED + "Market is closed. Cannot trade NIFTY50 Index." + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Launching WebSocket listener for NIFTY50 Index..." + Style.RESET_ALL)
                run_websocket_listener(full_access_token, access_token, "trade_nifty_index_listener.py")
                print(Fore.GREEN + "WebSocket listener launched. Check the new terminal for output." + Style.RESET_ALL)
        elif choice == "2":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


def trade_stock_menu(full_access_token, access_token):
    """
    Submenu for Trade Stock.
    """
    while True:
        print(Fore.MAGENTA + "\nTrade Stock Menu:" + Style.RESET_ALL)
        print("1. Trade Vodafone-Idea")
        print("2. Previous Menu")
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
        if choice == "1":
            if not is_market_open():
                print(Fore.RED + "Market is closed. Cannot trade Vodafone-Idea." + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Launching WebSocket listener for Vodafone-Idea..." + Style.RESET_ALL)
                run_websocket_listener(full_access_token, access_token, "trade_VI_stock_listener.py")
                print(Fore.GREEN + "WebSocket listener launched. Check the new terminal for output." + Style.RESET_ALL)
        elif choice == "2":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


def start_trading_menu(full_access_token, access_token):
    """
    Main submenu for Start Trading.
    """
    while True:
        print(Fore.CYAN + "\nStart Trading Menu:" + Style.RESET_ALL)
        print("1. Show Available Symbols")
        print("2. Trade Index")
        print("3. Trade Stock")
        print("4. Trade F/O")
        print("5. Trade Currency")
        print("6. Trade Commodities")
        print("7. Previous Menu")
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice == "1":
            show_available_symbols(stockSymbols, indexSymbols, currencySymbols,commoditiesSymbols)
        elif choice == "2":
            trade_index_menu(full_access_token, access_token)
        elif choice == "3":
            trade_stock_menu(full_access_token, access_token)
        elif choice == "4":
            print("Work in Progress")
            #trade_fo()
        elif choice == "5":
            print("Work in Progress")
            # trade_currency()
        elif choice == "6":
            print("Work in Progress")
            #trade_commodities()
        elif choice == "7":
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


def show_main_menu():
    """
    Display the main menu options.
    """
    print(Fore.CYAN + "\nMain Menu:" + Style.RESET_ALL)
    print("1. View Profile")
    print("2. View Available Funds")
    print("3. View User Holdings")
    print("4. Retrieve Order List")
    print("5. View Positions")
    print("6. View Trades")
    print("7. Start Trading")
    print("8. Exit Application")


def main():
    # Step 1: Authenticate the user and get access token
    try:
        auth = Auth()
        auth.generate_auth_code()
        auth_code = input("Enter the generated auth code: ").strip()
        access_token = auth.generate_access_token(auth_code)

        if not access_token:
            log_error("Failed to get access token", "")
            return
    except Exception as e:
        log_error(f"Authentication failed: {e}", "")
        return

    # Combine client_id with access_token
    full_access_token = f"{CLIENT_ID}:{access_token}"

    # Initialize user profile and orders
    user_profile = Profile(access_token)
    orders = Order(access_token)

    while True:
        show_main_menu()
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice == "1":
            try:
                user_profile.generate_profile()
            except Exception as e:
                log_error(f"Error retrieving profile: {e}", "")
        elif choice == "2":
            try:
                user_profile.get_available_funds()
            except Exception as e:
                log_error(f"Error retrieving available funds: {e}", "")
        elif choice == "3":
            try:
                user_profile.get_user_holdings()
            except Exception as e:
                log_error(f"Error retrieving user holdings: {e}", "")
        elif choice == "4":
            try:
                orders.retrieve_all_order()
            except Exception as e:
                log_error(f"Error retrieving orders: {e}", "")
        elif choice == "5":
            try:
                print("Work in Progress")
                # view_positions()
            except Exception as e:
                log_error(f"Error retrieving positions: {e}", "")
        elif choice == "6":
            try:
                print("Work in Progress")
                # view_trades()
            except Exception as e:
                log_error(f"Error retrieving trades: {e}", "")
        elif choice == "7":
            start_trading_menu(full_access_token, access_token)
        elif choice == "8":
            print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
