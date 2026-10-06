# Neutrino mass hypothesis vs DESI DR2 (2026-10-06)

Hypothesis (labelled speculation, unforced; coefficient 1 fitted by inversion): m_lightest = rho_Lambda^(1/4) = 2.24 meV, normal ordering, so sum m_nu = 0.0613 eV.

Data: Elbers et al. 2025 (arXiv:2503.14744), DESI DR2 Results II (arXiv:2503.14738). Numbers read from the paper text.

| check | result |
|---|---|
| m_l < 0.023 eV (95%) | pass (0.0022) |
| sum < 0.0642 eV (LCDM, 95%) | pass by 0.0029 eV (0.15 sigma) |
| sum < 0.053 eV (Feldman-Cousins 95%) | FAIL |
| sum < 0.163 eV (w0wa, 95%) | pass |
| effective-mass tension | FAIL at ~3.0 sigma (calibrated to DESI's 3.0 at 0.059) |

Reading: the hypothesis sits 0.0026 eV (0.06 sigma) above the minimal normal-ordering sum, so DESI cannot separate it from minimal normal ordering. It shares the tension that DESI + CMB in LCDM puts on all neutrino masses allowed by oscillations, and it gets no worse. This is not evidence for the hypothesis. It can be killed only if the cosmological tension resolves to a sum below 0.0613 while oscillations still hold, or the inverted ordering is established.

R1/R2: background radiation as the source of a0. Dipole drag from the CMB (or a relic-neutrino bound with full absorption) on a Sun moving at 220 km/s is ~3e-29 m/s^2, ~1e-19 a0. It also points against the motion, not toward the centre.

Run: `python3 nu_desi_test.py` (5/7, exit 0); `MUTATE=1 python3 nu_desi_test.py` plants the inverted-ordering floor 0.101 eV and the LCDM 95% limit flips to FAIL (4/7).
