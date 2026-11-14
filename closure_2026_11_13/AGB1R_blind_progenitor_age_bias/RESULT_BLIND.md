# AGB1R — blind re-grade of AGB1 (supernova progenitor-age bias on DESI DR2 BAO + DES-SN5YR Dovekie): result

2026-11-14. Rules: `closure_2026_11_13/AGB1_progenitor_age_bias/FROZEN_CRITERIA.md`, read as in `READING.md` (committed
alone before any real-data number, 9090ca051c). Code written from scratch in this folder. Adopts nothing; edits no ledger.

## Blindness
Before this file was committed I opened only: AGB1's `FROZEN_CRITERIA.md`; `nuf1_run.py` (data constants, and the CAMB and
BAO helpers next to them); the four files in `_external_data/cfg684_inputs/des5/`. I opened no other AGB1 file, ran no
`git show` / `git diff` of the AGB1 folder, and opened neither AGB1 memory file. The session's memory index carried one
line on AGB1, cut off after "the Son et al. supernova age correction tested on…": no number and no word of the first
build. The recent-commit list I was shown held no AGB1 subject. I saw nothing of the first build's results.

## Words

| word | Part A (BAO + SN, no CMB) | Part C (BAO + compressed CMB prior + SN) |
|---|---|---|
| W1 / W1c, amplitude | **UNDECIDED, ROBUST** | **UNDECIDED, ROBUST** |
| W2 / W2c, today, fork A = 0 | **ACCELERATING TODAY** | **ACCELERATING TODAY** |
| W2 / W2c, today, fork A = 1 | **SIGN NOT SETTLED** | **SIGN NOT SETTLED** |
| W2 / W2c, today, fork A free | **SIGN NOT SETTLED** | **SIGN NOT SETTLED** |
| W3 / W3c, ever, every fork | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** |

Every check passed, so both sets of words are evaluable. `des_only` gives the same W2 and W3 words in every fork, in
both parts. ROBUST: W1's first word is UNDECIDED on `full`, `des_only` and `bao_overlap` (and on `rand197`); W1c's is
UNDECIDED on `full` and `des_only`.

In plain terms: the distances neither require nor exclude a drift with the S25 shape. The best amplitude is about
0.6 of S25's size, and both 0 and 1 sit inside Δχ² = 4. With the published correction at full size the best fit has
q0 > 0, but q0 = 0 costs only Δχ² 3.4 (Part A) and 3.6 (Part C). That is below the frozen 4, so deceleration today is
not established. Without the correction, acceleration today holds at Δχ² 18.6 (Part A) and 27.4 (Part C). On `full`, in every fork
and both parts, a flat w0–wa universe that never accelerated on 0 ≤ z ≤ 2.33 is excluded by Δχ² 28.7 to 199.

## Known-answer checks

| check | result | target, tolerance | verdict |
|---|---|---|---|
| counts | 1,820; DES 1,623 (z 0.0733–1.1442, median 0.519); legacy 197 (z 0.0251–0.0870) | as frozen | PASS |
| KT | Δage_S(1.0) 5.440 Gyr; T_S(1.0) 0.1632 mag; Δage_W(1.2) 1.990 Gyr | [5.0, 5.6]; [0.15, 0.17]; [1.7, 2.1] | PASS |
| K1 | BAO-only flat ΛCDM: Ω_m 0.2973, h r_d 101.55 Mpc (χ² 10.54) | 0.2975 ± 0.003; 101.54 ± 0.3 | PASS |
| K2 | `full` SN-only flat ΛCDM, A = 0: Ω_m 0.3303 (χ² 1631.42) | 0.330 ± 0.0075 | PASS |
| K3 twin A_true 1 | A_free +1.00001, Ω_m 0.31000, w0 −0.80000, wa −0.59998, h r_d 101.600, χ²_min −4 × 10⁻⁸, Δχ²(A = 0) 5.59 | as frozen | PASS |
| K3 twin A_true 0 | A_free −0.00001, w0 −0.80000, wa −0.60000, χ²_min −4 × 10⁻⁸, Δχ²(A = 1) 5.35 | as frozen | PASS (script exit 3) |
| K4 | max relative difference to CAMB 1.6.6 PPF 4.5 × 10⁻⁴ (D_H at z 2.33; radiation) | ≤ 10⁻³ | PASS |
| KA | `full`: spline minimum A +0.6182, χ² 1636.2445; A-free +0.6182, χ² 1636.2445 | 0.03; 0.05 | PASS |
| K5 | BAO + prior: χ²(w0–wa) 7.342 − χ²(ΛCDM) 15.585 = −8.243 | −8.0 ± 1.0 | PASS |
| K6 | `full`, A = 0: w0 −0.820, wa −0.643 | −0.803 ± 0.040; −0.72 ± 0.16 | PASS |

Templates reproduce the pre-freeze values in the criteria to the printed digit: median age 6.703 Gyr at z 0; Δage_S
0.637, 1.205, 2.168, 2.944, 4.075, 4.807, 5.440, 5.675 Gyr at z 0.05 … 1.2; T_W median age 2.303 Gyr, Δage_W 1.573, 1.924,
1.990 at z 0.5, 1.0, 1.2; Δage_S(1.0) on a flat Ω_m 0.3, H0 70 background 5.290 Gyr (`agb1r_template.out`).

## Numbers

χ² values leave out the DES file's constant log(1ᵀW1/2π) (READING.md). Intervals come from a cubic spline through the
grid profile, measured from the A-free minimum. "open" means the interval runs past the grid end.

### A profile

| part | sample | best A | Δχ² = 1 interval | Δχ² = 4 interval | Δχ²(A = 0) | Δχ²(A = 1) | χ²_min (A free) | first word |
|---|---|---|---|---|---|---|---|---|
| A | `full` | +0.618 | [+0.191, +1.049] | [−0.233, +1.484] | 2.100 | 0.785 | 1636.245 | UNDECIDED |
| A | `des_only` | +0.346 | [−0.123, +0.813] | [−0.569, +1.281] | 0.545 | 1.959 | 1426.221 | UNDECIDED |
| A | `rand197` | +0.725 | [+0.283, +1.170] | [−0.155, +1.620] | 2.709 | 0.383 | 1450.836 | UNDECIDED |
| A | `bao_overlap` | +0.681 | [+0.238, +1.122] | [−0.209, +1.563] | 2.355 | 0.522 | 1634.993 | UNDECIDED |
| C | `full` | +0.624 | [+0.231, +1.021] | [−0.158, +1.424] | 2.537 | 0.896 | 1637.230 | UNDECIDED |
| C | `des_only` | +0.533 | [+0.141, +0.929] | [−0.248, +1.331] | 1.853 | 1.384 | 1427.686 | UNDECIDED |

Profile prior edges (no word depends on them): on `full`, the best fit sits on wa = −3 for A ≥ 1.8 (Part A) and A ≥ 2.0
(Part C). On `des_only` Part A, it sits on w0 + wa = 0 for A ≤ −0.3, so that sample's lower Δχ² = 4 bound, −0.569, is
shaped by that prior. The upward and downward sweeps agree to 3 × 10⁻⁸ (Part A) and 4 × 10⁻⁷ (Part C) at every grid point.

### Part A forks

| sample | fork | fit | Ω_m | w0 | wa | q0 | A | χ² | χ² split | smallest q (z) | Δχ² | word |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `full` | A0 | best | 0.3141 | −0.843 | −0.538 | −0.367 | +0.000 | 1638.345 | BAO 8.81, SN 1629.54 | −0.367 (0.000) |  |  |
| `full` | A0 | q0 = 0 | 0.3491 | −0.512 | −2.401 | +0.000 | +0.000 | 1656.984 | BAO 16.25, SN 1640.74 | −0.297 (0.315) | 18.639 | ACCELERATING TODAY |
| `full` | A0 | q ≥ 0 on [0, 2.33] | 0.3160 | −0.462 | −0.437 | +0.026 | +0.000 | 1806.490 | BAO 40.29, SN 1766.20 | −0.000 (0.240) | 168.145 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `full` | A1 | best | 0.3675 | −0.377 | −1.935 | +0.142 | +1.000 | 1637.030 | BAO 6.33, SN 1630.70 | −0.151 (0.400) |  |  |
| `full` | A1 | q0 = 0 | 0.3508 | −0.513 | −1.249 | +0.000 | +1.000 | 1640.444 | BAO 8.58, SN 1631.86 | −0.129 (0.310) | 3.414 | SIGN NOT SETTLED |
| `full` | A1 | q ≥ 0 on [0, 2.33] | 0.3348 | −0.442 | −0.619 | +0.059 | +1.000 | 1674.555 | BAO 37.18, SN 1637.37 | −0.000 (0.325) | 37.526 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `full` | Afree | best | 0.3467 | −0.561 | −1.391 | −0.049 | +0.618 | 1636.245 | BAO 6.68, SN 1629.56 | −0.181 (0.285) |  |  |
| `full` | Afree | q0 = 0 | 0.3520 | −0.514 | −1.540 | +0.000 | +0.704 | 1636.290 | BAO 6.50, SN 1629.79 | −0.172 (0.320) | 0.045 | SIGN NOT SETTLED |
| `full` | Afree | q ≥ 0 on [0, 2.33] | 0.3578 | −0.372 | −0.954 | +0.141 | +1.421 | 1664.953 | BAO 35.36, SN 1629.59 | −0.000 (0.445) | 28.708 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `des_only` | A0 | best | 0.2877 | −1.002 | +0.247 | −0.570 | +0.000 | 1426.766 | BAO 10.11, SN 1416.65 | −0.570 (0.000) |  |  |
| `des_only` | A0 | q0 = 0 | 0.3505 | −0.513 | −2.037 | +0.000 | +0.000 | 1438.329 | BAO 9.85, SN 1428.48 | −0.246 (0.320) | 11.563 | ACCELERATING TODAY |
| `des_only` | A0 | q ≥ 0 on [0, 2.33] | 0.3309 | −0.447 | −0.580 | +0.051 | +0.000 | 1525.597 | BAO 37.67, SN 1487.93 | −0.000 (0.315) | 98.831 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `des_only` | A1 | best | 0.3593 | −0.453 | −1.613 | +0.064 | +1.000 | 1428.179 | BAO 6.90, SN 1421.28 | −0.145 (0.360) |  |  |
| `des_only` | A1 | q0 = 0 | 0.3520 | −0.514 | −1.356 | +0.000 | +1.000 | 1428.358 | BAO 7.46, SN 1420.90 | −0.145 (0.315) | 0.178 | SIGN NOT SETTLED |
| `des_only` | A1 | q ≥ 0 on [0, 2.33] | 0.3408 | −0.429 | −0.696 | +0.076 | +1.000 | 1462.397 | BAO 36.38, SN 1426.01 | −0.000 (0.360) | 34.217 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `des_only` | Afree | best | 0.3148 | −0.819 | −0.419 | −0.342 | +0.346 | 1426.221 | BAO 8.39, SN 1417.83 | −0.342 (0.000) |  |  |
| `des_only` | Afree | q0 = 0 | 0.3523 | −0.515 | −1.497 | +0.000 | +0.767 | 1427.277 | BAO 6.61, SN 1420.66 | −0.166 (0.320) | 1.056 | SIGN NOT SETTLED |
| `des_only` | Afree | q ≥ 0 on [0, 2.33] | 0.3529 | −0.391 | −0.876 | +0.120 | +1.553 | 1453.702 | BAO 35.42, SN 1418.28 | −0.000 (0.420) | 27.481 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `bao_overlap` | A0 | best | 0.2998 | −0.851 | −0.285 | −0.394 | +0.000 | 1637.348 | BAO 7.43, SN 1629.92 | −0.394 (0.000) |  |  |
| `bao_overlap` | A0 | q0 = 0, AT PRIOR EDGE wa | 0.3843 | −0.541 | −3.000 | +0.000 | +0.000 | 1646.814 | BAO 11.37, SN 1635.44 | −0.317 (0.280) | 9.467 | (numbers only) |
| `bao_overlap` | A0 | q ≥ 0, AT PRIOR EDGE Ω_m | 0.0500 | −0.349 | −0.031 | +0.002 | +0.000 | 1781.524 | BAO 21.27, SN 1760.26 | −0.000 (0.265) | 144.176 | (numbers only) |
| `bao_overlap` | A1 | best | 0.2563 | −0.407 | −0.853 | +0.046 | +1.000 | 1635.515 | BAO 4.41, SN 1631.11 | −0.117 (0.490) |  |  |
| `bao_overlap` | A1 | q0 = 0 | 0.1593 | −0.397 | −0.427 | +0.000 | +1.000 | 1635.633 | BAO 4.27, SN 1631.36 | −0.108 (0.625) | 0.118 | (numbers only) |
| `bao_overlap` | A1 | q ≥ 0, AT PRIOR EDGE Ω_m | 0.0500 | −0.348 | −0.036 | +0.004 | +1.000 | 1656.441 | BAO 21.06, SN 1635.38 | −0.000 (0.370) | 20.926 | (numbers only) |
| `bao_overlap` | Afree | best | 0.2635 | −0.542 | −0.579 | −0.099 | +0.681 | 1634.993 | BAO 4.63, SN 1630.36 | −0.143 (0.260) |  |  |
| `bao_overlap` | Afree | q0 = 0 | 0.2975 | −0.474 | −1.000 | +0.000 | +0.828 | 1635.158 | BAO 4.65, SN 1630.51 | −0.135 (0.375) | 0.165 | (numbers only) |
| `bao_overlap` | Afree | q ≥ 0, AT PRIOR EDGE Ω_m | 0.0500 | −0.346 | −0.043 | +0.007 | +1.237 | 1651.769 | BAO 20.99, SN 1630.78 | −0.000 (0.485) | 16.776 | (numbers only) |

No fork best fit and no constrained fit on `full` or `des_only` is at a prior edge. Every never-accelerated fit meets
q ≥ −10⁻³; the smallest q is −8 × 10⁻⁶. With only the low-redshift BAO bins (`bao_overlap`), the never-accelerated fits
run to the Ω_m = 0.05 floor (a near-coasting universe). Those Δχ²_never values are therefore conditional on the Ω_m prior.
They carry no word.

### Part C forks

| sample | fork | fit | h | Ω_m | w0 | wa | q0 | A | χ² | χ² split | smallest q (z) | Δχ² | word |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `full` | A0 | best | 0.6732 | 0.3129 | −0.820 | −0.643 | −0.345 | +0.000 | 1639.766 | BAO 9.68, SN 1629.50, prior 0.59 | −0.345 (0.005) |  |  |
| `full` | A0 | q0 = 0 | 0.6590 | 0.3311 | −0.498 | −1.923 | +0.000 | +0.000 | 1667.145 | BAO 16.22, SN 1650.11, prior 0.82 | −0.255 (0.340) | 27.379 | ACCELERATING TODAY |
| `full` | A0 | q ≥ 0 on [0, 2.33] | 0.6028 | 0.3814 | −0.461 | −0.833 | +0.072 | +0.000 | 1839.103 | BAO 50.42, SN 1776.71, prior 11.97 | −0.000 (0.310) | 199.336 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `full` | A1 | best | 0.6307 | 0.3579 | −0.396 | −1.732 | +0.118 | +1.000 | 1638.126 | BAO 7.51, SN 1630.53, prior 0.08 | −0.142 (0.400) |  |  |
| `full` | A1 | q0 = 0 | 0.6362 | 0.3501 | −0.513 | −1.301 | +0.000 | +1.000 | 1641.693 | BAO 8.27, SN 1632.70, prior 0.72 | −0.138 (0.315) | 3.567 | SIGN NOT SETTLED |
| `full` | A1 | q ≥ 0 on [0, 2.33] | 0.6008 | 0.3858 | −0.399 | −1.059 | +0.133 | +1.000 | 1695.111 | BAO 43.95, SN 1642.80, prior 8.36 | −0.000 (0.390) | 56.985 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `full` | Afree | best | 0.6463 | 0.3403 | −0.561 | −1.299 | −0.055 | +0.624 | 1637.230 | BAO 7.36, SN 1629.64, prior 0.23 | −0.177 (0.285) |  |  |
| `full` | Afree | q0 = 0 | 0.6416 | 0.3456 | −0.509 | −1.441 | +0.000 | +0.731 | 1637.311 | BAO 7.28, SN 1629.87, prior 0.16 | −0.164 (0.325) | 0.082 | SIGN NOT SETTLED |
| `full` | Afree | q ≥ 0 on [0, 2.33] | 0.5933 | 0.3976 | −0.276 | −1.431 | +0.251 | +1.609 | 1676.511 | BAO 41.80, SN 1629.33, prior 5.38 | −0.000 (0.500) | 39.281 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `des_only` | A0 | best | 0.6779 | 0.3081 | −0.878 | −0.460 | −0.412 | +0.000 | 1429.539 | BAO 10.26, SN 1418.34, prior 0.94 | −0.412 (0.000) |  |  |
| `des_only` | A0 | q0 = 0 | 0.6513 | 0.3375 | −0.503 | −1.703 | +0.000 | +0.000 | 1442.822 | BAO 10.09, SN 1432.60, prior 0.12 | −0.213 (0.335) | 13.283 | ACCELERATING TODAY |
| `des_only` | A0 | q ≥ 0 on [0, 2.33] | 0.6012 | 0.3851 | −0.407 | −1.030 | +0.124 | +0.000 | 1547.784 | BAO 44.52, SN 1494.55, prior 8.71 | −0.000 (0.385) | 118.246 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `des_only` | A1 | best | 0.6347 | 0.3529 | −0.458 | −1.529 | +0.056 | +1.000 | 1429.070 | BAO 7.55, SN 1421.28, prior 0.23 | −0.143 (0.360) |  |  |
| `des_only` | A1 | q0 = 0 | 0.6383 | 0.3484 | −0.512 | −1.355 | +0.000 | +1.000 | 1429.325 | BAO 7.68, SN 1421.21, prior 0.44 | −0.148 (0.320) | 0.255 | SIGN NOT SETTLED |
| `des_only` | A1 | q ≥ 0 on [0, 2.33] | 0.5988 | 0.3891 | −0.360 | −1.183 | +0.170 | +1.000 | 1479.448 | BAO 42.24, SN 1430.12, prior 7.09 | −0.000 (0.430) | 50.378 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |
| `des_only` | Afree | best | 0.6545 | 0.3312 | −0.661 | −1.002 | −0.163 | +0.533 | 1427.686 | BAO 7.74, SN 1419.42, prior 0.53 | −0.212 (0.185) |  |  |
| `des_only` | Afree | q0 = 0 | 0.6407 | 0.3463 | −0.510 | −1.419 | +0.000 | +0.790 | 1428.257 | BAO 7.32, SN 1420.73, prior 0.21 | −0.160 (0.325) | 0.572 | SIGN NOT SETTLED |
| `des_only` | Afree | q ≥ 0 on [0, 2.33] | 0.5943 | 0.3960 | −0.289 | −1.392 | +0.238 | +1.709 | 1466.160 | BAO 41.53, SN 1418.93, prior 5.70 | −0.000 (0.490) | 38.474 | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |

K5 detail (BAO + prior, no SN): ΛCDM h 0.6838, Ω_m 0.3002, χ² 15.585; w0–wa h 0.6375, Ω_m 0.3506, w0 −0.448, wa −1.638,
q0 +0.063, χ² 7.342.

## Reported only (no frozen word)
- **`tmpl_W`** (Madau–Dickinson SFH, τ^−1.13 from 40 Myr; T_W(1.0) = 0.058 mag, about a third of T_S):
  `full` best A_W +2.287 (Ω_m 0.359, w0 −0.449, wa −1.822, q0 +0.069); Δχ² = 1 interval [+0.611, open]; Δχ² = 4 interval
  open at both grid ends (Δχ²(A_W = −1) 3.83, Δχ²(A_W = 3) 0.18); Δχ²(A_W = 0) 1.859, Δχ²(A_W = 0.23) 1.505, Δχ²(A_W = 1) 0.590.
  `des_only` best A_W +1.939; Δχ² = 1 [+0.179, open]; Δχ² = 4 open both ends; Δχ²(A_W = 0) 1.213, (0.23) 0.943, (1) 0.286.
  The short-delay shape is too shallow for these data to fix its amplitude.
- **`legacy_offset`** (`full`): a constant step δ on the 197 legacy supernovae, age template off: best δ +0.0336 mag
  (legacy fainter), Δχ²(δ = 0) 1.694. With δ and A both free: best A +0.497 (δ +0.0239 mag), Δχ² = 1 [+0.045, +0.951],
  Δχ² = 4 [−0.410, +1.406], Δχ²(A = 0) 1.210, Δχ²(A = 1) 1.227. A step between surveys takes up part of the wanted drift
  but not all of it. None of these numbers reaches 4.
- **S25's printed fits beside ours** (S25 used the older DES-SN5YR calibration and full CMB likelihoods; comparisons only):

| combination | S25 Ω_m, w0, wa, q0 | AGB1R Ω_m, w0, wa, q0 |
|---|---|---|
| BAO + SN corrected, no CMB | 0.374, −0.320, −2.136, +0.199 ± 0.070 | Part A `full` A = 1: 0.3675, −0.377, −1.935, +0.142 |
| BAO + CMB + SN corrected | 0.363, −0.337, −1.902, +0.178 ± 0.061 | Part C `full` A = 1: 0.3579, −0.396, −1.732, +0.118 |
| BAO + CMB + SN uncorrected | 0.319, −0.754, −0.848, −0.271 ± 0.061 | Part C `full` A = 0: 0.3129, −0.820, −0.643, −0.345 |
| BAO + CMB, no SN | w0 −0.430, wa −1.704, q0 +0.075 | K5 w0–wa: −0.448, −1.638, +0.063 |

  On Dovekie the corrected fits move the same way as S25's, but less far. Their q0 > 0 at 2.8 to 2.9σ becomes q0 +0.12 to
  +0.14 with Δχ²(q0 = 0) of 3.4 to 3.6, about 1.9σ.
- **Part B not run.** It executes CFG684 and CFG689 sources and reads LGS1's committed outputs. Those files are outside
  what this blind lane may open.

## Cross-checks (not frozen steps)
- **Brute-force grids, Part A** (`agb1r_xcheck.py`, `full` and `des_only`). A 3-D grid of 593,274 points (Ω_m step 0.01,
  w0 step 0.025 from −1.6 to 0.6, wa step 0.05) for the best and never-accelerated fits, and a 2-D grid for q0 = 0. Each
  grid best was polished by Nelder–Mead. 17 of the 18 fork fits match the frozen runs to 10⁻⁴ in χ². The 18th (`des_only`, A free, never-accelerated)
  comes out 3 × 10⁻⁴ lower in the cross-check. Every Δχ²_today and Δχ²_never is unchanged at the printed precision, including the threshold-nearest
  Δχ²_today of 3.414 (`full`, A = 1).
- **Part C, A = 1 fork on `full`** (`agb1r_xcheckC.py`), Δχ²_today 3.567 against the threshold 4. The best fit and the
  q0 = 0 fit were re-run from the frozen starts plus 8 seeded random starts and returned the same minima (1638.1257,
  1641.6928; Δχ²_today 3.5671).
- **Matmul warnings.** numpy 1.26 on Apple Accelerate raises spurious divide, overflow and invalid flags in `W @ x`.
  The results were checked finite and equal to `einsum` to 2 × 10⁻¹⁶, and these warnings are filtered in
  `agb1r_common.py`.

## Ambiguities and how they were resolved (from READING.md)
- **ℳ marginalisation.** Profiled, without the DES constant log(1ᵀW1/2π). That constant is the same at every parameter
  point of a sample, and K3's χ²_min ≤ 10⁻³ needs it left out.
- **`rand197` draw.** `default_rng(20261113).choice(DES row positions, 197, replace=False)`; the first dropped CIDs are
  1259241, 1306366, 1317164, …. LGS1's own call was not on my reading list, so AGB1's 197 may differ from mine. It is a
  control with no word of its own, and its first word agrees here anyway.
- **"The neighbouring grid point".** Read as either neighbour, with two sweeps and the lower kept. The sweeps never
  differ by more than 4 × 10⁻⁷.
- **Constrained fits.** q0 = 0 by substitution; never-accelerated by a staged quadratic penalty (10² to 10⁸) on the smallest
  q over a 0.005 grid in z.
- **Part C starts.** Each fixed start's (w0, wa), with h solved from the prior's θ*. The restart polish is two Nelder–Mead
  rounds in Hessian-whitened coordinates.
- **Interval spline.** Through the grid points only, with the A-free χ² as reference. Adding the A-free point to the
  spline changes no Part A interval at the printed precision; Part C was not checked this way.

## What this may and may not say
A is the size of a redshift drift with the S25 shape, inside the flat w0–wa family. It cannot tell progenitor age from
any other cause with that shape: a survey step, selection, dust, or an expansion history outside the family. "Never
accelerated" means no member of the family with q ≥ 0 on 0 ≤ z ≤ 2.33 fits. The Dovekie moduli carry the DES team's bias
corrections, computed in a reference cosmology, and those are inherited here. Part C rests on standard physics before
recombination; it is reported beside Part A, never in place of it.

## Files
`agb1r_common.py` (data, templates, models, minimiser, words), `agb1r_template.py` (T_S, T_W, KT), `agb1r_checks.py`
(counts, K1, K2, K4, K3 with exit 3/4), `agb1r_partA.py MODE`, `agb1r_partC.py MODE` (k5, full, des_only),
`agb1r_collect.py` (checks and words, `agb1r_results.json`, `agb1r_collect.out`), `agb1r_xcheck.py`, `agb1r_xcheckC.py`.
Each run writes `.json` and `.out` of the same name. Threads: OMP / BLAS 2 per process. Runtime: Part A about 6 min per
sample, Part C about 35 min per sample.

kappa = 1/2 FITTED; not theory closed.
