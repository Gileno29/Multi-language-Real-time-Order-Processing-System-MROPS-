import unittest
import json
from models.order import Order

class TestOrder(unittest.TestCase):

    def setUp(self):
        self.order = Order(
            order_id=123,
            user_id=1,
            product="Notebook",
            price=3500.00,
            quantity="2",
            status="pending"
        )

    def test_to_dict(self):
        expected = {
            "order_id": 123,
            "user_id": 1,
            "product": "Notebook",
            "amount": "2",
            "status": "pending"
        }
        self.assertEqual(self.order.to_dict(), expected)

    def test_to_json(self):
        expected_dict = {
            "order_id": 123,
            "user_id": 1,
            "product": "Notebook",
            "amount": "2",
            "status": "pending"
        }
        expected_json = json.dumps(expected_dict)
        self.assertEqual(self.order.to_json(), expected_json)

    def test_default_status(self):
        order = Order(100, 2, "Mouse", 99.90, "1")  # sem passar status
        self.assertEqual(order.status, "created")

if __name__ == "__main__":
    unittest.main()
