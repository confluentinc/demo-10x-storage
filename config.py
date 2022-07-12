"""Kafka and Schema Registry client configuration"""
import os
from dotenv import load_dotenv


# Load sensitive credentials from .env file into environment variables
load_dotenv()

# Define Kafka Configurations
KAFKA_CONFIG: 'dict[str,str]' = {
    # Kafka cluster
    "bootstrap.servers": os.environ["CCLOUD_BOOTSTRAP_ENDPOINT"],
    "sasl.username": os.environ["CCLOUD_CLUSTER_API_KEY"],
    "sasl.password": os.environ["CCLOUD_CLUSTER_API_SECRET"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    # Schema Registry
    "schema.registry.url": os.environ["CCLOUD_SCHEMA_REGISTRY_ENDPOINT"],
    "basic.auth.user.info": f"{os.environ['CCLOUD_SCHEMA_REGISTRY_API_KEY']}:{os.environ['CCLOUD_SCHEMA_REGISTRY_API_SECRET']}"
}

SCHEMA_REGISTRY_CONFIG: 'dict[str,str]' = {
    "url": KAFKA_CONFIG["schema.registry.url"],
    "basic.auth.user.info": KAFKA_CONFIG["basic.auth.user.info"]
}


if __name__ == "__main__":
    for item in KAFKA_CONFIG.items() :
        print(item)
