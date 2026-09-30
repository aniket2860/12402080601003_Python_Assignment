# Assignment 1
# Question 7 - Interactive Formula Validator with Custom Exceptions

import re


# Custom exceptions
class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


# Check whether the operand is a valid number
def is_number(value):

    try:
        float(value)
        return True

    except ValueError:
        return False


# Check whether the operand is a valid variable name
def is_variable(value):

    return re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*",
        value
    ) is not None


# Get the value of an operand
def get_operand_value(operand, variables):

    # Check number
    if is_number(operand):
        return float(operand)

    # Check variable
    if is_variable(operand):

        if operand not in variables:
            raise UnknownVariableError(
                f"Unknown variable: {operand}"
            )

        return variables[operand]

    raise InvalidFormatError(
        f"Invalid operand: {operand}"
    )


# Evaluate a formula
def calculate_formula(formula, variables):

    parts = formula.split()

    if len(parts) != 3:
        raise InvalidFormatError(
            "Formula must be in the form: operand operator operand"
        )

    left = parts[0]
    operator = parts[1]
    right = parts[2]

    # Check supported operators
    if operator not in ["+", "-", "*", "/", "%"]:
        raise UnsupportedOperatorError(
            f"Unsupported operator: {operator}"
        )

    left_value = get_operand_value(
        left,
        variables
    )

    right_value = get_operand_value(
        right,
        variables
    )

    # Check division by zero
    if operator in ["/", "%"] and right_value == 0:
        raise DivisionByZeroError(
            "Division by zero is not allowed"
        )

    # Perform calculation
    if operator == "+":
        result = left_value + right_value

    elif operator == "-":
        result = left_value - right_value

    elif operator == "*":
        result = left_value * right_value

    elif operator == "/":
        result = left_value / right_value

    elif operator == "%":
        result = left_value % right_value

    # Check result
    assert result == result

    return result


# Format output value
def format_result(result):

    if result.is_integer():
        return str(int(result))

    return str(result)


# Main function
def main():

    variables = {}

    while True:

        try:

            line = input().strip()

            if not line:
                continue

            # Stop the program
            if line.lower() == "quit":
                break

            # Check assignment
            if "=" in line:

                parts = line.split("=")

                if len(parts) != 2:
                    raise InvalidFormatError(
                        "Invalid assignment format"
                    )

                variable = parts[0].strip()
                value = parts[1].strip()

                if not is_variable(variable):
                    raise InvalidFormatError(
                        "Invalid variable name"
                    )

                if not is_number(value):
                    raise InvalidFormatError(
                        "Assigned value must be a number"
                    )

                variables[variable] = float(value)

                continue

            # Calculate formula
            result = calculate_formula(
                line,
                variables
            )

            print(format_result(result))

        except DivisionByZeroError as error:

            print("DivisionByZeroError")
            print(error)

        except UnsupportedOperatorError as error:

            print("UnsupportedOperatorError")
            print(error)

        except UnknownVariableError as error:

            print("UnknownVariableError")
            print(error)

        except InvalidFormatError as error:

            print("InvalidFormatError")
            print(error)

        except AssertionError:

            print("InvalidFormatError")
            print("Invalid calculation result")

        except KeyboardInterrupt:

            print("\nProgram stopped by user.")
            break


# Start program
if __name__ == "__main__":
    main()