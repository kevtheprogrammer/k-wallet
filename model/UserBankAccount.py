

class Bank():
    
    def __init__(self):
        self.user_accounts = []
        
    def add_user_account(self,accounts:list)->bool:
        for acc in accounts:
            self.user_accounts.append(acc)
            print(f'added user account {acc.names}')
        return True
        
    def list_accounts(self):
        for acc in self.user_accounts:
            print(f"{acc.names}({acc._account_number})==> {acc.balance}")
        return True
    
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
         
    @staticmethod
    def validate_amount(amount):
        try:
            amount = float(amount)
        except ValueError:
            return False
        return amount > 0 
    
    @property
    def balance(self):
        return self._balance
     
    @balance.setter
    def balance(self, amount):
        amount = float(amount)
        
        if  amount < 0:
            raise ValueError('Value amount can not be negative')
                
 
        if amount>self.MAX_BALANCE:
            raise ValueError('Balance exceedes account limit!')
         
        self._balance = amount
        return False
    
    @property
    def names(self):
        return self._names
    
    @property
    def account_number(self):
        return self._account_number
    
    def get_withdraw_charge(self, amount:float)->float:
        for limit, fee in self.WITHDRAWAL_FEES:
            if amount <= limit:
                return fee
            
    
    def get_sending_fee(self,amount:float)->float:
        return (amount*.6)/100
    
    def deposit(self, amount:float) -> bool:
        amount = float(amount)

        if not self.validate_amount(amount):
            print('Unable to complete transaction. Amount can not be negative')
            return False


        if self.balance + amount > self.MAX_BALANCE:
            raise ValueError("Deposit exceeds account limit")
    
        self._balance += amount
        print(
            f"You have deposited {self.BASE_CURRENCY}{amount} into account number {self.account_number} {self.names}. You new balance is {self.balance}"
        )
        return False

    def withdraw(self, amount:float, commission:str)->bool:
        amount = float(amount)
        if not self.validate_amount(amount):
                print('Unable to complete transaction. Amount can not be negative')
                return False
            
        fee = self.get_withdraw_charge(amount)
        total = amount + fee
         
        
        if total > self.balance:
            print('Unable to complete transaction - Insufficient balance.')
            return False
        
        self._balance -= total
        commission._balance += fee 
        print(
            f"You have withdrawn {self.BASE_CURRENCY}{amount:.2f} "
            f"from account {self.account_number}."
        )

        print(f"Withdrawal fee: {self.BASE_CURRENCY}{fee:.2f}")
        print(f"Total deducted: {self.BASE_CURRENCY}{total:.2f}")
        print(f"New balance: {self.BASE_CURRENCY}{self.balance:.2f}")
         
        return True
    
    def send(self,amount:float, receiver:str, commission:str)->bool:
        amount = float(amount)
        fee = self.get_sending_fee(amount)
        total = amount + fee
        
        if not self.validate_amount(amount):
            print('Unable to complete transaction. Amount can not be negative')
            return False

        if total > self.balance:
            print('Transaction failed: Insufficient account balance!')
            return False
        
        if receiver.balance + amount > receiver.MAX_BALANCE:
            print('Unable to complete transaction. Reiver has reached thier limit')
            return False
        self.balance -= total
        receiver.balance += amount
        
        commission.balance += fee
        
        print(
            f"K{amount:.2f} sent from "
            f"{self.names} to {receiver.names}"
        )

        print(f"{self.names} balance: { self.balance}") 
        print(f"{receiver.names} balance: {receiver.balance}")
        return True
     
     

k_money = Bank()
kelvin = UserBankAccount('975550955','Kelvin Banda' )
matildah = UserBankAccount('771806932', 'Matildah Banda')
# matildah.MAX_BALANCE = 20
k_money_sending_account = UserBankAccount('001','Commission Send')
k_money_withdraw_account = UserBankAccount('002','Commission Withdraw')

k_money.add_user_account([kelvin, matildah, k_money_sending_account, k_money_withdraw_account])
 
kelvin.deposit(10000)
kelvin.send(7500, matildah, k_money_sending_account)

matildah.withdraw(5500, k_money_withdraw_account)


k_money.list_accounts()