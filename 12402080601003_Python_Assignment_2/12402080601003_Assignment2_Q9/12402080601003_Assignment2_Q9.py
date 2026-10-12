# Assignment 2
# Question 9 - OOP Inventory Merger with Operator Overloading

class Product:
    def __init__(self, product_id, name, stock, purchase, selling):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.purchase = purchase
        self.selling = selling


class Inventory:
    def __init__(self):
        self.products = {}

    def add(self, product):
        if product.product_id in self.products:
            print("Product already exists")
            return

        self.products[product.product_id] = product
        print("Product added")

    def delete(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            print("Product deleted")
        else:
            print("Product not found")

    def update(self, product_id, stock):
        if product_id in self.products:
            self.products[product_id].stock = stock
            print("Stock updated")
        else:
            print("Product not found")

    def __add__(self, other):
        result = Inventory()

        for product_id, product in self.products.items():
            result.products[product_id] = Product(
                product.product_id,
                product.name,
                product.stock,
                product.purchase,
                product.selling
            )

        for product_id, product in other.products.items():
            if product_id in result.products:
                existing = result.products[product_id]
                existing.stock += product.stock
                existing.purchase = min(
                    existing.purchase, product.purchase
                )
                existing.selling = max(
                    existing.selling, product.selling
                )
            else:
                result.products[product_id] = Product(
                    product.product_id,
                    product.name,
                    product.stock,
                    product.purchase,
                    product.selling
                )

        return result

    def total_value(self):
        return sum(
            p.stock * p.purchase for p in self.products.values()
        )

    def __lt__(self, other):
        return self.total_value() < other.total_value()

    def display(self):
        for product_id in sorted(self.products):
            p = self.products[product_id]
            print(
                p.product_id, p.name,
                "stock=" + str(p.stock),
                "purchase=" + str(p.purchase),
                "selling=" + str(p.selling)
            )


def main():
    a = Inventory()
    b = Inventory()

    n = int(input())

    for _ in range(n):
        product_id, name, stock, purchase, selling = input().split()
        a.add(Product(
            product_id, name, int(stock),
            int(purchase), int(selling)
        ))

    m = int(input())

    for _ in range(m):
        product_id, name, stock, purchase, selling = input().split()
        b.add(Product(
            product_id, name, int(stock),
            int(purchase), int(selling)
        ))

    q = int(input())

    for _ in range(q):
        parts = input().split()
        operation = parts[0]

        if operation == "ADD":
            inventory = a if parts[1] == "A" else b
            inventory.add(Product(
                parts[2], parts[3], int(parts[4]),
                int(parts[5]), int(parts[6])
            ))

        elif operation == "DELETE":
            inventory = a if parts[1] == "A" else b
            inventory.delete(parts[2])

        elif operation == "UPDATE":
            inventory = a if parts[1] == "A" else b
            inventory.update(parts[2], int(parts[3]))

        elif operation == "MERGE":
            a = a + b
            a.display()
            print("Total value:", a.total_value())

        elif operation == "COMPARE":
            if a < b:
                print("A has lower value")
            elif b < a:
                print("B has lower value")
            else:
                print("Equal value")


if __name__ == "__main__":
    main()