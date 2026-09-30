# Assignment 1
# Question 3 - Recursive Expression Engine with Memoization

import sys

sys.setrecursionlimit(1000000)

MIN_INT64 = -(2 ** 63)
MAX_INT64 = (2 ** 63) - 1


# Expression parser

class ExpressionParser:

    def __init__(self, text):
        self.text = text
        self.position = 0
        self.length = len(text)

    # Skip spaces
    def skip_spaces(self):
        while (
            self.position < self.length
            and self.text[self.position].isspace()
        ):
            self.position += 1

    # Parse complete expression
    def parse(self):
        self.skip_spaces()

        if self.position >= self.length:
            raise ValueError()

        tree = self.parse_expression()

        self.skip_spaces()

        if self.position != self.length:
            raise ValueError()

        return tree

    # Parse + and -
    def parse_expression(self):
        node = self.parse_term()

        while True:
            self.skip_spaces()

            if self.position >= self.length:
                break

            operator = self.text[self.position]

            if operator not in "+-":
                break

            self.position += 1
            right = self.parse_term()

            node = ("operator", operator, node, right)

        return node

    # Parse *
    def parse_term(self):
        node = self.parse_factor()

        while True:
            self.skip_spaces()

            if self.position >= self.length:
                break

            if self.text[self.position] != "*":
                break

            self.position += 1
            right = self.parse_factor()

            node = ("operator", "*", node, right)

        return node

    # Parse number, variable or brackets
    def parse_factor(self):
        self.skip_spaces()

        if self.position >= self.length:
            raise ValueError()

        character = self.text[self.position]

        # Parse brackets
        if character == "(":
            self.position += 1

            node = self.parse_expression()

            self.skip_spaces()

            if (
                self.position >= self.length
                or self.text[self.position] != ")"
            ):
                raise ValueError()

            self.position += 1
            return node

        # Parse number
        if character.isdigit():

            start = self.position

            while (
                self.position < self.length
                and self.text[self.position].isdigit()
            ):
                self.position += 1

            number = int(self.text[start:self.position])

            return ("number", number)

        # Parse variable
        if character.isalpha() or character == "_":

            start = self.position
            self.position += 1

            while self.position < self.length:

                current = self.text[self.position]

                if current.isalnum() or current == "_":
                    self.position += 1
                else:
                    break

            name = self.text[start:self.position]

            return ("variable", name)

        raise ValueError()


# Expression evaluator

class ExpressionEngine:

    def __init__(self, definitions):
        self.definitions = definitions
        self.parsed = {}
        self.memo = {}
        self.state = {}

        # Parse all variable expressions
        self.parse_all_expressions()

    # Parse variable expressions
    def parse_all_expressions(self):

        for variable, expression in self.definitions.items():

            parser = ExpressionParser(expression)

            self.parsed[variable] = parser.parse()
            self.state[variable] = 0

    # Evaluate a variable
    def evaluate_variable(self, variable):

        # Use saved value if already calculated
        if variable in self.memo:
            return self.memo[variable]

        # Check for cycle
        if self.state.get(variable, 0) == 1:
            raise RuntimeError("CYCLE")

        # Check for undefined variable
        if variable not in self.parsed:
            raise ValueError()

        # Mark as currently being evaluated
        self.state[variable] = 1

        value = self.evaluate_tree(
            self.parsed[variable]
        )

        # Check 64-bit range
        if not (MIN_INT64 <= value <= MAX_INT64):
            raise ValueError()

        # Save value for memoization
        self.memo[variable] = value

        # Mark as completed
        self.state[variable] = 2

        return value

    # Evaluate expression tree
    def evaluate_tree(self, node):

        node_type = node[0]

        # Number
        if node_type == "number":
            return node[1]

        # Variable
        if node_type == "variable":
            return self.evaluate_variable(node[1])

        # Operator
        if node_type == "operator":

            operator = node[1]

            left = self.evaluate_tree(node[2])
            right = self.evaluate_tree(node[3])

            if operator == "+":
                return left + right

            if operator == "-":
                return left - right

            if operator == "*":
                return left * right

        raise ValueError()


# Check variable name

def is_valid_variable_name(name):

    if not name:
        return False

    if not (name[0].isalpha() or name[0] == "_"):
        return False

    for character in name[1:]:

        if not (character.isalnum() or character == "_"):
            return False

    return True


# Read variable definition

def read_definition(line):

    if "=" not in line:
        raise ValueError()

    variable, expression = line.split("=", 1)

    variable = variable.strip()
    expression = expression.strip()

    if not is_valid_variable_name(variable):
        raise ValueError()

    if not expression:
        raise ValueError()

    return variable, expression


# Main function

def main():

    try:

        # Read number of variables
        first_line = sys.stdin.readline().strip()

        if not first_line:
            print("INVALID")
            return

        variable_count = int(first_line)

        if not (1 <= variable_count <= 200000):
            print("INVALID")
            return

        definitions = {}

        # Read variable definitions
        for _ in range(variable_count):

            line = sys.stdin.readline().rstrip("\r\n")

            variable, expression = read_definition(line)

            if variable in definitions:
                raise ValueError()

            definitions[variable] = expression

        # Read final expression
        final_expression = sys.stdin.readline().strip()

        if not final_expression:
            print("INVALID")
            return

        # Create expression engine
        engine = ExpressionEngine(definitions)

        # Parse final expression
        parser = ExpressionParser(final_expression)

        final_tree = parser.parse()

        # Calculate final result
        result = engine.evaluate_tree(final_tree)

        # Check 64-bit range
        if not (MIN_INT64 <= result <= MAX_INT64):
            print("INVALID")
            return

        print(result)

    except RuntimeError as error:

        if str(error) == "CYCLE":
            print("CYCLE")
        else:
            print("INVALID")

    except (ValueError, OverflowError):

        print("INVALID")


# Start program

if __name__ == "__main__":
    main()