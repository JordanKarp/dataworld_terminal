from dataclasses import dataclass
from datetime import datetime

STARTING_CASH = 1_000


@dataclass
class Transaction:
    description: str
    _amount: int
    _balance: float
    date: datetime

    @property
    def balance(self):
        return f"${self._balance:,.2f}"

    @property
    def amount(self):
        return f"${self._amount:,.2f}"

    def __repr__(self):
        return f"{self.date:%m/%d/%Y - %H:%M:%S}: {self.description} {self.amount} - Balance: {self.balance}"


class BankAccount:
    def __init__(self, acccount_number=None, balance=STARTING_CASH):
        self.account_number = acccount_number
        self._balance = balance
        self._transactions = []

    def __getitem__(self, item):
        return getattr(self, item, "")

    def add_transaction(self, description, amount, date):
        self._transactions.append(Transaction(description, amount, self._balance, date))

    def create_account(self, date=datetime.now()):
        if not self.account_number:
            self.account_number = 1
        self.add_transaction("Create Account", 0, date)

    def deposit(self, description, amount, date):
        if amount > 0:
            self._balance += amount
            self.add_transaction(description, amount, date)
        else:
            self.add_transaction("Invalid Deposit", 0, date)

    def withdraw(self, description, amount, date):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            self.add_transaction(description, -1 * amount, date)
        else:
            self.add_transaction("Invalid Withdrawal", 0, date)

    @property
    def transactions(self):
        # return self._transactions
        return sorted(self._transactions, key=lambda x: x.date, reverse=False)
        # return self._transactions.sort(key=lambda x: x.date, reverse=False)

    @property
    def recent_transactions(self):
        return self._transactions[-5:]

    @property
    def balance(self):
        return f"${self._balance:,.2f}"

    def __str__(self):
        return f"Bank Account ({self.account_number}): {self.balance}"
