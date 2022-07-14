'''Prodce SUSY data to Confluent Cloud topics'''
import csv
import random
import sys
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from config import KAFKA_CONFIG, SCHEMA_REGISTRY_CONFIG, TOPIC_TRAIN, TOPIC_TEST
from data import SUSY_COLUMNS, SUSY_AVRO_SCHEMA




def log_produce_errors(err, msg):
    """Producer callback to log records that failed to send"""
    if err:
        print(f"Failed to producer with error {err}", file=sys.stdout)


def produce_SUSY_data(
    path_to_csv: str,
    producer: SerializingProducer
    ) -> None:
    """produce SUSY records to Kafka from CSV"""
    records_produced = 0
    with open(path_to_csv) as data:
        reader = csv.DictReader(data,fieldnames=SUSY_COLUMNS)
        for row in reader:
            row_with_float_values = {field:float(value) for field, value in row.items()}
            rand = random.random()
            while True:
                try:
                    # randomly select 70% of data to the training set and 30% to test
                    if rand < 0.7:
                        producer.produce(
                            topic=TOPIC_TRAIN,
                            value=row_with_float_values,
                            on_delivery=log_produce_errors)
                    else:
                        producer.produce(
                            topic=TOPIC_TEST,
                            value=row_with_float_values,
                            on_delivery=log_produce_errors)
                    producer.poll(0)
                    records_produced += 1
                    break
                except BufferError as err:
                    print(err, file=sys.stderr)
                    print(f"produced {records_produced} records", file=sys.stdout)
                    producer.flush()
    print(f"produced a totoal of {records_produced} records", file=sys.stdout)
    producer.flush()

if __name__ == "__main__":

    # configure schema registry client and avro serializer
    schema_registry_client = SchemaRegistryClient(SCHEMA_REGISTRY_CONFIG)
    SUSY_avro_serializer = AvroSerializer(
        schema_registry_client=schema_registry_client,
        schema_str=SUSY_AVRO_SCHEMA
    )
    producer_config = KAFKA_CONFIG.copy()
    producer_config['value.serializer'] = SUSY_avro_serializer

    # Configure other producer properties to tune performance. 
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    producer_config['queue.buffering.max.messages'] = 1000000
    producer_config['linger.ms'] = 500
    producer_config['batch.size'] = 2000000
    producer_config['compression.type'] = 'snappy'

    # Create producer and produce data
    SUSY_producer = SerializingProducer(producer_config)
    produce_SUSY_data('./SUSY.csv', producer=SUSY_producer)
