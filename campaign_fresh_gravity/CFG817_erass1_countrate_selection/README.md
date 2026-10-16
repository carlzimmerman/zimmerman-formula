# CFG817: eRASS1 count-rate selection forward model. Eddington bias is SMALL; it does NOT explain the tercile pattern

**Fitted to the catalogue (12,247 clusters).**
- Completeness in source counts: logistic with N50 = 21.6 counts and N90 = 49.6 counts.
- Counts–mass relation: ln(N/Exp) ∝ 1.05 ln M_gas − 2 ln d_L + 2.22 z, with σ_int = 0.35.
- Measurement error: σ_meas(ln M_gas) = e^2.09 N^−0.80, i.e. 0.75 at 20 counts and 0.09 at 300.
- Mass-function slope (completeness-weighted): α = 2.13.

| version | median M_true/M_obs per tercile | CFG815 P terciles after | reading |
|---|---|---|---|
| **frozen primary** (condition on M_obs only) | 0.48 / 0.33 / **0.27** | 2.18 / 2.39 / 1.85 | **unphysical** (see below) |
| frozen MUTATE (no selection) | 0.04 / 0.04 / 0.04 | — | confirms the pathology |
| **post-freeze correction** (condition on M_obs AND observed counts) | **1.00 / 0.90 / 0.92** | **1.27 / 1.59 / 0.96** (still non-monotonic) | **credible** |
| CFG816's −ασ² approximation | 0.29 / 0.84 / 0.95 | 2.58 / 1.59 / 0.93 | overstated at low mass |

**The frozen result (REVISES) is not credible.**
- Conditioning only on M_obs lets very faint simulated clusters, with huge extrapolated measurement errors, flood each mass
  window. That gives a ×0.27 correction even for heavy clusters with 16% errors.
- A real catalogue cluster also has its observed counts. Conditioning on them is the correct question, and it makes the
  selection probability cancel (selection depends only on counts). This correction was made after seeing the frozen run, so
  it is disclosed as post-freeze.

**Credible result.**
- Eddington corrections are small: 0–10%.
- The non-monotonic tercile pattern **persists**: CFG815 P goes 1.27 / 1.59 / 0.96.
- **The middle-tercile shortfall (~1.6, Z ≈ +4) is real.** It is not a selection artefact.
- CFG816's crude −ασ² correction overstated the low-mass bias, as its own failed MUTATE suggested.

**Controls.** K1 null (C = 1, σ_meas = 0): max |corr − 1| = 0.003, PASS. 8 clusters (7 light) had too few simulation draws
and kept a correction of 1.

**Caveat.** The model treats the M_gas measurement noise as independent of the counts noise. In the catalogue, M_gas is
derived from the same X-ray photons, so the joint model is approximate.

κ fitted; not theory closed.
