from auth import Auth
from order import Order
from data_feed import connect_fyers_websocket
from utils import log_error, log_info
from user_api import Profile
from config import CLIENT_ID
from colorama import Fore, Style
from datetime import datetime, time
import pytz
import sys
import threading

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

    # Start WebSocket connection in a separate thread
    websocket_thread = threading.Thread(target=connect_fyers_websocket, args=(full_access_token,))
    websocket_thread.daemon = True
    websocket_thread.start()

    while True:
        if not is_market_open():
            handle_market_close()  # Call the function to handle market closure

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
                print(Fore.GREEN + "Live data connection is handled in the background..." + Style.RESET_ALL)

        elif choice == "6":
            print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
