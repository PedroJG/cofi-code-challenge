import json
from collections import Counter
prod_file = "products.json"
disc_file = "discounts.json"


class Product:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price
        self.discounted = False
        self.discount_price = self.price

    def __str__(self):
        return json.dumps({
            "code": self.code,
            "name": self.name,
            "price": self.price,
            "discounted": self.discounted,
            "discount_price": self.discount_price
        })


class Store:
    def __init__(self):
        self._cart = {}
        self._products = {}
        self._start()

    def _start(self):
        json_products = self.load_products()
        json_discounts = self.load_discounts()

        for prod in json_products["products"]:
            self._products[prod["code"]] = Product(
                prod["code"], prod["name"], prod["price"])

        for disc in json_discounts["discounts"]:
            self._products[disc["code"]] = Product(
                disc["code"], disc["name"], disc["price"]
            )

    def load_products(self):
        with open(prod_file) as f:
            return json.load(f)
        
    def load_discounts(self):
        with open(disc_file) as f:
            return json.load(f)

    def check_discounts(self, cart):
        dummy_cart = dict(cart)

        # SWAG discount
        if dummy_cart.get("VOUCHER", 0) > 0 and dummy_cart.get("TSHIRT", 0) > 0 and dummy_cart.get("MUG", 0) > 0:
            # Get how many times to apply the "SWAG" discount
            swag_amount = min([dummy_cart["VOUCHER"], dummy_cart["TSHIRT"], dummy_cart["MUG"]])

            dummy_cart["VOUCHER"] -= swag_amount
            dummy_cart["TSHIRT"] -= swag_amount
            dummy_cart["MUG"] -= swag_amount

            dummy_cart["SWAG"] = swag_amount

        # 2-for-1 VOUCHER discount
        if dummy_cart.get("VOUCHER", 0) >= 2:
            # Get how many times to apply the "2x1" discount
            voucher2x1_amounts = dummy_cart["VOUCHER"] // 2
            dummy_cart["VOUCHER"] -= voucher2x1_amounts * 2

            dummy_cart["VOUCHER2x1"] = voucher2x1_amounts

        # Bulk TSHIRT discount
        if dummy_cart.get("TSHIRT", 0) >= 3:
            dummy_cart["BULK_TSHIRT"] = dummy_cart["TSHIRT"]
            dummy_cart["TSHIRT"] = 0

        # Remove empty elements
        if dummy_cart.get("VOUCHER", 0) == 0:
            dummy_cart.pop("VOUCHER", None)
        if dummy_cart.get("TSHIRT", 0) == 0:
            dummy_cart.pop("TSHIRT", None)
        if dummy_cart.get("MUG", 0) == 0:
            dummy_cart.pop("MUG", None)

        return dummy_cart

    def scan(self, code):
        if code not in self._cart:
            self._cart[code] = 1
        else:
            self._cart[code] += 1

    def get_cart_original(self):
        return self._cart
        """for prod_code in self._products:
            if prod_code in self._cart:
                print(json.dumps({prod_code: self._cart[prod_code]}))"""

    def get_cart_discounted(self):
        return self.check_discounts(self._cart)

    def total(self):
        prices_sum = 0

        print("CART:", self.get_cart_original())
        print("DISCOUNTS:", self.get_cart_discounted())

        new_cart = self.get_cart_discounted()
        
        for prod in new_cart:
            prices_sum += (self._products[prod].price * new_cart[prod])

        return prices_sum


app = Store()

app.scan("VOUCHER")
app.scan("VOUCHER")
app.scan("VOUCHER")
app.scan("TSHIRT")
app.scan("MUG")

# print(app.get_cart_original())
print(app.total())
