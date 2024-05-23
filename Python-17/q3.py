class Bank:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def withdraw(self, money):
        if(self.account_number>0):
            if(self.balance>money):
                self.balance = self.balance - money
                return (self.balance)
            else:
                return "None"

    def deposit(self, money):
        if(self.account_number>0):
            self.balance = self.balance + money
            return (self.balance)
        else:
            return "None"
    
obj1 = Bank(-12345, 'kanishk', 12000)
obj2 = Bank(67891, 'naveen', 12000)
print(obj1.deposit(500))
print(obj2.withdraw(500))