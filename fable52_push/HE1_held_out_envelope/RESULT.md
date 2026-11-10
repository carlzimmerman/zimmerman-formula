# HE1 RESULT (criteria 0e67f3c64a; amendments A1 22e1d5a6ba, A2 9163ca4fe6)

Commit ids: the hashes in this folder are the shared checkout's. On origin the same commits are 91d343f150 (criteria),
ab52b18eda (A1), d6c99b61de (A2) and 5137d5e374 (result).

**HE1: FAILS / FAILS** (canonical / alt).

At the primary R_out (the turnaround radius of (1 + X) M_b), every X of the stated set fails:

| X | failing gates (canonical) | failing gates (alt) |
|---|---|---|
| X_share 5.562 | G4, G5 | G4, G5 |
| X_census 5.364 N (53.64; 51.08 at log M 10.9) | G4, G5 | G4, G5 |
| X_cap 53.64 | G1, G4, G5 | G1, G4, G5 |

- **The label does not rest on G5.** No X at any R_out passes G1 to G4 together, primary or bracket, on either footing.
- **G5 fails as frozen on two clusters, near R500 only.** A644's hydrostatic mass (M_FORW) falls beyond 0.8 R500 and A2319's
  component mass flattens beyond 0.9 R500, so the frozen lower bound on the component pressure goes to zero there. The
  groups and the other five clusters hold everywhere in [0.05, 1] R500. With the NFW-fit mass (post hoc) all seven hold.
- **G4 and G4b** (the free-calibration companion) agree at the primary R_out: both fail for every X. They disagree at three
  canonical brackets, where G4b passes and G4 fails: X_share at 1.5 Mpc, X_census at 3 Mpc, X_cap at 3 Mpc.
- **No bracket passes all gates.** The brackets that pass G4 on alt (the same three) fail G2: their walls at low masses run
  past R_K.

TEST lane, quarantined. Adopts nothing and relabels nothing; not registered. kappa = 1/2 FITTED; not theory closed. Footings
never pooled.

**Checks.** The first two runs were NO VERDICT (known answers failed; see "Runs and amendments"). In the third run every
known answer passes. HE1.lean compiles with standard axioms only (20 theorems) and its twin fails with seven errors, all in
the false versions. All three MUTATE arms bite.

## The answer in plain words

The construction holds statically. For every mass and every share in the record, an isothermal envelope sitting outside the
wall at pressure balance exists. It is stable, it leaves discs alone (except the cap share at the highest masses), and it
fills about 0.2 % of space or less. Groups and five of the seven clusters keep the law off; in the other two the frozen
statistic fails near R500, where their measured hydrostatic mass stops rising.

It fails where it was expected to fail: KiDS's late-type lenses. With the share spread to its own turnaround radius, the wall
sits at 0.04 to 0.34 R_K. Outside it, the envelope's lensing is 0.12 to 0.36 of the law. The late-type stacks sit near 1.5
of the law in the middle window (0.16 to 0.38 R_K). To put that window inside the wall, the wall must reach about 0.38 R_K
for every lens. Every R_out that does this at the heavier KiDS masses pushes the low-mass walls past R_K and breaks the
filling line (q 0.18 to 0.66 against 0.0354; 0.18 to 0.46 for the three that pass G4 on alt).

## Part A (exact; `HE1.lean`, 20 theorems, standard axioms only)

| statement | content | numerical departure in Part B |
|---|---|---|
| A1 `deep_balance` | deep wall pressure = singular envelope pressure iff R_w = (r_M / 3)(v_f / sigma)^4 | exact W puts the wall at 0.96-1.00 of it (`deep` column) |
| A2 `amplitude_form` | R_w / r_M = (4/3) / A^2, A = 2 sigma^2 / v_f^2 | same |
| A3 `sis_mass` | singular envelope mass 2 sigma^2 R / G = A (R / r_M) M_b | the exact Jeans envelope holds 1.11-1.89 times A (x_out - x_w) M_b (`shell` column) |
| A4 `W_lower3` (new) | (2/3) u^3 / (1 + u)^2 <= W(u) for u >= 0 | |
| A5 `dW_dy`, `slope_identity`, `slope_bracket` | d ln p_wall / d ln R = -2 y (u - y) / W lies in [-3, -2) for every y | -2.96 to -3.00 at the walls found |
| A6 `W_le_deep_q`, `cubic_mono`, `W_lower_q`, `exact_vs_deep` | R_deep / (1 + r_M / R_w)^2 <= R_w <= R_deep | 0.96-1.00, inside the bracket |
| A7 `stable_frozen`, `deep_sis_stable`, `swept_restoring` | an envelope falling as R^-n with n < 2 is stable against any wall displacement (the brief's n = 2 against R^-3 is the special case); a swept layer always restores | |
| A8 `jeans_wall_slope`, `deep_stable_iff` | at the deep balance the envelope's Jeans log-slope at the wall is -(3/2) A; stable iff A < 4/3 | -0.18 to -0.56 |

**Where my hand derivation departs from the exact solution.**
- *Exact W.* The wall moves inward by at most (1 + r_M / R_w)^-2, which is 0.96-1.00 here.
- *Exact Jeans solution.* The singular exterior assumes the enclosed mass at the wall is (4 / (3A)) M_b, about 4-11 M_b at the
  primary R_out. The true value is M_b. So the envelope's density falls only as r^-(1.5A) near the wall, and it holds 1.1 to 1.9 times the
  singular-shell mass for the same sigma.
- *Consequence.* For a given share, the exact A is lower and the wall further out than the closed form gives. Example:
  X_census to 3 Mpc at log M 10.7 gives A 0.116 and R_w 99 r_M (0.38 R_K), where my pre-freeze singular-shell estimate gave
  0.18 and 43 r_M.
- *A second, inner root* exists at x_w = 0.06-0.10 r_M: the wall deep inside the galaxy, so the law is effectively off.
  The construction takes the outer root.

## Part B: the four KiDS masses, primary R_out (canonical; alt in brackets)

| X | log M_b | R_out (Mpc) | R_w (kpc) | R_w / r_M | R_w / R_K | sigma / v_f | A | M_env < 200 kpc / 1 Mpc / 3 Mpc (M_b) |
|---|---|---|---|---|---|---|---|---|
| share | 9.4 | 0.237 | 171 (173) | 88 (98) | 0.34 (0.34) | 0.25 (0.24) | 0.12 (0.12) | 2.15 / 5.56 / 5.56 |
| share | 10.45 | 0.530 | 360 (366) | 56 (62) | 0.21 (0.22) | 0.28 (0.27) | 0.15 (0.15) | 0 / 5.56 / 5.56 |
| share | 10.7 | 0.642 | 430 (436) | 50 (56) | 0.19 (0.19) | 0.29 (0.28) | 0.16 (0.15) | 0 / 5.56 / 5.56 |
| share | 10.9 | 0.748 | 495 (503) | 45 (51) | 0.18 (0.18) | 0.29 (0.28) | 0.17 (0.16) | 0 / 5.56 / 5.56 |
| census | 9.4 | 0.479 | 102 (112) | 53 (64) | 0.20 (0.22) | 0.28 (0.27) | 0.16 (0.14) | 13.2 / 53.6 / 53.6 |
| census | 10.45 | 1.073 | 113 (141) | 17.5 (23.9) | 0.067 (0.083) | 0.37 (0.34) | 0.27 (0.23) | 5.4 / 50.8 / 53.6 |
| census | 10.7 | 1.300 | 109 (137) | 12.6 (17.4) | 0.048 (0.061) | 0.40 (0.37) | 0.32 (0.27) | 5.0 / 43.9 / 53.6 |
| census | 10.9 | 1.492 | 125 (157) | 11.5 (15.8) | 0.044 (0.055) | 0.41 (0.38) | 0.34 (0.29) | 3.2 / 37.4 / 51.1 |
| cap | 10.9 | 1.516 | 106 (133) | 9.8 (13.4) | 0.038 (0.047) | 0.43 (0.39) | 0.36 (0.31) | 4.6 / 38.8 / 53.6 |

X_cap equals X_census below log M 10.9. The brackets are in he1.out, for example:
- X_share at 1.5 Mpc: R_w / R_K 2.56 / 0.69 / 0.50 / 0.39.
- X_census at 3 Mpc: 3.05 / 0.60 / 0.38 / 0.27.

## G1 discs untouched (R_w >= 10 r_M at the KiDS masses and the GSMF grid, z 0)

| X, R_out | smallest R_w / r_M, canonical (alt) | where | gate |
|---|---|---|---|
| share, r_ta | 27.6 (30.9) | log M 12 | PASS / PASS |
| census, r_ta | 11.5 (15.8) | log M 10.75-10.9 | PASS / PASS |
| cap, r_ta | 3.1 (3.9) | below 10 from log M 11.0 (canonical) / 11.25 (alt) to 12, and 9.8 at KiDS's 10.9 (canonical) | **FAIL / FAIL** |
| share 1.5 / 3 Mpc | 23.0 / 52.5 (25.8 / 58.5) | | PASS |
| census 1.5 / 3 Mpc | 11.7 / 33.8 (14.0 / 38.4) | | PASS |
| cap 1.5 / 3 Mpc | 0.35 / 2.1 (0.48 / 2.6) | | FAIL |

There is no component inside R_w in any solution, by construction. Every (mass, X, R_out) has a balance: 0 NO BALANCE.

## G2 filling (SWT1's `compensated`, line q <= 0.0354 at z 0, 0.5, 1)

| X, R_out | q_tot z 0 / 0.5 / 1, canonical | alt | filling f_V (max) | late types only, q (max) | gate |
|---|---|---|---|---|---|
| share, r_ta | 0.0026 / 0.0039 / 0.0041 | 0.0027 / 0.0041 / 0.0044 | 0.0029 / 0.0031 | 0.0019 / 0.0020 | PASS / PASS |
| census, r_ta | 0.0002 / 0.0001 / 0.0001 | 0.0003 / 0.0002 / 0.0001 | 0.0002 | 0.0001 | PASS / PASS |
| cap, r_ta | 0.0001 / 0.0000 / 0.0000 | 0.0001 / 0.0001 / 0.0000 | 0.0001 | 0.0001 | PASS / PASS |
| share, 1.5 Mpc | 0.18 / 0.33 / 0.39 | 0.19 / 0.34 / 0.40 | 0.21 | 0.32 | FAIL |
| share, 3 Mpc | 0.66 / 0.66 / 0.66 | 0.66 | 1.97 (not dilute) | 0.65 | FAIL |
| census, 1.5 Mpc | 0.014 / 0.019 / 0.017 | 0.016 / 0.021 / 0.019 | 0.0125 / 0.0141 | 0.018 / 0.021 | PASS |
| census, 3 Mpc | 0.27 / 0.41 / 0.40 | 0.29 / 0.46 / 0.46 | 0.22 / 0.24 | 0.38 / 0.42 | FAIL |
| cap, 1.5 / 3 Mpc | as census | as census | | | PASS / FAIL |

Every primary filling is under GAL1's 0.0197 and under its 0.0134 for a z 6 switch-on. At r_ta, the late-only proxy halves the
already small numbers.

## G3 stability of the exact solution

| X, R_out | envelope pressure log-slope at the wall, KiDS masses (canonical) | wall pressure log-slope | worst margin over KiDS + GSMF, canonical (alt) | gate |
|---|---|---|---|---|
| share, r_ta | -0.19 / -0.23 / -0.25 / -0.26 | -2.99 to -3.00 | 2.65 (2.67) | PASS / PASS |
| census, r_ta | -0.24 / -0.42 / -0.50 / -0.52 | -2.97 to -2.99 | 2.45 (2.54) | PASS / PASS |
| cap, r_ta | -0.24 / -0.42 / -0.50 / -0.56 | -2.96 to -2.99 | 1.84 (1.99) | PASS / PASS |
| cap, 1.5 Mpc | | | -2.27 (-1.14) | FAIL (walls of 0.35 r_M, Newtonian regime) |

Reported:
- **Swept-layer reading.** It restores at every KiDS mass (A7).
- **Quasi-static reading in he1.py** (envelope re-solved at fixed sigma and share, wall displaced by +-5 %). It restores for
  X_share (p_env / p_wall 1.21-1.27 outward, 0.80-0.83 inward) and for the census share at log M 9.4. For X_census and X_cap
  at log M >= 10.45 it reported "not restoring" with ratios of 0.17-0.63 and 57-136. Those numbers come from a second root of
  the share condition about e^1 away, not the local response.
- **Post hoc check (he1_extra.py, reported only).** With the nearest root, every +-1 % and +-5 % displacement restores (one
  -5 % case has no nearby root).
- **But those same census and cap envelopes sit past the turnover of the share condition.** At fixed sigma,
  d ln M_env / d ln rho_w is -0.03 to -0.16, and the density contrast rho(R_w) / rho(R_out) is 59-250, against about 14 for
  a critical Bonnor-Ebert sphere. That points to a gravothermal instability of the envelope itself, which no gate here
  grades. The X_share envelopes have contrast 1.2-1.3 and d ln M / d ln rho near +0.93: well before any turnover.

## G4 KiDS late stacks (KO1's machinery, joint jackknife, Hartlap 45/49; PASS iff p > 0.05 on both stacks)

Data window amplitudes (outer / middle / inner, with errors), reproduced to KO1's digits:
- W30 late: 0.534 +- 0.228 / 1.543 +- 0.260 / 0.920 +- 0.164 (alt 0.486 / 1.405 / 0.840).
- Host-free late: -0.189 +- 0.391 / 1.532 +- 0.403 / 1.583 +- 0.266 (alt -0.172 / 1.394 / 1.444).

| model | W30 late: model A; chi2, p | host-free late: model A; chi2, p | G4 | G4b (free c), p W30 / hf |
|---|---|---|---|---|
| law alone, canonical | 1 / 1 / 1; 8.72, 0.033 | 1 / 1 / 1; 17.66, 0.0005 | FAIL | 0.014 / 0.0002 |
| law alone, alt | 8.63, 0.035 | 16.99, 0.0007 | FAIL | 0.014 / 0.0002 |
| **share, r_ta**, canonical | 0.05 / 0.40 / 1.04; 22.08, 0.0001 | 0.05 / 0.33 / 1.05; 13.06, 0.0045 | **FAIL** | 0.0000 / 0.038 |
| share, r_ta, alt | 0.05 / 0.42 / 1.04; 21.74, 0.0001 | 0.05 / 0.34 / 1.05; 11.04, 0.012 | **FAIL** | 0.0000 / 0.047 |
| **census, r_ta**, canonical | 0.36 / 0.39 / 0.66; 24.10, 0.0000 | 0.35 / 0.39 / 0.65; 23.11, 0.0000 | **FAIL** | 0.005 / 0.009 |
| census, r_ta, alt | 0.32 / 0.32 / 0.76; 21.37, 0.0001 | 0.32 / 0.32 / 0.75; 19.33, 0.0002 | **FAIL** | 0.0004 / 0.009 |
| **cap, r_ta**, canonical | 0.37 / 0.41 / 0.58; 26.04, 0.0000 | 0.37 / 0.44 / 0.50; 26.86, 0.0000 | **FAIL** | 0.017 / 0.003 |
| cap, r_ta, alt | 0.33 / 0.34 / 0.70; 21.55, 0.0001 | 0.34 / 0.38 / 0.62; 22.02, 0.0001 | **FAIL** | 0.001 / 0.010 |
| share, 1.5 Mpc, canonical / alt | p 0.44 / 0.52 | p 0.047 / 0.097 | FAIL / PASS | PASS / PASS |
| census, 3 Mpc, canonical / alt | p 0.23 / 0.32 | p 0.044 / 0.114 | FAIL / PASS | PASS / PASS |
| cap, 3 Mpc, canonical / alt | p 0.13 / 0.24 | p 0.021 / 0.067 | FAIL / PASS | PASS / PASS |
| other brackets | p <= 0.011 | p <= 0.0006 | FAIL | FAIL |

- **What fails.** The middle window, 0.16-0.38 R_K, lies outside the wall at every primary R_out. There the model is 0.3-0.4
  of the law and both late stacks are near 1.5.
- **The shape statistic agrees.** Data outer / inner is 0.58 (W30 late) and -0.12 (host-free late). The model gives 0.05
  (X_share) and 0.54 (X_census).
- Without the Hartlap factor the p values are lower: X_share host-free late 0.0026 / 0.0073.
- The raw projection (P_model / glaw instead of the differential form) changes model amplitudes by at most 0.009.
- **The veto edge (reported, post hoc, low power).** Host-free late with the veto widened:
  - Data: 0.01 / 1.46 / 1.59 at 1.3 R_h, and **0.13 / 0.33 / 1.61** at 1.6 R_h (errors 0.68 / 0.67 / 0.47).
  - At 1.6 R_h the X_share model fits (p 0.73 / 0.83), as do the law (p 0.25 / 0.22) and X_census (p 0.29 / 0.45).
  - At 1.3 R_h: X_share p 0.17 / 0.25, law 0.075 / 0.079, X_census 0.020 / 0.047.
  - So the middle-window excess that kills the construction is itself not stable against the veto radius. That is the
    edge effect KO1 found, and it is why a pass on these stacks could only ever be a consistency check.
- The late-type split was first seen post hoc in KO1 and shares its edge effect. A pass here would have been a consistency
  check, not a confirmation; the fail is a fail on the record's stacks as frozen.

## G5 hot systems (wall pressure of a system's own baryons against its component's hydrostatic pressure, [0.05, 1] R500)

| system | max p_wall / p_c, canonical (alt) | at 0.05 / 0.25 / 0.5 R500 (canonical) | first radius where p_wall >= p_c | post hoc, M_NFW |
|---|---|---|---|---|
| A1795 | 0.163 (0.181) | 0.010 / 0.025 / 0.073 | none | 0.24 |
| A2029 | 0.164 (0.183) | 0.010 / 0.023 / 0.071 | none | 0.21 |
| A2142 | 0.235 (0.261) | 0.008 / 0.024 / 0.059 | none | 0.19 |
| **A2319** | **7.8 (8.6)** | 0.005 / 0.018 / 0.068 | **0.86 R500** | 0.40 |
| **A644** | **diverges** (p_c -> 0) | 0.006 / 0.011 / 0.125 | **0.62 R500** | 0.19 |
| A85 | 0.149 (0.166) | 0.006 / 0.022 / 0.060 | none | 0.17 |
| ZW1215 | 0.067 (0.074) | 0.005 / 0.013 / 0.034 | none | 0.09 |
| Lovisari groups, 20 x (f* 0, 1) | 0.52 (0.58); median 0.12 | | none (40 of 40 held) | |

**G5: FAIL / FAIL as frozen.**
- A644's M_FORW decreases beyond 0.8 R500 (4.94e14 at 0.99 R500, 4.17e14 at 1.44 R500). A2319's component mass is flat
  beyond 0.9 R500. With the density clipped at zero and no tail, the frozen lower bound on p_c vanishes near R500.
- In the other five clusters the wall pressure is at most 0.24 of the component pressure, and in the groups at most 0.58.
  In A644 and A2319 it is at most 0.14 out to 0.5 R500. Everywhere it is about 0.01 at 0.05 R500.
- Post hoc, with the monotone NFW-fit mass, all seven clusters hold (max 0.44). The gate as frozen fails, and I report it
  that way.

## G6 formation (reported)

| X (primary R_out) | sigma / sigma_vir | envelope vs collapsed singular halo of the same share inside R_out / 2: M < 200 kpc (M_b) | share that must never have been inside R_w | envelope pressure at R_out / infall ram pressure |
|---|---|---|---|---|
| share | 0.95-1.07 (alt 0.96-1.09) | 0-2.2 vs 3.0-5.6 | **100 %** (R_w > R_out / 2; SWT1's placement: 60-65 %) | **9-14** |
| census / cap | 0.60-0.68 | 1.5-13.2 vs 13.7-44.8 | 14-47 % | 1.0-1.2 |

- **What it would take.** The share would have to stay outside R_w from the start: it never collapsed through the wall
  radius. SNP1 shows the wall cannot push a bound share out, and nothing here forms the envelope.
- For the record's share at its own turnaround radius the envelope is not even confined: its pressure at R_out exceeds the
  infall ram pressure by about 10, so it would expand into the flow.
- The census share is confined at about the ram pressure, but is 35 % colder than virial and needs 14-47 % of a collapsed
  halo to have stayed out.
- **Formation is open.** A passing version would need a mechanism that keeps the component hot and outside about 0.2 R_K
  from early times.

## The record's pooled KiDS gate with every lens cleared (B21 Fig. 9, 59 points; reported)

| X | points outside the wall | points beyond 0.05 dex of the law (differential / raw) | chi2 vs data: law -> model, canonical (alt) |
|---|---|---|---|
| share | 23 / 59 | 29 / 29 | 279 -> 937 (209 -> 904) |
| census | 39 (36) | 43 (41-42) | 279 -> 1077 (209 -> 1074) |
| cap | 39 (36) | 43 (41-43) | 279 -> 1042 (209 -> 1055) |

As expected, it fails badly. The pooled stack is carried by early types, which this construction says are not cleared. A
completion along these lines must treat early types separately, and that is not graded here.

## Closure C (reported): sigma^2 = G (1 + X) M_b / (2 R_out), primary R_out

| X | R_w / R_K at the KiDS masses (canonical) | A | G1 | G2 (q max) | G3 | G4 p (W30 / hf), canonical; alt |
|---|---|---|---|---|---|---|
| share | 0.39 / 0.24 / 0.22 / 0.20 | 0.05-0.10 | PASS | PASS (0.0060) | PASS | 0.0007 / 0.011; 0.0010 / 0.029 FAIL |
| census | 0.25 / 0.14 / 0.12 / 0.11 | 0.20-0.38 | PASS | PASS (0.0011) | PASS | 0.0000 / 0.0003; 0.0000 / 0.0006 FAIL |
| cap | 0.25 / 0.14 / 0.12 / 0.11 | 0.20-0.39 | PASS | PASS (0.0010) | PASS | 0.0000 / 0.0002; 0.0000 / 0.0005 FAIL |

The label does not depend on the closure.

## Known answers (third run, all PASS)

| check | result |
|---|---|
| KA1 deep limit | R_exact / R_deep 0.99963 at 1e3 r_M, 0.99996 at 1e4 (bounds 3e-3, 3e-4); singular start stays singular to 1.2e-10; point-mass Boltzmann profile to 4.9e-10 |
| KA2 p_wall | own implementation vs swt1.py 1.0e-13 at 20 y in [1e-8, 1e4]; W vs quadrature 1.3e-13 |
| KA3 projection | thick shell 1.0e-14, thin shell vs a 1e-5-thick shell 3.1e-5, truncated singular sphere 9.5e-15, untruncated 4 G DeltaSigma / (2 sigma^2 / R) = 1.00000 |
| KA4 KO1 reproduced | 40,667 host-free; all 12 window amplitudes and errors equal to ko1_extra.out's digits |
| KA5 lens-model limits | no wall: window amplitudes 1 to 1e-12; point baryons raw = (4 / pi) g to 1e-16 |
| KA6 (A1) grid convergence | largest window move between the 0.01- and 0.005-dex grids 0.0003 over 48 case-stacks (line 0.01). The frozen pointwise check, reported only: 7.5 relative, 0.035 absolute (square-root behaviour at wall crossings) |
| KA7 r_ta scaling | 1.2e-6 |
| KA8 `compensated` import | 0.0180 / 0.0182 (SWT1's printed values) |
| root bracketing (A2) | 0 unconfirmed sign changes |

## MUTATE (separate outputs, `he1_MUTATE_M*.json / .out`, `run_mutate_M*.txt`)

| arm | what it breaks | what happened | bite |
|---|---|---|---|
| M1 | wall pressure with the opposite sign | NO BALANCE for every mass, X and R_out on both footings. G1, G3 and G4 fail for every X. G5 "passes" trivially, since p_wall < 0 | **BITES** |
| M2 | p_wall / 100 | No balance at any of the 17 masses (four KiDS and 13 GSMF) for any X at r_ta on either footing, so G1 fails for every X. KA1's deep limit then misses the closed form by exactly the factor 0.01 (R_exact / R_deep 0.0100), and the run is NO VERDICT | **BITES** |
| M3 | envelope projected as a point mass at the centre | KA3's singular-sphere check gives 1.27324 = 4/pi, and the run is NO VERDICT. Model window amplitudes move by up to 0.122 against the graded run, e.g. X_census middle 0.39 -> 0.49 (canonical) | **BITES** |

The Lean twin (`HE1_MUTATE.lean`): seven false versions, exit 1, seven errors, all inside the false versions
(`compile_MUTATE.txt`).

Disclosed: M2 first crashed in G3's aggregation, which unpacked a NO BALANCE entry. The line was fixed (it cannot touch a run
without NO BALANCE entries), and M2 and the main run were re-run with the fixed code. M1 has no balance anywhere and M3 has a
balance everywhere, so the changed line returns the same values for both; they were not re-run.

## Runs and amendments

- **Run 1 (NO VERDICT).** KA1 failed: my "negligible" density of 1e-14 carries about 5 M_b over three decades in radius.
  KA6 failed as frozen: the pointwise per-bin interpolation check cannot pass at any grid.
- **AMENDMENT A1.** Corrected KA1 and KA3 (KA3's tolerance had been coded looser than frozen). Replaced KA6 by a convergence
  test on the stacked window amplitudes. Refined the lens grid from 0.1 to 0.005 dex.
- **Run 2 (NO VERDICT).** The new KA6 failed (0.023). It traced to a root-bracketing bug: when a sign change was
  unconfirmed, the inner root was silently kept at isolated masses.
- **AMENDMENT A2** records the bug and the fix (no criterion changes).
- **Run 3** is the graded run. Its gate outcomes are the same as runs 1 and 2: the bug touched isolated lens-grid nodes and
  moved no gate.
- All three runs' outputs are kept: `he1_run1_noverdict.*`, `he1_run2_noverdict.*`, `run_main_run1.txt`,
  `run_main_run2.txt`.

## What works

1. **A static equilibrium exists everywhere.** For every KiDS and GSMF mass, every X and every R_out, an isothermal envelope
   balances the law's wall pressure: 0 NO BALANCE. The hand closed forms hold to 0-4 % in the wall radius.
2. **It is stable against wall displacement with a wide margin.** The exact wall pressure always falls faster than R^-2
   (Lean A5). The envelope's pressure at the wall falls only as R^-(0.2 to 0.6). Lean A7 makes any n < 2 stable, and the
   swept-layer and local quasi-static readings restore.
   - Caveat: the heavy (census and cap) envelopes at log M >= 10.45 sit past the isothermal turnover, with density contrast
     59-250 (he1_extra.py). The record's-share envelopes do not (contrast 1.3).
3. **Discs untouched for the record's share and the census share** (walls at 11.5 r_M or more). **Filling tiny** for every
   X at its turnaround radius (q <= 0.0044, f <= 0.0031), far under SWT1's and GAL1's lines.
4. **Hot systems keep the law off.** All 20 groups and five of seven X-COP clusters hold everywhere in [0.05, 1] R500. The
   wall pressure there is about 1 % of the component's pressure at 0.05 R500, with no new constant. This is SWT1's ordering
   (galaxies clear, clusters do not), now with measured masses.
5. **The record's share spread to its own turnaround radius has the virial dispersion** of (1 + X) M_b to within 5-9 %, so
   the envelope is not a tuned object.
6. New exact results: W >= (2/3) u^3 / (1 + u)^2; the wall's log-slope lies in [-3, -2) for all y; the exact wall radius is
   bracketed by R_deep / (1 + r_M / R_w)^2 and R_deep.

## What is open: what a passing version would need

1. **A wall at 0.38-0.43 R_K for every late-type lens.** Inside 0.38 R_K the late stacks' middle window lies within the wall.
   Beyond 0.43 R_K the filling breaks CMB lensing. In this construction R_w / r_M is fixed by X and R_out / r_M. Holding
   R_w / R_K fixed for every mass needs R_out to grow as r_M, as M^(1/2), about 150-180 r_M for the record's share.
   Turnaround gives M^(1/3). Nothing in the record supplies that scale without a new constant. The brackets show both sides:
   - Fixed 1.5 or 3 Mpc reaches 0.39-0.69 R_K at the heavy KiDS masses, and G4 passes on alt.
   - The same choice sends the low-mass walls past R_K, and G2 fails by 5-13x.
2. **Formation.** The share must never have been inside R_w: all of it for X_share, 14-47 % for the census share. SNP1 shows
   the wall cannot remove a bound share. For X_share at r_ta the envelope also over-pressures its surroundings about tenfold.
3. **Early types.** The construction leaves them uncleared, and the pooled B21 stack then fails by about 650-870 in chi2.
   Their treatment is not part of this construction.
4. **The KiDS middle-window excess is fragile.** Host-free late types drop from 1.53 to 0.33 +- 0.67 when the veto is
   widened to 1.6 R_h, where the construction fits (p 0.73). A spectroscopic isolation sample with a veto well beyond the
   measured range (README item 5.2) would decide whether G4's fail is the lenses' own field or the veto's edge.
5. **G5's two failing clusters** need a monotone hydrostatic mass beyond 0.6 R500, or a tail. The NFW-fit bracket says they
   hold, but that is post hoc.

## Against the hand estimates (frozen before any number)

- **Mine.** X_share at r_ta: hit (walls 45-98 r_M against my 40-55; A 0.12-0.17 against 0.15-0.18). X_census at r_ta:
  hit at the heavy end (11.5-17.5 r_M against 9-12), but G1 passes where I expected a marginal fail. At 3 Mpc: **miss**
  (99 r_M, 0.38 R_K, A 0.12 against my 43 r_M, 0.16, 0.18; I used the singular-shell mass). G2, G3, G4 and the B21 fail:
  hit. **G5 PASS: miss** (it fails as frozen on two clusters' data near R500). Label FAILS: hit.
- **The lead's.** Census share to 3 Mpc: sigma 0.24 v_f, A 0.12, R_w 99 r_M = 0.38 R_K at L*, against the estimate of
  0.26 v_f, 0.14, 65 r_M, 0.37 R_K. Close on R_w / R_K. Filling near 1.5 %: the 3 Mpc bracket gives 15-22 % (it fails),
  r_ta gives 0.02 %. "Late-type stacks prefer the cliff mildly over the law": on the frozen veto, no. The law (p 0.033 /
  0.0005) beats the cleared model at r_ta (p 0.0001 / 0.0045) on both stacks. At 1.6 R_h both fit.

## Files

FROZEN_CRITERIA.md (0e67f3c64a), AMENDMENT_A1.md (22e1d5a6ba), AMENDMENT_A2.md (9163ca4fe6) (local commit ids); he1.py ->
he1.json / he1.out (run_main.txt with timing); he1_MUTATE_M1 / M2 / M3.json / .out (run_mutate_M*.txt); he1_run1_noverdict.*,
he1_run2_noverdict.*, run_main_run1.txt, run_main_run2.txt; he1_extra.py -> he1_extra.json / .out (post hoc, reported only); HE1.lean, HE1_MUTATE.lean, compile.txt, compile_MUTATE.txt.

Graded run: one thread, 631 s, peak 1.13 GB. This is the re-run after the G3 aggregation fix; its he1.out is identical to the first run-3 output apart from timings. Each MUTATE run took about 10 minutes. The shear catalogue was not read and nothing was downloaded. Lean was compiled
with `lake env lean` from the copy of fable_independent_2026/lean_2026 that has its Mathlib build.

Not registered: the closure register belongs to the orchestrator. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
