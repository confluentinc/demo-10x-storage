'''Prodce SUSY data to Confluent Cloud topics'''
from confluent_kafka import Producer
from config import KAFKA_CONFIG