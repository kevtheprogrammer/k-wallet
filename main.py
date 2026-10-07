from .database.schema import create_tables
from .models.account_service import create_account


def create_account_menu():

    print("\n--- CREATE ACCOUNT ---")

    name = input("Enter your name: ")
    phone = input("Enter phone number: ")

    pin = input("Create PIN: ")
    confirm_pin = input("Confirm PIN: ")

    if pin != confirm_pin:
        print("\nPINs do not match.")
        return

    if len(pin) != 4 or not pin.isdigit():
        print("\nPIN must be exactly 4 digits.")
        return

    account = create_account(
        name=name,
        phone=phone,
        pin=pin
    )

    if account:
        print("\nAccount created successfully!")
        print(f"Welcome to {account.name}")
        print(f"Your phone number is {account.phone}")


def main():

    create_tables()

    while True:

        print("\n====================")
        print("      K-MONEY")
        print("====================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            create_account_menu()

        elif choice == "2":
            print("\nLogin coming next...")

        elif choice == "3":
            print("\nThank you for using K-Money.")
            break

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()