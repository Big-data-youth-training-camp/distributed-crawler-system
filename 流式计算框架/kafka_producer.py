from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['localhost:9092','localhost:9093','localhost:9094'])
producer.send('flink-stream-in-topic', b'www.baidu.com')
producer.flush()