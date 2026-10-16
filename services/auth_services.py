from getpass import getpass
from model.UserBankAccount import UserBankAccount
from .main_menu import menu


def login():
    phone = input("Enter your phone number: ").strip()
    pin = getpass("Enter your PIN: ")

    user = UserBankAccount.authenticate_user(phone, pin)

    if "error" in user:
        print(user["error"])
        return

    print(f"Welcome back, {user['names']}!")
    menu()