
from confluent_kafka import Producer

class KafkaProducer:
    def __init__(self, brokers: str, topic: str):
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': brokers})

    def delivery_report(self, err, msg):
        if err:
            print(f"Delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    
    def send_message(self, key: str, value: str):
        self.producer.produce(
            topic=self.topic,
            key=key,
            value=value,
            callback=self.delivery_report
        )
        self.producer.flush()