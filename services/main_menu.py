from .transaction import deposit_money, send_money, check_balance, withdraw_money


def menu():
    print("\n**************************************\n")
    print("\n**** K-Wallet Customer Menu ****\n")
    print("\n**************************************\n")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Send Money")
    print("4. Withdraw Money")
    print("5. Exit\n\n")
    key = input('input:\t')
    menu_call(key)

def menu_call(key):
    match key:
        case '1':
            check_balance()
            menu()
        case '2':
            deposit_money()
            menu()
        case '3':
            send_money()
            menu()
        case '4':
            withdraw_money()
            menu()
        case '5':
            print("coming soon!")
 
        case _:
            menu()
