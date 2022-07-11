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

# Define the data model in the supersymmetry dataset.
# The first column is the class label (1 for signal, 0 for background),
# followed by the 18 features (8 low-level features then 10 high-level features).
# The first 8 features are kinematic properties measured by the particle detectors in the accelerator.
# The last 10 features are functions of the first 8 features.
# These are high-level features derived by physicists to help discriminate between the two classes.
# See https://archive.ics.uci.edu/ml/datasets/SUSY for more information.
COLUMNS: 'list[str]' = [
          #  labels
           'class',
          #  low-level features
           'lepton_1_pT',
           'lepton_1_eta',
           'lepton_1_phi',
           'lepton_2_pT',
           'lepton_2_eta',
           'lepton_2_phi',
           'missing_energy_magnitude',
           'missing_energy_phi',
          #  high-level derived features
           'MET_rel',
           'axial_MET',
           'M_R',
           'M_TR_2',
           'R',
           'MT2',
           'S_R',
           'M_Delta_R',
           'dPhi_r_b',
           'cos(theta_r1)'
           ]

if __name__ == "__main__":
    for item in KAFKA_CONFIG.items() :
        print(item)
    print(COLUMNS)