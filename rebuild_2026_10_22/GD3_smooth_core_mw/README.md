# GD3_smooth_core_mw

**Question (owner, 10-29).** The smooth core ρ₀/(1+x²)^(3/2) pulls up to 0.3487 · 2πGρ₀r₀, against Burkert's 0.2545. With
that shape and q re-calibrated on SPARC for it, does the flagship (route E + OS1 core law) pass the Milky Way inside the
published priors? Criteria were frozen first (d5dafa534e).

## Verdict (frozen): UNDECIDED, footings disagree. The smooth shape does NOT rescue the Milky Way.

| | canonical | alt |
|---|---|---|
| q_fS (SPARC, smooth) vs OS1 Burkert q_f | **0.530** vs 0.892 | **0.366** vs 0.748 |
| SPARC A rms / median Υ at q_fS | 0.0632 / 0.53, line PASS | 0.0682 / **0.43, line FAIL** |
| MW Σ/Σ_a₀ (PRIMARY, V_last 173) | 1.339 (Burkert OS1: 1.635) | 1.223 (1.510) |
| **Class (PRIMARY, bg A)** | **FEASIBLE (WIDE PRIORS ONLY)** | **SPARC LINE FAILS** (MW: WIDE PRIORS ONLY) |
| cells passing all four lines | 5, all R_d 1.93 | 8, R_d 1.93–2.27 |
| best in-prior cell (R_d 2.60, M★ 6.1e10) | D 3.14: v_c 209.9, χ²_Ou 188 | D 2.17: v_c 213.0, χ²_Ou 130 |
| VARIANT (V_last 229), reported beside | WIDE PRIORS ONLY (in-prior D 1.84) | V+K ONLY (in-prior D 1.61) |

**Reading.**
- SPARC takes back the shape's gain. A flat-topped core holds more mass inside r₀, so SPARC wants a weaker σ-scaling:
  q falls from 0.89 → 0.53 (canonical) and 0.75 → 0.37 (alt). That lowers the Milky Way's Σ by about 20 %, which cancels
  most of the 37 % larger peak pull.
- Net: the Milky Way still passes only with short discs (R_d ≤ 2.27 kpc, outside Licquia & Newman's 2.64 ± 0.13), as in
  GD2. No cell inside both priors passes. On McMillan 2017 baryons, v_c(R₀) is 201.7 / 204.9 km/s (PRIMARY) against
  Eilers' 229.1 ± 4.6.
- On alt the smooth shape also fails SPARC's Υ floor (0.43 < 0.50), the same failure as X70_smooth_core_shape.
- The pre-freeze chat number (218.6 / 221.7 km/s, V_last 229) used the Burkert q with the smooth shape. That is not a
  consistent model. Reported here: at the Burkert q the smooth core goes V+K ONLY on the box (the K_z overshoot breaks Ou+24).
- So the external suggestion (Argon, relayed 10-29) that the smooth core lifts V_c to ~227 km/s at R_d 2.64 is not
  borne out: it double-counted OS1's Σ factor and ignored the q re-calibration.

**Checks 7/7.**
- K0: the Burkert shape reproduces OS1's q_f and SPARC rms exactly (both footings).
- K1: B_S matches quadrature; B_S(1) = 0.69707 (as X70).
- K2: Burkert + OS1 q reproduces GD2's classes and best-cell D on all four graded keys.
- K3–K4: the halo raises v_c and K_z in every cell; peak RSS 0.38 GB.
- MUTATE (q = 0): K5 fails as required. The q = 0 class is V+K ONLY on canonical.

κ = ½ FITTED; c_f not used; not theory closed. Nothing here says the data favour the framework.

## Files and reproduction

`FROZEN_CRITERIA.md`, `gd3_smooth_core_mw.py`, `.out` / `_results.json`, `_MUTATE` versions, `gd3_x30_machinery.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gd3_smooth_core_mw.py            # ~70 s
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gd3_smooth_core_mw.py --mutate   # q = 0, K5 must fail
