# Assignment 2
# Question 1 - Regex-Based Email Intelligence Extractor

import re
import sys
import os


def main():
    path = input().strip().strip('"')
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    email_pattern = re.compile(
        r"(?<![A-Za-z0-9._%+-])"
        r"[A-Za-z0-9._+-]+"
        r"(?<![.+_-])"
        r"@"
        r"[A-Za-z0-9-]+"
        r"(?:\.[A-Za-z0-9-]+)*"
        r"\.(?:com|edu|org)"
        r"(?![A-Za-z0-9.-])",
        re.IGNORECASE
    )

    domains = {}

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                for match in email_pattern.finditer(line):
                    email = match.group(0)
                    domain = email.rsplit("@", 1)[1].lower()

                    if domain not in domains:
                        domains[domain] = set()

                    domains[domain].add(email)

    except OSError:
        print("INVALID")
        return

    for domain in sorted(domains):
        emails = domains[domain]
        smallest_email = min(emails)

        print(domain, len(emails), smallest_email)


if __name__ == "__main__":
    main()