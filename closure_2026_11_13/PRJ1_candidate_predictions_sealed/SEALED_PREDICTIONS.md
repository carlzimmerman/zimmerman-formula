# PRJ1: sealed predictions of the candidate sixth rule (the crossing-speed joint)

**These are predictions of a CANDIDATE rule that is NOT ADOPTED. Sealing them is not adoption. Nothing here says the
data favour the framework. kappa = 1/2 and the share 5.41 are FITTED.**

Sealed 2026-11-13. The seal is the commit that adds this file together with `SEAL.txt` (nothing else in that commit).
Every number below is printed by `prj1_numbers.py` in `prj1_numbers.out` (committed before the seal; 51 of 51 SI checks
against JNT2, SRJ2, FLD1, LNJ1, DSC1 and DSC1R stored values pass). Footings are canonical (a0 = 9.3603e-11 m/s^2) and alt
(1.1312e-10 m/s^2), written canonical / alt, never pooled; each footing is graded on its own. Cold dark energy is this
record's name for a gravitating field component; it is not a particle. This file edits no ledger, registry or
pre-registration.

A SURVIVES below is a hit, never a confirmation: it needs an independent blind re-grade before the record may count it,
and the rule stays NOT ADOPTED until the owner decides. A KILLED reading needs the same blind re-grade before it counts.
The two directions are treated the same way throughout.

## 0. The rule, the rivals, the shared definitions

**The candidate (CJ1's rule 6, JNT2 / JNT2R).** A system is ABOVE the switch when its baryon mass exceeds
log M_b*(z) = log[v*(z)^4 / (G a0)], v*(z) = a0 / (10 (1 + 5.41) H(z)) (flat, Omega_Lambda 0.6847, H0 67.4, a0 constant
in z). Above, it keeps its share as cold dust in the record's reference layout at every radius. Below, the law holds
inside R_set = f x R_fold (FLD1), the reference layout outside. Values (`prj1_numbers.out` section 1):

| z | 0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.3 | 2.5 | 3.0 | 4.0 | 4.5 | 5.0 | 6.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v*(z) canonical, km/s | 668.5 | 505.5 | 373.3 | 282.2 | 220.4 | 192.9 | 177.4 | 146.4 | 105.6 | 91.7 | 80.6 | 64.1 |
| v*(z) alt, km/s | 807.9 | 610.9 | 451.1 | 341.1 | 266.4 | 233.1 | 214.4 | 176.9 | 127.6 | 110.8 | 97.4 | 77.4 |
| log M_b* canonical | 13.206 | 12.721 | 12.194 | 11.708 | 11.279 | 11.047 | 10.901 | 10.567 | 10.000 | 9.755 | 9.531 | 9.133 |
| log M_b* alt | 13.453 | 12.967 | 12.441 | 11.955 | 11.526 | 11.293 | 11.148 | 10.814 | 10.247 | 10.002 | 9.778 | 9.379 |

**Rival R1: the split at FRZ1's constant v_stiff** (265.8 / 288.1 km/s; SRJ2's membership: FRZ1's v_vir of the record's
reference halo). In baryon mass its boundary barely moves: log M_b = 11.324 / 11.432 at z 0, 11.108 / 11.216 at z 1,
10.933 / 11.042 at z 2, 10.708 / 10.818 at z 4, 10.632 / 10.742 at z 5 (rebuilt here; equal to SRJ2's stored values to
5e-4). Above it, the reference; below it, the law inside f R_fold.
**Rival R2: the unsplit settled family.** The law inside f R_fold in every system; no switch.
**R0: a standard cold halo.** A halo in every system, smooth in mass, no law and no switch. Its amplitude in each cell
(an abundance-matched mass) is NOT computed here; where R0 is compared, only its shape and the absence of a step are used.

**The two boundaries cross.** The candidate's switch mass falls as -4 log E(z); R1's falls by about 0.7 dex from z 0 to
z 5. They cross at z = 2.564 (log M_b 10.856) canonical and z = 2.811 (10.936) alt. Below that redshift the candidate's
switch lies above R1's (by 1.09 / 1.23 dex at z 1); above it, below R1's (by 0.91 / 0.78 dex at z 4.5). This crossing is
what makes the candidate distinctive: it is the only one of the three that puts massive z ~ 1 discs on the law and
moderate z ~ 4.5 discs on the reference.

**The reference (A = 1).** The record's reference halo as DSC1R amendment A1 and SRJ2 / SRJ3 / LNJ1 build it: cold mass
X M_b laid out as an NFW profile to the turnaround radius, M_ta = X M_b h / (1 - f_b), X = 59.49 / 59.50 for z < 1 and
55.72 / 55.73 for z >= 1 (PD1's median share), FRZ1's concentration 10.14 (M / 2e12)^-0.081 (1 + z)^-1.01 and
turnaround overdensity. A is a free multiple of that halo. **The law** is g = [g_N + sqrt(g_N^2 + 4 g_N a0)] / 2 on the
disc's own Newtonian field.

**How far apart the law and the reference are (the size of every disc signal below).** For three of the six named model discs (thin
exponential discs; `prj1_numbers.out` section 5), V_c^2 / V_bar^2 under the law and under the reference at A = 1, the
difference d = log V_c(law) - log V_c(reference), and A_eq, the multiple of the reference that gives the law's g at that
radius:

| model disc | footing | radius | law | reference A = 1 | d (dex) | A_eq |
|---|---|---|---|---|---|---|
| cell A: z 2.3, log M_b 11.45, R_1/2 5 kpc | canonical | 3 / 4 / 5 R_1/2 | 1.335 / 1.542 / 1.772 | 1.592 / 2.014 / 2.531 | -0.038 / -0.058 / -0.078 | 0.566 / 0.534 / 0.504 |
| | alt | 3 / 4 / 5 R_1/2 | 1.390 / 1.622 / 1.879 | 1.592 / 2.015 / 2.532 | -0.030 / -0.047 / -0.065 | 0.658 / 0.613 / 0.574 |
| cell B: z 1.2, log M_b 11.5, R_1/2 6 kpc | canonical | 3 / 4 / 5 R_1/2 | 1.408 / 1.650 / 1.916 | 1.576 / 1.983 / 2.478 | -0.025 / -0.040 / -0.056 | 0.709 / 0.661 / 0.620 |
| | alt | 3 / 4 / 5 R_1/2 | 1.472 / 1.743 / 2.040 | 1.576 / 1.983 / 2.478 | -0.015 / -0.028 / -0.042 | 0.819 / 0.756 / 0.703 |
| cell C: z 4.5, log M_b 10.25, R_1/2 1.5 kpc | canonical | 3 / 4 / 5 R_1/2 | 1.443 / 1.701 / 1.983 | 1.661 / 2.132 / 2.709 | -0.031 / -0.049 / -0.068 | 0.670 / 0.619 / 0.576 |
| | alt | 3 / 4 / 5 R_1/2 | 1.511 / 1.800 / 2.115 | 1.661 / 2.132 / 2.709 | -0.021 / -0.037 / -0.054 | 0.773 / 0.707 / 0.652 |

So in every cell the reference at A = 1 is heavier than the law, by 0.015 to 0.08 dex in V_c at 3 to 5 R_1/2; the law
reads as a reference halo of 0.50 to 0.82 times the record's (and 0.96 at 2 R_1/2 for the alt z 0.9 model disc). At 2 R_1/2
the difference is 0.002 to 0.022 dex. Any test below separates the law from the reference only through this
amplitude-and-shape difference, which trades almost one for one with the baryon mass. That is why the minimum data
quality below is strict.

**Shared frozen machinery for P1 to P4.**
- *Qualifying disc (each one; otherwise it is left out and listed).* (a) A rotation curve whose outermost measured point
  lies at or beyond 4 R_1/2, with at least two independent resolution elements beyond 3 R_1/2. (b) Fitted by
  beam-forward modelling with the disc's own point-spread function and the points' covariance (an inner cut is not a
  substitute). (c) Gas mass from a measured tracer, with its conversion fixed before the kinematic fit and not taken from
  it; stellar mass from population synthesis with its stated error. (d) Inclination from independent morphology with its
  stated error. (e) The pressure (drift) correction as the data paper states it. (f) Not one of the seven curves DSC1 and
  DSC1R graded as digitised (COS4 01351, D3a 6397, GS4 43501, zC 406690, zC 400569, D3a 15504, zC-488879), not a SPARC
  galaxy, not an RC100 single point; new data on those same discs qualify.
- *Membership* by the model rule on each disc's independent central M_b and z, per footing. Discs within 0.15 dex of
  either boundary (the candidate's or R1's) are left out of every cell and listed.
- *Statistic.* Per disc and model, chi^2 with the disc's nuisances (M_b, inclination) profiled inside their independent
  priors and the full covariance. T = chi^2(law) - chi^2(reference, A = 1), summed over the cell's discs. A_fit = the
  free multiple of the reference (nuisances profiled), with its 95 % interval. s^2 = max(1, chi^2_min / dof) of the
  best layout, applied to every line (misfit inflation, as DSC1 and DSC1R did).
- *Power.* Build two noise-free mock sets on the cell's real radii, covariance and baryon models: one from the law, one
  from the reference at A = 1. Let T_L and T_R be T on each. The cell has power only if it has at least 5 qualifying discs
  and min(-T_L, T_R) >= 18 s^2 (twice the decision line). Otherwise the word is **NO POWER**. The power rule is
  applied first, in every prediction: a set without power reads NO POWER whatever its statistic.
- *Brackets, all run on both footings, on the candidate's reading and on each rival's reading, in both directions:*
  pressure term none / as published / doubled; M_b at -1 and +1 sigma of its independent prior; inclination at -1 and
  +1 sigma; the gas conversion at the low and high ends of its published range; membership by measured speed (v_meas
  against v*(z) and against v_stiff) in place of the model rule; reference concentration x 0.7 and x 1.4 (LNJ1's
  bracket); the z < 1 share in place of the z >= 1 share and the reverse; the covariance as supplied against a diagonal
  one inflated to two points per beam. A word that any bracket changes is written FRAGILE, naming the bracket. A FRAGILE
  KILLED and a FRAGILE SURVIVES are treated alike: neither counts until a blind re-grade reproduces it.
- *Dependence on f.*
  - *P1 to P3 do not depend on f.* This holds anywhere in the ungraded window [1.25, 2] and for any f >= 0.35.
    - In cells A and C the candidate is above the switch and gives the reference at every radius.
    - In cell B, R_set at f = 1.25 is at least 115 / 125 kpc (the cell's low-mass corner at z 1.7; FLD1). Outermost
      points sit at about 30 kpc at most; R_set reaches 30 kpc only at f = 0.33 / 0.30.
  - *P4 depends on f, on its law side.* Below the switch at z >= 4.5, R_set is only 3.9 to 12.9 kpc canonical (log M_b
    0.5 to 0.15 dex below M_b*, f = 1.25 to 2), and 1.5 to 3.4 kpc at z 6. That is comparable to the outer radii of
    compact discs. There the candidate gives the law inside R_set and the reference outside.
  - *The rivals' readings in cell C depend on f at z >= 4.5.* At the cell's high-mass corner R_set is 16.5 to 26.3 kpc
    at z 4.5 and 6.6 to 10.5 kpc at z 6 (canonical).
  - Every reading that depends on f is frozen as "the law inside f R_fold, the reference outside". It is computed at
    f = 1.25 and at f = 2, and a word that differs between the two is written FRAGILE (f).

## P1. Cell A: massive discs at z 1.8 to 2.6 above the switch carry the record's reference halo, not the law

**Statement.** Discs at 1.8 <= z <= 2.6 with log M_b >= log M_b*(z) + 0.15 follow baryons plus the record's reference
halo at A = 1 at every observed radius, with no law boost.

**Numbers.** Cell A lower edge in log M_b: 11.594 / 11.841 at z 1.8, 11.429 / 11.676 at z 2.0, 11.197 / 11.443 at z 2.3,
10.981 / 11.228 at z 2.6. Predicted A = 1 (the record's halo). At the model disc above, the law would read as A_eq 0.57
/ 0.66 at 3 R_1/2 and 0.53 / 0.61 at 4 R_1/2. Independent of f (section 0).

**Rivals and distinctiveness.** R1 also says the reference here (its boundary is 10.85 to 10.96 / 10.96 to 11.07,
below cell A). R2 says the law (A_eq about 0.5 to 0.66 inside 5 R_1/2). R0 says a halo of free amplitude. So P1
separates the candidate from R2 only. It is sealed because a law-like reading here kills the candidate while sparing R2,
and because the record's only on-disk hit for the candidate (DSC1, canonical) sits in this cell.

**Data.** Existing but insufficient: DSC1 and DSC1R on Genzel+2017's digitised curves. Of their three canonical
above-switch discs, zC 400569 and D3a 15504 are in cell A by its 0.15 dex margin and zC 406690 is not (margin +0.02); on alt none of the three is in the cell
(margins -0.23, +0.06, +0.07).
- DSC1 reads A = 0.670 [0.250, 1.175] canonical, "HOLDS, FRAGILE", and NO POWER on alt.
- The blind DSC1R reads A = 0.590 [-0.130, 1.580] / 0.120 [-0.585, 1.160], "NO POWER, FRAGILE" on both footings.
- Neither build confirms the other. Both canonical best values (0.67, 0.59) lie between 1 and the law's A_eq for the
  cell A model disc (0.59 at 2 R_1/2, 0.57 at 3 R_1/2), close to the law. The alt DSC1R value (0.12) lies below both.
- RC100 has one point per disc (SRJ3: NO POWER). ALPAKA's ring curves read NO POWER in ALP1 and ALP1R.
- CJ1's row 5 (RC100 coverage) FAILS ON COVERAGE ONLY. That is the coverage line, not data, and this test does not use it.
Expected: deeper resolved curves of massive z ~ 2 discs reaching at least 4 R_1/2 with measured gas profiles. Date not
known.

**Frozen lines (per footing; shared machinery of section 0).**
- **KILLED** if T <= -9 s^2 (the law beats the reference at A = 1), or if A_fit's 95 % interval excludes 1 on either side.
- **SURVIVES** (a hit awaiting a blind re-grade) if T >= +9 s^2 and A_fit's 95 % interval contains 1.
- **NO VERDICT** otherwise. **NO POWER** under section 0's power rule, or with fewer than 5 qualifying discs.

## P2. Cell B: massive discs at z 0.5 to 1.7 below the switch follow the law, not the reference

**Statement.** Discs at 0.5 <= z <= 1.7 whose baryon mass lies above R1's boundary and below the candidate's switch
(each with a 0.15 dex margin) follow the law at every observed radius.

**Numbers.** Cell B in log M_b:

| z | 0.5 | 0.8 | 1.0 | 1.2 | 1.5 | 1.7 |
|---|---|---|---|---|---|---|
| canonical | [11.342, 12.571] | [11.272, 12.252] | [11.258, 12.044] | [11.218, 11.843] | [11.163, 11.558] | [11.129, 11.380] |
| alt | [11.450, 12.817] | [11.380, 12.499] | [11.366, 12.291] | [11.326, 12.090] | [11.272, 11.805] | [11.238, 11.626] |

The predicted curve is the law. At the cell B model disc the law reads as A_eq 0.71 / 0.82 at 3 R_1/2 and 0.66 / 0.76 at
4 R_1/2 (d = -0.040 / -0.028 dex at 4 R_1/2). For the alt z 0.9 model disc A_eq is 0.81 at 4 R_1/2 and 0.96 at
2 R_1/2, so the alt footing needs the outer points most. Independent of f (R_set 193 to 309 kpc at the model disc).

**Rivals and distinctiveness.** R1 says the reference at A = 1 (every cell B disc is above v_stiff). R2 says the law,
the same as the candidate. R0 says a halo. So P2 separates the candidate from R1 and from a standard halo at the
record's amplitude. A standard halo with a free mass can mimic the law's amplitude at one radius, and only the shape
across 2 to 5 R_1/2 separates them: A_eq drifts with radius, for example 0.74 to 0.62 from 2 to 5 R_1/2 at the canonical
model disc.

**Data.** Existing but insufficient: of the seven on-disk curves only D3a 6397 (z 1.50, log M_b 11.36, canonical) falls
in cell B, and it reaches 1.26 R_1/2.
- The DSC1 / DSC1R "below" group (z 0.85 to 1.6) lies mostly below R1's boundary, so it is not this cell.
- On it, both builds prefer a free reference halo at A about 1.25 to 1.57 over the law. DSC1 reads "LAW FAILS BELOW,
  FRAGILE" and DSC1R "LAW HOLDS BELOW, FRAGILE". The words differ by the decision line, not the data (RECONCILE.md).
  That on-disk reading leans toward a halo, against this prediction, and decides nothing.
- KURVS (22) and NOEMA3D (10) curves are on disk, ungraded by any lane, and below v* (DSC1's inventory). They may hold
  cell B members. A testing lane must apply the quality rule. This seal precedes any
  grading of them.
Expected: deeper curves of massive discs at z 0.5 to 1.7. Date not known.

**Frozen lines (per footing).**
- **KILLED** if T >= +9 s^2 (the reference at A = 1 beats the law), or if chi^2(law) - chi^2(free A) >= 9 s^2 (a free
  halo beats the law; the analogue of DSC1R's L - min(N, H) line).
- **SURVIVES** (a hit awaiting a blind re-grade) if T <= -9 s^2 and chi^2(law) - chi^2(free A) < 9 s^2.
- **NO VERDICT** otherwise. **NO POWER** as in section 0.

## P3. Cell C: moderate discs at z 3.5 to 6 above the switch carry the reference halo, not the law

**Statement.** Discs at 3.5 <= z <= 6 whose baryon mass lies above the candidate's switch and below R1's boundary (each
with a 0.15 dex margin) follow baryons plus the record's reference halo at A = 1, with no law boost.

**Numbers.** Cell C in log M_b:

| z | 3.5 | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 |
|---|---|---|---|---|---|---|
| canonical | [10.419, 10.604] | [10.150, 10.558] | [9.905, 10.518] | [9.681, 10.482] | [9.474, 10.449] | [9.283, 10.419] |
| alt | [10.666, 10.713] | [10.397, 10.668] | [10.152, 10.628] | [9.928, 10.592] | [9.721, 10.559] | [9.529, 10.529] |

The cell is nearly empty at z 3.5 on alt (0.05 dex wide). Predicted A = 1. At the cell C model disc the law would read
as A_eq 0.67 / 0.77 at 3 R_1/2 and 0.62 / 0.71 at 4 R_1/2 (d = -0.049 / -0.037 dex at 4 R_1/2). Independent of f.

**Rivals and distinctiveness.** R1 says the law here (below v_stiff, inside f R_fold; f-dependent at z >= 4.5, see
section 0). R2 says the law. R0 says a halo. **This is the one cell where the candidate differs from both rivals.**

**Data.** No lane has graded any disc in this cell.
- CRISTAL (14 curves at z 4.4 to 5.7) is on disk, but its baryons are kinematic fits (DSC1). It fails quality rule (c)
  and cannot be the test.
- ALPAKA's discs at z 2.2 to 3.6 read NO POWER (ALP1, ALP1R) and lie mostly below this redshift range.
Expected: resolved curves at z 3.5 to 6 with independent stellar and gas masses. Date not known.

**Frozen lines (per footing).** As P1: **KILLED** if T <= -9 s^2 or if A_fit's 95 % interval excludes 1; **SURVIVES**
(a hit awaiting a blind re-grade) if T >= +9 s^2 and the interval contains 1; **NO VERDICT** otherwise; **NO POWER** as in
section 0.

## P4. Where the switch sits at z 3.5 to 6: on log M_b*(z), not at v_stiff and not absent

**Statement.** Among qualifying discs at 3.5 <= z <= 6 (all masses, no cell cut), the discs are reference-like above
log M_b*(z) and law-like below it, so the fitted offset of the switch from log M_b*(z) is zero.

**Numbers.** Fit one offset delta: disc i takes the reference at A = 1 if log M_b,i > log M_b*(z_i) + delta, and
otherwise the law inside f R_fold with the reference outside.
- Candidate: delta = 0.
- R1 corresponds to delta_v(z) = log M_b(v_stiff) - log M_b*(z): +0.485 / +0.347 at z 3.5, +0.708 / +0.571 at 4.0,
  +0.913 / +0.776 at 4.5, +1.100 / +0.964 at 5.0, +1.274 / +1.138 at 5.5 and +1.436 / +1.300 at 6.0.
- R2 corresponds to delta = +infinity (no disc on the reference).
- R0 corresponds to delta = -infinity (no disc on the law).

**Dependence on f.** P4 depends on f, on its law side. At z >= 4.5 the law side's R_set is 3.9 to 12.9 / 4.7 to
15.6 kpc for f 1.25 to 2 and log M_b 0.5 to 0.15 dex below M_b*. At z 6 it is 1.5 to 4.2 kpc. So P4 is run at
f = 1.25 and at f = 2:
- a word that differs between the two is FRAGILE (f);
- at z near 6 the law side is mostly reference beyond a few kpc, so the delta = 0 and delta = -infinity readings converge
  there, and the power rule decides whether those discs can count.

**Rivals and distinctiveness.** Distinct from all three, provided the fit can exclude delta_v at the sample's median
redshift.

**Data.** As P3. No lane has run any part of it.

**Frozen lines (per footing).** Scan delta over [-2, +2] in steps of 0.01 together with the two no-step models (all law,
all reference). The profile is chi^2(delta) = sum_i chi^2_i (layout assigned by delta), with each disc's nuisances
profiled. The 95 % interval is where chi^2(delta) - min <= 3.84 s^2.
- **KILLED** if the interval excludes 0. That includes the case where either no-step model is the best fit and beats
  delta = 0 by more than 3.84 s^2.
- **SURVIVES** (a hit awaiting a blind re-grade) if the interval contains 0, excludes delta_v at the median redshift of
  the qualifying discs, and both no-step models are worse than the best delta by at least 9 s^2.
- **NO VERDICT** otherwise.
- **NO POWER** if fewer than 5 qualifying discs lie in [log M_b* - 0.5, log M_b*] or fewer than 5 in [log M_b*,
  log M_b* + 0.5], or if on noise-free mocks built at delta = 0 on the real radii and covariance the 95 % interval does
  not exclude delta_v at the median redshift.

**What a low-redshift slice would need.** The same fit at z 0.5 to 1.7 tests the other side of the crossing (R1's
delta_v is -1.09 / -1.23 at z 1). It needs qualifying discs at log M_b 11.7 to 12.6, near the candidate's switch, and
there are very few such discs. It is not sealed as a separate prediction.

## Not sealed: kill-only conditions, pointers and dropped statements

These are recorded so a reader sees what the rule says. None is in the sealed list above, because none separates the
candidate from its rivals, or because it is already registered, or because its outcome may already be public.

- **The forest at flux level (kill only; NOT DISTINCTIVE).**
  - *What the rule says.* With f in [1.25, 2], the split's forest passes the flux-level gate (Delta chi^2 <= 4). Haloes
    above the switch are pure reference: switch M200c 5.72e11 / 1.01e12 Msun/h at z 2.2, 2.93e11 / 5.17e11 at 2.6,
    1.59e11 / 2.81e11 at 3.0, 2.74e10 / 4.84e10 at 4.4.
  - *First test.* FRZ6 (running; its FROZEN_CRITERIA.md governs, cases S at f = 1.25 and 2; this lane read nothing of
    FRZ6 but that file).
  - *What would kill the stated window on a footing.* "FOREST ROW FAILS AT FLUX LEVEL" for case S at both f = 1.25 and
    f = 2, as FRZ6's frozen lines define it, and, like every kill in this file, only after an independent blind
    re-grade. A fail at f = 2 only would narrow the window. The
    window's lower edge rests on G4, which SRH1R found cannot see f, so such a fail kills the stated window, not every f.
  - *Why not distinctive.* A FRZ6 hold is not distinctive: FRZ6's own hand estimate expects case S close to the unsplit
    family, and the split at v_stiff switches at a nearly constant 1e12. FRZ6's outcome is not known to this lane.
- **Strong lenses: already registered as EUC1-F (EUC1 RESULT section 8, frozen 2026-11-12); not re-registered.**
  - The candidate puts 26 / 0 of 6,173 Euclid lenses above v*(z), all at z_l 1.09 to 1.72 (LNJ1).
  - Inside R_E the reference at the cosmic share gives about what the law gives (LNJ1: -0.018 dex). At the record's
    PD1 share it adds about 0.1 dex more (LNJ1). The membership (26 / 0) does not depend on the share.
  - So the candidate's lens prediction is the law's. A "LENS GATE FAILS" on EUC1-F (lower bound of b_med >= 0.25)
    kills the candidate exactly as it kills the law, and rule 6 offers no rescue on its own membership.
  - Today EUC16 grades EUC1-F at N(P) = 11: +0.405 [+0.137, +0.589] / +0.385 [+0.121, +0.574], NO VERDICT / NO VERDICT,
    with the centre on the failing side of the 0.25 line.
  - Switch masses at the lenses: log M_b* 12.551 / 12.797 at z_l 0.66.
  - The wide-lens ceiling break is not the switch (1 / 0 of 316 wide lenses above; LNJ1 "NO POWER, FRAGILE /
    NO POWER"). The rule then requires group baryons along the sightline that no lane has counted. Not quantified here.
- **Groups and poor clusters at z ~ 0 (dropped: NOT DISTINCTIVE).**
  - Today's switch is at v200 668.5 / 807.9 km/s, M200c 1.03e14 / 1.82e14 Msun (log 14.013 / 14.260), log M_b 13.206 /
    13.453.
  - The settled layout keeps the reference's enclosed cold mass at R_set (FZS1's junction). The candidate therefore
    differs from the reference only in shape inside R_set, which is 1,235 to 1,977 kpc for log M_b 13.0 at z 0.
  - JNT2 reports at most 7.3e-02 / 7.7e-02 between the joint and the reference on any cluster or group statistic, at
    every f. JNT2R reads groups at R500 NO POWER. DPR1 row 9 finds the share to turnaround NOT DISTINCTIVE, and GO2's
    error is 0.9 to 1.8 against a gate of 0.20.
  - No lane has computed the shape difference between R500 and turnaround. A lane that does may reopen this.
- **Wide binaries and the Solar System: EQUAL THE LAW; registered in DR4MAP (Gaia DR4 due 2026-12-02).** The frozen
  Gaia pre-registration is untouched. Rule 6 adds nothing there.
- **Massive local spirals, z < 0.5 (not sealed: the outcome may already be public).**
  - The candidate says the law up to log M_b 12.7 to 13.2 / 13.0 to 13.5. R1 says the reference above log M_b 11.2 to
    11.3 / 11.3 to 11.4.
  - JNT1R already reads 9 / 2 massive SPARC spirals: the law fits, fragile (canonical), and alt has no power.
  - Published analyses of local massive spirals exist that the record has not read, so a seal here could be a
    post-diction.

**Not predicted by the rules.**
- The width of the switch: the candidate switches sharply, and nothing derives a width. Discs within 0.15 dex of a
  boundary are left out for that reason, not because a width is predicted.
- The value of f inside [1.25, 2].
- The amplitude of a standard cold halo in each cell.
- What happens exactly at the switch.

## Ledger status

Nothing here is entered in any ledger or registry. If the owner adopts rule 6, the one line to add to the main ledger is
given in the lane's hand-back (it names this file, the seal commit and the sha256 in `SEAL.txt`).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
