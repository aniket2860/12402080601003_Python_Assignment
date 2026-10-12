# Assignment 2
# Question 6 - Log Anomaly Detector using Sliding Window

import re
from collections import defaultdict, deque


def to_minutes(time):
    h, m = map(int, time.split(":"))
    return h * 60 + m


def main():
    try:
        x, t = map(int, input().split())
        n = int(input())

        if x < 1 or t < 1 or n < 1:
            print("INVALID")
            return

        pattern = re.compile(
            r"^(\d{2}:\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$",
            re.IGNORECASE
        )

        failures = defaultdict(deque)
        suspicious = {}

        for _ in range(n):
            line = input().strip()
            match = pattern.fullmatch(line)

            if not match:
                print("INVALID")
                return

            timestamp, user, ip, status = match.groups()
            user = user.lower()
            current_time = to_minutes(timestamp)
            status = status.upper()

            queue = failures[user]

            while queue and current_time - queue[0][0] > t:
                queue.popleft()

            if status == "FAIL":
                queue.append((current_time, ip))

            elif len(queue) >= x:
                if any(failed_ip != ip for _, failed_ip in queue):
                    if user not in suspicious:
                        suspicious[user] = timestamp

        for user in sorted(suspicious):
            print(user, suspicious[user])

    except (ValueError, EOFError):
        print("INVALID")


if __name__ == "__main__":
    main()