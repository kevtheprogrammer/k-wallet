from database.models import *
from model.UserBankAccount import UserBankAccount 
from .user_session import session_user

def deposit_money():
 
    user = session_user.get()
  
    if not user:    
        print("Error: No user information available.")
        return
    
    wallet = UserBankAccount(
        account_number=user["account_number"],
        names=user["names"],
        balance=user["balance"],
    )
    
    amount = float(input("Enter the amount to deposit: "))
    wallet.deposit(amount=amount, account_id=user['account_id'])
    print(f"Deposit successful! New balance: ZMW {wallet.balance:.2f}")

def send_money(): 
    
    sender = session_user.get()
    
    if not sender:
        print("Error: No sender information available.")
        return
     
    rec = input('Enter receiver account number: ') 
    receiver = UserBankAccount.get_user_by_phone(phone=rec)
     
    if not receiver:
        print("Error: Receiver not found.")
        return
    
    amount_ = input('Enter Amount: ')
    
    
    if sender and receiver:
        wallet = UserBankAccount(
            account_number=sender["account_number"],
            names=sender["names"],
            balance=sender["balance"],
        )

        wallet.send(
            amount=amount_,
            receiver_account_number=receiver["account_number"],
            commission_account_number="2074468656",
        )
