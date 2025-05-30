import os
import json
from flask import Flask
from random import choice
from kafka import KafkaProducer
from models.order import Order

KAFKA_BROKER = 'localhost:9092'
TOPIC = 'orders'

config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:9092',  # if in same Docker network
    # or
        #'sasl.username':     '<CLUSTER API KEY>',
        #'sasl.password':     '<CLUSTER API SECRET>',

        # Fixed properties
        #'security.protocol': 'SASL_SSL',
        #'sasl.mechanisms':   'PLAIN',
        #'acks':              'all'
    }
def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(topic=msg.topic(),
                                                                                               key=msg.key().decode('utf-8'),
                                                                                               value=msg.value().decode('utf-8')))

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print("im the error")
    #log.error('I am an errback', exc_info=excp)



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/order')
    def order():
        new_order = Order(20, 10, 30, 200.00)
        producer = KafkaProducer(bootstrap_servers='localhost:9092',retries=5, key_serializer=lambda x: json.dumps(x).encode("ascii"), value_serializer=lambda x: json.dumps(x).encode("ascii"))

        try:
            producer.send(TOPIC, new_order.to_json()).add_callback(on_send_success).add_errback(on_send_error)

        except Exception as e:
            print(e)

        #producer.poll(10000)
        producer.flush()
        return 'your order was sent'

    return app
create_app()