# AGB3R — blind re-grade of AGB3: result

2026-11-14. An independent second implementation of lane AGB3, written from `../AGB3_des_host_star_formation/FROZEN_CRITERIA.md`
alone (its README, scripts and outputs were not opened). My reading of the rules, committed alone before any fit:
`READING.md` (local commit fede243fba). Scripts: `agb3r_model.py` (two-component model), `agb3r_data.py` (loader),
`agb3r_hosts.py` (KM, K1, K2, K3, K4, Part D), `agb3r_cosmo.py` (KS, Parts S, J, E), `agb3r_collect.py` (gates and words;
`agb3r_collect.out`, `agb3r_results.json`; post hoc: `agb3r_posthoc_prior_width.py`). AGB1's fitter and AGB2's `joint` and galaxy model are imported unchanged.
A test of a published claim (Son et al., arXiv:2510.13121) on public data. Adopts nothing; no ledger edited.

## Checks (judged before the words)

| check | result | numbers |
|---|---|---|
| KM (i) burst age | PASS | log s −13, z 0.05: 10.665 Gyr against burst age 10.681 (−0.14 %; limit 2 %) |
| KM (ii) constant 6 Gyr | PASS | model 1.9023, quadrature 1.9023 Gyr (limit 0.001) |
| KM (iii) mass-only galaxies | PASS | largest \|two-component − mass-only\| 1.194 Gyr (z 0.05, log M 11.0; 0.784 at z 0.5); limit 1.5 |
| K1 table | PASS | sha256 matches; all 1,820 rows joined by (CID, IDSURVEY): zHD, zHEL, MU and MUERR_RENORM/MUERR identical (max diff 0); identity step 0.03344 mag, scatter 0.00059 / 0.00066 |
| K2 raw step, reading B, `full` | PASS | g = +0.0326 ± 0.0079 mag (low-mass fainter); \|g − 0.033\| ≤ 0.016 |
| K3 twins (12) | PASS (exit 3) | every \|Â − A_true\| < 10⁻¹⁰, χ²_min < 10⁻²³ |
| K4 D1 | PASS | σ_A 0.792; shuffle mean −0.027 σ; scatter ratio 1.185; sandwich ratio 1.195 |
| K4 D2 | PASS | σ_A 0.0793; shuffle mean −0.077 σ; scatter ratio 1.197; sandwich ratio 1.161 |
| K4 U | PASS | σ_A 0.0650; shuffle mean −0.066 σ; scatter ratio 1.100; sandwich ratio 1.116 |
| KS harness | PASS | A = 0 and AGB1's T_S at 1, `full` and `des_only`: all eight Δχ²_today / Δχ²_never equal AGB1's committed forks to < 10⁻⁴ |

Reproduction of the criteria's own pre-freeze numbers (not checks): the two-component table (27 entries) to 0.005 Gyr;
design-only σ_A 0.079 / 0.065 (D2 / U, `des_only`), 0.055 / 0.050 (`full`), D1 0.79 / 0.44: all equal; T_H(`full`) at the
twelve listed redshifts equal to the printed 0.000 … 0.099 to three decimals; the `full` bin-mean ages 5.77, 4.75, 3.45,
2.57, 2.88, 2.88, 2.46 Gyr equal. Every gate is open: Parts D, S, E and J are evaluable.

## Words

| word | first word | second word |
|---|---|---|
| **D2** | **NEITHER** | **FRAGILE (half template)** |
| **U** | **SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA** | **FRAGILE (half template; mass-only ages)** |
| **S2** | **SIGN NOT SETTLED** | **FRAGILE (`des_only`)** |
| **S3** | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** | (same on all four forks) |
| **J2** | **ACCELERATING TODAY** | **FRAGILE (half-template prior)** |
| **J3** | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** | (same on all five forks) |
| **E2** | **SIGN NOT SETTLED** | **FRAGILE (blue hosts; log s ≥ −10)** |
| **E3** | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** | (same on both forks) |

## Part D — the slope from the hosts (A in units of 0.030 mag/Gyr; Δχ² = (Â − a)²/σ²)

| fit | n | Â ± σ | Δχ²(A=0) | Δχ²(A=1) | word on this fit |
|---|---|---|---|---|---|
| **D2 primary** (`des_only`, R, 20 bins, z_f 3, step free) | 1623 | **+0.389 ± 0.079** | 24.01 | 59.36 | NEITHER |
| D2 reading P | 1623 | +0.384 ± 0.077 | 24.71 | 63.34 | NEITHER |
| D2 `full` | 1820 | +0.257 ± 0.055 | 22.01 | 184.85 | NEITHER |
| D2 40 bins | 1623 | +0.389 ± 0.080 | 23.49 | 57.75 | NEITHER |
| D2 `pure` | 1498 | +0.388 ± 0.080 | 23.77 | 58.94 | NEITHER |
| D2 z_f 2 | 1623 | +0.441 ± 0.096 | 21.13 | 33.83 | NEITHER |
| D2 z_f 5 | 1623 | +0.348 ± 0.069 | 25.72 | 90.23 | NEITHER |
| D2 half template (2Â ± 2σ) | 1623 | +0.778 ± 0.159 | 24.01 | 1.97 | AGE BIAS REQUIRED AT 3 SIGMA |
| **U primary** (`des_only`, R, g = 0) | 1623 | **+0.398 ± 0.065** | 37.44 | 86.03 | SLOPE OVERPREDICTS AT 3 SIGMA |
| U reading B | 1623 | +0.369 ± 0.060 | 37.38 | 109.21 | SLOPE OVERPREDICTS AT 3 SIGMA |
| U `full` | 1820 | +0.299 ± 0.050 | 35.52 | 196.05 | SLOPE OVERPREDICTS AT 3 SIGMA |
| U 40 bins | 1623 | +0.396 ± 0.066 | 36.21 | 84.61 | SLOPE OVERPREDICTS AT 3 SIGMA |
| U `pure` | 1498 | +0.405 ± 0.065 | 38.45 | 82.90 | SLOPE OVERPREDICTS AT 3 SIGMA |
| U z_f 2 | 1623 | +0.456 ± 0.078 | 34.52 | 49.25 | SLOPE OVERPREDICTS AT 3 SIGMA |
| U z_f 5 | 1623 | +0.356 ± 0.057 | 39.14 | 127.98 | SLOPE OVERPREDICTS AT 3 SIGMA |
| U half template | 1623 | +0.795 ± 0.130 | 37.44 | 2.49 | HOSTS AS LARGE AS THE SLOPE NEEDS |
| U mass-only ages | 1623 | +0.719 ± 0.147 | 23.87 | 3.63 | HOSTS AS LARGE AS THE SLOPE NEEDS |

The constant step beside D2: g = +0.002 ± 0.012 (R; the age template takes the whole raw step), −0.037 ± 0.012 (P).
Sandwich errors beside the WLS errors: D2 0.092 (vs 0.079), U 0.073 (vs 0.065).

**Reported only** (W1 rules printed for orientation, no frozen word):
- D1 (step run, AGB2's template): `des_only` +0.53 ± 0.79 (Δχ² 0.45 / 0.35); `full` −0.16 ± 0.44 (0.14 / 6.95); `des_only` P
  +1.21 ± 0.79 (2.37 / 0.07). Combined by inverse variance with AGB2's Pantheon+ fit without DES (H1, diagonal weights,
  +0.151 ± 0.457): **+0.246 ± 0.396** (Δχ² 0.39 / 3.63; UNDECIDED by the W1 rules).
- AGB2's H2 on this sample (mass-only ages per host, step free, `des_only`): R +0.685 ± 0.212 (Δχ² 10.47 / 2.21); P
  +0.936 ± 0.210 (19.83 / 0.09).
- D2 with the short-delay distribution: +0.388 ± 0.075 (26.64 / 66.34). D2 `full` in reading P: +0.249 ± 0.054
  (21.51 / 195.51). U `full` in reading P: +0.193 ± 0.048.
- Steps band by band (`full`, young side minus old side, mag), beside the slope's prediction at A = 1 (two-component):

| split | reading | z 0–0.1 | 0.1–0.3 | 0.3–0.5 | 0.5–0.7 | 0.7–1.2 |
|---|---|---|---|---|---|---|
| mass < 10 | R | +0.020 ± 0.018 | +0.042 ± 0.021 | +0.044 ± 0.015 | +0.039 ± 0.015 | +0.014 ± 0.033 |
| mass < 10 | P | −0.001 ± 0.017 | +0.021 ± 0.021 | −0.001 ± 0.015 | −0.014 ± 0.015 | +0.011 ± 0.033 |
| mass < 10 | predicted | +0.033 | +0.097 | +0.090 | +0.091 | +0.073 |
| log s ≥ −10 | R | +0.017 ± 0.016 | +0.038 ± 0.020 | +0.054 ± 0.015 | +0.046 ± 0.014 | +0.059 ± 0.023 |
| log s ≥ −10 | P | +0.027 ± 0.016 | +0.018 ± 0.019 | +0.035 ± 0.015 | +0.037 ± 0.014 | +0.053 ± 0.023 |
| log s ≥ −10 | predicted | +0.167 | +0.158 | +0.130 | +0.104 | +0.073 |
| colour ≤ 1.0 | R | +0.044 ± 0.016 | +0.076 ± 0.020 | +0.055 ± 0.014 | +0.040 ± 0.014 | +0.029 ± 0.023 |
| colour ≤ 1.0 | P | +0.043 ± 0.016 | +0.057 ± 0.020 | +0.029 ± 0.014 | +0.019 ± 0.014 | +0.019 ± 0.023 |
| colour ≤ 1.0 | predicted | +0.108 | +0.126 | +0.107 | +0.092 | +0.065 |

(Mass-only predictions for the mass split: +0.081, +0.067, +0.050, +0.040, +0.032; all rows in `agb3r_D.out`.)

## Part S — the sample's own age drift through AGB1's Part A fit (BAO + supernovae, flat w0–wa)

T_H(`full`) at z 0.03 … 1.0: 0.000, 0.005, 0.031, 0.070, 0.096, 0.094, 0.087, 0.088, 0.087, 0.090, 0.097, 0.099 mag.
T_H(`des_only`) at the same redshifts: 0.000, 0.000, 0.000, 0.003, 0.032, 0.021, 0.018, 0.021, 0.016, 0.026, 0.029, 0.030.

| T_H | fork | A_H | Ω_m | w0 | wa | q0 | Δχ²_today | Δχ²_never | words |
|---|---|---|---|---|---|---|---|---|---|
| **two-comp., z_f 3, `full`** | **A_H = 1** | 1 | 0.359 | −0.424 | −2.205 | **+0.092** | **1.25** | **79.88** | SIGN NOT SETTLED; EXCLUDED 3σ |
| | A_H = 0 | 0 | 0.314 | −0.843 | −0.538 | −0.367 | 18.64 | 168.14 | ACCELERATING; EXCLUDED 3σ |
| | A_H free | +0.141 | 0.321 | −0.787 | −0.769 | −0.302 | 2.66 | 79.14 | SIGN NOT SETTLED; EXCLUDED 3σ |
| `des_only`, own T_H | A_H = 1 | 1 | 0.304 | −0.905 | −0.181 | −0.444 | 7.18 | 87.40 | ACCELERATING; EXCLUDED 3σ |
| | A_H free | +1.113 | 0.306 | −0.894 | −0.228 | −0.430 | 5.64 | 77.70 | |
| mass-only ages, `full` | A_H = 1 | 1 | 0.340 | −0.618 | −1.283 | −0.112 | 1.88 | 91.02 | SIGN NOT SETTLED; EXCLUDED 3σ |
| | A_H free | +2.200 | 0.371 | −0.333 | −2.196 | +0.186 | 0.40 | 34.30 | |
| z_f 2, `full` | A_H = 1 | 1 | 0.358 | −0.440 | −2.082 | +0.077 | 0.88 | 75.44 | SIGN NOT SETTLED; EXCLUDED 3σ |
| z_f 5, `full` | A_H = 1 | 1 | 0.360 | −0.409 | −2.311 | +0.107 | 1.67 | 83.16 | SIGN NOT SETTLED; EXCLUDED 3σ |
| host by host, `full` | A_H = 1 | 1 | 0.351 | −0.519 | −1.685 | −0.005 | 0.00 | 75.68 | (reported) |
| | A_H free | +0.161 | 0.320 | −0.792 | −0.723 | −0.308 | 12.73 | 141.29 | |

A_H free and Δχ² at 0 and 1 (from the profile): `full` +0.141, Δχ²(0) 0.155, Δχ²(1) 5.761; `des_only` +1.113, 3.264, 0.033;
mass-only +2.200, 3.713, 1.102; z_f 2 +0.168, 0.159, 4.001; z_f 5 +0.123, 0.151, 7.646; host by host +0.161, 10.09, **272.46**
(the per-host correction at the published slope adds 263 to χ² against the smooth curve). Fork fits and profile fits at
A_H = 0 and 1 agree to < 10⁻⁵ in χ². No best fit at a prior edge in Part S.

## Part J — D2's slope as a prior on A_H (agb2_joint.joint, unchanged)

| configuration | prior | joint A_H (68 %) | Δχ²(0) | Δχ²(1) | q0 at joint A_H | Δχ²_today | Δχ²_never | words |
|---|---|---|---|---|---|---|---|---|
| **primary** (`full`, D2 primary) | 0.389 ± 0.079 | **+0.377 [0.299, 0.455]** | 23.71 | 64.66 | **−0.193** | **4.46** | **113.67** | ACCELERATING; EXCLUDED 3σ |
| `des_only` distances + T_H | 0.389 ± 0.079 | +0.401 [0.321, 0.480] | 25.92 | 58.03 | −0.519 | 9.65 | 93.88 | ACCELERATING; EXCLUDED 3σ |
| prior D2 reading P | 0.384 ± 0.077 | +0.374 [0.298, 0.450] | 24.42 | 68.66 | −0.194 | 4.57 | 114.40 | ACCELERATING; EXCLUDED 3σ |
| half-template prior | 0.778 ± 0.159 | +0.673 [0.527, 0.818] | 21.53 | 5.09 | −0.057 | 0.28 | 84.13 | SIGN NOT SETTLED; EXCLUDED 3σ |
| T_H mass-only | 0.389 ± 0.079 | +0.397 [0.318, 0.477] | 25.22 | 57.96 | −0.265 | 9.55 | 124.21 | ACCELERATING; EXCLUDED 3σ |
| U's amplitude as prior | 0.398 ± 0.065 | +0.389 [0.325, 0.454] | 37.10 | 91.30 | −0.187 | 4.42 | 115.83 | ACCELERATING; EXCLUDED 3σ |
| no prior, `full` | — | +0.141 [−0.219, 0.500] | 0.16 | 5.76 | −0.302 | 2.66 | 79.13 | |

No joint minimum on the edge of the A grid in the six judged configurations (the no-prior mass-only profile runs to the edge, A_H = 2).

## Part E — young hosts only (AGB1's Part A model on the subsample; published moduli; no age term)

| subsample | n (DES) | Ω_m | w0 | wa | q0 | Δχ²_today | Δχ²_never | words |
|---|---|---|---|---|---|---|---|---|
| **young** (log s ≥ −9.5) | 609 (586) | 0.323 | −0.762 | −0.764 | **−0.274** | **3.44** | **59.48** | SIGN NOT SETTLED; EXCLUDED 3σ |
| blue (colour ≤ 0.8) | 733 (699) | 0.322 | −0.772 | −0.723 | −0.286 | 4.97 | 69.78 | ACCELERATING; EXCLUDED 3σ |
| log s ≥ −10 | 1145 (1063) | 0.319 | −0.804 | −0.742 | −0.322 | 9.76 | 118.08 | ACCELERATING; EXCLUDED 3σ |
| old (complement) | 1211 (1037) | 0.315 | −0.838 | −0.575 | −0.362 | 16.17 | 136.52 | (reported) |
| young DES only | 586 (586) | 0.313 | −0.843 | −0.450 | −0.369 | 2.46 | 49.89 | (reported) |
| young, no BAO (extra) | 609 (586) | 0.414 | −0.730 | −3.000 (edge) | −0.142 | 0.66 | 27.87 | (extra) |

As the criteria say, SIGN NOT SETTLED on 609 supernovae means "too few", not "no": the young-host fit has q0 −0.27, close
to the whole sample's −0.37.

## What I think is wrong or under-specified in the criteria
1. **T_c is never stated.** "A part formed at a constant rate s × M over the last T_c" gives no default. I read T_c = time
   since the burst; that reproduces the printed table to 0.005 Gyr, so the reading is pinned by the criteria's numbers,
   but the text alone does not fix it.
2. **K1 says "row for row", but the two files are not in the same order** (the DES README says so). All 1,820 rows join
   exactly on (CID, IDSURVEY); a positional comparison would fail. An implementation that zipped the files would be wrong.
3. **T_H(`des_only`) "stays below 0.032 mag"** holds at the twelve listed redshifts (largest 0.0317, z 0.3) but not between
   them: the curve reaches 0.0349 at the bin-mean z 0.47.
4. **D2's word is NEITHER, and its one fragile fork is the half template.** The hosts want a slope near 0.39 × 0.030 =
   0.012 mag/Gyr: they exclude no age dependence at more than 4σ and the published slope at more than 7σ. The half-template
   fork flips this to REQUIRED, so the D2 word leans entirely on taking the star-formation contrast at face value.
5. **U is close to its fragile forks.** Under the half template or mass-only ages, Δχ²(A=1) is 2.5 and 3.6, both below 4.
6. **J2 primary sits 0.46 above its threshold** (Δχ²_today 4.46). The U-prior and reading-P forks give 4.42 and 4.57. It is the
   narrowest margin among the words. The K4 ratios for D2 (shuffle 1.20, sandwich 1.16, inside the allowed 1.25) say the
   WLS error is about 15–20 % small. Post hoc, not a frozen fork (`agb3r_posthoc_prior_width.py`): with the prior error set
   to the sandwich error (0.092) or the shuffle scatter (0.095), the joint A_H is +0.373 and Δχ²_today is 4.33 or 4.30,
   q0 −0.194; J2 does not flip. Only the half-template prior (Δχ²_today 0.28) does.
7. **Part S's primary drift is mostly a legacy-versus-DES step.** T_H(`full`) climbs 0.096 mag by z 0.3, almost all of it
   between the legacy hosts (z < 0.1) and the DES hosts, and is flat after. Inside DES the drift is ≤ 0.035 mag, and
   `des_only` gives ACCELERATING TODAY at A_H = 1. So S2's SIGN NOT SETTLED on `full` rests on the legacy hosts' listed
   star-formation rates, which the criteria themselves call inhomogeneous (27 % of legacy low-mass hosts listed as passive).
8. **Part E "on these supernovae alone"** does not say whether the BAO stay in. I kept them (it is "AGB1's Part A model")
   and print the no-BAO case as an extra: same words for `young`.
9. **J2's mass-only fork** pairs a two-component prior (D2) with a mass-only drift (T_H). I kept D2's two-component prior,
   as written. The pairing mixes two age models.
10. **The half-template fork for U** must apply "Â < 1" to 2Â. Here this changes nothing, because Δχ²(A=1) < 4 decides it.
11. The equal-count binning rule for ties is not given. I used rank with a stable sort. It reproduced every printed
    design-only error and T_H value, so I expect no effect.

kappa = 1/2 FITTED; not theory closed.
