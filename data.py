'''Define data model and avro schema'''

# Define the data model in the supersymmetry dataset.
# The first column is the signal label (1 for signal, 0 for background),
# followed by the 18 features (8 low-level features then 10 high-level features).
# The first 8 features are kinematic properties measured by the particle detectors in the accelerator.
# The last 10 features are functions of the first 8 features.
# These are high-level features derived by physicists to help discriminate between the two classes.
# See https://archive.ics.uci.edu/ml/datasets/SUSY for more information.
SUSY_COLUMNS: 'list[str]' = [
          #  labels
           'signal',
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

# Schema used to serialize and deserialize AVRO records.
# This enables us to use Confluent Schema Registry to
#   enforce data quality standards.
SUSY_AVRO_SCHEMA = """
{
    "namespace": "10x_storage_machine_learning",
    "name": "SUSYRecord",
    "type": "record",
    "fields": [
        {"name": "signal", "type": "float"},
        {"name": "lepton_1_pT", "type": "float"},
        {"name": "lepton_1_eta", "type": "float"},
        {"name": "lepton_1_phi", "type": "float"},
        {"name": "lepton_2_pT", "type": "float"},
        {"name": "lepton_2_eta", "type": "float"},
        {"name": "lepton_2_phi", "type": "float"},
        {"name": "missing_energy_magnitude", "type": "float"},
        {"name": "missing_energy_phi", "type": "float"},
        {"name": "MET_rel", "type": "float"},
        {"name": "axial_MET", "type": "float"},
        {"name": "M_R", "type": "float"},
        {"name": "M_TR_2", "type": "float"},
        {"name": "R", "type": "float"},
        {"name": "MT2", "type": "float"},
        {"name": "S_R", "type": "float"},
        {"name": "M_Delta_R", "type": "float"},
        {"name": "dPhi_r_b", "type": "float"},
        {"name": "cos_theta_r1", "type": "float"}
    ]
}
"""