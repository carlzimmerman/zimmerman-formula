# CFG857 — does the extra speed V_x depend on size, and does that remove the MW/M31 offset?

Criteria: `FROZEN_CRITERIA.md` (588cea002, before the script). Run: `python3 cfg857.py` (MUTATE `CFG857_MUTATE=1`). Seconds.

## Result — CLASS: **NO SIZE DEPENDENCE** (the M31 offset is not a size effect; the pooled extra speed still passes SPARC)
- 25 dwarfs with an excess (MW + M31 + field): log V_x = 1.027 + 0.197 (±0.131) log(r_1/2/0.3 kpc) — β is 1.5σ from 0. Alt: β 0.190 ± 0.156.
- With a host term, the M31 offset at FIXED size stays: c = +0.175 ± 0.061 dex (2.9σ; alt 2.4σ). Larger M31 radii do not explain it.
- SPARC re-test with the pooled form (V0 = 10.6 km/s at 0.3 kpc, β 0.20): D = −0.012 ± 0.023 → still PASS (alt −0.041 ± 0.023, pass).
  K1 reproduces CFG856 (+0.017). MUTATE (r_1/2 shuffled): β 0.06 canonical (as required); alt 0.33 ± 0.15 (disclosed).
- **Reading:** the extra component is ~10–11 km/s for the pooled sample and compatible with SPARC either way, but M31 satellites carry
  ~1.5× the MW value at the same size. (CFG843 found the excess in Δ equal at matched g_bar; the V_x parametrisation weights the
  larger M31 systems differently.) A host-dependent amplitude, or a hidden systematic in M31 dispersions, remains open.

κ = ½ fitted; cold energy mass required; not theory closed.
