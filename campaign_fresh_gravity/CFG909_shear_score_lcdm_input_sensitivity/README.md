# CFG909: how much do the ΛCDM-derived inputs in the cosmic-shear SCORING move the theory-v2 shear verdict? **ROBUST** (class), with an amplitude-driven Δχ²

- **Date:** 2026-10-20. Criteria: `FROZEN_CRITERIA.md`, written before any script. Its text (blob 3bb5e5a47) landed in a
  parallel session's commit 1049b615c (see Disclosures); the provenance note was then committed alone as e779d1a3f, still
  before any script.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Raw KiDS-1000 / DES Y3 data, framework-native
  scoring; no HMcode / BAHAMAS anywhere. Existing T1x (canonical) and T2x (alt) outputs vs CFG596 P0 rescored; no simulation
  started; NC1x not read, run or touched. A CONSISTENT class does not mean the data favour the framework. Not theory closed.

## Result

**Lane class ROBUST.** The KiDS class stays **CONSISTENT on both footings in every class-weighted variant**: four projection
Ω_m values, each with the as-scored and the re-derived kept set, plus covariance variants B1–B5. DES stays **NOT DIAGNOSTIC**
everywhere, because T-OWN fails in every variant (T-OWN χ² 1.1–3.1).

**The size of the framework's advantage is NOT robust.** CFG650's Δχ² −7.70 / −7.18 is mostly an amplitude effect. The
data want less lensing amplitude than the inherited projection gives:
- Lowering the projection Ω_m drops BOTH arms' χ² sharply (control 144.3 → 121.9 at Ω_m 0.2806).
- The framework's advantage shrinks with it: Δχ² −4.15 / −3.89 at CFG886's measured Ω_m 0.2976, and −0.94 / −0.91 at 0.2806.
- MUTATE M1 shows the same thing from the other side: projecting only the framework run at Ω_m 0.25 gives Δχ² −20.

So CFG650's negative Δχ² should be read like this: the framework run's 3–6% power deficit at k 0.3–1 does part of what a
lower amplitude would do against a projection whose amplitude is too high. It is not a preference for the framework's shape.
The CONSISTENT class survives because that class only requires the framework to be no worse than the control (Δχ² < 4, every
robust value < 9). The largest class-driving value in any variant is −0.91 (alt, Ω_m 0.2806), 4.9 below the TENSION line.

### KiDS-1000, Δχ² (framework − matched control). Class-driving statistic in bold where it differs from Δχ²

| variant | canonical (T1x) | alt (T2x) | robust range (canonical) | class (both) |
|---|---|---|---|---|
| as scored (Ω_m 0.31377, published C) = CFG650 | −7.70 | −7.18 | −10.96 .. −4.60 | CONSISTENT |
| A Ω_m 0.2806 (CFG886 − 2σ) | −0.94 | −0.92 | −2.59 .. +1.57 | CONSISTENT |
| A Ω_m 0.2806, support re-derived (103 pts) | −0.94 | −0.91 | −2.58 .. +1.59 | CONSISTENT |
| A Ω_m 0.2976 (CFG886 measured) | −4.15 | −3.89 | −6.55 .. −1.63 | CONSISTENT |
| A Ω_m 0.3085 (CFG682 row) | −6.48 | −6.05 | −9.46 .. −3.83 | CONSISTENT |
| A Ω_m 0.3308 (as scored + 2σ) | −11.93 | −11.09 | −16.24 .. −7.20 | CONSISTENT |
| B1 CV1-COMMON (one C at the framework signal, p = 1) | −8.45 | −7.83 | −11.96 .. −4.90 | CONSISTENT |
| B2 CVh-COMMON (p = ½) | −8.05 | −7.48 | −11.42 .. −4.74 | CONSISTENT |
| B3 CV1-OWN (each arm at its own signal, p = 1) | −1.60; **Δ(−2lnL) −4.99** | −1.55; **−4.67** | **−7.48 .. −2.59** | CONSISTENT (Δχ² alone also CONSISTENT) |
| B4 CVh-OWN (p = ½) | −4.96; **−6.41** | −4.66; **−5.98** | **−9.42 .. −3.48** | CONSISTENT (Δχ² alone also CONSISTENT) |
| B5 Ω_m 0.2976 + B1 | −4.55 | −4.24 | −7.10 .. −1.80 | CONSISTENT |
| B6 DIAG (reported only, no class weight) | −15.38 | −14.28 | −29.34 .. −7.11 | CONSISTENT (χ² not calibrated) |

- For Ω_m 0.2976, 0.3085 and 0.3308 the re-derived KiDS kept set equals the as-scored set (104 points). At 0.2806 it loses
  one point; those numbers are in the second row.
- Absolute χ² (control / framework, 104 points), canonical:
  - as scored: 144.3 / 136.6 (p 0.014 / 0.033);
  - Ω_m 0.2976: 130.4 / 126.3 (p 0.064 / 0.091);
  - Ω_m 0.2806: 121.9 / 120.9 (p 0.136 / 0.143);
  - Ω_m 0.3308: 164.9 / 153.0 (p 0.001 / 0.005).
- T-OWN (KiDS) passes in every variant: 13.8–31.1 (≥ 9).
- DES Δχ² by variant: −3.18 .. +0.05, NOT DIAGNOSTIC in every variant (T-OWN fails).
- Per-variant numbers for both footings and both surveys are in `cfg909_T.out` / `cfg909_results_T.json`. That file holds
  every robustness member, A_IA, p-values, T-OWN and the ratio statistics.

### Covariance variants: what each does, and its limitation

**The published file.** The KiDS-1000 xipm FITS holds one total covariance. The release contains no Gaussian /
non-Gaussian / super-sample split. So a **Gaussian-only variant is NOT AVAILABLE** from the published products, and none was
attempted. The release's config shows the matrix was iterated toward KiDS's own ΛCDM + HMcode best fit; the chain best fit
used as start values has S8 0.768, Ω_m 0.206, σ8 0.928. Those values were read, not used. The release does not state the
exact cosmology of the released matrix.

**The reference signal.** It is always the control's best fit with the published C. That is the in-pipeline stand-in for the
fiducial signal; building the true fiducial would need a ΛCDM nonlinear model, which is excluded. The per-point ratio
r = t_F / t_ref has median 0.97 and range 0.92–1.22 on KiDS. No point was clipped.

- **B1 / B2 (one covariance for both arms).** C' = R^p C R^p, with p = 1 as the upper bracket (it also scales the shape noise)
  and p = ½ as the lower bracket of the signal-dependent part. Two frozen iterations. Effect on Δχ²: ≤ 0.8.
  Convergence after the two iterations: max|r₂ − r₁| = 0.043 (p = 1) and 0.017 (p = ½) on KiDS. This is not fully converged,
  but the two brackets agree to 0.4 in Δχ².
- **B3 / B4 (each arm at its own signal).** The framework's covariance shrinks (r < 1 at most points), so its χ² rises
  (136.6 → 142.7 at p = 1), and Δχ² alone moves to −1.6. With different covariances in the two arms, Δχ² alone is not a
  likelihood ratio. The frozen class statistic Δ(−2 ln L) adds Δ ln det C (−3.38 canonical, p = 1) and gives −4.99.
  Limitation: a model-dependent covariance inside a Gaussian likelihood adds information the data do not carry. That is why
  B1 / B2 keep one covariance for both arms.
- **B6 DIAG.** It drops all correlations, including the real, mostly Gaussian ones. The 4 / 9 thresholds are not calibrated
  for it, so it is reported only. Its class does not change.
- **Uniform rescaling C → s² C (not run).** To first order it multiplies every Δχ² by 1/s² > 0. It cannot change the sign,
  and so cannot move a CONSISTENT class whose Δχ² is negative.

### Projection Ω_m: what it does, and its limitation

**What changes.** The library's Ω_m is replaced, identically in both arms, in three places:
- the PM distances;
- the lensing prefactor (3/2) Ω_m (H0/c)²;
- the NLA IA factor Ω_m / D(z), with D(z) recomputed.

**What does not change.** The simulated P(k, z) nodes, their z > 1 growth continuation (code check: the library's Dgrow reads
the global Ω_m at call time, so the swap happens only after the P matrices are built), the low-k shape, and the DESI member's
distances.

**Limitation.** This is not a self-consistent cosmology change: both runs were evolved at Ω_m 0.3138. Because C_ℓ ∝ Ω_m²,
the variant acts mainly as a lensing-amplitude rescaling: (0.2806 / 0.3138)² = 0.80 and (0.2976 / 0.3138)² = 0.90. That is
exactly why it exposes the amplitude dependence of Δχ² above.

## Controls

| control | result |
|---|---|
| K1: reproduce CFG650's committed Δχ², Δχ²_noIA, 4 + 3 robust values, χ²_S0, χ²_F, class, class_noIA and T-OWN χ², both footings × both surveys | **PASS**, max \|diff\| 0 (exact) |
| K2: Ω_m override path evaluated at the as-scored Ω_m | **PASS**, 0 |
| K3: common-covariance path with r ≡ 1 | **PASS**, 0 |
| K4: B3/B4 control keeps the published C (r = 1 exactly; χ²_S0 = K1's) | **PASS**, 0 |
| K5: the `--score` (NC1x) code path, as scored, on the stored pair CFG636 C1 vs P0 with CFG654's native library, against `cfg654_native_posthoc.json` native_all; plus its override at the native Ω_m | **PASS**, 0 / 0 |
| MUTATE M1: Ω_m 0.25 on the framework arm only | bites: KiDS shift −12.36 canonical / −13.17 alt (DES −10.85 / −10.89) |
| MUTATE M2: framework covariance × 0.5 | bites: KiDS shift +128.76 / +129.09 |

MUTATE exits 1, by design, meaning both controls bite (`cfg909_T_MUTATE.out`).

## NC1x (written, NOT run)

`cfg909_rescore.py --score NC1x NCS0` (MUTATE first with `--mutate`) applies the same grid to the native-input pair after
the chain has scored it. The scorer is mirrored as follows:
- CFG654's production scorer, `cfg654_native.py`, is imported read only.
- The native library is selected by the runs' `cfg654_inputs`.
- The robustness set is {widen2, noIA, held, LOC}, with DESI reported.
- The grid adds the native as-scored Ω_m (0.3104 for native_cmb).
- K1 there reproduces `cfg654_native_results_NC1x.json` once it exists; until then the lane class is labelled PROVISIONAL.

The native code path is validated by K5. A post hoc engineering exercise, not frozen and with no verdict: on that stored
CFG636 C1 pair, Ω_m 0.2976 moves C1's Δχ² from +13.60 (EXCLUDED) to +9.17 (TENSION). The amplitude coupling therefore
shrinks |Δχ²| for runs that differ from the control mainly in amplitude, whichever the sign of that difference.

## Disclosures

- **Criteria commit.** The criteria file was staged alone, but a parallel session's commit 1049b615c ("CFG906 ledger row
  ...") landed between this lane's `git add` and `git commit` and included it. The content is identical, and no CFG909
  script existed at that time. History is not rewritten. The provenance note was appended and committed alone (e779d1a3f,
  path-limited commit).
- **slogdet flags.** numpy's slogdet raised spurious Accelerate floating-point flags during B3/B4, like the matmul flags that
  `cfg654_native.py` already filters. `cfg909_slogdet_check.py` (post hoc, engineering only) confirms that
  ln det(RCR) − ln det C = 2 Σ ln r to 5e-12, which is the only quantity B3/B4 use. Its first version also required the
  absolute ln det of the full, ill-conditioned (cond 4.6e5) 270 × 270 KiDS matrix to match Cholesky to 1e-8. It misses that by
  1.3e-2 (relative 2e-6); this is irrelevant because ln det C cancels. The criterion was corrected to the difference identity
  and the first outcome is stated here.
- **What was seen when.** The MUTATE run (whose M1 already showed the amplitude effect) was seen before the main run. No
  criterion or variant was changed after any number was seen.
- **Compute.** One core, one process at a time.
  - Peak RSS: K1-only call 262 MB, MUTATE 255 MB, main 296 MB.
  - Wall time: main 37 min, native check 4 min.
  - The live 1024³ run was not touched.
- **Conditional, as in CFG650.** Inherited ΛCDM-shaped ICs and background (NC1x decides that), survey nuisance priors,
  massless neutrinos, and the L100 box (54% of KiDS and 77% of DES points lost).

## Files

- `cfg909_rescore.py`: all modes. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py [--k1 | --mutate | --native-check | --score JOBF JOBS]`.
- `cfg909_T.out` / `cfg909_results_T.json`: main run.
- `cfg909_T_K1.out` / `cfg909_results_T_K1.json`: K1-only first call.
- `cfg909_T_MUTATE.out` / `cfg909_results_T_MUTATE.json`: MUTATE run.
- `cfg909_native_check.out` / `cfg909_results_native_check.json`: K5 native-path check.
- `cfg909_slogdet_check.py` / `.out`: the log-determinant sanity check.


## NC1x re-score (2026-10-20, after the chain scored NC1x; frozen 'NC1x applicability' section, unchanged)

`OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py --score NC1x NCS0 --mutate`, then without `--mutate`. Outputs `cfg909_NC1x[_MUTATE].out`,
`cfg909_results_NC1x[_MUTATE].json`. Canonical footing only (NC1x is canonical; NC2x, the alt native rerun, is CFG654 A3).

| check / variant | KiDS Δχ² (F − S0) | class |
|---|---|---|
| K1 as scored (reproduces cfg654_native_results_NC1x.json, max diff 0) | −10.08 | CONSISTENT |
| projection Ω_m 0.2806 / 0.2976 / 0.3085 / 0.3138 / 0.3308 | −3.11 / −6.86 / −9.58 / −10.97 / −15.80 | CONSISTENT in all |
| CV1_COMMON / CVh_COMMON | −11.04 / −10.53 | CONSISTENT |
| CV1_OWN / CVh_OWN (framework's own covariance; Δχ² only) | −2.94 / −7.07 | CONSISTENT |
| COMB Ω_m 0.2976 + CV1_COMMON | −7.53 | CONSISTENT |
| DIAG (reported only) | −19.50 | CONSISTENT |

- LANE CLASS: **ROBUST**, no flips; worst class-driving statistic Ω_m 0.2806, −3.11 (margin 7.11 to the TENSION line). K1–K4 PASS.
- MUTATE bites (M1 Ω_m 0.25 on the framework arm: KiDS shift −22.19; M2 framework covariance × 0.5: +134.67).
- DES NOT DIAGNOSTIC throughout (T-OWN fails). numpy prints 'invalid value encountered in slogdet' warnings in the stderr logs
  (cfg909_NC1x*.err), as in the T1x run; cfg909_slogdet_check covers the determinant path.
- Reading: with native inputs the class survives every ΛCDM-input variant; the size of the advantage is set by the projection
  Ω_m (amplitude), as for T1x. Quote CONSISTENT, not a −10 preference. κ = ½ FITTED; not theory closed.

## NC2x re-score (2026-10-21, after the chain scored NC2x; reported sensitivity, no verdict weight, as CFG654 A3 allows)

`OMP_NUM_THREADS=1 nice -n 10 python3 cfg909_rescore.py --score NC2x NCS0 --mutate`, then without `--mutate`. Outputs
`cfg909_NC2x[_MUTATE].out` and `cfg909_results_NC2x[_MUTATE].json`. Alt footing only. NCS0 is the footing-independent control.

| check / variant | KiDS Δχ² (F − S0) | class |
|---|---|---|
| K1 as scored (reproduces cfg654_native_results_NC2x.json, max diff 0) | −9.39 | CONSISTENT |
| projection Ω_m 0.2806 / 0.2976 / 0.3085 / 0.3138 / 0.3308 | −2.93 / −6.40 / −8.93 / −10.22 / −14.69 | CONSISTENT in all |
| CV1_COMMON / CVh_COMMON | −10.22 / −9.78 | CONSISTENT |
| CV1_OWN / CVh_OWN (framework's own covariance; Δχ² only) | −2.81 / −6.63 | CONSISTENT |
| COMB Ω_m 0.2976 + CV1_COMMON | −6.99 | CONSISTENT |
| DIAG (reported only) | −18.07 | CONSISTENT |

- LANE CLASS: **ROBUST**, no flips. The worst class-driving statistic is at Ω_m 0.2806: −2.93, a margin of 6.93 to the TENSION line.
  K1–K4 PASS.
- MUTATE bites. M1 (Ω_m 0.25 on the framework arm) shifts KiDS by −23.08. M2 (framework covariance × 0.5) shifts it by +135.15.
- DES (alt): diagnostic and CONSISTENT as scored (−2.15). It is NOT DIAGNOSTIC at Ω_m 0.2806 / 0.2976 and in COMB, where T-OWN fails,
  and CONSISTENT elsewhere.
- The stderr log (cfg909_NC2x.err) carries numpy slogdet divide/overflow/invalid warnings, as in the NC1x and T1x runs.
  cfg909_slogdet_check covers the determinant path. The Δχ² classes do not use it.
- Reading, as for NC1x: with native inputs on the alt footing the class survives every ΛCDM-input variant. The size of the
  advantage is set by the projection Ω_m, i.e. by amplitude. Quote CONSISTENT, not a −9 preference. κ = ½ FITTED; footings never
  pooled; not theory closed.
