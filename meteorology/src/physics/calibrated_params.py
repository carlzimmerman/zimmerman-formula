# Calibrated Z² Intensity Model Parameters
# Generated: 2026-04-25T23:53:38.194089
# Training storms: irma_2017, maria_2017, michael_2018
# Test storms: dorian_2019, laura_2020

CALIBRATED_PARAMS = {
    'sst_threshold': 295.0000,  # K
    'mpi_slope': 14.0670,  # m/s per K
    'mpi_intercept': 36.2046,  # m/s
    'shear_scale': 9.7618,  # m/s
    'rate_coeff': 0.0410,  # fraction per hour
    'decay_rate': 0.0100,  # fraction per hour
    'z2_weight': 0.0266,  # structure contribution
}

# Performance metrics
# Training RMSE: 0.7644 m/s/hr
# Test RMSE: 0.3297 m/s/hr
