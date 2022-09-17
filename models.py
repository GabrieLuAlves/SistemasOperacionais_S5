from threading import Semaphore


class Client:
    def __init__(self, name):
        self.name = name
        self.account = None


class Account:
    def __init__(self):
        self.balance = 0


class CashMachine:
    def __init__(self) -> None:
        self.account: Account = None

    def deposit(self, amount):
        self.account.balance += amount

    def withdraw(self, amount):
        self.account.balance -= amount
