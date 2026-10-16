
def menu():
    print("\n**************************************\n")
    print("\n**** K-Wallet Customer Menu ****\n")
    print("\n**************************************\n")
    print("1. Account Management")
    print("2. Send Money")
    print("3. Withdraw Money")
    print("4. Pay Bills")
    print("5. Exit\n\n")
    key = input('input:\t')
    menu_call(key)

def menu_call(key):
    match key:
        case '1':
             print("coming soon!")
        case '2':
             print("coming soon!")
        case '3':
             print("coming soon!")
        case '4':
            print("coming soon!")
        case '5':
            print("coming soon!")
        case '6':       
            print("Thank you for using our services. See you next time!")
            exit()
        case _:
            print("Invalid option. Please try again.")
