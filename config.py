import os
from dotenv import load_dotenv


# Load sensitive credentials from .env file into environment variables
load_dotenv()

# Define Kafka Configurations
KAFKA_CONFIG: dict = {
    "bootstrap.servers": os.environ["CCLOUD_BOOTSTRAP_ENDPOINT"],
    "sasl.username": os.environ["CCLOUD_CLUSTER_API_KEY"],
    "sasl.password": os.environ["CCLOUD_CLUSTER_API_SECRET"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN"
}

if __name__ == "__main__":
    for item in KAFKA_CONFIG.items() :
        print(item)
