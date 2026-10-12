# Assignment 2
# Question 2 - Offline Web Scraping Ranker from HTML Pages

import re
import os
import html


def extract_products(file_path):
    products = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        content = html.unescape(content)

        pattern = re.compile(
            r'<div[^>]*class=["\'][^"\']*product[^"\']*["\'][^>]*>'
            r'(.*?)</div>',
            re.IGNORECASE | re.DOTALL
        )

        blocks = pattern.findall(content)

        for block in blocks:
            name_match = re.search(
                r'<[^>]*class=["\'][^"\']*name[^"\']*["\'][^>]*>(.*?)</',
                block,
                re.IGNORECASE | re.DOTALL
            )

            price_match = re.search(
                r'<[^>]*class=["\'][^"\']*price[^"\']*["\'][^>]*>'
                r'.*?(\d[\d,]*(?:\.\d+)?)',
                block,
                re.IGNORECASE | re.DOTALL
            )

            rating_match = re.search(
                r'<[^>]*class=["\'][^"\']*rating[^"\']*["\'][^>]*>'
                r'.*?(\d+(?:\.\d+)?)',
                block,
                re.IGNORECASE | re.DOTALL
            )

            if name_match and price_match and rating_match:
                name = re.sub(
                    r"<[^>]+>", "", name_match.group(1)
                ).strip()

                name = " ".join(name.split())
                price = float(price_match.group(1).replace(",", ""))
                rating = float(rating_match.group(1))

                if name and price >= 0 and 0 <= rating <= 5:
                    products.append((name, price, rating))

    except OSError:
        pass

    return products


def main():
    try:
        first_line = input().split()

        if len(first_line) != 2:
            print("INVALID")
            return

        p, k = map(int, first_line)

        if p < 1 or k < 1:
            print("INVALID")
            return

        files = []

        for _ in range(p):
            files.append(input().strip().strip('"'))

        unique_products = {}

        for file_path in files:
            for name, price, rating in extract_products(file_path):
                if (
                    name not in unique_products
                    or rating > unique_products[name][1]
                    or (
                        rating == unique_products[name][1]
                        and price < unique_products[name][0]
                    )
                ):
                    unique_products[name] = (price, rating)

        ranked = sorted(
            [
                (name, price, rating)
                for name, (price, rating) in unique_products.items()
            ],
            key=lambda item: (-item[2], item[1], item[0])
        )

        for name, price, rating in ranked[:k]:
            price_text = str(int(price)) if price.is_integer() else str(price)
            print(name, price_text, rating)

    except (ValueError, EOFError):
        print("INVALID")


if __name__ == "__main__":
    main()