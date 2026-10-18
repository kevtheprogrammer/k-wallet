from .transaction import deposit_money, send_money


def menu():
    print("\n**************************************\n")
    print("\n**** K-Wallet Customer Menu ****\n")
    print("\n**************************************\n")
    print("1. Account Management")
    print("2. Deposit Money")
    print("3. Send Money")
    print("4. Withdraw Money")
    print("5. Pay Bills")
    print("6. Exit\n\n")
    key = input('input:\t')
    menu_call(key)

def menu_call(key):
    match key:
        case '1':
             print("coming soon!")
        case '2':
            deposit_money()
            menu()
        case '3':
            send_money()
            menu()
   
        case '4':
            print("coming soon!")
        case '5':
            print("coming soon!")
        case '6':       
            print("Thank you for using our services. See you next time!")
            exit()
        case _:
            menu()
