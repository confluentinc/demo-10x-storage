'''Prodce SUSY data to Confluent Cloud topics'''
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from config import KAFKA_CONFIG
from data import SUSY_COLUMNS
import csv
import random

with open('./sample.csv') as data:
    reader = csv.DictReader(data,fieldnames=SUSY_COLUMNS)
    for row in reader:
        row_with_float_values = {field:float(value) for field, value in row.items()}
        r = random.random()
        if r < 0.7:
            print("produce to train")
        else:
            print("produce to test")
        print(row_with_float_values, '\n')