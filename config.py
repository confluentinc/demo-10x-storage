'''configure kafka client'''
import os
from dotenv import load_dotenv

load_dotenv()



KAFKA_CONFIG = {
    "": os.environ["CCLOUD_BOOTSTRAP_ENDPOINT"],
    "": os.environ["CCLOUD_CLUSTER_API_KEY"],
    "": os.environ["CCLOUD_CLUSTER_API_SECRET"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN"
}