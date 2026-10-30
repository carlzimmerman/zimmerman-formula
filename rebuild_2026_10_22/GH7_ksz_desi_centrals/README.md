# GH7_ksz_desi_centrals

**Question.** kSZ measures the electron column at any temperature. Is the gas route E needs on KiDS lensing (Zhang's gas
continuing to about 1.8 R_vir, GH2) present around MW-mass centrals? Data: ACT DR6.02 NILC T map (fetched with the owner's OK)
× 380,881 DESI DR1 BGS centrals, log M★ 10.6–11.0. Criteria were frozen before the map was fetched (a80be1b705); amendments are in
`AMENDMENTS.md`.

## Verdict: VOID (pipeline not validated)

The stack alone gives the class BELOW ROUTE E'S NEED at both R values. **That class is void.** The positive control, frozen
before it ran, needed S/N ≥ 4 on massive BGS galaxies and got **3.81**. The threshold was not moved. This lane neither finds nor
excludes the gas.

| A at matched filter (velocity-shuffle σ) | k = 1 | k = 1.8 | k = 3 |
|---|---|---|---|
| frozen R = 1.263 | +0.10 ± 0.15 | **+0.04 ± 0.08** | +0.03 ± 0.07 |
| context R = 0.724 | +0.17 ± 0.26 | **+0.07 ± 0.14** | +0.05 ± 0.12 |

- No detection: null χ² 6.7/8, shuffle p 0.56. Jackknife σ on A(1.8) is 0.21 at context R, 1.5× the shuffle σ.
- Splits, A(1.8) at context R: passive +0.26 ± 0.17; star-forming −0.09 ± 0.24; north +0.09 ± 0.18; south +0.34 ± 0.19.

| Positive control (all BGS, no central cut) | N | matched S/N | null χ²/8 |
|---|---|---|---|
| log M★ > 10.5 | 1,007,867 | **3.81** | 28.0 |
| log M★ > 11 | 337,753 | 2.64 | 17.5 |
| log M★ > 11.25 | 106,123 | 1.78 | 6.2 |

## What it shows

1. **The pipeline sees something, but not enough to trust a shortfall.** The control's χ² of 28.0/8 and its positive T̂ look like kSZ.
   That is a reading of the numbers, not a pass of the rule. Published work gets S/N of about 9 for BGS on DR2 (arXiv:2604.19745).
   Their reconstruction, tuning and sample differ, and this lane is below that level; the cause is not established.
2. **Even k = 1, the gas Zhang measures, comes out low:** 0.17 ± 0.26 at context R, about 3σ below 1. A shortfall in measured gas
   is not specific to route E. It points at the model's normalisation (1.84 M★ inside R_vir, from X-ray with assumed metallicity) or at
   this pipeline, rather than at the extension beyond R_vir.
3. **Velocity scale is the weak point.** The frozen mock's R of 1.263 is probably inflated by low-k window leakage. β = 0.44 is inherited;
   A scales as β_true/0.44.
4. **Extent:** not claimed. G2 passes at frozen R (4.89) and fails at context R (2.80), and the class is void anyway.

**For the theory.** Route E's gas is still neither detected nor excluded by a mass-weighted probe. GH2's need stays open. κ = ½ FITTED;
c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data
favour the framework.

## Disclosures

- **The control was added after T̂ was seen.** The result looked too strong to accept, so I added it. The rule was committed before the
  control ran (amendment 6). It uses the k = 1.8 shape, which may not suit group halos and can lower the control's S/N.
- **Gate:** run with no T̂. Frozen R: S(1.8) 10.26, S(1.8 − 1) 4.89. Context R: 5.88, 2.80. The gate's forecast of S ≈ 6–10 was not met by
  anything in the control. That is a warning about the signal model, the velocities, or both.
- **Control vs lens count:** all 380,881 lenses had valid stamps, a higher pass rate than expected for this mask rule. Lenses were not
  checked against the ILC footprint mask, which was not fetched.
- **Mock limits:** no sub-mesh velocities, lognormal not back-transformed, RSD not removed in the reconstruction, no lens weights.
- K5's frozen text was wrong and was corrected before running. `gh7_vel.py` peaked at 4.3 GB (limit 3 GB).

## Checks (all PASS)

K1 projection (−6.5e-5); K2 pixel geometry (7e-11 px); K3 mock r 0.799, right sign; K4 aperture vs analytic (1.3 % at θ ≥ 2′);
K5 injection recovered (1.0000); MUTATE sign flip exact, shuffled stack null (p 0.96). **These test the code path, not whether the
velocities correlate with true velocities on the sky. The control is the only test of that, and it fell short.**

## Files

`FROZEN_CRITERIA.md`, `AMENDMENTS.md`, `gh7_select.py`, `gh7_vel.py`, `gh7_cap.py`, `gh7_gate.py`, `gh7_measure.py`, `gh7_control.py`,
with `.out` and `.json`. Run in that order with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`; `gh7_control.py` needs GH6's cache. Map and
work files are in `_external_data/act_dr6_nilc/` and `_external_data/gh7_work/` (not committed); map sha256 e9f8cb7c….

**Forward note (GH8_ksz_velocity_hardened):** about 12 % of the lenses here sit in near-blank map regions, and v_rec has large z-shell means. GH8 fixes both. Use its numbers, not these.
