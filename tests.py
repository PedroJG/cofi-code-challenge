import unittest
from store import store
from store.store import ProductNotRegisteredError

app = store.Store()


class Tests(unittest.TestCase):
    def test_enunciado(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("TSHIRT")
        app.scan("MUG")
        self.assertEqual(app.total(), 30.0)

    def test_enunciado_not_equal(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("TSHIRT")
        app.scan("MUG")
        self.assertNotEqual(app.total(), 42.5)

    def test_fake_product(self):
        app.clear_cart()
        self.assertRaises(ProductNotRegisteredError, app.scan, "ASDF")
        
    def test_one_swag(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("TSHIRT")
        app.scan("MUG")
        self.assertEqual(app.total(), 25.0)

    def test_two_swag(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("MUG")
        app.scan("MUG")
        self.assertEqual(app.total(), 50.0)
        
    def test_swag_and_bulk_wrong(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("MUG")
        self.assertNotEqual(app.total(), 67.0)
        
    def test_swag_and_bulk(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("MUG")
        self.assertEqual(app.total(), 65.0)
        
    def test_two_swag_and_2x1_and_three_shirt(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("MUG")
        app.scan("MUG")
        self.assertEqual(app.total(), 112.0)

    def test_one_2x1(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        self.assertEqual(app.total(), 5.0)

    def test_two_2x1(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        self.assertEqual(app.total(), 10.0)

    def test_five_2x1(self):
        app.clear_cart()
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        app.scan("VOUCHER")
        self.assertEqual(app.total(), 25.0)

    def test_two_shirts(self):
        app.clear_cart()
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        self.assertEqual(app.total(), 40.0)

    def test_three_shirts(self):
        app.clear_cart()
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        self.assertEqual(app.total(), 57.0)
        
    def test_ten_shirts(self):
        app.clear_cart()
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        app.scan("TSHIRT")
        self.assertEqual(app.total(), 190.0)


if __name__ == '__main__':
    unittest.main()
