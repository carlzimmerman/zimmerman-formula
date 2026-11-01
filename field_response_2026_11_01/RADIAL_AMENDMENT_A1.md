# FR01 execution corrections, 1 November 2026

The frozen physical domain and numerical gates are unchanged.

1. radial_run_001 stopped before calculation because Python -I excluded the
   existing user-site NumPy/SciPy installation. The observed interpreter and
   installed package versions are in INPUTS.json. Subsequent runs use ordinary
   Python with the bounded runner's numerical thread controls. No installation.
2. radial_run_002 reached all six calculations, then strict JSON serialization
   rejected a NumPy Boolean. The original radial_stability.py is preserved.
   radial_stability_v2.py changes only conversion of NumPy scalar values to
   Python scalars for serialization; NaN/Infinity remain rejected. A regression
   control first failed for the absent adapter and then passed with it.

Neither unsuccessful run is current scientific evidence. New execution uses
radial_contract_v2.json and a fresh radial_run_003 directory; the initial
source and failed manifests remain available for provenance validation.
