from contextvars import ContextVar
from getpass import getpass

from database.connection import Base, engine
from database.models import *
from services.user_services import register_user
from model.UserBankAccount import UserBankAccount

from services.auth_services import login

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


# def account_management():
#     print("1. Change PIN")
#     print("2. Account Balance")
#     print("3. Transaction History")
#     print("4. Delete Account")
#     key = input("Select an option: ")
    
#     match key:
#         case '1':
#             print("Change PIN functionality coming soon!")
#         case '2':
#             print("Account Balance functionality coming soon!")
#         case '3':
#             print("Transaction History functionality coming soon!")
#         case '4':   
#             print("Delete Account functionality coming soon!")
#         case _:
#             print("Invalid option. Please try again.")




def auth_call(key):
    match key:
        case '1':
            onboard_user()
        case '2':
            login()
            auth_call(key)
        case _:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    initialize_database()
    print("\n**************************************\n")
    print("\n**** K-Wallet Customer Onboarding ****\n")
    print("\n**************************************\n")
    print("1. Register a new customer")
    print("2. Login") 
    print("0. Exit\n\n")
    
    # menu 
    val = input('input:\t')
    auth_call(val)
    
   