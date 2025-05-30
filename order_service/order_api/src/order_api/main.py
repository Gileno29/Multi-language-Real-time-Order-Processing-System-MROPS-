from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def delivery_report(err, msg):
    if err:
        print(f'Erro ao enviar mensagem: {err}')
    else:
        print(f'Mensagem enviada para {msg.topic()} [{msg.partition()}]')

producer.produce('meu-topico', key='chave1', value='Olá Kafka!', callback=delivery_report)
producer.flush()
