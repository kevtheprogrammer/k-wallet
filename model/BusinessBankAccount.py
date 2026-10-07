   
from .UserBankAccount import UserBankAccount  
   
class BusinessBankAccount(UserBankAccount):
    MAX_BALANCE = 100000.00
    
    WITHDRAWAL_FEES = [
        (100, 5.00),
        (500, 10.00),
        (1000, 15.00),
        (5000, 25.00),
        (float("inf"), 30.00),
    ]
    
    def __init__(self, account_number, names, business_name, balance=0):
        super().__init__(account_number, names, balance)
        self.business_name = business_name
        
    def get_sending_fee(self,amount):
        return (amount*3.5)/100
    
    @business_name.setter
    def business_name(self):
        return self._business_name
        


  