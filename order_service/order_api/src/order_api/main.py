from confluent_kafka import Producer
import os
import json
from flask import Flask, request, jsonify
from random import choice
from kafka_utils.kafka_producer import KafkaProducer
from models.order import Order




producer = KafkaProducer(brokers='localhost:9092', topic='order')
def delivery_report(err, msg):
    if err:
        print(f'Erro ao enviar mensagem: {err}')
    else:
        print(f'Mensagem enviada para {msg.topic()} [{msg.partition()}]')



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

    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/order', methods=['POST'])
    def order():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400

        try:
            new_order = Order(
                order_id=data['order_id'],
                user_id=data['user_id'],
                product=data['product_id'],
                quantity=data['quantity'],
                price=data['price']
            )

            print(f'this is my order {new_order}')

            producer.send_message(
                key=str(new_order.order_id),
                value=new_order.to_json()
            )

            return jsonify({"message": "Order sent", "order_id": new_order.order_id}), 200

        except KeyError as e:
            return jsonify({"error": f"Missing field: {str(e)}"}), 400

    return app