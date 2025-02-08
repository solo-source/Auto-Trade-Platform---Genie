# main.py
from auth import Auth
from order import Order
from utils import log_error, log_info
from user_api import Profile
from config import CLIENT_ID
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


def show_menu():
    """
    Display a menu for the user to choose operations.
    """
    print(Fore.CYAN + "\nMain Menu:" + Style.RESET_ALL)
    print("1. View Profile")
    print("2. View Available Funds")
    print("3. View User Holdings")
    print("4. Retrieve Order List")
    print("5. View Live Data (WebSocket)")
    print("6. Exit")


def run_websocket_listener(full_access_token, access_token):
    """
    Launch the WebSocket listener in a new terminal window.

    This function uses subprocess.Popen with the CREATE_NEW_CONSOLE flag (Windows)
    to open a new terminal that will run our dedicated listener script.
    """
    try:
        subprocess.Popen(
            [executable, "trade_nifty_listener.py", full_access_token, access_token],
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Windows-only flag
        )
    except Exception as e:
        print(Fore.RED + f"Error launching WebSocket listener: {e}" + Style.RESET_ALL)


def main():
    # Step 1: Authenticate the user and get access token
    try:
        auth = Auth()
        auth.generate_auth_code()
        auth_code = input("Enter the generated auth code: ")
        access_token = auth.generate_access_token(auth_code)

        if not access_token:
            log_error("Failed to get access token", "")
            return
    except Exception as e:
        log_error(f"Authentication failed: {e}", "")
        return

    # Combine client_id with access_token
    full_access_token = f"{CLIENT_ID}:{access_token}"
    user_profile = Profile(access_token)
    orders = Order(access_token)

    while True:
        if not is_market_open():
            handle_market_close()  # Handle market closure

        show_menu()
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
            if not is_market_open():
                print(Fore.RED + "Market is closed. Cannot connect to live data." + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Launching WebSocket listener in a new terminal..." + Style.RESET_ALL)
                run_websocket_listener(full_access_token,access_token)
                print(Fore.GREEN + "WebSocket listener launched. Check the new terminal for output." + Style.RESET_ALL)

        elif choice == "6":
            print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
