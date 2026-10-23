# F1_cluster_cores — the eRASS1 × KiDS cluster-core excess, rebuilt from the raw data

## Verdict: REAL FAILURE (of the law on the clusters' baryons)

The core excess survives every correction. In the primary rebuild (AQUAL μ = x/(1+x), native h 0.672–0.686, eRASS1 gas
rescaled to the pipeline's distances, catalogue miscentring), A_MID = **1.68–1.72 ± 0.12 (canonical, Z +5.6 to +6.2)** and
**1.54–1.58 ± 0.11 (alt, Z +4.9 to +5.5)**. With the boost sign fixed (A1, post-result) it is 1.81–1.85 / 1.66–1.70
(Z +5.5 to +6.9). At the corner most favourable to the law (f* = 0.30, Mgas500 at its +1σ, deep-X-ray gas factor ×1.09,
X-COP gas shape), A_MID is still 1.33–1.37 (Z +3.4 / +4.0) canonical and 1.23–1.26 (Z +2.5 / +3.0) alt. That corner also
pushes the outskirts below the law (A_OUTER 0.79 / 0.73), so the shape problem is there too. The frozen rule says REAL FAILURE.

κ = ½ is FITTED. The two footings are never pooled. No dark-matter particle. The theory is not closed.

## Reproduction (same data read)

- K1: the record's per-cluster file gives A_MID = 1.9102, the same as its JSON.
- K2: my own KiDS extraction (21,262,011 rows, own reader) and own estimator give a stack within 1.0σ of CFG687 in every
  MID/OUTER bin (z = −0.46…+0.73).
- K3: the record's recipe on my pipeline gives A_MID 1.868 ± 0.126 / 1.715 ± 0.115 and A_OUTER 1.042 / 0.954, with 326
  clusters. The record has 1.91 / 1.75 and 1.01 / 0.93 with 318.
- K4 projection self-test to < 0.4 % in MID/OUTER. K5 the spherical AQUAL identity holds to 4e-16. K6 the FITS and TSV agree exactly.
- Checks 6/6 PASS. `--mutate` (cross shear) breaks K2/K3 (4/6); the cross-shear MID is 0.28 ± 0.14 (2.0σ; CFG687 had 0.16 ± 0.11), disclosed.

## One correction at a time (from R0; canonical / alt A_MID, Z)

| correction | A_MID canonical | A_MID alt |
|---|---|---|
| R0 record recipe (ν_mono, h 0.70) | 1.868 (+6.9) | 1.715 (+6.2) |
| C1 ν_mono → AQUAL μ = x/(1+x) | 1.865 (+6.9) | 1.713 (+6.2) |
| C1b AQUAL vs QUMOND at fixed μ (spherical) | identical (K5) | identical |
| C2a eRASS1 gas rescaled to the pipeline distances (q^{5/2}) | 1.836 (+6.8) | 1.686 (+6.0) |
| C2 native h 0.672 / 0.686 (+ rescale) | 1.800 / 1.847 | 1.653 / 1.696 |
| C3a R500 ±0.033 dex (gas at fixed r) | 1.874 / 1.862 | 1.721 / 1.710 |
| C3b Mgas500 +1σ / −1σ | 1.639 / 2.273 | 1.506 / 2.085 |
| C3c X-COP measured gas shape / gas inside R500 only | 1.860 / 1.814 | 1.707 / 1.665 |
| C3d deep X-ray gas factor ×1.091 (ACCEPT 51 matches, median 1.034; X-COP 5, 1.236) | 1.780 (+6.5) | 1.635 (+5.8) |
| C4 stars f* 0.30 / 0.10 | 1.787 / 1.960 | 1.642 / 1.799 |
| C5a catalogue miscentring | 1.878 | 1.724 |
| C5b data "boost" (0.85–0.96: a deficit, see A1) | 1.734 | 1.592 |
| C5c two-halo bound (OUTER residual over the law) | bound 0, no change | bound 0 |
| C5d Σ_crit with bin n(z) (bound) | 2.028 | 1.862 |

The field equation does almost nothing. ν_mono is within 0.2–2 % of the action's ν at cluster accelerations, and AQUAL equals
QUMOND in spherical symmetry. Native h moves A_MID by 1–4 %, and the gas rescale by 1.5 %. The largest single lever is the
catalogue's own Mgas500 error (±12 %). The deep-X-ray cross-calibration says the eRASS1 gas is about right: 1.03 (16–84 %:
0.71–1.27). The photo-z dilution bound and the miscentring both make the excess larger. Newtonian baryons alone give
A_MID 9.8 ± 0.6.

## What the V3 theory says about cold mass inside 1 Mpc

NOT DERIVED. In V3 the Blanchet–Skordis dust abundance is an initial condition (FITTED; C2, C4). No nonlinear cluster profile
has been computed, and the BS mass μ (μ⁻¹ ≫ 100 kpc, free) is not in the parameter table. Reported only, never graded
(primary, h 0.672, dust traces the gas and sources the AQUAL field):

- To reach A_MID = 1 the dust must be 1.77 × the gas (canonical) or 1.39 × (alt). That is a median 1.2e13 / 9.5e12 M☉
  inside 0.5 Mpc and 3.0e13 / 2.4e13 M☉ inside 1 Mpc. OUTER then falls to 0.58 (overshoot).
- Dust at the cosmic ratio 5.364 tracing the gas overshoots everywhere: A_MID 0.62 / 0.58, A_OUTER 0.37 / 0.34.

## Addendum (coordinator request, post-freeze, ungraded): settled cold component at L187's c* = 0.40

CFG687's 1.91 / 1.75 was measured against the **baryon-only law** (ν_mono on gas × 1.2, no cold component; `cfg687_stack.py law()`).
L187's c* = 0.40 is **ΛCDM-PROCESSED**: it is an NFW concentration at R200c, fitted against the Dutton & Macciò c(M).
Here it is applied with no refit: 5.364 × baryons × u, NFW with c* = 0.40, self-consistent R200c (median 0.80 Mpc), truncated at R200.

| row (h 0.672 / 0.686) | A_MID can | A_OUTER can | A_MID alt | A_OUTER alt |
|---|---|---|---|---|
| u = 1, cold sources AQUAL | 0.61 / 0.62 (Z −8.9) | 0.42 / 0.43 | 0.57 / 0.58 (Z −10.6) | 0.39 / 0.40 |
| u = 0.443, sources AQUAL | 0.89 / 0.92 (Z −1.8 / −1.4) | 0.66 / 0.67 | 0.82 / 0.85 (Z −3.1 / −2.7) | 0.61 / 0.61 |
| u = 1, law(baryons) + Newtonian cold | 0.89 / 0.91 (Z −1.7 / −1.4) | 0.63 / 0.64 | 0.85 / 0.87 (Z −2.5 / −2.2) | 0.59 / 0.60 |
| u = 0.443, Newtonian cold | 1.20 / 1.23 (Z +2.3 / +2.9) | 0.82 / 0.83 | 1.12 / 1.16 (Z +1.6 / +2.1) | 0.76 / 0.77 |

Rows that bring MID to ~1 overpredict the outskirts by 35–40 % (A_OUTER 0.6–0.67, Z ≈ −5 to −7). The settled component
at c* = 0.40 fixes the core only by breaking the 1.2–3 Mpc match. The record's MID/OUTER shape (~1.8) is not reproduced:
a c* = 0.4 profile is too extended. So this is not a cure.

## What this does not show

- Asphericity: AQUAL ≠ QUMOND for non-spherical clusters. This is bounded in words only: the effect is second order in
  ellipticity for the azimuthal mean, and was not solved.
- The KiDS n(z) correction is a bound (bin n(z) only), not a calibration. The member-dilution boost could not be measured
  (deficit-dominated).
- eRASS1's use of ΛCDM(70, 0.3) distances is an external fact (PROVISIONAL). R500 stays ΛCDM-processed (bracketed).
- The framework's own two-halo term is not computed (CFG967).
- The T2 mass-scaling question (CFG687/688) was not re-graded.

Files: `f1_extract.py` (KiDS reader), `f1_cluster_cores.py`, `.out`, `_results.json`, `_MUTATE.*`, `ASSUMPTION_LEDGER.md`,
`FROZEN_CRITERIA.md`. Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 0.7 GB RSS. The measurement takes ~7 min and is cached in scratch.
