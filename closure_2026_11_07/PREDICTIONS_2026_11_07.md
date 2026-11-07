# Kill tests, 2026-11-07: three frozen predictions, each with its statistic and the line that kills the law

Collection only, per DIRECTION_2026_11_07.md item 3 (c1f7a6299e). No new prediction, no new lane, no new number:
every value below is a literal from the committed source named beside it, and `predictions_check.py` checks each one
against that file (MUTATE must bite). It adopts nothing. Footings 9.3603e-11 / 1.1312e-10 m/s², graded separately,
never pooled. No ΛCDM inputs. Kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.
A result on the law's side is worded "survives", never "confirmed".

## 1. Gaia DR4 wide binaries: v3s predicts Newton

**Prediction** (CQ2, `cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/SEALED_PREDICTION.md`, 95303af61c). v3s screens every DR4
binary, so it reads as Newton. Max γ_r − 1 is 4.45e-05 canonical and 4.01e-05 alt at 30 kAU. Through the frozen
pipeline, γ_inf V3S is 1.0019 canonical and 1.0100 alt, identical to Newton's in every realisation. The bare law
(plain QUMOND, no screening) gives 1.1494 / 1.2081. v3s vs Newton is NOT SEPARABLE; v3s vs plain QUMOND is SEPARABLE.

**Statistic** (owner decision 2026-11-05, `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05_DR4_FORKS.md`, 413c1c8e24,
D1-D6 (a) adopted; D7/D8 closed in `OWNER_DECISION_2026-11-05b_DR4_D7_D8.md`, d71a111d1d). The pooled γ̂ from the
frozen pipeline, σ = √(σ_fit² + σ_sys²), σ_fit = 0.019 √(30000/N), σ_sys by definition (b) measured on DR4. v3s is
scored as the screened / medium-first reading of the frozen D2 rows plus the R rule. Newton = 1.000.

**The line that kills v3s:**
- Screened (medium-first) excluded iff γ̂ − 1.000 ≥ 3σ, and γ̂ is not below the law-first anchor by ≥ 3σ.
- In the alt overlap (γ̂ ≥ 3σ above Newton and ≥ 3σ below the law) the reading is BOTH EXCLUDED (D5).
- R rule: KILL iff R − 1 ≥ max(0.01, 3σ_R).
- **Gate:** σ_sys(b) < 0.048 canonical / 0.058 alt. If the gate fails, that footing reads UNDECIDED whatever γ̂ is.
- **No verdict:** γ̂ > 1.23 (guard zone) and γ̂ ≤ 1 − 3σ (sub-Newtonian, D4) give no verdict for every reading.

**Where the edge lands.**
- **At the registered error** (N = 30,000, σ_sys 0.020, canonical): v3s is EXCLUDED for γ̂ in 1.083 – 1.23. The alt
  medium-first edge is also 1.083.
- **At the realistic N** (DP2, `dr4_push_2026_11_05/DP2_n_forecast_triples/README.md`, 583697a4f7): the frozen cuts
  give about 8,000 pairs (low 7,025 / central 8,039 / high 8,618), not the registered 30,000. At the central N,
  canonical, anchor 1.1614, the screened-excluded edge moves with the error model:

  | σ_fit model | σ_sys | screened-excluded edge |
  |---|---|---|
  | registered 0.0367 | 0.020 | γ̂ ≥ 1.125 |
  | registered 0.0367 | 0.0375 | γ̂ ≥ 1.157 |
  | DR3-cal 0.0483 | 0.0375 | γ̂ ≥ 1.184 |

  The edge is a function of the measured σ, not a fixed number. The rule above is the frozen line; the numbers are
  where it lands under each error model.

**Power.** A Newtonian sky excludes the bare law with P(decisive) 0.80 at registered σ_fit and σ_sys 0.020, but only
0.40 at σ_sys 0.0375. DR4 can only kill v3s; a Newtonian sky never separates it from Newton.

## 2. a0(z) flat: a0 tracks ρ_DE, not H(z)

**Prediction** (CFG689, `campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689_summary.md`, 6c064b83a3). The primary
reading uses BAO + SN with curvature free and no ΛCDM input. It gives the law's tracking √X = a0(z)/a0(0):

| z* | median | 68 % | rival E = H/H0 median | e_3σ |
|---|---|---|---|---|
| 0 | 1.00 (by definition) | | | |
| 1.0 | 0.913 | [0.762, 1.027] | 1.761 | 0.055 |
| 1.5 | 0.942 | [0.706, 1.115] | 2.353 | 0.074 |
| 2.33 | 0.909 | [0.325, 1.212] | 3.490 | 0.084 |

The closest gap between the law and the rival is +0.453 dex at z* 2.33.

**Statistic** (AT1, `rebuild_2026_10_22/AT1_a0z_tracking_decision/FROZEN_CRITERIA.md`, 2d68f8e546, Lean-certified).
- ȳ = log10(a0(z*)/a0,ref), where the reference uses the same estimator at z < 0.1, so κ and the footing cancel.
- d_T = (ȳ − T)/√(e² + tX²) and d_R = (R − ȳ)/√(e² + tE²), on CFG689's primary quantiles.
- Gate G1 power: e ≤ e_3σ(z*); otherwise NOT POWERED.

**The line that kills the law's a0(z):** RIVAL FAVOURED (|d_R| ≤ 2 and d_T ≥ 3) or NEITHER (|d_T| > 3 and |d_R| > 3) at
a powered z*. Either one falsifies the law's a0(z) at that redshift on the measured sample.

**Who can decide it** (AT2, `rebuild_2026_10_22/AT2_a0z_on_disk_samples/README.md`, 7b2840d209). Nobody, on the
present record.
- Every on-disk sample is blocked: 22 in-domain samples, 52 (sample, z*) cells, 52 BLOCKED.
- No same-estimator z < 0.1 reference exists on disk.
- Every sample's common mode (0.30-0.60 dex) is 4-11x above the largest e_3σ (0.084 dex).
- The only decider is a proposal-class sample with its own same-estimator reference and a declared common mode below e_3σ.
  That means a proposal-class ALMA sample (DIRECTION_2026_11_07.md item 3b).

## 3. Lensing = dynamics

**Prediction** (V3W W3, `rebuild_2026_10_22/V3W_v3s_weak_spots/README.md`, ee4210e959). At O(GM) the Ψ equation has
no source, so lensing and dynamics see one potential. The bound is |M_lens/M_dyn − 1| ≤ 1.1e-5 / 2.8e-5 / 6.5e-5 /
1.9e-4 at 30 / 100 / 310 / 2600 kpc (canonical; alt ×1.2). In short, M_lens/M_dyn = 1 to ≤ 6.5e-5 at 310 kpc.

**Statistic** (V3W `FROZEN_CRITERIA.md`, W3). A = ΔΣ_obs/ΔΣ_law (GLS, full covariance), on two data sets:
- D1: KiDS-1000 isolated, R ≤ 0.31 Mpc.
- D2: GH1 matched hosts, 50–300 kpc.

**The line that kills the law (frozen grade, per footing):** FAIL iff D1 is more than 2σ_tot from 1, or D2 is more than
3σ_tot from 1.

**Measured (PASS):**

| data set | canonical | alt |
|---|---|---|
| D1 | A = 1.129 ± 0.206 (+0.6σ) | A = 1.035 ± 0.187 (+0.2σ) |
| D2 | 0.974 ± 0.248 | 0.890 ± 0.227 |

**Power: weak.**
- The D1 line has little power on amplitude: σ_sys scales with A.
- Even in the MUTATE twin, Newtonian-baryon lensing (A = 5.5) is only 1.9σ_tot on D1.
- M★ ±0.2 dex moves A over 0.93–1.33 (canonical).
- The direct test is a dynamical-mass measurement on the same isolated lenses. No frozen line exists for that
  measurement, and none is set here.

## What this file does not do

It sets no new kill line and grades no data. If new raw data arrive (DR4, an ALMA proposal-class sample), the same
frozen statistics above are re-graded and nothing else. Kappa = 1/2 FITTED; not theory closed.
