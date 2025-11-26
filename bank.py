import json
import os 
import sys

class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()
        self.menu()

    def load_accounts(self):
        if os.path.exists('accounts.json'):
            with open('accounts.json', 'r') as f:
                self.accounts = json.load(f)

    def save_accounts(self):
        with open('accounts.json', 'w') as f:
            json.dump(self.accounts, f, indent = 4)

    def menu(self):
        while True:
            user_input = input("""
            Welcome to the Bank System!
            Enter 1 to Create Account
            Enter 2 to deposit money
            Enter 3 to withdraw money
            Enter 4 to check balance
            Enter 5 to exit
            """)

            options = {'1': self.create_account, '2': self.deposit, '3': self.withdraw, '4': self.check_balance, '5': self.exit_system}

            function = options.get(user_input)
            if function:
                function()

    def create_account(self):
        name = input("Enter your name: ")
        email_id = input("Enter your email ID: ")
        if email_id in self.accounts:
            print("Account already exists. Please try with some other email ID.")
            return
        
        try:
            security_pin = int(input("Set a security pin: "))
        except ValueError:
            print("Invalid input for security pin. Please enter a numeric value.")
            return 
            
        try:
            initial_balance = float(input("Enter initial balance (default is 0): ") or 0)
        except ValueError:
            print("Invalid input for balance. Setting initial balance to 0.")
            initial_balance = 0
        
        self.accounts[email_id] = {"name": name, "security_pin": security_pin, "balance": initial_balance}
        self.save_accounts()
        print("Account created successfully.")

    def validate_account(self, email_id, security_pin):
        if email_id not in self.accounts:
            print("Account does not exists.")
            return False
        
        try:
            security_pin = int(security_pin)
        except ValueError:
            print("Invalid input for security pin. Please enter a numeric value.")
            return False
        
        if security_pin != self.accounts[email_id]['security_pin']:
            print("Incorrect security pin.")
            return False
        
        return True

    def deposit(self):
        email_id = input("Enter your email ID: ")
        security_pin = input("Enter your security pin: ")
        if not self.validate_account(email_id, security_pin):
            return
        
        try:
            amount = float(input("Enter the amount to deposit: "))
        except ValueError:
            print("Invalid input for amount. Please enter a numeric value.")
            return
        
        self.accounts[email_id]['balance'] += amount
        self.save_accounts()
        print(f"Deposited {amount} successfully. New balance is {self.accounts[email_id]['balance']}.")

    def withdraw(self):
        email_id = input("Enter your email ID: ")
        security_pin = input("Enter your security pin: ")

        if not self.validate_account(email_id, security_pin):
            return 
        
        try:
            amount = float(input("Enter the amount to withdraw: "))
        except ValueError:
            print("Invalid input for amount. Please enter a numeric value.")
            return
        
        if amount > self.accounts[email_id]['balance']:
            print("Insufficient balance.")
            return
        self.accounts[email_id]['balance'] -= amount
        self.save_accounts()    
        print(f"Withdrew {amount} successfully. New balance is {self.accounts[email_id]['balance']}.")

    def check_balance(self):
        email_id = input("Enter your email ID: ")
        security_pin = input("Enter your security pin: ")
        if not self.validate_account(email_id, security_pin):
            return
        print(f"Your current balance is {self.accounts[email_id]['balance']}.")

    def exit_system(self):
        print("Exiting the system. Goodbye!")
        sys.exit()

if __name__ == "__main__":
    Bank()
