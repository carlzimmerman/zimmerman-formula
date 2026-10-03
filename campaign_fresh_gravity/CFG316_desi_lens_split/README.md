# CFG316: does spectroscopic isolation keep the KiDS early/late split? Measurement stage

> **Frame.** κ = ½ is FITTED. FLAT a₀(z) is the framework's distinctive law; this lane does not test a₀(z). The cold component is still required and no particle is added. Nothing here says the data favour either model. A failure was checked as hard as a pass would have been.

**Criteria:** `FROZEN_CRITERIA.md` (c57c69a81). Decisions D1–D9 are binding and were followed. Interpretations and departures are listed in the dated appendix below; the frozen text was not edited.

## Bottom line
**NOT DIAGNOSTIC.** Under the frozen rules, the spectroscopic-isolation samples on the KiDS-1000 × DESI DR1 overlap are **empty**: ISO-S has 0 lenses and ISO-S4 has 0. So H1, H2 and H3 cannot be evaluated, and neither declared reading applies. The C1 contrast (ISO-P, 296 lenses) formally passes, but it cannot tell a KiDS-size split from zero (σ_A = 1.8).

This is not a statistical accident:
- the frozen completeness cut D5 keeps 1,034 of 48,497 lenses;
- the unobserved-target rule excludes nearly every lens, because a lens has a median of 70 unobserved BGS targets within 3 Mpc;
- even with neither of those, spectroscopic isolation at 3 Mpc / 1000 km/s / 0.1 M★ keeps only 2–8% of z < 0.3 lenses.

The diagnostics give the analytic power for re-specifications (no shear read). The best spectroscopic variant reaches about 0.9σ, and **no isolation at all** reaches 3.3σ (1.9σ at ×1.58). **On the KiDS overlap alone, at DR1, the spectroscopic-isolation question cannot be answered by any specification.** The DES Y3 / HSC Y3 overlaps (the Stage-B shear the frozen file defers) are required.

## Counts (`cfg316_stageA.out`)
| cut | lenses |
|---|---|
| BGS_BRIGHT targets in the KiDS footprint (nside-1024 source pixels; overlap 448.7 deg² vs 448.2 published) | 360,852 |
| + D1 good redshift | 282,157 |
| + 0.1 < z < 0.5 | 237,772 |
| + CIGALE main/bright match | 200,140 |
| + FLAG_MASSPDF ∈ [1/5, 5] | 198,178 |
| + AGNFRAC < 0.1 (frozen proposal) | 59,337 |
| + 8 < log M★ < 11 | 58,000 |
| + KiDS-bright match (class b) | 48,497 (early fraction 0.25) |
| + **D5 completeness** | **1,034** |
| ISO-S (3 Mpc, 1000 km/s) | **0** |
| ISO-S4 (4 Mpc, 2000 km/s) | **0** |
| ISO-P (KiDS photo-z rule, C1) | 296 (72 early / 224 late) |

- **R2:** 21 complete lenses are excluded only by unobserved targets. Ignoring unobserved targets would still leave ISO-S with 21 lenses, i.e. 1,013 have an observed qualifying neighbour.
- **Brute-force recount** (`cfg316_stageA_diag.out`, no KD-tree): 1,002 of 1,034 complete lenses have ≥ 1 neighbour with a CIGALE mass inside 3 Mpc / 1000 km/s. The median is 10 such neighbours, and 23 for ISO-S4.
- **The AGN cut is class-dependent:** it keeps 18% of early types and 52% of late types. Without it the base is 2,234 lenses, ISO-S 0, ISO-P 488.
- **M★ bins (ISO-P):** 10.0–10.5 has 0 early / 110 late, so no measurement is possible there. 10.5–11.0 has 72 early / 114 late.
- **R3, CIGALE − LePhare(+0.15):** +0.21 dex for late types, +0.17 for early; the class offset is −0.04 dex.

## Power (analytic; `cfg316_stageA.out`, variants in `cfg316_stageA_diag.out`)
The model scales the June per-class jackknife by Σ M_gal n_src Σcrit⁻²/D_A². Checked post hoc against the measured ISO-P σ(D), measured/predicted has a median of 1.09.

The table assumes a KiDS-size split is true and tests it against B's D_B.

| sample | N | λ (×1) | median σ (×1) | median σ (×1.58) |
|---|---|---|---|---|
| ISO-S / ISO-S4 (frozen) | 0 | — | — | — |
| ISO-P (frozen) | 296 | 0.11 | no power | no power |
| obs-only ISO-S, no D5, no AGN cut | 10,118 | 1.4 | 0.9 | 0.8 |
| ISO-P, no D5, no AGN cut | 34,021 | 4.7 | 1.5 | 1.0 |
| no isolation, no D5, no AGN cut | 138,307 | 18.4 | 3.3 | 1.9 |

"No power" means λ ≈ 0, so the expected p is about 0.5.

## Results (`cfg316_stageB.out`; jackknife N = 30, Hartlap 21/29)
- **ISO-S, ISO-S4:** no measurement possible.
- **ISO-P (C1 contrast):**
  - D = [2.5, 21, −124, −70, −32, 23, 188] ± [34, 42, 49, 68, 66, 101, 179] M☉/pc². The KiDS June D is [3.3 … 33].
  - χ² vs zero: 13.9/7, p 0.054 (1.9σ); at ×1.31, p 0.33; at ×1.58, p 0.59 (0.5σ).
  - χ² vs D_B: 14.1 / 14.2 (canonical / alt), p 0.049 / 0.048. At ×1.58 they are 0.55σ.
  - A_P = −2.3 ± 1.8: within 2σ of 1 (C1 PASS) and 1.25σ from zero. **C1 cannot discriminate.**
  - R7: the χ² is carried by bins 10 and 11. Dropping bin 10 gives p 0.76.
  - R4 (CIGALE class): A = 3.3 ± 2.0.
- **Decision under the frozen rules:** "C1 FAIL → NOT DIAGNOSTIC" does not literally apply, because C1 passes. But C1's pass is vacuous, and H1–H3 have no lenses. **The lane is NOT DIAGNOSTIC.** B's failure on the KiDS split is neither removed nor confirmed by spectroscopic isolation.

## CFG315's environment question (does strict isolation remove the ×1.8–3.3 excess?)
**Not answerable:** there are no spectroscopically isolated lenses.

For the record, K1 with the law at catalogue M★, using the **diagonal** covariance from `cfg316_stageB_posthoc.out`:

| sample | Q, canonical | Q, alt |
|---|---|---|
| ISO-P | 0.55 ± 0.76 | 0.50 ± 0.70 |
| non-isolated complete base (1,034) | 0.57 ± 0.41 | 0.52 ± 0.37 |

- The 14×14 GLS fit in `cfg316_stageB.out` gives negative Q (−2.2 ± 0.7 for ISO-P). That is a symptom of a noisy 30-patch covariance (Hartlap factor 0.48) and is not to be read.
- Taken at face value, the bright, low-z (median z 0.12) DESI lenses on KiDS show no ×2–3 excess. But these are 1,034 lenses, with KiDS raw e (about 1.5% low, no m-correction) and KiDS reading 8.6% low against DES+HSC. This is a post hoc, weak indication only.

## Controls
- **SELFTEST: PASS 3/3** (`cfg316_selftest.out`; synthetic shear, real e1/e2 not read).
  - Noiseless recovery to 2e-14.
  - The equal injection gives D/ESD < 0.4%.
  - On the 48k matched geometry: the equal case gives p 0.57; the planted split gives A = 1.11 ± 0.11.
  - On the ISO-P geometry over 50 realisations: mean χ² 7.2, mean A 0.88 ± 0.12, per-realisation σ_A 0.67.
- **C2: PASS.** The June 181,477-lens sums are reproduced to 3.1e-11.
- **C3: PASS** (nesting; trivially so, since both sets are empty).
- **C4: FAIL (kept).**
  - Randoms, tangential: p 0.14. Randoms, cross: 22.3/7, p 0.002. The lens cross shear is null (p 0.38–0.83).
  - Post hoc: the random cross is at most 12 M☉/pc², or 0.18 σ(D) of ISO-P. The June estimator removes no additive c-term (⟨e2⟩ = 6e-4). A term common to both classes largely cancels in D, but it was not removed.
- **MUTATE (seed 316, per-patch swap):** χ² vs zero 16.5/7, p 0.021, which passes the p > 0.01 line. The control is **not informative**, because the main run does not discriminate either.

## Caveats
- The hot gas and the early-type M/L offset are shared with KiDS; DESI does not fix them.
- The CIGALE masses use WMAP7 distances (R6: the effect on D_B is ≤ 0.4 M☉/pc²), with solar metallicity fixed.
- The isolation census does not see BGS targets outside the DR1 tiles (edge lenses).
- The unobserved-target rule is maximally conservative at DR1 completeness (78% in the overlap).

## Runtime
| step | time |
|---|---|
| Stage A | 1.7 min |
| diagnostics | 1 min |
| SELFTEST | 2.8 min |
| stacking pass | 22 s (12 processes) |
| scoring | 45 s each |
| post hoc | 50 s |

The work arrays are in `../_external_data/cfg316_work/` (36 MB, outside git).

## Files
- **Code:** `cfg316_common.py`, `cfg316_stageA.py`, `cfg316_stageA_diag.py` (post hoc), `cfg316_selftest.py`, `cfg316_stageB_stack.py`, `cfg316_stageB.py`, `cfg316_stageB_posthoc.py` (post hoc).
- **Outputs:** each script writes its `.out` and `_results.json`; MUTATE writes `cfg316_stageB_MUTATE.*`.
- **Run order** (from the repository root): stageA → stageA_diag → selftest → stageB_stack → stageB → MUTATE=1 stageB → stageB_posthoc.

## Appendix (2026-10-03): interpretations and departures (frozen text not edited)
1. **CIGALE quality cut.** D1–D9 did not settle it, so the frozen proposal (FLAG_MASSPDF ∈ [1/5, 5], AGNFRAC < 0.1) was applied to lenses. Neighbour masses use the FLAG cut only. The no-AGN-cut variant is reported.
2. **Lens mass range.** 8 < log M★(CIGALE) < 11, taken from the original KiDS lens limit M★ < 10¹¹; the frozen text does not state one.
3. **Class (b) match.** The match radius is < 1″, and the KiDS-bright object must have masked == 0 and a finite u−r. No photo-z window is applied.
4. **Class (a) valley.** Transferred by quantile-matching the KiDS early fraction on the matched overlap: threshold 1.643, 85% agreement.
5. **Flux-to-mass.** It uses the lens-class median observed-frame M★/(F_r D_L²) in 0.01-wide z bins, with classes from (a). It is applied to unobserved targets, to good-z neighbours without a sane CIGALE mass, and to the D5 limit. Using the early-type M/L for every lens would leave 317 complete lenses.
6. **ISO-P.** Computed with the KiDS LePhare(+0.15) mass and photo-z of each lens's KiDS counterpart against the committed KiDS pool (|Δχ| < 10 Mpc, 3 Mpc/χ).
7. **Patches.** agentK's RA-quantile scheme with N = 30, all in KiDS-N: there is no KiDS-S overlap.
8. **Significance.** Also quoted at ×1.31 (CFG315 S1), in addition to the frozen ×1 and ×1.58.
9. **Not done.** No lens outside the frozen samples was stacked with real shear, so any re-freeze stays blind.
10. **Post hoc scripts.** `cfg316_stageA_diag.py` and `cfg316_stageB_posthoc.py` change no frozen verdict.
