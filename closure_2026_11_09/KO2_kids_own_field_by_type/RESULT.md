# KO2 RESULT (criteria 59e3c9ee9a; amendments A1 e5fca3518f, A2 014cef99b8, A3 ece364d804, A4 e84e2c9328)

**KO2: NO VERDICT for late types and NO VERDICT for early types, on both footings (canonical / alt).**

- **Why NO VERDICT.** One known answer (KA-3b) failed. A3/A4's diagnostic traces the failure to one cross-shear amplitude
  (the giant class's ext, +3.11 sigma among 15), not to the planted model.
- **Without KA-3b the label would still be NOT SEPARATED for both types** under the frozen bracket rule. Late types read
  ABSENT in the primary and PRESENT with the amplitudes untied. Early types read REDUCED in the primary and ABSENT with the far
  band closed at zero.
- **One MUTATE twin (M3) did not bite.** The reason is below: the statistic measures the shape of the outer profile, not its
  level.

**The type split HE1 needs (no extended own field for discs, one for early types) is not supported by any reading.** Tied, both
types sit low and do not differ: early minus late is +0.21 +- 0.19. Untied, late types sit at the law's level and early types
below it.

Commit ids: local 59e3c9ee9a (criteria), e5fca3518f (A1), 014cef99b8 (A2), ece364d804 (A3), e84e2c9328 (A4), 3e740c9e64
(result); on origin a1032f8e00, 6e89e08366, e43eac361f, 047c3ec669, d67f49a934, 9b23ffab26. A4 reached origin first (d67f49a934):
another session's lane push carried it before this lane pushed. So origin lists A4 before the criteria. The local history and
the author dates (criteria 20:54, A1 21:07, A2 21:11, A3 21:34, A4 21:51) keep the true order.

TEST lane, quarantined. Adopts nothing, relabels nothing, not registered. Footings never pooled. kappa = 1/2 FITTED; not theory
closed. A1 to A4 are post hoc and say so. A3 was committed before any fitted amplitude was opened. A4 and everything after
section 1 is reported, not gated.

## 1. The frozen statistic and labels

All 181,477 lenses. Every catalogued neighbour (888,795 pool objects, 12.8 million pairs inside reach at 230 Mpc, 71 per lens)
is modelled with the law's banded profile off-centre, with five shuffles subtracted. The ratio statistic is identical on both
footings to three decimals; only the floor and form B differ.

| reading (R = weighted a[beyond inner window] / a[inner]) | late | early |
|---|---|---|
| **primary (tied lens = neighbour amplitudes)** | 0.277 +- 0.183 -> ABSENT | 0.487 +- 0.071 -> REDUCED |
| B1 window 115 Mpc | 0.571 +- 0.179 -> ABSENT | 0.565 +- 0.076 -> REDUCED |
| B2 far band closed at zero | 0.229 +- 0.154 -> ABSENT | 0.393 +- 0.064 -> **ABSENT** |
| B3 untied (own amplitudes separate from neighbours') | **1.071 +- 0.199 -> PRESENT** | 0.739 +- 0.115 -> REDUCED |
| secondary (the brief's a[outer] / a[inner]) | 0.207 +- 0.278 -> ABSENT | 0.263 +- 0.111 -> ABSENT |
| law's floor (own-only fit to the law at mass factors 0.5-8) | 0.9999 | 0.9999 |
| **frozen label** | **NO VERDICT** (KA-3b); brackets alone: NOT SEPARATED (B3) | **NO VERDICT** (KA-3b); brackets alone: NOT SEPARATED (B2) |

Errors are s_tot = sqrt(s_jk^2 + 0.05^2). Early minus late (primary): +0.210 +- 0.194 (1.1 sigma). The neighbours carry
0.205 +- 0.011 of the model in bins 0-6.

## 2. Checks

- **Known answers: 12 of 13 pass.**
  - KA-0a/b: lenses in the pool with equal mass and type; per-lens sums reproduce `cfg96_stack` to 6e-14.
  - KA-1a: KO1's host-free scan gives 40,667 and KO1's host-free window amplitudes are reproduced exactly. KA-1b: the own bands
    sum to KO1's law cells to 5e-16. KA-1c: coverage complete.
  - KA-2a-d: the kernels against E8's closed form (1e-15), against direct quadrature (largest error 8.7e-4 of a band's maximum),
    against a uniform sheet (within 1.6 Monte Carlo errors of zero), and in the concentric limit.
  - KA-3a: 2,000 planted neighbours, tree equal to brute force to 1e-19, 29,495 lenses reached, 2,080 by more than one class.
  - KA-4: halvings, z spread 0.802 late and 0.956 early. Null: cross-shear inner and ext within 1.3 sigma.
  - **KA-3b FAILS**: largest pull 3.11 in all four plants. The plants are recovered as planted plus the cross-shear fit, so
    KA-3b tested 15 cross-shear amplitudes at 3 sigma each. **D1**: the 3.11 is the giant class's ext amplitude, a
    neighbour-only class; 2 of 15 exceed 2 sigma and 1 exceeds 3. The plants' ratios and labels came out as designed:
    law everywhere -> PRESENT / PRESENT, late truncated -> ABSENT (0.085 +- 0.130) / PRESENT.
- **MUTATE** (`ko2_MUTATE.out`):
  - M1 (type labels permuted): bites, but has no power, because the true difference is itself 1.1 sigma.
  - M2 (neighbour positions shuffled): bites. The neighbour share falls from 0.205 +- 0.011 to 0.001 +- 0.005.
  - **M3 (late WG x 0.4 in bins 0-6) does not bite** on the primary design (+0.013 +- 0.075), nor on the secondary or untied
    designs (**D2**).
  - Post hoc, beyond A4 (`ko2_m3_breakdown.out`): under M3 the late ext amplitude falls (0.27 -> 0.16 tied, 1.36 -> 0.65
    untied) **and so does the inner amplitude** (0.96 -> 0.56, 1.27 -> 0.59). The inner band is weighed mostly by its enclosed
    mass in those same bins. So R measures **the shape** of the profile in bins 0-6 (law-like extended against point-like
    enclosed), not its level. A uniform scaling cannot move it. M3 as frozen was the wrong twin for a ratio.
- **The model-only runs failed twice before any shear was read** (A1, A2: two known-answer definitions were wrong, and the
  kernel tables were refined). The first full run was stopped at 67 % of the pass for holding 2.4 GB. It now re-launches with
  macOS's `MallocMediumZone=0 MallocLargeCache=0`, peak 1.24 GB.

## 3. Form B's prediction (A3, declared before the result was opened)

Form B is PD1's rule, copied: share 59.49 / 59.50 M_b; for uncapped galaxies the phantom is truncated at
g_t = 2.60e-14 / 3.14e-14 m/s^2. That is R_trunc 287, 565, 483 and 658 kpc at the median late-low, late-high, early-low and
early-high lens (canonical). Every lens and neighbour follows the rule; the planted sums were fitted exactly as the data.

| | late | early |
|---|---|---|
| primary: measured | 0.277 +- 0.183 | 0.487 +- 0.071 |
| primary: law (floor 0.9999) | 3.96 s_tot above the measurement | 7.26 above |
| primary: form B 0.038 / 0.007 (canonical / alt) | 1.31 / 1.48 s_tot below | 6.40 / 6.89 below |
| primary: form B planted with the cross-shear as noise | 0.155 +- 0.188 | 0.062 +- 0.127 |
| secondary R_own: measured / law / form B | 0.207 +- 0.278 / 2.85 above / 0.020: 0.67 below | 0.263 +- 0.111 / 6.64 above / 0.037: 2.03 below |
| untied B3: measured | 1.071 +- 0.199 | 0.739 +- 0.115 |
| untied B3: law / form B (canonical) | 0.36 below / 0.181: 4.46 below | 2.28 above / 0.197: 4.73 below |
| untied B3: form B planted with the cross-shear as noise | **1.030 +- 0.282** | 0.127 +- 0.224 |

Distances are in s_tot; alt is within 0.5 of canonical everywhere. The two predictions sit 3.5 to 14 s_tot apart in every
design, so **noiselessly** the data could tell them apart.

- **Early types: neither.** In every design the measurement sits between them: 2.3 to 7.3 s_tot below the law's own-field
  level, and 1.9 to 6.9 above form B. It is above the noisy form-B plant by 2.9 sigma (primary) and 2.4 sigma (untied), with
  both errors combined.
- **Late types: cannot tell.** Tied, the measurement is consistent with form B (1.3 s_tot) and 4.0 below the law. Untied, it
  is consistent with the law (0.4 s_tot). But form B planted with the measured cross-shear as its noise reads 1.03 +- 0.28 in
  the untied design: the noise realisation alone lifts it by 0.85 to the data's value. **For late types the data cannot tell
  the law from form B.**

## 4. Reported items (canonical; alt identical in R)

- **D3, where the ext information comes from (tied design).** Own / neighbour / cross shares: late-low 0.16 / 0.84,
  late-high 0.35 / 0.64, early-low 0.13 / 0.84, early-high 0.23 / 0.72, giant 0 / 1. In the tied design a class's "own"
  amplitude is weighed mostly by that class acting as **neighbours** of other lenses (475,464 late pool objects, many of them
  near hosts). That is why tied and untied disagree for late types.
- **R1, amplitudes (centre / inner / ext, tied):**
  - late-low 1.14 / 0.93 / 0.47; late-high 0.97 / 0.99 / 0.09;
  - early-low 1.25 / 1.67 / 0.84; early-high 1.41 / 1.72 / 0.82; giant 0.71 / 2.04 / 0.70.
  - R_mid = a[middle] / a[inner] (secondary): late 0.42 +- 0.20, early 0.55 +- 0.06.
- **R3, redshift halves:** late 0.32 +- 0.32 (low z) and 0.02 +- 0.18 (high z); early 0.38 +- 0.07 and 0.62 +- 0.08. Early's
  high minus low is +0.24 +- 0.11 (2.3 sigma): **flagged**, unseen neighbours in the own term (flux limit).
- **R4:** without bin 3, 0.27 / 0.49; without bin 0, 0.26 / 0.59.
- **R6, KO1's host-free lenses, neighbours modelled:** late -0.03 +- 0.28, early 0.57 +- 0.10. The KO1 lead reappears in that
  subset only.
- **R7, KO1-style plain stacks of all lenses:**
  - late: outer 1.23 +- 0.14, middle 1.17 +- 0.17, inner 1.33 +- 0.10, R_s 0.93 +- 0.13;
  - early: 1.99 / 2.22 / 1.82, R_s 1.09 +- 0.08.
  - Both are flat: the full sample shows none of the host-free late deficit.
- **Ties:** no pool object sits on a mass threshold (late 10.49265, early 10.73435); 77 and 58 lie within 1e-4 dex. 429 objects
  with u - r exactly 2.0 are late, by the record's rule. No untyped objects, so that bracket was not needed.

## 5. What it means for the type split (a reading; relabels nothing)

1. **The KO1 lead does not generalise.** All 181,477 lenses stacked plainly give flat profiles for both types. Modelling the
   neighbours does not produce "late absent, early present" in any design. The host-free late deficit survives only inside the
   host-free subset, which carries the veto edge.
2. **What a disc's own outer field is depends on one modelling choice the data cannot make**: whether a disc's profile as a
   lens equals its profile as a neighbour. Tied, discs look truncated, like form B. Untied, they look like the law. The tied
   value is mostly late galaxies as neighbours (D3). The untied value is matched by form B plus the cross-shear noise
   realisation. Neither reading gives a late-type label that survives.
3. **Early types are the firmer result.** Every reading puts their outer profile shape below the law's own-field level and
   above PD1's truncated phantom. The flag in R3 says part of what they do show may be unseen neighbours, which would push them
   lower still.
4. **For HE1:** the evidence for its type split was the KO1 lead. On the full sample it is not there: not as a frozen label,
   and not as a reading.

## 6. Limits

- The ratio is a **shape** statistic (M3, section 2). It cancels the stellar-mass calibration, but it cannot see a uniform
  change of the outer level.
- Neighbours are placed at the lens's distance with the lens's critical density. Photo-z chance projections are removed in
  the mean only. The reach is R_h + 2 Mpc.
- The catalogue is flux-limited (R3 flag). Unmodelled gas at Mpc radii is not in the model (B21's hot-gas variant, KO1 R6).
- Satellite truncation is not modelled. The untied bracket is the only handle on it, and it decides the late reading.
- Form B uses PD1's convention, 4 G DeltaSigma = G M(<R) / R^2, the same convention in which the law is written here. Each
  neighbour's unresolved centre is a point, as in the law's columns. Two form-B kernel attempts failed their checks before the
  final run (`ko2_formB_attempts_fail.out`): the centre was first resolved, unlike the law's columns, and then tabulated.

## 7. Hand estimates against outcome

- The brief: late error near 0.2. Right for the primary (0.18); 0.28 for its own R_own. Late low (0 to 0.4): right only in the
  tied design. Early 0.7 to 1.0: wrong in the tied design (0.49), right untied (0.74).
- Mine: late 0.3 to 0.8 and early 0.8 to 1.1, labels late NOT SEPARATED and early PRESENT. The late label was right in effect;
  the early one was wrong.
- A3's form-B estimate (0.1 to 0.4) was a little high: 0.0 to 0.04 tied, 0.13 to 0.20 untied.

## Files

FROZEN_CRITERIA.md, AMENDMENT_A1-A4.md, ko2_design_toy.py (pre-freeze, model only), ko2.py -> ko2.json / ko2.out /
ko2_MUTATE.json / ko2_MUTATE.out, ko2_run0_kernels_fail.out (the first model-only run), ko2_formB.py -> ko2_formB.json /
ko2_formB.out (A3 prediction and the A4 diagnostics D1-D4), ko2_formB_attempts_fail.out, ko2_m3_breakdown.py -> .out (post hoc,
beyond A4).

One thread. Main run 524 s, peak 1.24 GB; form B 499 s, peak 0.86 GB. The shear catalogue was not read. Caches (kernel tables,
per-lens neighbour columns) stayed in the session scratchpad.

Not registered. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
