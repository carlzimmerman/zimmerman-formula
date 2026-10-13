# CFG684 — narrowing the tracking band CMB-free: chronometers + SN-set swaps (criteria 4696798a1; block CFG680–689)

Inputs (outside the repo, `_external_data/cfg684_inputs/`): Moresco CCcovariance BC03 table (15 H(z), cov = diag + IMF + SPS-ooo per
Moresco's notebook; H0 profiled, no prior); DES-SN5YR **Dovekie** recalibrated Hubble diagram (the release now on des-science/DES-SN5YR;
SNANA format; STAT+SYS inverse cov); Union3 binned spline-node μ + weight matrix. BAO/X(z)/bands as CFG681–683. No CMB.
| combination | Δχ²_max over Ω_m 0.24–0.36 | tracking √X(2.33) band | rival E(2.33) | e_3σ (z* 2.33) | flat-a0 Ω_m |
|---|---|---|---|---|---|
| BAO+PP (ref) | 0.48 | 0–2.18 | 3.44–3.55 | 0.051 | 0.3086 ± 0.0078 |
| BAO+CC | 0.22 | 0–2.35 | 3.27–3.63 | none | 0.2866 ± 0.0143 |
| BAO+PP+CC | 0.53 | 0–2.17 | 3.43–3.55 | 0.050 | 0.3082 ± 0.0078 |
| BAO+DES5+CC | 1.72 | 0.69–2.17 | 3.43–3.53 | 0.056 | 0.3070 ± 0.0073 |
| BAO+U3+CC | 1.48 | 0.58–2.30 | 3.47–3.59 | 0.042 | 0.3154 ± 0.0081 |
| BAO+DES5 | 1.67 | 0.69–2.17 | 3.43–3.53 | 0.056 | 0.3067 ± 0.0074 |
| BAO+U3 | 1.41 | 0.29–2.31 | 3.48–3.60 | 0.040 | 0.3159 ± 0.0082 |
- **DEGENERACY NOT BROKEN** by any combination (Δχ²_max ≤ 1.72 < 4). The 15 chronometers add almost nothing (σ_H 4–50 km/s/Mpc).
  χ² minimum sits at the Ω_m = 0.24 grid edge in every combination (the degenerate direction; not a measurement).
- **ROBUST**: flat-a0 Ω_m from DES5(+CC) and U3(+CC) agree with PP(+CC) within 1σ (largest gap U3 +0.0072 vs combined σ 0.011).
  All four SN choices agree with Planck's 0.3153 ± 0.0073 (0.4–0.8σ; Union3 lands on it).
- DES5 and Union3 lift the tracking band's lower edge at z 1–2.33 (≥ 0.58–0.69 at 2.33, ≥ 0.79 at 1.5): with them, a0 cannot have
  collapsed by cosmic noon under the tracking law. The CMB-free decision target stays e ≈ 0.04–0.06 dex (z* 2.33).
MUTATE (CC → BAO+PP best-fit E(z)): χ²_min(BAO+PP+CCmock) − χ²_min(BAO+PP) = −0.005 ≤ 1 ✓.
κ fitted; cold energy mass required; not theory closed.
