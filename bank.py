import json
import os 
import sys
from datetime import datetime

class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        if os.path.exists('accounts.json'):
            with open('accounts.json', 'r') as f:
                self.accounts = json.load(f)

    def save_accounts(self):
        with open('accounts.json', 'w') as f:
            json.dump(self.accounts, f, indent = 4)

    def create_account(self, name, email_id, security_pin, balance):
        if email_id in self.accounts:
            return False, "Account already exists. Please try with some other email ID."
        
        try:
            security_pin = int(security_pin)
        except ValueError:
            return False, "Invalid input for security pin. Please enter a numeric value." 
            
        try:
            initial_balance = float(balance)
        except ValueError:
            initial_balance = 0
            return False, "Invalid input for balance. Setting initial balance to 0."
            
        
        self.accounts[email_id] = {"name": name, "security_pin": security_pin, "balance": initial_balance, "transactions": []}
        self.save_accounts()
        return True, "Account created successfully."

    def validate_account(self, email_id, security_pin):
        if email_id not in self.accounts:
            return False, "Account does not exists."
        
        try:
            security_pin = int(security_pin)
        except ValueError:
            return False, "Invalid input for security pin. Please enter a numeric value."
        
        if security_pin != self.accounts[email_id]['security_pin']:
            return False, "Incorrect security pin."
        
        return True, "Validation successful."

    def deposit(self, email_id, security_pin, amount):
        valid, message = self.validate_account(email_id, security_pin)
        if not valid:
            return False, message
        
        try:
            amount = float(amount)
        except ValueError:
            return False, "Invalid input for amount. Please enter a numeric value."
        
        self.accounts[email_id]['balance'] += amount
        self.record_transaction(email_id, "deposit", amount)
        self.save_accounts()
        return True, f"Deposited {amount} successfully. New balance is {self.accounts[email_id]['balance']}."

    def withdraw(self, email_id, security_pin, amount):
        valid, message = self.validate_account(email_id, security_pin)
        if not valid:
            return False, message 
        
        try:
            amount = float(amount)
        except ValueError:
            return False, "Invalid input for amount. Please enter a numeric value."
        
        if amount > self.accounts[email_id]['balance']:
            return False, "Insufficient balance."
            
        self.accounts[email_id]['balance'] -= amount
        self.record_transaction(email_id, "withdraw", amount)
        self.save_accounts()    
        return True, f"Withdrew {amount} successfully. New balance is {self.accounts[email_id]['balance']}."

    def check_balance(self, email_id, security_pin):
        valid, message = self.validate_account(email_id, security_pin)
        if not valid:
            return False, message 
        return True, f"Your current balance is {self.accounts[email_id]['balance']}."

    def record_transaction(self, email_id, transaction_type, amount):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": self.accounts[email_id]['balance']
        }
        self.accounts[email_id]['transactions'].append(transaction)
        self.save_accounts()

    def view_transactions(self, email_id, security_pin):
        valid, message = self.validate_account(email_id, security_pin)
        if not valid:
            return False, message
        
        transac = self.accounts[email_id]['transactions']
        if not transac:
            return False, "No transactions found."
        return True, transac

    def exit_system(self):
        return "Exiting the system. Goodbye!"
        sys.exit()

# if __name__ == "__main__":
#     Bank()
