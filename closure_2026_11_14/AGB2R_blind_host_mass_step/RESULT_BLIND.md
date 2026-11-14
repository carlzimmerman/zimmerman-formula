# AGB2R — blind re-grade of AGB2 (host-mass step against redshift in Pantheon+): result

2026-11-14. A second implementation of lane AGB2, written from `FROZEN_CRITERIA.md` and `AMENDMENT_1.md` only
(reading in `READING.md`, committed alone first). AGB2's scripts, outputs and README, and the write-ups of AGB1 and of
the later AGB lanes, were not opened. AGB1's fitter, template and its three committed JSON files were used, as Part J
prescribes. Nothing here is compared with AGB2's own numbers except the values printed inside the two files above.

## Words

| word | as amended (amendment 1; diagonal weights) — **the evaluable reading** | as frozen (full covariance) |
|---|---|---|
| H1 step run | **UNDECIDED, FRAGILE (median age)** (amendment 1) | NOT EVALUABLE (K4); reading: AGE BIAS FAVOURED, FRAGILE (reading P, sample measured) |
| H2 per host | **AGE BIAS EXCLUDED AT 3 SIGMA, ROBUST** (amendment 1) | NOT EVALUABLE (K4); reading: NEITHER, FRAGILE (sample measured) |
| J1 joint amplitude | **UNDECIDED, FRAGILE (AGB1 des_only, both)** (amendment 1) | NOT EVALUABLE (K4); reading: AGE BIAS FAVOURED, FRAGILE (both) |
| J2 today | **SIGN NOT SETTLED** (amendment 1) | NOT EVALUABLE (K4); reading: SIGN NOT SETTLED |
| J3 ever | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** (amendment 1) | NOT EVALUABLE (K4); reading: NEVER-ACCELERATED EXCLUDED AT 3 SIGMA |

The as-frozen reading is **not evaluable under the frozen rules**: the frozen K4 fails for the per-host template in
this build too (shuffle scatter 1.42 σ_A against the allowed 0.8–1.25), so by the frozen rule H1, H2 and J1–J3 are
NOT EVALUABLE as frozen. The amended checks all pass, so the amended words are evaluable.

## Checks

| check | result | numbers |
|---|---|---|
| KG (i) | PASS | log M_Q(0.35) = 10.5473 (10.55 ± 0.01); branches at z = 1.5: 10.7881, 10.7885 |
| KG (ii) | PASS | z = 0 mean age 1.027, 3.073, 8.715, 10.454 Gyr at log M 8, 10, 11.5, 12: fraction of the rise inside 10–11.5 = 0.598 (≥ 0.5) |
| KG (iii) | PASS | log M 11.5 track today: half its formed mass by lookback 10.905 Gyr (in [8, 11.5]); 25 %–75 % between 11.323 and 10.019 Gyr, width 1.304 (≤ 2) |
| KG (iv) | PASS | 2 Myr against 4 Myr step: largest change 0.0036 Gyr (mean), 0.0039 Gyr (median) (≤ 0.05) |
| K1 | PASS | Ω_m = 0.3316 ± 0.0182 on `k1` (1,590 rows), χ² 1402.92 (target 0.334; allowed difference 0.009) |
| K2, as amended (diagonal) | PASS | reading R constant step g = +0.0388 ± 0.0080 mag, low-mass hosts fainter ([0.02, 0.09]); reading P −0.0027 ± 0.0076 |
| K2, as frozen (full) | PASS | g = +0.0404 ± 0.0105 mag; reading P −0.0029 ± 0.0096 |
| K3, full covariance | PASS | 8 of 8 twins: Â within 1 × 10⁻¹⁰ of A_true, χ²_min ≤ 2 × 10⁻²² (exit 3) |
| K3, diagonal | PASS | 8 of 8 twins, same precision (exit 3) |
| K4, frozen form, full covariance, step run | PASS | mean Â +0.028 (+0.070 σ_A); scatter 0.479 = 1.197 σ_A (σ_A 0.400) |
| K4, frozen form, full covariance, per host | **FAIL** | mean Â +0.009 (+0.089 σ_A); scatter 0.141 = **1.423 σ_A** (σ_A 0.099) |
| K4, amended form, diagonal, step run | PASS | mean +0.023 (+0.055 σ_A); scatter 0.414 = 1.007 σ_A; sandwich 0.405 = 0.986 σ_A (σ_A 0.411) |
| K4, amended form, diagonal, per host | PASS | mean +0.005 (+0.039 σ_A); scatter 0.129 = 1.047 σ_A; sandwich 0.123 = 1.003 σ_A (σ_A 0.123) |
| KJ, `full` | PASS | from my spline of the committed profile on −1 … 2: Δχ²(0) 2.1002, Δχ²(1) 0.7854 (AGB1 2.1002, 0.7854); re-fitted f at A = 0, 1 equal to the committed values (difference 0 to printed precision); t − f at A = 0, 1: 18.6384, 3.4148 (AGB1 18.6384, 3.4148); n − f: 168.1406, 37.5226 (AGB1 168.1406, 37.5226) |
| KJ, `des_only` | PASS | Δχ²(0) 0.5449, Δχ²(1) 1.9586 (AGB1 0.5449, 1.9586); re-fits equal; t − f 11.5627, 0.1782; n − f 98.8262, 34.2153 (all equal to AGB1's to 10⁻⁴) |

(For information: the clustered sandwich error of the full-covariance fits, in my GLS-score form, is 1.63 σ_A for
the step run and 2.90 σ_A per host; the amended K4 form would fail on the full covariance for both templates.)

**Comparison with the numbers the two files quote (not checks):** my galaxy model reproduces every mean age printed in
the criteria (21 values at z = 0, 0.5, 1.0) to 0.01 Gyr and the z = 0 medians to 0.01 Gyr; Δτ(z) for `all` is
3.448, 3.303, 3.077, 2.675, 2.331, 1.785, 1.377, 1.066 Gyr against the quoted 3.45, 3.31, 3.08, 2.68, 2.33, 1.79, 1.38,
1.07; KG (iii) 10.905 / 1.304 against the quoted 10.92 / 1.28 (my convention for the formed-mass quantiles differs a
little); KG (iv) 0.004 as quoted. The design-only σ_A (full covariance) are 0.400, 0.322, 0.405, 0.509, 0.400 (step run:
primary, median, 40 bins, measured, P) and 0.099, 0.074, 0.100, 0.153, 0.097 (per host), against the quoted 0.40, 0.32,
0.40, 0.51, 0.40 and 0.10, 0.07, 0.10, 0.15, 0.10; diagonal 0.411 and 0.123 against the amendment's 0.41 and 0.12.
K1 (0.3316), both constant steps (+0.0404 ± 0.0105 and −0.0029 ± 0.0096 on the full covariance) and the K4 failure
(1.42 against 1.44) agree with the amendment; the amendment's diagonal error triplets (claimed, sandwich, shuffle)
0.411, 0.405, 0.418 and 0.123, 0.123, 0.128 come out here as 0.411, 0.405, 0.414 and 0.123, 0.123, 0.129.

## Part H — the host measurement

Primary configuration: `all` (1,563 rows), reading R (mB − μ_fid with stretch and colour free), mean age, 20 equal-count
bins. Δχ² = (Â − a)²/σ_A².

| configuration | weights | step run Â ± σ_A | Δχ²(0) | Δχ²(1) | word | per host Â ± σ_A | Δχ²(0) | Δχ²(1) | word |
|---|---|---|---|---|---|---|---|---|---|
| primary | diagonal | +0.378 ± 0.411 | 0.846 | 2.292 | UNDECIDED | +0.129 ± 0.123 | 1.106 | 50.26 | EXCLUDED |
| reading P | diagonal | +0.334 ± 0.411 | 0.659 | 2.632 | UNDECIDED | +0.124 ± 0.121 | 1.046 | 52.30 | EXCLUDED |
| median age | diagonal | +0.305 ± 0.331 | 0.847 | **4.403** | DISFAVOURED | +0.057 ± 0.082 | 0.474 | 131.1 | EXCLUDED |
| 40 bins | diagonal | +0.461 ± 0.416 | 1.226 | 1.680 | UNDECIDED | +0.141 ± 0.124 | 1.300 | 48.26 | EXCLUDED |
| `measured` (1,251) | diagonal | +0.203 ± 0.515 | 0.155 | 2.399 | UNDECIDED | +0.210 ± 0.153 | 1.882 | 26.57 | EXCLUDED |
| primary | full | +0.811 ± 0.400 | 4.112 | 0.224 | FAVOURED | +0.298 ± 0.099 | 9.020 | 49.92 | NEITHER |
| reading P | full | +0.784 ± 0.400 | 3.846 | 0.293 | UNDECIDED | +0.267 ± 0.097 | 7.612 | 57.34 | NEITHER |
| median age | full | +0.656 ± 0.322 | 4.146 | 1.136 | FAVOURED | +0.157 ± 0.074 | 4.500 | 130.1 | NEITHER |
| 40 bins | full | +0.918 ± 0.405 | 5.133 | 0.041 | FAVOURED | +0.310 ± 0.100 | 9.659 | 47.82 | NEITHER |
| `measured` | full | +0.361 ± 0.509 | 0.502 | 1.579 | UNDECIDED | +0.171 ± 0.153 | 1.259 | 29.52 | EXCLUDED |

("EXCLUDED" = AGE BIAS EXCLUDED AT 3 SIGMA, "DISFAVOURED" = AGE BIAS DISFAVOURED, "FAVOURED" = AGE BIAS FAVOURED.)
The constant step g in the primary diagonal fits: +0.008 ± 0.034 (step run; the template carries the step) and
+0.029 ± 0.012 (per host). Stretch and colour: a = −0.140, b = +2.52 (diagonal), −0.134, +2.47 (full).

**H1's second word turns on one fork that sits near its threshold:** with the median age the gap Δτ is larger, σ_A
shrinks to 0.331, and Δχ²(A = 1) = 4.40 crosses 4 (DISFAVOURED). The other three forks stay UNDECIDED.
**H2's exclusion of A = 1 is large in every fork (Δχ²(A = 1) from 26.6 to 131) and rests on the model's age–mass shape inside each
mass group:** at A = 1 the per-host template predicts that hosts of log M 11.5 are 0.16 mag brighter than hosts of
log M 10.0 at z = 0.03 (0.11 at z = 0.3, 0.08 at z = 0.6), a trend above 10¹⁰ that a single step cannot absorb, and the
data do not show it. As the criteria say, this has four times the grip and four times the reliance on the C14 model.

**Full covariance against diagonal.** The full-covariance step-run amplitude (+0.81) sits about one σ above the
diagonal one (+0.38) on the same data; the full-covariance per-host amplitude (+0.30) more than two of its own claimed
σ above the diagonal one (+0.13). That is the leverage of the off-diagonal terms that K4 detected.

## Reported only (no frozen word)

**The constant step band by band** (one fit: 20 bin offsets, five band steps, global a, b in reading R), mag, low-mass
hosts fainter when positive; beside it the step the slope predicts at A = 1 (mean of 0.030 Δτ(z_i) over the band):

| band (rows; mean z) | R, diagonal | P, diagonal | R, full | P, full | A = 1 predicts |
|---|---|---|---|---|---|
| 0.01–0.05 (534; 0.026) | +0.044 ± 0.014 | +0.001 ± 0.014 | +0.061 ± 0.016 | +0.016 ± 0.015 | 0.103 |
| 0.05–0.15 (181; 0.096) | +0.047 ± 0.020 | +0.004 ± 0.020 | +0.047 ± 0.021 | −0.002 ± 0.020 | 0.093 |
| 0.15–0.30 (381; 0.226) | +0.036 ± 0.015 | −0.004 ± 0.015 | +0.028 ± 0.016 | −0.012 ± 0.016 | 0.078 |
| 0.30–0.50 (282; 0.375) | +0.043 ± 0.017 | +0.002 ± 0.017 | +0.037 ± 0.018 | −0.007 ± 0.018 | 0.063 |
| 0.50–1.00 (185; 0.633) | +0.009 ± 0.026 | −0.031 ± 0.026 | +0.008 ± 0.026 | −0.037 ± 0.025 | 0.045 |
| straight line, mag per unit z | −0.043 ± 0.042 | −0.036 ± 0.042 | −0.077 ± 0.041 | −0.074 ± 0.041 | −0.099 |

**Reading R with g fixed at 0** ("all of the step is age"): step run A = +0.473 ± 0.096 (diagonal), +0.524 ± 0.122
(full); per host +0.352 ± 0.081 (diagonal), +0.382 ± 0.082 (full).

**Model and sample forks** (reading R and P; Â ± σ_A):

| fork | weights | rows | step run R | step run P | per host R | per host P |
|---|---|---|---|---|---|---|
| alternate M_Q (Eq. 11) | diag | 1563 | +0.311 ± 0.337 | +0.274 ± 0.337 | +0.133 ± 0.116 | +0.128 ± 0.114 |
| T_W delay times | diag | 1563 | +0.502 ± 0.545 | +0.443 ± 0.545 | +0.109 ± 0.140 | +0.099 ± 0.138 |
| masses + 0.2 dex | diag | 1563 | +0.329 ± 0.358 | +0.291 ± 0.358 | +0.127 ± 0.112 | +0.124 ± 0.110 |
| masses − 0.2 dex | diag | 1563 | +0.442 ± 0.481 | +0.390 ± 0.480 | +0.137 ± 0.138 | +0.131 ± 0.137 |
| z ≤ 0.7 | diag | 1513 | +0.442 ± 0.442 | +0.420 ± 0.442 | +0.127 ± 0.123 | +0.114 ± 0.122 |
| drop SDSS | diag | 1242 | +0.419 ± 0.426 | +0.361 ± 0.426 | +0.185 ± 0.140 | +0.191 ± 0.138 |
| drop SNLS | diag | 1403 | +0.343 ± 0.492 | +0.344 ± 0.491 | +0.132 ± 0.126 | +0.115 ± 0.124 |
| drop PS1 | diag | 1294 | +0.459 ± 0.456 | +0.472 ± 0.456 | +0.159 ± 0.136 | +0.124 ± 0.134 |
| drop DES | diag | 1362 | +0.149 ± 0.457 | +0.130 ± 0.457 | +0.149 ± 0.129 | +0.144 ± 0.127 |
| drop Foundation | diag | 1390 | +0.463 ± 0.437 | +0.353 ± 0.437 | +0.138 ± 0.129 | +0.112 ± 0.127 |
| drop other low-z | diag | 1129 | +0.599 ± 0.521 | +0.644 ± 0.521 | +0.152 ± 0.157 | +0.179 ± 0.155 |
| alternate M_Q (Eq. 11) | full | 1563 | +0.670 ± 0.328 | +0.646 ± 0.328 | +0.288 ± 0.096 | +0.261 ± 0.094 |
| T_W delay times | full | 1563 | +1.078 ± 0.531 | +1.041 ± 0.530 | +0.318 ± 0.103 | +0.273 ± 0.100 |
| masses + 0.2 dex | full | 1563 | +0.706 ± 0.348 | +0.682 ± 0.348 | +0.273 ± 0.095 | +0.250 ± 0.093 |
| masses − 0.2 dex | full | 1563 | +0.949 ± 0.468 | +0.917 ± 0.467 | +0.332 ± 0.104 | +0.292 ± 0.102 |
| z ≤ 0.7 | full | 1513 | +0.862 ± 0.429 | +0.856 ± 0.429 | +0.285 ± 0.100 | +0.254 ± 0.097 |
| drop SDSS | full | 1242 | +0.766 ± 0.415 | +0.808 ± 0.415 | +0.368 ± 0.109 | +0.342 ± 0.107 |
| drop SNLS | full | 1403 | +0.861 ± 0.486 | +0.917 ± 0.485 | +0.294 ± 0.102 | +0.259 ± 0.100 |
| drop PS1 | full | 1294 | +1.008 ± 0.443 | +0.969 ± 0.443 | +0.347 ± 0.107 | +0.305 ± 0.104 |
| drop DES | full | 1362 | +0.621 ± 0.443 | +0.622 ± 0.442 | +0.318 ± 0.103 | +0.279 ± 0.100 |
| drop Foundation | full | 1390 | +0.938 ± 0.424 | +0.821 ± 0.424 | +0.307 ± 0.103 | +0.257 ± 0.100 |
| drop other low-z | full | 1129 | +0.612 ± 0.509 | +0.694 ± 0.508 | +0.113 ± 0.153 | +0.174 ± 0.151 |

## Part J — the two measurements of the slope together

χ²_J(A) = AGB1's committed Part A profile (cubic spline on −1.0 … 2.0) + (A − Â_H1)²/σ_H1². t(A) (q0 = 0) on the 0.1 grid
and n(A) (never accelerated) on the 0.25 grid were re-fitted here with AGB1's fitter and starts (311 fits per sample).
Minima on a grid of 0.001; no joint minimum and no 95 % interval touches the edge of the A grid. In the `full` sample
the q0 = 0 fits at A ≤ −0.4 (and in `des_only` at A = −1.0) sit on AGB1's bound wa = −3; that region is far from every
prior and from every minimum (the q0 = 0 minima lie at A 0.27 to 0.78).

**As amended (Â_H1 = +0.378 ± 0.411, diagonal, reading R) — the evaluable reading:**

| AGB1 sample, host amplitude | joint Â | 68 % | 95 % | Δχ²_J(0) | Δχ²_J(1) | J1 first word | q0_J | Δχ²_today | J2 | Δχ²_never | J3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **full, H1 R (judged)** | **+0.493** | [+0.198, +0.789] | [−0.097, +1.087] | **2.782** | **2.914** | UNDECIDED | **−0.113** | **0.440** | SIGN NOT SETTLED | **34.23** | EXCLUDED AT 3 SIGMA |
| full, H1 P | +0.470 | [+0.175, +0.766] | [−0.120, +1.063] | 2.530 | 3.188 | UNDECIDED | −0.125 | 0.536 | SIGN NOT SETTLED | 34.67 | EXCLUDED AT 3 SIGMA |
| des_only, H1 R | +0.364 | [+0.056, +0.672] | [−0.257, +0.981] | 1.388 | **4.248** | DISFAVOURED | −0.330 | 1.743 | SIGN NOT SETTLED | 34.21 | EXCLUDED AT 3 SIGMA |
| des_only, H1 P | +0.339 | [+0.031, +0.647] | [−0.283, +0.956] | 1.204 | 4.590 | DISFAVOURED | −0.347 | 1.912 | SIGN NOT SETTLED | 34.73 | EXCLUDED AT 3 SIGMA |
| full, H2 in place of H1 (reported) | +0.167 | [+0.049, +0.284] | [−0.069, +0.402] | 1.997 | 49.83 | EXCLUDED AT 3 SIGMA | −0.281 | 7.582 | ACCELERATING TODAY | 80.06 | EXCLUDED AT 3 SIGMA |
| des_only, H2 (reported) | +0.143 | [+0.025, +0.261] | [−0.094, +0.380] | 1.451 | 52.02 | EXCLUDED AT 3 SIGMA | −0.475 | 6.897 | ACCELERATING TODAY | 68.37 | EXCLUDED AT 3 SIGMA |

J1 is FRAGILE because AGB1's `des_only` profile (best A +0.346, against +0.618 on `full`) pulls the joint amplitude
down to +0.36, and Δχ²_J(A = 1) then crosses 4 (4.25); with H1's reading-P amplitude alone the word is unchanged.

**As frozen (Â_H1 = +0.811 ± 0.400, full covariance) — NOT EVALUABLE (K4), printed as a reading:**

| AGB1 sample, host amplitude | joint Â | 68 % | 95 % | Δχ²_J(0) | Δχ²_J(1) | J1 first word | q0_J | Δχ²_today | J2 | Δχ²_never | J3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| full, H1 R | +0.721 | [+0.429, +1.014] | [+0.138, +1.309] | 6.104 | 0.901 | FAVOURED | +0.003 | 0.000 | SIGN NOT SETTLED | 30.63 | EXCLUDED AT 3 SIGMA |
| full, H1 P | +0.707 | [+0.415, +1.000] | [+0.123, +1.294] | 5.866 | 0.999 | FAVOURED | −0.004 | 0.001 | SIGN NOT SETTLED | 30.85 | EXCLUDED AT 3 SIGMA |
| des_only, H1 R | +0.614 | [+0.311, +0.918] | [+0.007, +1.222] | 4.085 | 1.611 | FAVOURED | −0.172 | 0.494 | SIGN NOT SETTLED | 29.71 | EXCLUDED AT 3 SIGMA |
| des_only, H1 P | +0.599 | [+0.296, +0.902] | [−0.008, +1.206] | 3.884 | 1.745 | UNDECIDED | −0.181 | 0.551 | SIGN NOT SETTLED | 29.99 | EXCLUDED AT 3 SIGMA |
| full, H2 (reported) | +0.315 | [+0.218, +0.411] | [+0.122, +0.508] | 10.59 | 50.18 | NEITHER | −0.204 | 4.604 | ACCELERATING TODAY | 75.98 | EXCLUDED AT 3 SIGMA |
| des_only, H2 (reported) | +0.300 | [+0.204, +0.397] | [+0.107, +0.494] | 9.555 | 51.87 | NEITHER | −0.372 | 4.603 | ACCELERATING TODAY | 63.14 | EXCLUDED AT 3 SIGMA |

**The host amplitude against AGB1's best A** (+0.618 on `full`, the side of its 68 % interval facing the host value
taken as its error): diagonal Â_H1 − Â_AGB1 = −0.240, combined error 0.593, **−0.41 σ**; full covariance +0.193, combined
error 0.588, +0.33 σ. The two measurements of the slope agree within their errors in both weightings.

## What in the criteria I think is wrong or under-specified

1. **The frozen K4 fails in this independent build as well** (per host, scatter 1.42 σ_A; the step run passes at
   1.20), so the amendment's premise is reproduced; under the frozen rules H1, H2 and J1–J3 are NOT EVALUABLE. The
   amendment's change of weights is supported by the amended K4 here (claimed, sandwich and shuffle errors agree to
   5 % for both templates with diagonal weights; with the full covariance the sandwich is 1.6 and 2.9 times the claimed
   error). The amendment changes the estimator after the frozen check failed, and the amended H1 amplitude (+0.38) differs
   from the frozen one (+0.81) by about one σ, so the amended words depend on that choice; the amendment records that no
   amplitude had been read when it was written, which I cannot check from the two files.
2. **Two second words turn on a single fork near a threshold.** H1 is FRAGILE only through the median-age fork,
   Δχ²(A = 1) = 4.40 against 4; J1 is FRAGILE only through AGB1's `des_only` profile, Δχ²_J(A = 1) = 4.25 against 4.
   Both moves go towards excluding A = 1, not towards requiring it.
3. **H2 is the strongest statement and the most model-bound.** The per-host template predicts, at A = 1, a brightness
   trend with mass inside the high-mass group (0.16 mag between log M 10.0 and 11.5 at z ≈ 0.03) that comes from the
   C14 model's steep age–mass relation above 10¹⁰; the fit puts the amplitude of that shape at +0.13 ± 0.12. A real age–mass relation
   that is flatter above 10¹⁰ (S25's own point that host mass tracks age poorly) would weaken the exclusion by the same
   factor. The criteria state this; the frozen words still call it EXCLUDED AT 3 SIGMA with no model-error term.
4. **Under-specified in the criteria** (my choices in `READING.md`; none moves a word as far as I can see, since my
   model reproduces every quoted age, gap and forecast error to the printed precision): the galaxy integration
   details (step-start quenching, mid-step mass-loss ages, the seed's role, averaging the delay-time distribution over a
   step); how ties are handled in equal-count bins; whether Δτ averages over rows or supernovae; the exact shuffle
   procedure of K4 (my step-run scatter, 1.197 σ, differs from the amendment's 1.22 only by the draws); the sandwich's
   small-sample factor (irrelevant: 1,446 clusters); whether HST (code 100) belongs to "the other low-z sets"; how the
   band-by-band steps and their straight line are fitted; and KG (iii)'s quantile convention (mine 10.905 / 1.304 against
   the quoted 10.92 / 1.28).
5. **J2's q0_J and Δχ²_today live in AGB1's background model** (w0–wa with BAO); the host term only moves A. With the
   amended prior the joint best A is +0.49, where AGB1's own free fit at that A has q0 = −0.11; J2 is SIGN NOT SETTLED
   because Δχ²_today = 0.44, the same verdict AGB1 gives at its own free A. The host prior is too weak (σ 0.41) to change
   AGB1's Part A words; only the model-bound H2 prior would (ACCELERATING TODAY at Δχ²_today 7.6, reported only).
6. **Reading R's selection caveat stands untested:** the band steps in reading R are flat to within errors
   (slope −0.043 ± 0.042 mag per unit z against −0.099 at A = 1), and reading P shows no step at all up to z 0.5. The lane
   cannot separate a smaller slope from a smaller real age gap than C14's, as the criteria say.
7. The criteria's "C14 mass-function-weighted median age today (3.2 Gyr)" could not be recomputed: the mass function is
   not given in the two files.

## Files and commits
- `READING.md` (commit 673da707dc, alone, before any measured magnitude was read).
- `agb2r_galaxy.py` (model, KG, tables `agb2r_tables.npz`, `agb2r_KG.json`, `agb2r_galaxy.out`); `agb2r_run.py design`
  (K3 twins and σ_A forecasts, no magnitude; `agb2r_design.*`), `K1` (`agb2r_K1.*`), `H` (K2, K4, Part H, reported items;
  `agb2r_H.*`); `agb2r_joint.py full|des_only` (AGB1's fitter at fixed A with q0 = 0 and never accelerated;
  `agb2r_J_*.*`); `agb2r_collect.py` (checks, words, Part J; `agb2r_results.json`, `agb2r_collect.out`).
  Scripts and the magnitude-free outputs were committed in c2fc40ce60 before K1 or Part H was run.

kappa = 1/2 FITTED; not theory closed.
