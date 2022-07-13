"""Consume from Kafka topic and train ML model"""

import pandas as pd
import tensorflow as tf
import tensorflow_io as tfio

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

from config import TOPIC_TRAIN, KAFKA_CONFIG, SCHEMA_REGISTRY_CONFIG
from data import SUSY_AVRO_SCHEMA


schema_registry_client = SchemaRegistryClient(SCHEMA_REGISTRY_CONFIG)
SUSY_avro_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    schema_str=SUSY_AVRO_SCHEMA
)

consumer_config = KAFKA_CONFIG.copy()
consumer_config['value.deserializer'] = SUSY_avro_deserializer

BATCH_SIZE=64
SHUFFLE_BUFFER_SIZE=64

train_ds = tfio.IODataset.from_kafka(
    topic=TOPIC_TRAIN,
    configuration=consumer_config
)

train_ds = train_ds.shuffle(buffer_size=SHUFFLE_BUFFER_SIZE)
train_ds = train_ds.map(decode_kafka_item)
train_ds = train_ds.batch(BATCH_SIZE)