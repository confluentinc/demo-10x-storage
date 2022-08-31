"""Kafka and Schema Registry client configuration"""
import os
import sys

try:
    os.environ["CCLOUD_CLUSTER_API_KEY"]
except KeyError:
    print("please source the env.sh script to set up your environment")
    sys.exit(1)

# hardcode training and validation topic names
TOPIC_TRAIN = "10x.storage.machine-learning.train"
TOPIC_TEST = "10x.storage.machine-learning.test"

# Define Kafka Configurations
KAFKA_CONFIG: 'dict[str,str]' = {
    # Kafka cluster
    "bootstrap.servers": os.environ["CCLOUD_BOOTSTRAP_ENDPOINT"],
    "sasl.username": os.environ["CCLOUD_CLUSTER_API_KEY"],
    "sasl.password": os.environ["CCLOUD_CLUSTER_API_SECRET"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN"
    }

SCHEMA_REGISTRY_CONFIG: 'dict[str,str]' = {
    "url": os.environ["CCLOUD_SCHEMA_REGISTRY_ENDPOINT"],
    "basic.auth.user.info": f"{os.environ['CCLOUD_SCHEMA_REGISTRY_API_KEY']}:{os.environ['CCLOUD_SCHEMA_REGISTRY_API_SECRET']}"
}


if __name__ == "__main__":
    for item in KAFKA_CONFIG.items() :
        print(item)
