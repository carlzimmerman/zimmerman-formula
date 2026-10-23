# F1_cluster_cores — FROZEN CRITERIA (before any script or number)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Inputs: `ASSUMPTION_LEDGER.md`.
κ = ½ FITTED. Both footings (canonical 9.3603e-11, alt 1.1312e-10 m/s²), never pooled. No dark-matter particle.
Never "theory closed"; never "the data favour the framework".

## Statistic

A_band = Σ_i Σ_j W_ij D_ij / Σ_i Σ_j W_ij P_ij over clusters i and radial bins j in the band (inverse-variance shape-noise
weights W), bins 0.15–3 Mpc in 8 log bins (record's edges), bands INNER 0.15–0.5 (reported, not graded), MID 0.5–1.2,
OUTER 1.2–3 Mpc. Error: jackknife over 30 equal-count RA-ordered patches. Z_MID = (A_MID − 1)/σ.

## Reproduction (must pass before anything else is read)

- K1: from the record's own `cfg687_percluster.npz`, A_MID canonical reproduces 1.91 ± 0.12 to 0.005 (same data read).
- K2: my independent measurement (own extraction, own estimator code, record conventions) gives a stack ΔΣ within 1.0 σ_record
  of CFG687's stack in each MID and OUTER bin (bins 3–7).
- K3: my record-recipe prediction (ν_mono, β = 2/3, r_c = 0.15 R500, f* = 0.20, h = 0.70, no gas rescale) gives
  A_MID within ±0.10 of 1.91 / 1.75 and A_OUTER within ±0.10 of 1.01 / 0.93; cluster count within 318 ± 15.
- K4: projection self-test (SIS ΔΣ = σ²/2GR) to < 1 % in MID and OUTER bins.
- K5: spherical AQUAL with μ = x/(1+x) solved from Gauss's law equals QUMOND with the inverse ν to < 1e-9 (identity), and
  ν_mono differs from it (the record's kernel is not the action's).
- K6: eRASS1 FITS and TSV agree on Mgas500 and R500 for the used clusters (relative ≤ 1e-3).

## Corrections, one at a time from the reproduced record (R0), each reported on both footings

- C1 kernel: ν_mono → AQUAL μ = x/(1+x) (spherical). C1b: AQUAL vs QUMOND at fixed μ = 0 in spherical symmetry (identity);
  asphericity bounded in words, not solved.
- C2 native background: h = 0.672 and 0.686 (r_d = 101.54/h), with C2a the eRASS1 gas rescale q^{5/2} / R500 × q from
  ΛCDM(70, 0.3) to the pipeline's distances (applied at h = 0.70 alone, then with native h).
- C3 gas calibration: (a) R500 ±0.033 dex with gas mass at fixed physical radius held; (b) catalogue Mgas500_L / _H;
  (c) gas shape G1 (X-COP measured shape) and G2 (measured aperture only); (d) deep X-ray cross-calibration (ACCEPT / X-COP
  matched gas masses) reported as a ratio and applied as the median factor.
- C4 stars: f* 0.30 (most favourable to the law).
- C5 projection and miscentring: (a) catalogue offset miscentring on the prediction; (b) data boost (member dilution);
  (c) two-halo bound at MID; (d) Σ_crit with bin n(z) (bound).

## Primary rebuild (all corrections that are not brackets, applied together)

AQUAL μ = x/(1+x); native h at both ends (0.672, 0.686); eRASS1 gas rescaled; β-model G0 normalised to the rescaled Mgas500;
f* = 0.20; data boost applied; catalogue miscentring applied. Reported on both footings and both h ends.
**Most-favourable corner** (for the law): primary with f* = 0.30, Mgas500_H, C3(d) factor if > 1, gas shape giving the larger
MID prediction, two-halo bound subtracted from the data, Σ_crit bound in the direction that lowers A.

## Verdict rule (both footings must agree; else the footing split is reported and the verdict is the weaker one)

- **REAL FAILURE**: primary Z_MID ≥ 3 at both h ends AND most-favourable corner Z_MID ≥ 2.
- **EXPLAINED**: primary |Z_MID| < 2 at both h ends, with the ingredient whose single application moves A_MID most named;
  no fitted parameter introduced.
- **UNDECIDABLE**: anything else; name the missing input.

Separately reported, never graded: (i) the dust mass the V3 theory would need inside 0.5 and 1 Mpc under AQUAL with the dust
sourcing the field (shape tracing the gas, amplitude solved for A_MID = 1 — a "needed" number, not a fit used for the verdict),
and the A_MID / A_OUTER that dust at the cosmic ratio Ω_c/Ω_b = 5.364 tracing the gas would give; (ii) whether V3 predicts the
cluster-core dust: DERIVED / FITTED / NOT COMPUTABLE, with the reason.

## Script and mutate

`f1_cluster_cores.py` prints `K# PASS|FAIL value threshold`, ends `F1_CLUSTER_CORES COMPLETE: N/M checks PASS.`, exit 0 iff all
pass; writes `f1_cluster_cores.out`, `f1_cluster_cores_results.json`. `--mutate` measures the cross shear instead of the
tangential shear (outputs `*_MUTATE.*`): K2 and K3 must FAIL. Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes.

## AMENDMENTS (append-only)

- **A0 (implementation, pre-result):** cluster centres are eRASS1 RA_XFIT / DEC_XFIT (the record's TSV columns are these);
  the miscentring offset is |(RA, DEC) − (RA_XFIT, DEC_XFIT)|. Sources with Z_B = 1.2 exactly are dropped (float32 1.2 > 1.2),
  as in the record. The measurement is cached in session scratch so reruns do not re-measure.
- **A1 (POST-RESULT):** the measured "boost" is < 1 at every radius (0.85–0.96): a source deficit (masking / blending near
  clusters), not member dilution. A dilution correction is ≥ 1, so the frozen primary's boost (which lowered A by ~7 %, in the
  law's favour) is wrong in sign. Reported: the primary with the boost clipped at 1. The frozen-rule verdict is computed on the
  frozen primary (more lenient); A1 only strengthens it.
- **A2 (POST-FREEZE, coordinator request):** one reported, ungraded row family: the law + the settled cold component of
  Ω_c/Ω_b = 5.364 × baryons in an NFW with L187's c* = 0.40 relative to a self-consistent R200c (truncated at R200), with u = 1
  and u = 0.443 (DS_FINAL), the cold mass either sourcing the AQUAL field (V3 reading) or added Newtonian (CFG949 reading).
  L187's c* is ΛCDM-PROCESSED (NFW concentration fitted against Dutton & Macciò c(M) at R200c, Planck ρ_c). No refit.
