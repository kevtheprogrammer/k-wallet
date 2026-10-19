
 
        
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