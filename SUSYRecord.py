from dataclasses import dataclass

@dataclass
class SUSYRecord:
    """
    Class that represents a record in the SUSY dataset.
    The first column is the 'signal' label (1 for signal, 0 for background),
    followed by the 18 features (8 low-level features then 10 high-level features).
    The first 8 features are kinematic properties measured by the particle detectors in the accelerator.
    The last 10 features are functions of the first 8 features.
    These are high-level features derived by physicists to help discriminate between the two classes.
    See https://archive.ics.uci.edu/ml/datasets/SUSY for more information. 
    """
    # labels
    signal: float
    # low-level features
    lepton_1_pT: float
    lepton_1_eta: float
    lepton_1_phi: float
    lepton_2_pT: float
    lepton_2_eta: float
    lepton_2_phi: float
    missing_energy_magnitude: float
    missing_energy_phi: float
    # high-level features
    MET_rel: float
    axial_MET: float
    M_R: float
    M_TR_2: float
    R: float
    MT2: float
    S_R: float
    M_Delta_R: float 
    dPhi_r_b: float
    cos_theta_r1: float
