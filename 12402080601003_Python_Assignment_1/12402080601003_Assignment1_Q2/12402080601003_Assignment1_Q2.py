# Assignment 1
# Question 2 - Optimized Password Audit with Pattern Constraints

from collections import deque


class AhoCorasick:

    def __init__(self):
        self.next = [{}]
        self.fail = [0]
        self.output = [False]

    def add_word(self, word):

        node = 0

        for char in word.lower():

            if char not in self.next[node]:
                self.next[node][char] = len(self.next)

                self.next.append({})
                self.fail.append(0)
                self.output.append(False)

            node = self.next[node][char]

        self.output[node] = True

    def build(self):

        queue = deque()

        for child in self.next[0].values():
            queue.append(child)

        while queue:

            current = queue.popleft()

            for char, child in self.next[current].items():

                queue.append(child)

                failure = self.fail[current]

                while failure and char not in self.next[failure]:
                    failure = self.fail[failure]

                if char in self.next[failure]:
                    self.fail[child] = self.next[failure][char]
                else:
                    self.fail[child] = 0

                if self.output[self.fail[child]]:
                    self.output[child] = True

    def contains_banned(self, text):

        node = 0

        for char in text.lower():

            while node and char not in self.next[node]:
                node = self.fail[node]

            if char in self.next[node]:
                node = self.next[node][char]
            else:
                node = 0

            if self.output[node]:
                return True

        return False


def has_repeated_character(password):

    count = 1

    for i in range(1, len(password)):

        if password[i] == password[i - 1]:
            count += 1

            if count > 3:
                return True
        else:
            count = 1

    return False


def classify_password(password, automaton):

    if automaton.contains_banned(password):
        return "COMPROMISED"

    if has_repeated_character(password):
        return "WEAK_PATTERN"

    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    has_lower = False
    has_upper = False
    has_digit = False
    has_symbol = False

    for char in password:

        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in "$#@":
            has_symbol = True

    if has_lower and has_upper and has_digit and has_symbol:
        return "STRONG"

    return "WEAK_PATTERN"


def main():

    try:
        b = int(input())

        if b < 1:
            print("INVALID")
            return

        automaton = AhoCorasick()

        for _ in range(b):
            word = input().strip()

            if word:
                automaton.add_word(word)

        automaton.build()

        n = int(input())

        if n < 1:
            print("INVALID")
            return

        for i in range(1, n + 1):

            password = input().strip()

            classification = classify_password(
                password,
                automaton
            )

            print(
                f"{i}: {classification}"
            )

    except (ValueError, EOFError):
        print("INVALID")


if __name__ == "__main__":
    main()