# KR1: a running K-mass from a non-quadratic K(Q). FAIL on both footings: the mass runs, but galaxies capture the dust

Adopts nothing. Kappa = 1/2 FITTED; not theory closed. This is a TEST lane under the owner's 11-04 rule. It reopens the
action's K(Q) sector, which is cold dark energy, never dark matter, and has no particle.

- Criteria: FROZEN_CRITERIA.md (77ebbd6ad2), pushed alone before any script or number (merged as d11c425804).
- Scripts:
  - `kr1.py`: main run 20 s, peak RSS 254 MB; MUTATE run 15 s, 212 MB.
  - `kr1_static.py`: 9 s, 204 MB.
  - All runs use one thread.
- Outputs: kr1.json / kr1.out, kr1_MUTATE.json / kr1_MUTATE.out, kr1_static.json / kr1_static.out, and the run_*.txt logs.
- Read-only engines: CK4 (solve3, fsigma8, P1D), GL1's corrected `limber_n` (n = 4), KD1 (model P, GB1 gates), F1A
  (the cold fit). No other lane's file was written.

**Label, canonical: FAIL. Label, alt: FAIL.**

| member | blocked by |
|---|---|
| D0 | GC |
| D1 | S0, CS, GC |
| D2 | S0, CS, GC |
| D3 | S0, CS, GC, (iii) |

**The brief's own kill does not fire.** Three members (D0, D1, D2) meet (i) BBN, (ii) the growth line and (iii)
mu_K(0) <= 79.43 on the background, and the mass runs the right way. The lane still fails, because of a fact the brief's
framing missed: **the dust inside a galaxy never feels mu_K(0).** It feels the mass at its own local density, and condition
(ii) itself forces that mass to be large.

## The family and how it was fixed

- **Family.** Blanchet-Skordis's DBI K = (2 mu^2/lambda)[1 - sqrt(1 - lambda q^2)]. It is the action's authors' own
  non-quadratic K, and lambda -> 0 gives back the quadratic K.
  - K' diverges at q_max = lambda^(-1/2), so dK/dQ is not asymptotically linear: there is no stiff partner.
  - The mass runs as M = mu Qbar r^(3/2) with r = sqrt(1 + lambda Z^2), so M ~ a^(-9/2) early.
- **Amplitude.** I0 = 3 (100/c)^2 omega_d, with omega_d from F1A's B2 cold fit: 4.036973e-8 (canonical) and
  4.035347e-8 (alt) Mpc^-2.
- **lambda** is fixed by M(z = 3) = 630.957 Mpc^-1.
  - That number is GL1's corrected-kernel growth line. The brief's "361" is not in the record and is read as a digit
    transposition. 631 is the tighter line, and every member also clears 361.
  - M rises monotonically with z on every member, so z = 3 is the binding point. That is checked on a 200-point grid.
- **Members.** D0-D3 sit at the record's own landmarks for mu: 1e-3, 0.1 (S4), 9.998 (BS cap) and 79.43 (QX3).
  mu_K(0) is READ.

## mu_K(z) = M(z) in Mpc^-1, canonical (alt identical to 3-4 digits; both in kr1.json)

| member | mu | lambda | q_max | z 0 (READ) | z 3 | z 10 | z 100 | z 1100 | z 3400 | z 1e5 |
|---|---|---|---|---|---|---|---|---|---|---|
| D0 | 1e-3 | 3.242e7 | 1.76e-4 | **1.232** | 631 | 5.98e4 | 1.29e9 | 6.01e13 | 9.62e15 | 3.90e22 |
| D1 | 0.1 | 6.986e12 | 3.78e-7 | **1.265** | 631 | 5.98e4 | 1.29e9 | 6.01e13 | 9.62e15 | 3.90e22 |
| D2 | 9.998 | 1.498e18 | 8.17e-10 | **10.45** | 631 | 5.97e4 | 1.29e9 | 5.99e13 | 9.59e15 | 3.89e22 |
| D3 | 79.43 | 3.542e20 | 5.31e-11 | **79.65** | 631 | 5.70e4 | 1.23e9 | 5.72e13 | 9.16e15 | 3.71e22 |

- **The read mu_K(0) has a floor.** Along the whole constraint curve, mu_K(0) >= 630.957 / 4^4.5 = 1.232 Mpc^-1, which
  D0 reaches.
  - It is inside QX3's <= 79.43.
  - It is 12 times S4's isolated-galaxy guard of 0.1.
- D3 reads 79.65, just over 79.43, which is its (iii) FAIL.

## Column x member (both footings identical in status)

| Column | D0 | D1 | D2 | D3 | numbers (canonical) |
|---|---|---|---|---|---|
| B1a cold at z 3400 (w <= 0.01) | PASS | PASS | PASS | PASS | w 3.9e-17 to 2.2e-20 |
| B1b BBN (i) (X <= 0.067) | PASS | PASS | PASS | PASS | X 1.2e-9 to 3.6e-16 (quadratic K at the same mu: 5.3e18 to 8.4e8) |
| R2 growth line (ii), min M over z 3-1100 >= 631 | PASS | PASS | PASS | PASS | 630.96, at z 3, by construction; M rises with z |
| C1 primary CMB at mu_K(1100) | PASS | PASS | PASS | PASS | max w(z 100-3400) <= 1.5e-12; comoving hold a M >= 1.2e7 Mpc^-1 vs the 2.5 line; abundance at z 1100 within 1.8e-4. So F1A's cold fit (omega_d/omega_b 5.410 / 5.412) applies, with a residual hold factor <= 4e-16 |
| GL CMB lensing, corrected kernel | PASS | PASS | PASS | PASS | chi^2 8.571, Delta chi^2 +0.000 |
| GF DESI fsigma8 | PASS | PASS | PASS | PASS | Rf 0.9997-1.0000 |
| GFo forest P1D | PASS | PASS | PASS | PASS | ratio 0.9993-1.0000 |
| CT c_T | PASS | PASS | PASS | PASS | analytic: K(Q) does not enter the tensor sector |
| S0 stationary branch exists (q_max >= 9.87e-9 / 5.38e-7 / 1.11e-5) | PASS | **FAIL** (MW, cluster) | **FAIL** (all three) | **FAIL** (all three) | the DBI root is complex at the khronon charge a bound system needs |
| CS Cassini | PASS | **FAIL** | **FAIL** | **FAIL** | D0: near field 1.1e-27. D1-D3 have no stationary branch at the Sun |
| GC galaxy capture (2 pi/M_ta >= 234 kpc) | **FAIL** | **FAIL** | **FAIL** | **FAIL** | M_ta 2261 / 2261 / 2255 / 2173 Mpc^-1, Jeans length 2.8-2.9 kpc |
| (iii) mu_K(0) <= 79.43 | PASS | PASS | PASS | **FAIL** | 1.232 / 1.265 / 10.45 / 79.65 |
| G1-G8 (consequence of GC; KD1 model P at M_ta) | G1-G7 FAIL, G8 PASS | same | same | same | see below |

G1-G8 at M_ta (`kr1_static.py`). The core is pi/M = 1.4 kpc, and 5,612 of 5,633 points sit in captured systems.

| Gate | canonical | alt |
|---|---|---|
| G1 SPARC | Z -0.70, rms 0.777 (line 0.146) | Z -0.71, rms 0.789 (line 0.143) |
| G2 X-COP | mean -0.70 | mean -0.71 |
| G3 groups | 1/20 and 0/20 | 1/20 and 0/20 |
| G4 ellipticals | -0.47 | -0.47 |
| G5 Coma UDGs | +2.29 sigma_U | +2.14 sigma_U |
| G6 dSph classes | +0.61 to +0.93 | +0.59 to +0.90 |
| G7 KiDS | +2.46 sigma | +2.46 sigma |
| G8 Solar System | PASS | PASS |

These are KD1's wall-1 failures, reproduced at the running K's own local mass.

## Why it fails: one ordering, for any K(Q) (criteria section 4)

- Q is a local scalar, and for convex K the density rho_K(Q) is strictly increasing. So the kernel mass
  M^2 = Q^2 K''/2 is a function of the sector's own local density, everywhere.
- Condition (ii) requires M >= 631 at the background densities of z 3 to 1100, that is, 64 to 1.3e9 times today's mean.
- A galaxy turning around at z_c = 2 holds its dust at 5.55 x 27 = 149.9 times today's mean. That is the background
  density of z = 4.31, inside the window.
- So M_ta >= 631 Mpc^-1, far above the 26.85 Mpc^-1 at which the Jeans length equals the 234 kpc turnaround radius.
  The dust is captured.
- This holds for every galaxy turning around at z_c >= 1.259 (computed: 1.259 on every member).
- It holds for every K(Q), not only DBI. The forest's own line, M >= 53 at that density, already forces it.
- What a disc sees is M at its local density, and (ii) fixes that value directly. Tuning mu_K(0) cannot change it.
- S0 is DBI-specific. On D1-D3 the pole q_max lies below the khronon charge that bound systems carry (|psi|/c^2), so the
  stationary branch on which the record's statics and law S are derived does not exist there. D0 escapes S0 (q_max 1.8e-4)
  and is killed by GC alone.

## Reported row RB: GL1's corrected-kernel iter3 member (beta 0.8, mu0 1259), never graded on BBN or the CMB

| | value |
|---|---|
| K | ~ q^1.385 |
| q reaches 1 at | z 67.3 |
| w beyond that | 2.60 (stiffer than a^-6) |
| log10 X_BBN | 47.3, so (i) FAIL |
| M | 1259 today, 45.2 at z 3, a minimum of 0.092 at z 60.8 |
| running direction | the wrong way at late times, so (ii) FAIL |

GL1's "member found" passes lensing only because the lensing statistic does not test BBN or the primary CMB. Both
footings agree.

## Known answers and MUTATE (all PASS; nothing was graded until they did)

- **KA1.** At lambda = 0 the general machinery gives KD1's mu_B1a and mu_B1b:
  - 198.254232 / 8.890114e6 (canonical) and 198.244865 / 8.889273e6 (alt);
  - relative error <= 1.3e-15.
- **KA2.** F1A R = 5.409583 / 5.412268, |d| = 0.
- **KA3.** Sympy, DBI on its background: K' = I0/a^3, K'' = 2 mu^2 r^3, the excess, K, and the lambda -> 0 limit
  I0 (1 + w0/a^3)/a^3. All residuals are 0. M = mu Qbar at lambda = 0.
- **KA4.** On N3's corner (0.0215, 65, 0.95), the CK4 solver plus GL1's n = 4 kernel reproduces GL1 L2 at mu 63.1 / 100 /
  251 / 631 / 1000:
  - 449.1686 / 196.0794 / 19.3088 / 1.4719 / 0.4631;
  - |d| <= 2.8e-13;
  - and the iter3 member at 2.7798 (|d| 1.1e-13).
- **KA5.** Cold limit: ratios within 4.4e-16 of 1, Delta chi^2 0.
- **KA6.** kd1.py's own KA1/KA3/KA4 pass; KD at I0 = 0 equals GB1 L0 with |d| = 0.
- **M-A, the quadratic K (partner present).** B1b FAILS at every member: X 5.3e18 (mu 1e-3) to 8.4e8 (79.43). On KD1's
  setting it reproduces KD1's converse w 0.0591981 and X 8.39246e8 (relative 1.1e-16; alt 4.4e-16). **Bites.**
- **M-B, constant mu (wall 1).** GL Delta chi^2 is 279.9 / 679.8 / 1158.1 / 308.1 at the four mu values; all FAIL.
  At 79.43 this sits beside KD1's corrected converse of 309.0. **Bites.**
- **M-C, GC has power.** A constant M = 0.1 is not captured (Jeans length 62.8 Mpc). **Bites.**

## KR2's window

No window had arrived from KR2 (kr2-today-window) when this file was written. (iii) is graded against QX3's 79.43 only.
By the ordering above, the label does not depend on that window. Whatever present-day mu_K(0) KR2 allows, galaxy dust
sits at M_ta >= 631, which is set by (ii) and not by mu_K(0). If KR2's window arrives, its reading is added as a
fix-forward note.

## Assumptions and disclosures

- **C1 is a sufficiency reading, not a new Boltzmann fit.**
  - The column checks that the sector is cold, at the cold fit's abundance and pressureless on every TT scale over z 100
    to 3400, with margins of 1e9 or more.
  - Under those conditions F1A's cold fit applies unchanged (KA2). No new likelihood run was made.
- **The GL, GF and GFo engine runs on N3's background** (QX3 iter2's worst corner, as in CK4, CE2 and GL1). The footing
  enters through M(a), and the lensing statistic does not depend on the footing a priori.
- **S0 lines are order-of-magnitude** (Q7's v_c^2/c^2). They under-state |psi|/c^2, which favours the candidate. S0 is
  graded here, where Q7 only reported it; that tightens.
- **Capture uses QX3 G3's convention**: turnaround at z_c = 2, dust following the matter, Jeans line r_ta = 234 kpc.
  G1-G8 use KD1's model P at M_ta. M_ta is the lowest local mass, because M rises with density for DBI, so this is the
  generous reading.
- **Post-freeze fix (reported row only).** The first run graded RB's (ii) at z 1100 alone. That was a coding error: the
  frozen line is the minimum over z 3 to 1100. It was fixed and the run repeated. No member number changed, and RB's (ii)
  went from PASS to FAIL.
- **Worktree data.** The temporary worktree was given a symlink to the shared checkout's gitignored
  `real_research/data/lensing_rar/brouwer2021_rar` (the HY1/KR2 pattern). It is not committed.

## In plain words

The owner asked whether the action's own dust sector could be rescued by letting its mass scale run: heavy early, so it
stays cold for nucleosynthesis, the CMB and growth, and light today, so galaxies are left alone. The answer is that the
running works on the cosmic background. With the action's authors' own DBI form, the mass can rise from about 1 to 80 per
Mpc today to 631 by z 3 and to 1e13 or more at recombination. That gives:
- no stiff phase at nucleosynthesis;
- the CMB's cold amount (5.41 times the baryons);
- CMB lensing, fsigma8 and the Lyman-alpha forest, all passing.

But the mass in such a sector is set by the dust's own local density, not by the calendar. A galaxy's dust is about 150
times denser than today's cosmic mean, which is the density the whole universe had at z 4. There the growth requirement
itself forces the mass to be large. So the dust clumps on 3 kpc scales and is captured in every disc. That puts back
KD1's wall: SPARC is off by 0.78 dex against a line of 0.15. For most of the family the DBI square root also has no
solution in the Solar System or the Galaxy.

This holds for any K(Q), so the running-mass door inside the action family is closed. Clusters and the CMB remain
uncovered by the action.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

## Fix-forward note, 2026-11-08: KR2's window arrived after this file was written

KR2 sent its window after this file was written: result 05be295028, criteria 92c1ced823.

**KR2's reading.** The present-day window is **EMPTY on both footings**:
- X-COP (C2) is empty at every mu_K(0) in 0.1-79.43;
- groups [1.585, 3.98] and hosts [0.1, 0.631] are disjoint;
- partial windows: SPARC [0.1, 6.31] on canonical only (alt C1 is empty under KR2's frozen T = 0 clause), KiDS [0.1, 3.98].

**(iii) graded against it.** No member has a mu_K(0) inside an empty window, so (iii) is FAIL for every member on both
footings. D0 and D1 (1.232 / 1.265) sit inside the partial KiDS window, and inside the partial SPARC window on canonical only. D2 (10.45) and D3 (79.65) are outside
both.

**Brief kill.** Graded against KR2's window, it now **FIRES** on both footings: no member meets (i) + (ii) with mu_K(0) in
the window. The QX3 79.43 reading in the table above does not fire, and stays as frozen.

**Label.** Unchanged: FAIL / FAIL. GC blocked every member before this note. As KR2 also notes, the dust inside hosts
feels the local M (2173 at galaxy turnaround and more in denser cores), not mu_K(0). No graded number in this file moves.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
