import json
from collections import Counter

prod_file = "products.json"
disc_file = "discounts.json"


class Product:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

    def __str__(self):
        return json.dumps({
            "code": self.code,
            "name": self.name,
            "price": self.price
        })


class Store:
    def __init__(self):
        # Initialize empty cart and products list
        self._cart = {}
        self._products = {}

        # Setup the application by loading the products and discounts
        self._setup()

    def _setup(self):
        json_products = self.load_products()
        json_discounts = self.load_discounts()

        # Add a Product() object for each product defined in the JSON file
        for prod in json_products["products"]:
            self._products[prod["code"]] = Product(
                prod["code"], prod["name"], prod["price"])

        # Add a Product() object for each discount defined in the JSON file
        for disc in json_discounts["discounts"]:
            self._products[disc["code"]] = Product(
                disc["code"], disc["name"], disc["price"]
            )

    def load_products(self):
        # Load products from the JSON file
        with open(prod_file) as f:
            return json.load(f)

    def load_discounts(self):
        # Load discounts as another regular item
        with open(disc_file) as f:
            return json.load(f)

    def check_discounts(self, cart):
        # Create a copy of our cart as to not modify the original one
        dummy_cart = dict(cart)

        # SWAG discount
        if dummy_cart.get("VOUCHER", 0) > 0 and dummy_cart.get("TSHIRT", 0) > 0 and dummy_cart.get("MUG", 0) > 0:
            # Get how many times to apply the "SWAG" discount
            swag_amount = min(
                [dummy_cart["VOUCHER"], dummy_cart["TSHIRT"], dummy_cart["MUG"]])

            # Substract from our dummy cart the items included in the discount
            dummy_cart["VOUCHER"] -= swag_amount
            dummy_cart["TSHIRT"] -= swag_amount
            dummy_cart["MUG"] -= swag_amount

            # Add the "SWAG" Product instead of the previous items
            dummy_cart["SWAG"] = swag_amount

        # 2-for-1 VOUCHER discount
        if dummy_cart.get("VOUCHER", 0) >= 2:
            # Get how many times to apply the "2x1" discount
            voucher2x1_amounts = dummy_cart["VOUCHER"] // 2

            # Substract from our dummy cart the items included in the discount
            dummy_cart["VOUCHER"] -= voucher2x1_amounts * 2

            # Add the "VOUCHER2x1" Product instead of the previous items
            dummy_cart["VOUCHER2x1"] = voucher2x1_amounts

        # Bulk TSHIRT discount
        if dummy_cart.get("TSHIRT", 0) >= 3:
            # Equate the "BULK_TSHIRT discount to the amount of shirts over 3"
            dummy_cart["BULK_TSHIRT"] = dummy_cart["TSHIRT"]

            # Remove all "TSHIRT" items
            dummy_cart["TSHIRT"] = 0

        # Remove empty elements from dummy_cart
        if dummy_cart.get("VOUCHER", 0) == 0:
            dummy_cart.pop("VOUCHER", None)
        if dummy_cart.get("TSHIRT", 0) == 0:
            dummy_cart.pop("TSHIRT", None)
        if dummy_cart.get("MUG", 0) == 0:
            dummy_cart.pop("MUG", None)

        return dummy_cart

    def scan(self, code):
        # Dict.get(key, default_value) returns the value of key
        # or default_value if it is not defined, instead of raising KeyError
        self._cart[code] = self._cart.get(code, 0) + 1

    def clear_cart(self):
        self._cart = {}

    def get_cart_original(self):
        return self._cart

    def get_cart_discounted(self):
        return self.check_discounts(self._cart)

    def total(self):
        total = 0

        # Check for the total without altering the original cart
        new_cart = self.get_cart_discounted()
        for prod in new_cart:
            total += (self._products[prod].price * new_cart[prod])

        return total
