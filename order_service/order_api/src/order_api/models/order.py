
import random
import time
# Connect to Kafka broker (Docker container network name)


# Create a Kafka producer


class Order:
    def __init__(self, order_id: int, user_id: int, product: str, amount: float, status: str = "created"):
        self.order_id = order_id
        self.user_id = user_id
        self.product = product
        self.amount = amount
        self.status = status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "product": self.product,
            "amount": self.amount,
            "status": self.status
        }

    def to_json(self):
        return json.dumps(self.to_dict())