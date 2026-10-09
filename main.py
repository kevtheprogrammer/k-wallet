from getpass import getpass

from database.connection import Base, engine
from database.models import *
from services.user_services import register_user


def initialize_database():
    Base.metadata.create_all(bind=engine)

def onboard_user():
   
    first_name = input("First name: ")
    last_name = input("Last name: ")
    nrc = input("NRC number: ")
    address = input("Residential address: ")
    phone = input("Phone number: ")
    email = input("Email (optional): ").strip() or None

    pin = getpass("Create a 4-digit PIN: ")
    confirm_pin = getpass("Confirm your PIN: ")

    if pin != confirm_pin:
        print("Error: PINs do not match.")
        return

    try:
        result = register_user(
            first_name=first_name,
            last_name=last_name,
            nrc=nrc,
            address=address,
            phone=phone,
            email=email,
            pin=pin,
        )

        print("\nCustomer registered successfully!")
        print(f"Customer ID: {result['user_id']}")
        print(f"Name: {result['full_name']}")
        print(f"Account number: {result['account_number']}")
        print("Opening balance: ZMW 0.00")

    except ValueError as error:
        print(f"\nRegistration failed: {error}")

    except Exception:
        print("\nRegistration failed due to a database or system error.")
        # Log the actual exception securely during development.


def account_management():
    print("1. Change PIN")
    print("2. Account Balance")
    print("3. Transaction History")
    print("4. Delete Account")
    key = input("Select an option: ")
    
    match key:
        case '1':
            print("Change PIN functionality coming soon!")
        case '2':
            print("Account Balance functionality coming soon!")
        case '3':
            print("Transaction History functionality coming soon!")
        case '4':   
            print("Delete Account functionality coming soon!")
        case _:
            print("Invalid option. Please try again.")


def send_money():
    amount = float(input("Enter amount to send: \t"))
    if amount <= 0:
        print("Invalid amount. Please enter a positive number.")
    else:
        print(f"Sending ZMW {amount}...")
        user_id = input("Enter recipient's number: ")
        if not user_id.isdigit():
            print("Invalid recipient number. Please enter a valid number.")
        else:
            print(f"Successfully sent ZMW {amount} to user ID {user_id}.")

    return 

def menu(key):
    match key:
        case '1':
            onboard_user()
        case '2':
            account_management()
        case '3':
            send_money()
        case '4':
            print("coming soon!")
        case '5':
            print("coming soon!")
        case '6':       
            print("Thank you for using our services. See you next time!")
            exit()
        case _:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    initialize_database()
    print("\n**************************************\n")
    print("\n**** K-Wallet Customer Onboarding ****\n")
    print("\n**************************************\n")
    print("1. Register a new customer")
    print("2. Account Management")
    print("3. Send Money")
    print("4. Withdraw Money")
    print("5. Pay Bills")
    print("6. Exit\n\n")
    
    
    # menu 
    val = input('input:\t')
    menu(val)
    
    
    onboard_user()