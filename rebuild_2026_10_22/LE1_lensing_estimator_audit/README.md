# LE1_lensing_estimator_audit: ESTIMATORS DISAGREE, NO DEFECT. The law's lensing failure survives every estimator swap. NP1's CX1 pass comes from CX1's error budget

Criteria `FROZEN_CRITERIA.md` (7efbb03f3d), committed alone before any script or number. `AMENDMENT_A1.md` (e6082dc9dd) is POST-RESULT: diagnostics only, no label changes. Script `le1.py`, with modes `controls`, `real`, `keys_controls`, `keys_real`, `post` (POST-RESULT) and `verdict`. Outputs are `le1_<mode>.{json,out}`. Run with `PYTHONHASHSEED=0 nice -n 10 python3 -I le1.py <mode>`, one thread, RSS under 0.45 GB. The key chain runs about 2 min per run, 26 runs in all.

**Not blind.** κ = ½ FITTED. The cold sector stays retired; nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. LE1 only reads: **no grader was edited.** The key chain runs from this lane's own copies, with one recorded hook (`HOOK` in `le1.py`).

## Verdict (frozen precedence)
- **Reproduction passes.**
  - R1, RQ3's A30: law +9.27 / +6.52, NP1 L3 +8.45 / +6.75. RQ3's own `rows_lens` and this lane's G1 both reproduce these exactly.
  - R2, all 60 key Z values against RQ3's cache: d 0.0.
  - R3, NP1's CX1 lensing z: +1.686 / +0.918.
- **MUTATE bites in every grader.**
- **One known answer fails, KA2a, and the miss is immaterial.**
  - The G2 cluster projector recovers ΔΣ of a SIS to 0.989 in the innermost bin. Line 0.01, miss 1.1 %.
  - The cause is the projector's inner start, not truncation: a truncated-SIS reference gives the same ratios (P2).
  - Bound on any key Z: 0.015 (law), 0.026 (NP1), against the 1.0 line. **No defect sets the label.**
- **G1 (A30) and G3 (CX1's lensing line) agree on the law: both FAIL.**
- **They disagree on NP1's L3 rule:** G1 FAIL +8.45 / +6.75, G3 PASS +1.69 / +0.92.
- **No single swap brings the law's A30 within |Z| 2,** on either footing.
- So the label is **ESTIMATORS DISAGREE, NO DEFECT**, with the spread reported as a systematic.
  - The disagreement is NP1's alone.
  - For the plain law, every estimator on record agrees the lensing data sit above it.

## Step 1: what each grader does
| | G1: RQ3 A30 (CRG1 Ln) | G2: 15 cluster keys (RQ3/LW1 path → NF1/X73 → X30 → X2/F1) | G3: CX1 lensing line (via NP1 `cx_rows`) |
|---|---|---|---|
| Data | KiDS-1000 bright isolated lenses, Fig-3, 4 M★ bins × 15 radii, 0.035-2.6 Mpc, ESD_t/(1+K) | eRASS1 clusters × KiDS-1000 sources (F1/CFG687 replay), 8 bins, 0.15-3 Mpc. Bands INNER 0-2, MID 3-5, OUTER 6-7 | Same Fig-3 files, raw e/(1+K), R ≤ 0.3 Mpc, 28 rows |
| Baryons | M★ + M_cg (gas-to-star relation) + hot gas 0.5 M★ min(1, (r/100 kpc)³), on a grid in M★ | β-model gas, r⁻³ past 2.2 R500, cut at 3 Mpc, +0.005 dex (GS4), × (1 + f★), f★ 0.034 / 0.0615 | Point mass M★ (WLENS-weighted bin mean) + 0.25 M★ gas, gas share 0.2 ASSUMED |
| Phantom mass, projection | M_lens = M_B ν(g_N/a0), the spherical dynamical mass. ΔΣ from CRG1's `Stencil` with a linear tail | M_lens = r² g/G from the candidate. ρ = dM/dr / 4πr². Σ by floored log-projection to 30 Mpc. ΔΣ taken at the bin centre (interpolated, not an annulus mean) | No model projection. The data are turned into g_obs = 4GΔΣ (the SIS deprojection) and compared to the candidate's g at R |
| Miscentring | none (isolated galaxies) | per cluster, the catalogue position against the X-ray fit, as a ring average on the model | none |
| Two-halo | P_grav template, free b ≥ 0 per bin | none | none |
| Boost/dilution | none; the published K bias divided out | data × B = den/den_r (DA1: B < 1 in places); leakage template subtracted | none |
| n(z), Σ_crit | the data's own. Native conversion F = (h_N/0.70) × 1.0128; R rescaled by χ | point Z_B, Z_B > z_l + 0.2, m −0.01, inverse-Σ_crit² weights; model × reduced-shear factor from per-cluster Σ_crit moments | the data's own, no native conversion |
| Stacking | lens-weighted stack over the M★ grid, masses at native h and Ω | W-weighted cluster sums per band and tercile, as a ratio to the C★ reference vector | one mean mass per bin |
| Aperture | fixed radii | fixed Mpc bins; terciles by catalogue Mgas500 / KT; R500 from eRASS1's ΛCDM-run catalogue | fixed radii |
| Covariance | published 60 × 60 | cluster bootstrap/jackknife per key, stat only | diagonal: CX1's Monte Carlo sd (data error + M★ 0.15 dex + gas ±0.1 ASSUMED, drawn per bin, then averaged as if independent) |
| Statistic | χ² after the b fit, Z = (χ² − 56)/√112, \|Z\| ≤ 2 | Z = (meas − pred)/s per key, worst over 2 h × 2 f★, \|Z\| ≤ 2 | weighted mean of log10(g_obs/g), z = mean/se, \|z\| ≤ 2 |

S2/BL1 (Brouwer+21 RAR, 4GΔΣ, own AQUAL ΔΣ) is described from its text only, not rerun.

## Step 2: known answers (`le1_controls.out`, `le1_keys_controls.out`)
| ID | Result | |
|---|---|---|
| KA1a G1 Stencil, against closed forms (SIS, point mass, NFW) | max dev 4e-6 | PASS |
| KA1b G1 noise-free self-recovery | χ² 1e-10, b to 4e-7 | PASS |
| KA1c G1 χ², 300 mocks | mean 58.0, sd 10.6 | PASS |
| KA1d G1 covariance assembly | each cell filled once, symmetric, positive definite | PASS |
| KA1e cross ESD against the covariance | χ²_x 51.2/60; 23.3/32 for R ≤ 0.31 | PASS: the covariance isn't underestimated |
| KA2a G2 projector | SIS 0.989-0.999 by bin (fails the 0.01 line in bin 0 only); NFW ≤ 0.11 %; Plummer 0.03 % | **FAIL, immaterial** (key Z bound ≤ 0.026) |
| KA2b G2 miscentring ring | ≤ 0.21 % | PASS |
| KA2c G2 swap hook, replica | dZ 0 | PASS |
| KA3a G3 4GΔΣ against the law's own profile | +0.006 / +0.006 dex (rows up to +0.019 at 35 kpc) | PASS |
| KA3b G3 SIS | 4e-6 | PASS |
| MUT (×2) | G1 χ² 154 → 970; G2 10 of 15 keys flip, pred × 2.006-2.09; G3 z moves 13 | BITES |

## Step 3: law, NP1 real L3 and Newton through each grader
**G1 swap ladder (Z, canonical / alt)**
| Swap | Law | NP1 L3 |
|---|---|---|
| S0 base (A30) | **+9.27 / +6.52** | **+8.45 / +6.75** |
| S1 R ≤ 0.31 | +5.55 / +3.59 | +5.38 / +4.58 |
| S2 no two-halo | +9.19 / +6.17 | +8.42 / +6.40 |
| S3 CX1 baryons | +16.13 / +12.05 | +10.25 / +7.58 |
| S4 diagonal covariance | +10.01 / +7.01 | +9.08 / +7.20 |
| S5 no native conversion | +10.14 / +7.03 | +9.14 / +7.28 |
| S6 one mass per bin | +9.13 / +6.52 | +8.35 / +6.76 |
| S7 all CX1-like | +10.44 / +7.50 | +3.76 / +2.84 |
| A1: G1 model, G3 statistic | z +6.69 / +3.78 (mean +0.089 / +0.050 dex) | z +5.43 / +4.69 |

Newton: +125 (fails everywhere, as it must).

**G3:**
| Model | z (canonical / alt) | Label |
|---|---|---|
| Law | +5.01 / +3.32 | FAIL |
| NP1 | +1.69 / +0.92 | PASS |
| Newton | +52 | FAIL |

With the model mapped to its own 4GΔΣ (KA3a's correction): law +4.74 / +3.07, NP1 +1.53 / +1.03. No label moves.

**G2 keys (fails of 15, canonical / alt):**
| Model | Base | K1 no miscentring | K2 no reduced shear |
|---|---|---|---|
| Law | 5 / 5 | 5 / 5 | 5 / 5 |
| NP1 | 4 / 6 | 4 / 6 | 3 / 5 |

- **The law's failing keys don't move:** G-MID-T2, T3, b, G-OUT-b, G-OUT-M3 (+4.76 / +3.99). Every one is meas > pred, the law short of mass. Model-side miscentring and reduced shear move them by ≤ 0.12.
- **NP1's failing keys:** OUTER over-predicted (G-OUT-all −3.01 / −3.31, Mall, M2), plus G-MID-T3 +2.08.
- **Data-side choices aren't rerun here** (B = 1, bin n(z) need X7's re-measurement or the 17 GB catalogue): NOT COMPUTABLE in this lane. DA1's record: n(z) worsens G-OUT-M3 to +5.19 on its candidates; B = 1 gives +4.83.

## What carries A30, and the NP1 disagreement
- **A30 for the law, by the frozen rule:** the largest single |ΔZ| is S3 (+6.9, CX1's point-mass baryons make it worse).
  - The only single swap that helps much is S1, dropping R > 0.31: −3.7 / −2.9. It still fails, at +5.55 / +3.59.
  - The χ² splits about evenly (P1): 72 inside 0.31 Mpc, 82 outside (canonical).
  - Data/model runs 1.1-1.8 at 0.3-1.5 Mpc in bins 2-4, and 0.6-0.8 at 35 kpc and at 2.6 Mpc.
  - The two-halo term, covariance, native conversion and stacking each move it by ≤ 0.9.
  - So A30's failure for the law isn't a choice of estimator among those on record. The data sit above the law at R ≤ 0.3 Mpc in every grader: A1 +0.089 dex, G3 +0.116 dex.
- **NP1: G3 PASS against G1 FAIL** comes mostly from G3's error budget, not from G3's estimator.
  - With data-only σ per row (P3), NP1 fails G3 too: +4.06 / +2.82.
  - The law fails harder with data-only σ: +9.14 / +6.42.
  - CX1's per-row sd (median 0.125 dex against 0.086 data-only) adds ASSUMED M★ and gas terms. These are drawn per bin but averaged over rows as if independent, so the error is treated incoherently.
  - The amplitude-only statistic matters less: with CX1-like baryons, one mass, no conversion and A30's statistic restricted (S7), NP1 still reads +3.76 / +2.84.
- **This is reported as a systematic, not a defect.** No known answer fails materially. Whether the row-level M★/gas term belongs in G3, and whether it should be coherent per bin, is the owner's call.

## Departures, all disclosed
1. **KA2a's NFW reference** is an independent quadrature of the profile truncated at the grid edge, as frozen. The SIS reference is untruncated. P2 shows truncation doesn't matter.
2. **G2's moved number for KA2a is a bound** (band deviation × |pred| / s), not a rerun with an exact projector. AMENDMENT_A1, post-result.
3. **The key chain** writes its X74 by-products (`x74_*`, gitignored) into this lane's directory and its runs into `cache_keys/` (gitignored, prints local paths). Only the `le1_*` JSON carry its numbers.
4. **The frozen "carries" rule names the worsening swap S3.** The text above also names S1, the one swap that helps.
5. **The first key attempt failed** on a path (run dir as HERE). It was rerun with HERE = this lane, as RQ3 does, before any key number was read.

κ = ½ FITTED. Not theory closed.
