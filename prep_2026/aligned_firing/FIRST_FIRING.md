# FIRST FIRING — directional-EFE aligned statistic with REAL g_ext directions (n=16)

**Date:** 2026-07-16
**Script:** `fire_aligned_n16.py` (exit 0; all numbers computed at run time, none hard-coded)
**Machine-readable results:** `fire_aligned_n16_results.json`

## MANDATORY FRAMING (read first)

- **EXPLORATORY.** n = 16. Computed sensitivity at the primary config: analytic
  sigma(Ahat) = 3.13, i.e. an E[Ahat]=1 AQUAL-floor signal registers at **~0.3 sigma**
  (the ~5x loop-orbit bracket top at ~1.6 sigma). This run **CANNOT trigger either
  pre-registered kill condition** (banked: detection-at-AQUAL-amplitude or a <0.5%
  null both require N in the hundreds-to-thousands; confrontation.py section 5).
  The kill conditions remain ARMED and UNTOUCHED.
- **Value of this run:** pipeline proof — the first evaluation in history of the
  pre-registered aligned statistic with real per-galaxy g_ext DIRECTIONS — and the
  first number on record. The number is reported straight, whatever it says.

## The headline number (reported as-is)

Pre-registered matched-filter stack `Ahat = sum(A_i p_i / s^2) / sum(p_i^2 / s^2)`
(E[Ahat] = 1 AQUAL local-force floor, up to ~5 with loop-orbit amplification;
~0.24–0.30 Branch B; 0 for null / pure MI):

| config | n | Ahat | boot sd | analytic sd | perm p (2-sided, Z) | perm p (1-sided, Z) | perm p (2-sided, Ahat) |
|---|---|---|---|---|---|---|---|
| **PRIMARY: all, canonical a0=9.36e-11, max-clustering e_N** | 16 | **+2.95** | 1.05 | 3.13 | **0.061** | **0.029** | 0.115 |
| robust-direction rows only | 11 | +2.85 | 1.12 | 3.20 | 0.091 | 0.044 | 0.163 |
| alt a0 = 1.13e-10, maxclu | 16 | +3.29 | 1.25 | 3.59 | 0.063 | 0.031 | 0.101 |
| canonical, no-clustering e_N | 16 | +23.74 | 8.18 | 24.85 | 0.054 | 0.025 | 0.107 |
| variant: gamma factor off (G=1) | 16 | +3.27 | 1.23 | 3.57 | 0.069 | 0.034 | — |
| variant: Upsilon_disk = 0.70 (framework RAR fit) | 16 | +3.28 | 1.05 | 3.37 | 0.046 | 0.023 | — |

Straight reading, exploratory: **the first-ever aligned stack comes out POSITIVE —
the attractor-facing side is faster on average, the sign AQUAL-class MG predicts —
at Ahat ~ +3 (3x the AQUAL local-force floor, inside the banked 1–5x loop-orbit
bracket), with an isotropic-direction permutation null giving p ~ 0.03 (one-sided)
/ 0.06 (two-sided) on the matched-filter Z.** The Ahat-based permutation p is
weaker (0.10–0.12). At n=16 this is a ~2-sigma-at-best exploratory alignment hint,
not a detection: it neither kills Branch B nor supports it, and it is firewalled
from the kill conditions. Footing forks (both a0, both clustering brackets,
Upsilon 0.5/0.70, gamma on/off) and the robust-only stratum all move the number
in the same direction — none flips the sign.

Honesty notes on the error bars:
- The permutation null (directions re-drawn isotropically per galaxy, psi AND
  gamma recomputed, 10^4 draws) is the pre-registered noise floor; null sd(Z) ~ 0.4,
  so observed Z = +0.94 lands at p1 = 0.029. The analytic sd (3.13) uses the
  70-galaxy WHISP lopsidedness rms (0.187 in this convention); the 16-galaxy
  subsample happens to be less lopsided (that is why Z and the permutation p
  disagree in apparent significance — the permutation calibrates on the actual
  sample and is the honest one).
- Leave-one-out: Ahat stays in +2.46 (drop NGC4559) … +3.24 (drop NGC4100);
  no single galaxy owns the sign.
- 5/16 galaxies sit below the banked map range (x < 0.05, clamped up: their true
  |A_map| is larger, so their predictor is understated; all have x >> 2e — no
  sign-reversal ambiguity).
- The no-clustering bracket rescales the predictor down ~8x, so Ahat inflates to
  ~+24 with proportionally huge errors; the Z/p values are the invariant content.

## Sample (the exact 16)

Signed per-side WHISP (van Eymeren+2011a, Table 3) x Chae+21 published e_N x
gext_vectors_2026 direction; committed UGC-SPARC crossmatch re-verified 16/16
against `whisp_ugc_aliases.csv`. Chae's published amplitudes used for all 16
(all are overlap galaxies; the +0.10 dex own-amplitude path was not needed).
Dominant attractor is Virgo for 15/16 (direction share 0.30–0.72).

| galaxy | flag | A_i | psi [deg] | gamma_a/b [deg] | x | e | p_i [%] |
|---|---|---|---|---|---|---|---|
| NGC2903 | robust | -0.0277 | -98.9 | 40/81 | 0.121 | 0.0064 | -0.103 |
| UGC05721 | robust | -0.1230 | -158.0 | 1/32 | 0.044 | 0.0096 | -3.168 |
| UGC05829 | robust | +0.0108 | -61.7 | 9/54 | 0.072 | 0.0083 | +0.924 |
| UGC06446 | robust | +0.0116 | -27.6 | 25/17 | 0.048 | 0.0052 | +1.749 |
| NGC3726 | robust | -0.0565 | -43.8 | 55/0 | 0.083 | 0.0073 | +1.040 |
| UGC06787 | soft | +0.0768 | +61.6 | 11/52 | 0.089 | 0.0049 | +0.473 |
| NGC3992 | soft | -0.0065 | -70.6 | 66/3 | 0.130 | 0.0037 | +0.145 |
| NGC4088 | soft | -0.1188 | -47.5 | 49/7 | 0.290 | 0.0075 | +0.348 |
| NGC4100 | robust | +0.0795 | -166.8 | 23/5 | 0.117 | 0.0053 | -0.931 |
| UGC07151 | robust | +0.0642 | -112.6 | 40/65 | 0.128 | 0.0106 | -0.536 |
| UGC07323 | robust | -0.0192 | +134.3 | 53/11 | 0.173 | 0.0088 | -0.673 |
| UGC07524 | robust | -0.0039 | -142.5 | 17/55 | 0.064 | 0.0079 | -1.686 |
| UGC07603 | robust | +0.1294 | -14.4 | 10/21 | 0.049 | 0.0092 | +3.215 |
| NGC4559 | robust | -0.1355 | -140.8 | 6/43 | 0.083 | 0.0118 | -2.080 |
| UGC09133 | soft | -0.0563 | +177.7 | 19/22 | 0.033 | 0.0027 | -1.030 |
| UGC12732 | soft | +0.0712 | +55.4 | 23/68 | 0.047 | 0.0028 | +0.439 |

(primary config values; x/e at canonical a0, max-clustering e_N)

## Conventions (all stated, none implicit)

1. **A_i = 2(v_rec − v_appr)/(v_rec + v_appr)**, sign tied to the RECEDING side —
   the pre-registered laneA definition, recomputed from v_rec/v_appr. (The
   vanEymeren CSV's `A_signed` column is eps_kin = (v_rec−v_appr)/2v_c, ~half
   this; the noise was recomputed in the same convention: rms = 0.187, robust =
   0.083 over the 70 WHISP — the banked 0.092/0.048 are the eps_kin-convention
   twins, factor ~2 is pure convention.)
2. **PA**: east of north, of the receding-side kinematic major axis (van
   Eymeren+2011a).
3. **g_ext unit vector**: ICRS Cartesian, points TOWARD the net attractor
   (gext_vectors_2026 convention, u = g/|g|, GATE-B validated).
4. **psi** = wrap180( PA(sky-projected g_ext at the galaxy, east of north) −
   PA(receding side) ). psi = 0 means the attractor lies on the receding side.
   Sky projection independently cross-checked against a great-circle-bearing
   computation (agreement < 0.05 deg on 4 spot checks).
5. **gamma** = angle of g_ext to the disk plane, sin(gamma) = |u . n_disk| with
   n_disk = cos(i) LOS ± sin(i) (minor-axis sky direction); the tilted-ring
   near-side two-fold ambiguity is unresolved, so BOTH candidates are computed
   and the banked gamma factor is averaged over the two.
6. **Predictor** p_i = A_map(x_i, e_i) x G(gamma_i) x cos(psi_i), signed.
   A_map = banked laneA BVP map (framework nu, gamma=0, signed — carries the
   x <~ e sign reversal), bilinear in (log x, e), the committed confrontation.py
   interpolator. G(gamma) = banked A(gamma)/A(0) rows parsed from laneA_final.out
   (mean of the e=0.05/0.20 shapes: [1, 1.37, 0.78, 0] at [0, 30, 60, 90] deg).
   Banked sign: attractor-facing side FASTER for x >~ 2e, so p_i > 0 predicts
   A_i > 0.
7. **x_i** = outer g_bar/a0: mean of the outermost 3 SPARC rotmod points,
   Upsilon_disk = 0.5 (0.70 variant reported), Upsilon_bulge = 0.7.
8. **e_i** = 10^(log e_N) x 1.2e-10 / a0 from Chae's PUBLISHED amplitudes
   (max-clustering primary, no-clustering bracket).
9. **Footings** (standing rule, both run): a0 = 9.36e-11 canonical (cH_Lambda/Z)
   and 1.13e-10 alt. Same-direction, no verdict flip.
10. **Errors**: bootstrap over galaxies (10^4) + permutation null re-drawing each
    galaxy's g_ext direction isotropically on the sphere (10^4, psi and gamma
    both recomputed). p-values quoted from the null distribution of the
    matched-filter Z (and of Ahat itself, weaker).

## What this does and does not change

- Does NOT touch the pre-registered kill conditions (underpowered by design at
  n=16; they fire only at N ~ hundreds–thousands).
- Does NOT distinguish AQUAL from Branch B (needs (1−w) separation, far beyond
  this n) and does NOT confront pure MI's exact-zero prediction at any
  meaningful power.
- DOES prove the full pipeline end-to-end: signed per-side asymmetries +
  reconstructed g_ext vectors + banked prediction map -> the pre-registered
  statistic evaluates, with honest nulls, for the first time.
- First number on record: **Ahat = +2.95 (perm p1 = 0.029, p2 = 0.061), positive
  = aligned with the attractor, amplitude inside the banked loop-orbit bracket.**
  If the sign had come out negative or the p flat, that would have been reported
  identically. The forward path stays what it was: WALLABY-scale per-side
  kinematics x the g_ext vector pipeline (N ~ 1157 banked requirement).
