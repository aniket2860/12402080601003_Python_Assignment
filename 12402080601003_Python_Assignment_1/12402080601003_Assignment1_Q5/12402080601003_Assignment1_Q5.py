# Assignment 1
# Question 5 - Object-Oriented Bank Settlement System

import sys


# Custom exception for transaction errors
class TransactionError(Exception):
    pass


# Account class
class Account:

    def __init__(self, account_id, balance):
        self._account_id = account_id
        self._balance = balance
        self._history = []

    # Account ID getter
    @property
    def account_id(self):
        return self._account_id

    # Balance getter
    @property
    def balance(self):
        return self._balance

    # Balance setter
    @balance.setter
    def balance(self, value):
        self._balance = value

    # Transaction history getter
    @property
    def history(self):
        return self._history

    # Add transaction to history
    def add_transaction(self, transaction):
        self._history.append(transaction)

    # Deposit money
    def deposit(self, amount):

        if amount <= 0:
            raise TransactionError("Invalid amount")

        self._balance += amount

    # Withdraw money
    def withdraw(self, amount):

        if amount <= 0:
            raise TransactionError("Invalid amount")

        if amount > self._balance:
            raise TransactionError("Insufficient balance")

        self._balance -= amount


# Transaction class
class Transaction:

    def __init__(
        self,
        transaction_type,
        from_account,
        to_account,
        amount
    ):
        self.transaction_type = transaction_type
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount


# Bank class
class Bank:

    def __init__(self):
        self._accounts = {}
        self._batch_active = False
        self._batch_number = 0
        self._batch_changes = {}
        self._failed_batches = []

    # Add account
    def add_account(self, account_id, balance):
        self._accounts[account_id] = Account(
            account_id,
            balance
        )

    # Get account
    def get_account(self, account_id):

        if account_id not in self._accounts:
            raise TransactionError("Account not found")

        return self._accounts[account_id]

    # Save account state before batch operation
    def save_batch_state(self, account_id):

        if account_id not in self._batch_changes:

            account = self.get_account(account_id)

            self._batch_changes[account_id] = (
                account.balance,
                len(account.history)
            )

    # Deposit operation
    def deposit(self, account_id, amount):

        account = self.get_account(account_id)

        if self._batch_active:
            self.save_batch_state(account_id)

        account.deposit(amount)

        transaction = Transaction(
            "DEPOSIT",
            None,
            account_id,
            amount
        )

        account.add_transaction(transaction)

    # Withdraw operation
    def withdraw(self, account_id, amount):

        account = self.get_account(account_id)

        if self._batch_active:
            self.save_batch_state(account_id)

        account.withdraw(amount)

        transaction = Transaction(
            "WITHDRAW",
            account_id,
            None,
            amount
        )

        account.add_transaction(transaction)

    # Transfer operation
    def transfer(self, from_id, to_id, amount):

        if from_id == to_id:
            raise TransactionError(
                "Same account transfer"
            )

        from_account = self.get_account(from_id)
        to_account = self.get_account(to_id)

        if self._batch_active:
            self.save_batch_state(from_id)
            self.save_batch_state(to_id)

        # Withdraw first so failed transfers change nothing
        from_account.withdraw(amount)
        to_account.deposit(amount)

        transaction = Transaction(
            "TRANSFER",
            from_id,
            to_id,
            amount
        )

        from_account.add_transaction(transaction)
        to_account.add_transaction(transaction)

    # Start a batch
    def begin_batch(self):

        if self._batch_active:
            raise TransactionError(
                "Batch already active"
            )

        self._batch_active = True
        self._batch_number += 1
        self._batch_changes = {}

    # End a batch
    def end_batch(self):

        if not self._batch_active:
            raise TransactionError(
                "No active batch"
            )

        self._batch_active = False
        self._batch_changes = {}

    # Rollback current batch
    def rollback_batch(self):

        for account_id, state in self._batch_changes.items():

            account = self.get_account(account_id)

            original_balance = state[0]
            original_history_length = state[1]

            account.balance = original_balance

            del account.history[
                original_history_length:
            ]

        self._failed_batches.append(
            self._batch_number
        )

        self._batch_active = False
        self._batch_changes = {}

    # Get all accounts
    @property
    def accounts(self):
        return self._accounts

    # Get failed batches
    @property
    def failed_batches(self):
        return self._failed_batches


# Process all operations
def process_operations(bank, operations):

    for operation in operations:

        parts = operation.split()

        if not parts:
            continue

        command = parts[0].upper()

        try:

            if command == "DEPOSIT":

                if len(parts) != 3:
                    raise TransactionError(
                        "Invalid deposit"
                    )

                account_id = parts[1]
                amount = int(parts[2])

                bank.deposit(
                    account_id,
                    amount
                )

            elif command == "WITHDRAW":

                if len(parts) != 3:
                    raise TransactionError(
                        "Invalid withdrawal"
                    )

                account_id = parts[1]
                amount = int(parts[2])

                bank.withdraw(
                    account_id,
                    amount
                )

            elif command == "TRANSFER":

                if len(parts) != 4:
                    raise TransactionError(
                        "Invalid transfer"
                    )

                from_id = parts[1]
                to_id = parts[2]
                amount = int(parts[3])

                bank.transfer(
                    from_id,
                    to_id,
                    amount
                )

            elif command == "BATCH_BEGIN":

                bank.begin_batch()

            elif command == "BATCH_END":

                bank.end_batch()

            else:
                raise TransactionError(
                    "Unknown operation"
                )

        except (TransactionError, ValueError):

            # Rollback the complete batch if an operation fails
            if bank._batch_active:
                bank.rollback_batch()


# Main function
def main():

    try:

        # Read number of accounts
        n = int(input().strip())

        if n <= 0:
            print("INVALID")
            return

        bank = Bank()

        # Read initial accounts
        for _ in range(n):

            parts = input().split()

            if len(parts) != 2:
                print("INVALID")
                return

            account_id = parts[0]
            balance = int(parts[1])

            if balance < 0:
                print("INVALID")
                return

            bank.add_account(
                account_id,
                balance
            )

        # Read number of operations
        q = int(input().strip())

        if q <= 0:
            print("INVALID")
            return

        operations = []

        # Read operations
        for _ in range(q):
            operations.append(
                input().strip()
            )

        # Process operations
        process_operations(
            bank,
            operations
        )

        # Print failed batches
        for batch_number in bank.failed_batches:
            print(f"FAILED {batch_number}")

        # Print final balances in account ID order
        for account_id in sorted(bank.accounts):

            account = bank.accounts[account_id]

            print(
                account_id,
                account.balance
            )

    except (ValueError, EOFError):

        print("INVALID")

    except KeyboardInterrupt:

        print("\nProgram stopped by user.")


# Start program
if __name__ == "__main__":
    main()