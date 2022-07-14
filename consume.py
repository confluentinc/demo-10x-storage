"""Consume from Kafka topic and train ML model"""

import tensorflow as tf
import tensorflow_io as tfio

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

from config import TOPIC_TEST, TOPIC_TRAIN, KAFKA_CONFIG, SCHEMA_REGISTRY_CONFIG
from data import SUSY_AVRO_SCHEMA, SUSY_COLUMNS


def deserialize_kafka_record(raw_record_value, raw_record_key):
    """
    Deserialize avro value and transform into a structure tf.keras model expects.
    The model expects a tuple (x,y) where x is a list representing a SUSY data row *without* the "signal" column (features),
    and y represents the "signal" column (label).
    """
    record_value = tfio.experimental.serialization.decode_avro(raw_record_value, schema=SUSY_AVRO_SCHEMA)
    # tf.print(record_value)
    record_key = record_value.pop('signal')
    # tf.print([v for k,v in record_value.items()])
    return [v for k,v in record_value.items()], record_key

schema_registry_client = SchemaRegistryClient(SCHEMA_REGISTRY_CONFIG)
SUSY_avro_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    schema_str=SUSY_AVRO_SCHEMA
)

consumer_config = KAFKA_CONFIG.copy()
# consumer_config['value.deserializer'] = SUSY_avro_deserializer
consumer_config['auto.offset.reset'] = "earliest"

BATCH_SIZE=1000
SHUFFLE_BUFFER_SIZE=1000

train_ds = tfio.experimental.streaming.KafkaGroupIODataset(
    topics=[TOPIC_TRAIN],
    group_id="training_group",
    servers= consumer_config['bootstrap.servers'],
    configuration=[f"{k}={v}" for k,v in consumer_config.items()]
)
# Remove schema ID (4 bytes) and magic byte from record value.
# See https://blog.devgenius.io/how-the-kafka-avro-serialization-works-581abf7f3959
train_ds = train_ds.map(lambda v, k: (tf.strings.substr(v, 5, -1), k))
# Deserialize avro value
train_ds = train_ds.map(deserialize_kafka_record)
train_ds = train_ds.shuffle(buffer_size=SHUFFLE_BUFFER_SIZE)
train_ds = train_ds.batch(BATCH_SIZE)



# Set the parameters

OPTIMIZER="adam"
LOSS=tf.keras.losses.BinaryCrossentropy(from_logits=True)
METRICS=['accuracy']
EPOCHS=10

# design/build the model
model = tf.keras.Sequential([
    # inputs are all columns except "signal". We are trying to predict "signal"
    tf.keras.layers.Input(shape=(len(SUSY_COLUMNS)-1,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

print(model.summary())


# compile the model
model.compile(optimizer=OPTIMIZER, loss=LOSS, metrics=METRICS)

# fit the model
model.fit(train_ds, epochs=EPOCHS)


# Infer on the test data
test_ds = tfio.experimental.streaming.KafkaGroupIODataset(
    topics=[TOPIC_TEST],
    group_id="testing_group",
    servers= consumer_config['bootstrap.servers'],
    configuration=[f"{k}={v}" for k,v in consumer_config.items()]
)
# Remove schema ID (4 bytes) and magic byte from record value.
# See https://blog.devgenius.io/how-the-kafka-avro-serialization-works-581abf7f3959
test_ds = test_ds.map(lambda v, k: (tf.strings.substr(v, 5, -1), k))
# Deserialize avro value
test_ds = test_ds.map(deserialize_kafka_record)
test_ds = test_ds.batch(BATCH_SIZE)

res = model.evaluate(test_ds)
print("test loss, test acc:", res)
