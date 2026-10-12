# Assignment 2
# Question 7 - Generator-Based JSON ETL Pipeline

import json


def read_records(file_path):
    corrupted = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                record = json.loads(line)

                device = record["device_id"]
                temperature = float(record["temperature_c"])
                humidity = float(record["humidity"])

                if not device or not 0 <= humidity <= 100:
                    raise ValueError

                yield device, temperature, humidity

            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                corrupted += 1

    yield None, None, corrupted


def main():
    file_path = input("JSONL file path: ")

    devices = {}
    corrupted = 0

    try:
        for device, temperature, humidity in read_records(file_path):
            if device is None:
                corrupted = humidity
                continue

            fahrenheit = (temperature * 9 / 5) + 32

            if device not in devices:
                devices[device] = {
                    "count": 0,
                    "min": fahrenheit,
                    "max": fahrenheit,
                    "total": 0
                }

            data = devices[device]
            data["count"] += 1
            data["min"] = min(data["min"], fahrenheit)
            data["max"] = max(data["max"], fahrenheit)
            data["total"] += fahrenheit

        for device in sorted(devices):
            data = devices[device]
            average = data["total"] / data["count"]

            print(
                f"{device} count={data['count']} "
                f"min={data['min']:.2f} "
                f"max={data['max']:.2f} "
                f"avg={average:.2f} "
                f"corrupted={corrupted}"
            )

    except OSError:
        print("INVALID")


if __name__ == "__main__":
    main()