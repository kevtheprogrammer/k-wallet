from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime, timezone

from sqlalchemy import select
from database.connection import SessionLocal
from database.models import Account, Transaction, User
import bcrypt
from contextvars import ContextVar
from services.user_session import session_user

class UserBankAccount():

    MAX_BALANCE = 10000.00 
    BANK_NAME = 'K-Money'
    BASE_CURRENCY = 'ZMW'
    WITHDRAWAL_FEES = [
            (100, 2.00),
            (500, 5.00),
            (1000, 10.00),
            (5000, 20.00),
            (float("inf"), 30.00),
        ]
    
    def __init__(self, account_number, names, balance=.0):
        self._account_number = account_number
        self._names = names
        self.balance = balance
        self._transactions = []

    @classmethod
    def get_bank_details(cls):
        print(
            f"Bank Name:\t{cls.BANK_NAME}\nCurrency:\t{cls.BASE_CURRENCY}\nMax Balance:\t{cls.MAX_BALANCE}"
        )
    
    def get_user_by_phone(phone: str):
        with SessionLocal() as session:
            user = session.scalar(
                select(User).where(User.phone == phone)
            )

            if user is None:
                return None
            
            acc = session.scalar(
                select(Account).where(Account.user_id==user.id)
            )

            if acc is None:
                return {'error': f"Account for user {user.first_name} {user.last_name} was not found."}
            
            return {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "names": f"{user.first_name} {user.last_name}",
                "phone": user.phone,
                "email": user.email,
                "nrc": user.nrc,
                "address": user.address, 
                "account_id":acc.id,
                "account_number": acc.account_number,
                "balance": acc.balance,
            }

    @staticmethod
    def authenticate_user(phone: str, pin: str):
        try:
            with SessionLocal() as session:
                user = session.scalar(
                    select(User).where(User.phone == phone)
                )

                if user is None:
                    return {
                        "error": "User not found. Please check your phone number."
                    }

                # Verify the entered PIN against the stored bcrypt hash
                if not bcrypt.checkpw(
                    pin.encode("utf-8"),
                    user.pin_hash.encode("utf-8")
                    if isinstance(user.pin_hash, str)
                    else user.pin_hash
                ):
                    return {
                        "error": "Incorrect PIN. Please try again."
                    }
                  
                acc = session.scalar( select(Account).where(Account.user_id==user.id))
                
                if acc is None:
                    return  
                
                # if successful login
                session_user.set({
                    "id": user.id,
                    "names": f"{user.first_name} {user.last_name}",
                    "phone": user.phone,
                    "account_id":acc.id,
                    "account_number":acc.account_number,
                    "balance": acc.balance,
                })

                return {
                    "user_id": user.id,
                    "names": f"{user.first_name} {user.last_name}",
                    "phone": user.phone,
                }

        except Exception as e:
            print(f"Authentication error: {e}")
            return {
                "error": "Authentication failed due to a system error."
            }
  
    @property
    def balance(self) -> Decimal:
        return self._balance
     
    @balance.setter
    def balance(self, amount) -> bool:
        amount = Decimal(amount)
        
        if  amount < 0:
            raise ValueError('Value amount can not be negative')
                
 
        if amount>self.MAX_BALANCE:
            raise ValueError('Balance exceedes account limit!')
         
        self._balance = amount
        return False
    
    @property
    def names(self):
        return self._names

    @staticmethod
    def _to_money(amount) -> Decimal:
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Enter a valid amount.")

        if not value.is_finite() or value <= Decimal("0.00"):
            raise ValueError("Amount must be greater than zero.")

        if value != value.quantize(Decimal("0.01")):
            raise ValueError("Amount cannot have more than 2 decimal places.")

        return value

    @classmethod
    def _get_account(cls, session, account_number):
        account = session.scalar(
            select(Account).where(
                Account.account_number == account_number
            )
        )

        if account is None:
            raise ValueError(f"Account {account_number} was not found.")

        if account.status != "ACTIVE":
            raise ValueError(f"Account {account_number} is not active.")

        return account

    @staticmethod
    def _record_transaction(session, account, amount, transaction_type):
        transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type=transaction_type,
        )
        session.add(transaction)

    @property
    def account_number(self):
        return self._account_number
    
    def get_withdraw_charge(self, amount:float)->float:
        for limit, fee in self.WITHDRAWAL_FEES:
            if amount <= limit:
                return fee
            
    def get_sending_fee(self, amount: Decimal) -> Decimal:
        fee = (amount * Decimal("0.6")) / Decimal("100")
        return fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
    def deposit(self, amount: Decimal, account_id: int) -> bool:
        amount = self._to_money(amount)

        if not amount:
            print("Unable to complete transaction. Amount must be positive.")
            return False

        try:
            with SessionLocal.begin() as session:
                acc = session.scalar(
                    select(Account)
                    .where(Account.id == account_id)
                    .with_for_update()
                )

                if acc is None:
                    print("Account not found.")
                    return False

                current_balance = Decimal(str(acc.balance))

                if current_balance + amount > Decimal(str(self.MAX_BALANCE)):
                    print("Deposit exceeds account limit.")
                    return False

                # Update the database balance
                acc.balance = current_balance + amount
                
                self._record_transaction(
                    session=session,
                    account=acc,
                    amount=amount,
                    transaction_type="DEPOSIT",
                )


            # Update the in-memory wallet balance
            self._balance = acc.balance
                
            
                

            print(
                f"You have deposited ZMW {amount:.2f} "
                f"into account {self.account_number} ({self.names}). "
                f"Your new balance is ZMW {self._balance:.2f}."
            )

            return True

        except Exception as e:
            print(f"Deposit failed: {e}")
            return False

    def withdraw(self, amount, commission_account_number) -> bool:
        try:
            amount = self._to_money(amount)

            # Your existing withdrawal fee schedule
            fee = Decimal(
                str(self.get_withdraw_charge(float(amount)))
            )
            total = amount + fee

            with SessionLocal.begin() as session:
                account = self._get_account(
                    session, self.account_number
                )
                commission = self._get_account(
                    session, commission_account_number
                )

                if account.id == commission.id:
                    raise ValueError(
                        "Your account cannot be the commission account."
                    )

                balance = Decimal(str(account.balance))

                if total > balance:
                    raise ValueError("Insufficient balance.")

                account.balance = balance - total
                commission.balance = (
                    Decimal(str(commission.balance)) + fee
                )

                self._record_transaction(
                    session, account, amount, "WITHDRAWAL"
                )
                self._record_transaction(
                    session, account, fee, "WITHDRAWAL_FEE"
                )
                self._record_transaction(
                    session, commission, fee, "COMMISSION_RECEIVED"
                )

                new_balance = account.balance

            self._balance = float(new_balance)

            print(f"Withdrawn: ZMW {amount:.2f}")
            print(f"Fee:       ZMW {fee:.2f}")
            print(f"Total:     ZMW {total:.2f}")
            print(f"Balance:   ZMW {new_balance:.2f}")

            return True

        except (ValueError, InvalidOperation) as error:
            print(f"Withdrawal failed: {error}")
            return False

    def send(
        self,
        amount,
        receiver_account_number,
        commission_account_number,
    ) -> bool:
        try:
            amount = self._to_money(amount)
            fee = self.get_sending_fee(amount)  
            fee = fee.quantize(Decimal("0.01"))
            total = amount + fee

            with SessionLocal.begin() as session:
                sender = self._get_account(
                    session, self.account_number
                )
                receiver = self._get_account(
                    session, receiver_account_number
                )
                receiver_user = session.get(User, receiver.user_id)
                receiver_name = (
                    f"{receiver_user.first_name} {receiver_user.last_name}"
                    if receiver_user
                    else "Unknown recipient"
                )
                commission = self._get_account(
                    session, commission_account_number
                )

                if sender.id == receiver.id:
                    raise ValueError(
                        "You cannot send money to the same account."
                    )

                if sender.id == commission.id:
                    raise ValueError(
                        "Sender cannot be the commission account."
                    )

                if receiver.id == commission.id:
                    raise ValueError(
                        "Receiver cannot be the commission account."
                    )

                sender_balance = Decimal(str(sender.balance))
                receiver_balance = Decimal(str(receiver.balance))
                commission_balance = Decimal(
                    str(commission.balance)
                )

                if total > sender_balance:
                    raise ValueError("Insufficient balance.")

                if (
                    receiver_balance + amount
                    > Decimal(str(receiver.MAX_BALANCE))
                    if hasattr(receiver, "MAX_BALANCE")
                    else receiver_balance + amount > Decimal("10000.00")
                ):
                    raise ValueError(
                        "Receiver has reached the account balance limit."
                    )

                sender.balance = sender_balance - total
                receiver.balance = receiver_balance + amount
                commission.balance = commission_balance + fee

                self._record_transaction(
                    session, sender, amount, "TRANSFER_SENT"
                )
                self._record_transaction(
                    session, sender, fee, "TRANSFER_FEE"
                )
                self._record_transaction(
                    session, receiver, amount, "TRANSFER_RECEIVED"
                )
                self._record_transaction(
                    session, commission, fee, "COMMISSION_RECEIVED"
                )

                new_balance = sender.balance
                # receiver_balance_after = receiver.balance

            self._balance = float(new_balance)
            # print('receiver user---:', receiver)
            print(f"Sent ZMW {amount:.2f} to {receiver_name} at a Fee  ZMW {fee:.2f}. ")
            print(f"Your balance: ZMW {new_balance:.2f}")
          
            return True

        except (ValueError, InvalidOperation) as error:
            print(f"Transfer failed: {error}")
            return False
 
 