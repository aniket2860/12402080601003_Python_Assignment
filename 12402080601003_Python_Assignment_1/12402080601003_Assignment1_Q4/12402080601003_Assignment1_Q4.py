# Assignment 1
# Question 4 - Exception-Safe CSV Transaction Splitter

import csv
from datetime import datetime


# Check whether a transaction row is valid
def validate_row(row):

    if len(row) != 5:
        return False, "Invalid number of fields"

    transaction_id = row[0].strip()
    account_id = row[1].strip()
    transaction_type = row[2].strip().upper()
    amount_text = row[3].strip()
    timestamp = row[4].strip()

    if not transaction_id:
        return False, "Missing transaction_id"

    if not account_id:
        return False, "Missing account_id"

    if transaction_type not in ("CREDIT", "DEBIT"):
        return False, "Invalid transaction type"

    # Check amount
    try:
        amount = float(amount_text)

        if amount <= 0:
            return False, "Amount must be greater than 0"

    except ValueError:
        return False, "Amount is not numeric"

    # Check timestamp
    try:
        datetime.fromisoformat(timestamp)

    except ValueError:
        return False, "Invalid timestamp"

    return True, ""


# Process the CSV file
def process_file(input_file):

    balances = {}

    try:
        with open(
            input_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            # Read header
            header = next(reader)

            if len(header) != 5:
                raise ValueError("Invalid CSV header")

            # Create output files
            with open(
                "credit.csv",
                "w",
                newline="",
                encoding="utf-8"
            ) as credit_file, \
            open(
                "debit.csv",
                "w",
                newline="",
                encoding="utf-8"
            ) as debit_file, \
            open(
                "error.csv",
                "w",
                newline="",
                encoding="utf-8"
            ) as error_file:

                credit_writer = csv.writer(credit_file)
                debit_writer = csv.writer(debit_file)
                error_writer = csv.writer(error_file)

                # Write headers
                credit_writer.writerow(header)
                debit_writer.writerow(header)
                error_writer.writerow(
                    header + ["reason"]
                )

                # Process every row
                for row in reader:

                    try:
                        valid, reason = validate_row(row)

                        if not valid:
                            error_writer.writerow(
                                row + [reason]
                            )
                            continue

                        account_id = row[1].strip()
                        transaction_type = row[2].strip().upper()
                        amount = float(row[3].strip())

                        # Calculate account balance
                        if account_id not in balances:
                            balances[account_id] = 0

                        if transaction_type == "CREDIT":
                            balances[account_id] += amount
                            credit_writer.writerow(row)

                        else:
                            balances[account_id] -= amount
                            debit_writer.writerow(row)

                    except Exception as error:
                        error_writer.writerow(
                            row + [str(error)]
                        )

        return balances

    except FileNotFoundError:
        print("Error: Input file not found.")
        return None

    except PermissionError:
        print("Error: Permission denied.")
        return None

    except Exception as error:
        print(f"Error: {error}")
        return None


# Display account-wise balances
def display_balances(balances):

    # Sort by absolute balance in descending order
    sorted_balances = sorted(
        balances.items(),
        key=lambda item: (-abs(item[1]), item[0])
    )

    for account_id, balance in sorted_balances:

        # Print integer without decimal point
        if balance.is_integer():
            balance = int(balance)

        print(account_id, balance)


# Main function
def main():

    try:
        # Read input CSV path
        input_file = input(
            "Enter CSV file path: "
        ).strip()

        if not input_file:
            print("Error: File path cannot be empty.")
            return

        # Process the file
        balances = process_file(input_file)

        if balances is None:
            return

        # Display final summary
        display_balances(balances)

        print(
            "Files created: credit.csv, debit.csv, error.csv"
        )

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

    except Exception as error:
        print(f"Error: {error}")


# Start program
if __name__ == "__main__":
    main()