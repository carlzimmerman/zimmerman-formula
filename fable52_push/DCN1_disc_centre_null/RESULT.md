# DCN1 RESULT: is the static clock ill-posed at a disc's centre null?

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. kappa = 1/2 FITTED; not theory closed.
- Footings: canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10), reported separately and never pooled.
- The component is cold dark energy, never a particle.
- Criteria d603f1703c. Six amendments, all post hoc, each committed alone: A1 0a6e46fb52, A2 15f6f993e4, A3 f5e101ba9a,
  A4 d08610695e, A5 00d6869022, A6 830aeed427. **A5 and A6 were written after the outcome was seen** (disclosures below).

## Label (per footing): **ARTEFACT / ARTEFACT** (A6, the last of six readings)

**Every reading frozen before the outcome was seen is NO VERDICT, each on a known-answer gate.** A6 is the only reading in
which every known answer passes.

| Reading | Known answers | P1 external-field null (canonical / alt) | P2 isolated centre (canonical / alt) | **Lane (canonical / alt)** |
|---|---|---|---|---|
| frozen | KA4 fails (null-cell value 0.78 of exact); KA3 fails (test grid) | ARTEFACT / ILL-POSED (1 of 8: a negative Q creeping 0.5 % per level, see below) | STABLE AT THE CENTRE / STABLE AT THE CENTRE | NO VERDICT / NO VERDICT |
| A1 | KA3 fails | as frozen | as frozen | NO VERDICT / NO VERDICT |
| A3 as written | KA3 fails; KA4 (P2 geometry) fails on the rule's p <= 6 window only | NO VERDICT / NO VERDICT (5 / 3 of 8 open) | NO VERDICT / NO VERDICT (2 of 4 open) | NO VERDICT / NO VERDICT |
| A5 (post hoc) | KA3 fails | ARTEFACT / ARTEFACT (8 / 8 stable) | STABLE AT THE CENTRE / STABLE AT THE CENTRE (4 / 4) | NO VERDICT / NO VERDICT |
| **A6 (post hoc, last)** | **all pass** | **ARTEFACT / ARTEFACT** (8 / 8 stable) | **STABLE AT THE CENTRE / STABLE AT THE CENTRE** (4 / 4) | **ARTEFACT / ARTEFACT** |

The labels are read off the outputs by dcn1_labels.py (dcn1_labels.out / .json).

**What does not depend on the reading:** on every one of the 24 resolved local solves, at all five resolutions:
- every cell has D.P > 0: no negative phantom density, so no growing cell (SCS3 Lean growth_sign: Gamma^2 > 0 iff D.P < 0);
- every route-L rate is negative, i.e. the clock oscillates and does not grow;
- the profile near the null is the deep-law one (|D.P| ~ s^-0.5, u ~ s^+0.5);
- the rate is bounded at the null, as Part A proves it must be.

The readings differ only on whether the rule certifies the magnitude of the least-negative rate, and on how strict the
known-answer gate is.

## What it means for SCS1 and SCS2's STABLE

- **SCS1 (point mass): untouched.** A point mass has no null: |grad Phi| goes to infinity at the centre.
- **SCS2 (isolated discs): STABLE extends to the centre** for these disc models, on both footings.
  - At a smooth disc's centre (the thick disc, four masses) the resolved D.P is positive everywhere. Its minimum is
    0.80-0.90 rho_0, and it diverges as s^-1/2 toward the centre.
  - The clock there oscillates at a rate of 1.03-1.10 x sqrt(4 pi G rho_0), the baryons' own Jeans-type rate.
  - The masked region of SCS2 / SCS3 (r < 0.002-0.010 R_d) holds no instability.
  - The razor-thin and Kuzmin discs have no off-plane null at the centre. The negative cells that appear next to r_min when
    the mask is removed move with r_min (1e-4 -> 1e-6 R_d) and shrink with resolution. They are an inner-boundary artefact.
- **SCS3's open item (the thick twin's centre null in an external field) is closed as an artefact.**
  - SCS3's RATE UNBOUNDED sits on the global grid's axis cells: 0-12 theta cells from the axis at R4-R6.
  - There u = 0.18-0.59 and D.P = -0.75e10 to -6.5e10 Msun/kpc^3 (-13 to -115 rho_0), deepening with refinement. The
    resolved field never exceeds u = 0.25 anywhere in a box of half-size 5-6 pc around the null.
  - Resolved on a local grid 7-13 times finer, the same place has D.P >= +2.6 rho_0.
  - The external-field discs' STABLE stays excluded by SCS3's halo instability (slow, r >~ 0.75 r_e). This lane changes
    nothing about that.

## The answer in plain words

A null of the field inside baryons does not make the static clock ill-posed. The growth rate there is bounded by an
identity, and on every resolved disc its sign is decay.

- **Why it cannot blow up (Part A, sympy-exact; Lean for the algebra).**
  - On any background of the law, route L's rate is exactly

        Gamma_loc^2 = (2 + u) [ u Phi_nn/(1 + u) - 4 pi G rho_b ],   u Phi_nn = n . grad(|grad Phi|^2) / (2 a0).

  - At a null inside baryons the law goes deep-MOND (the 3-Laplacian): |grad Phi| ~ s^(1/2), D.P ~ s^(-1/2).
  - So D.P diverges, but u Phi_nn is homogeneous of degree 0 and stays finite: u -> 0 cancels D.P's divergence.
  - The slab and the uniform sphere give -4 pi G rho and -(5/3) 4 pi G rho at the null: decay.
  - Growth at a null would need u Phi_nn > 4 pi G rho_b, i.e. D.P < 0 there. No resolved disc has it.
- **The stiffness and the blend cannot change this.** The adopted Pi^6 blend equals the raw switch, identically zero, wherever
  D.P < 0. So where growth could occur the symbol is the gamma_L = 0 one, bounded in k. Where D.P > 0 the stiffness adds
  +k^2 and is stabilising.
- **What SCS3 saw.** Its global spherical grid puts the null on the axis, a few cells from the axis wedge. Those axis cells
  carry a D.P of the wrong sign (-13 to -115 rho_0) that deepens with refinement. A uniform
  cylindrical grid around the null, 7-13 times finer, with the same law, the same face rule and the global solution as
  Dirichlet data, has no negative cell at any resolution.
- **A side finding: the frozen thick deposit.** It puts the thin-disc mass inside r_min (12.6 Msun at log M_b 9.4, about
  2700 times the thick disc's own 0.0046 Msun) at the centre as a point mass. That spurious mass hid the isolated centre
  behind a point-mass field. Variant C removes it, and the centre is still stable once resolved (P2).

## Per background (A6 / A5 label; finest local grid N_R 243)

- **Q_A** is the maximum of Gamma_loc^2 over the annulus L/8-L/2, in units of 4 pi G rho_0 (negative = oscillation).
- **Inner shell** is the innermost graded shell (s >= 8h) on the finest two grids.
- **Null in box** is where g_z changes sign on the axis inside the analysis region (dcn1_nullcheck.out).

| Problem | Footing | log M_b | g_e / a0 | L (pc) | null in box | Q_A / 4piGrho_0 | inner shell / 4piGrho_0 | min D.P / rho_0 | D.P < 0 cells | label |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | canonical | 9.4 | 0.1 | 5.26 | yes (0.099 L) | -0.96 | -0.95, -0.94 | 2.66 | 0 | stable |
| P1 | canonical | 9.4 | 0.01 | 0.52 | yes (0.154 L) | -0.18 | -1.01, -1.01 | 8.38 | 0 | stable |
| P1 | canonical | 10.45 | 0.1 | 1.60 | yes | -0.49 | -0.13, -0.41 | 2.68 | 0 | stable |
| P1 | canonical | 10.45 | 0.01 | 0.83 | no (null < 1e-3 R_d) | -1.11 | -1.12, -1.12 | 1.66 | 0 | stable |
| P1 | canonical | 10.7 | 0.1 | 1.36 | yes | -0.53 | -0.65, -0.46 | 2.67 | 0 | stable |
| P1 | canonical | 10.7 | 0.01 | 0.94 | no | -1.12 | -1.13, -1.13 | 1.33 | 0 | stable |
| P1 | canonical | 10.9 | 0.1 | 1.19 | yes | -0.82 | -0.21, -0.77 | 2.76 | 0 | stable |
| P1 | canonical | 10.9 | 0.01 | 1.10 | no | -1.13 | -1.15, -1.15 | 1.11 | 0 | stable |
| P1 | alt | 9.4 | 0.1 | 6.01 | yes (0.031 L) | -0.91 | -0.30, -0.85 | 2.92 | 0 | stable |
| P1 | alt | 9.4 | 0.01 | 0.56 | yes | -0.29 | -0.49, -0.23 | 9.83 | 0 | stable |
| P1 | alt | 10.45 | 0.1 | 2.00 | yes | -0.37 | -0.25, -0.20 | 2.60 | 0 | stable |
| P1 | alt | 10.45 | 0.01 | 0.81 | no | -1.09 | -1.11, -1.11 | 1.92 | 0 | stable |
| P1 | alt | 10.7 | 0.1 | 1.63 | yes | -1.00 | -1.00, -0.99 | 2.76 | 0 | stable |
| P1 | alt | 10.7 | 0.01 | 0.92 | no | -1.11 | -1.12, -1.12 | 1.54 | 0 | stable |
| P1 | alt | 10.9 | 0.1 | 1.42 | yes | -0.65 | -0.64, -0.59 | 2.69 | 0 | stable |
| P1 | alt | 10.9 | 0.01 | 1.08 | no | -1.12 | -1.13, -1.13 | 1.28 | 0 | stable |
| P2 | canonical | 9.4 / 10.45 / 10.7 / 10.9 | 0 | 47.4 / 14.1 / 11.8 / 10.6 | corner | -1.10 / -1.06 / -1.05 / -1.05 | -1.07 / -1.04 / -1.04 / -1.04 | 0.89 / 0.82 / 0.81 / 0.80 | 0 | stable (4) |
| P2 | alt | 9.4 / 10.45 / 10.7 / 10.9 | 0 | 57.3 / 17.0 / 14.2 / 12.8 | corner | -1.10 / -1.06 / -1.06 / -1.05 | -1.07 / -1.04 / -1.04 / -1.04 | 0.90 / 0.82 / 0.81 / 0.80 | 0 | stable (4) |

Notes on the table:
- **The six P1 boxes with no null in them** are at 0.01 a0 and log M_b 10.45-10.9. There the null sits closer to the
  centre than the frozen search window's 1e-3 R_d, so the box (from the window's edge) holds no null. Their stable label
  is a region near the centre, not the null.
- **The null itself at 0.01 a0** lies within about 1e-3 R_d of the centre, where P2's centre limit applies. Both 9.4
  boxes at 0.01 a0 do contain their null.
- **The free-fall time** 1/sqrt(4 pi G rho_0) is 5.6 / 3.05 / 2.79 / 2.65 Myr for log M_b 9.4 / 10.45 / 10.7 / 10.9.
- **The least-negative P1 rates** sit near the null on the flank. They come within 0.13-0.5 of marginal but never cross
  zero (no D.P < 0 cell).

## Part A, known answers, MUTATE, Lean

| Item | Result |
|---|---|
| A1 identity (sympy; random cubics) | algebra difference 0; cubics 0 relative. PASS |
| A2 null limit | slab -1, sphere -5/3 (units of 4 pi G rho); D.P sqrt(s) finite; blow-up u Phi_nn degree 0. PASS |
| A3 stiffness / blend | k -> infinity at F'' = 0: G (1 - Km)/m (bounded); with stiffness and D.P > 0: + infinity; blend C4 onto 0. PASS |
| KA1 SCS3's flagged rows R4-R6 | 6 rows reproduced, relative 0. PASS |
| KA2 SCS2's isolated R1 rows | 32 rows, relative 0; D.P > 0 in every masked-in cell. PASS |
| KA3 the rule | on h = 1.5^-i from 1: FAIL (9 of 12 converge; the p = 0.75 ones' E > 20 %); on the lane's h = 1/N_R (A6): PASS (12 of 12, 2.4e-15; h^-1, h^-0.5 diverging; 1 + h^0.3 not converged) |
| KA4 uniform sphere (exact) | Q at the null cell -> -4.13e-29 vs exact -5.33e-29 (frozen FAIL; A1 PASS); Q_A on the annulus within 1.3e-4 / 1.2e-4 of exact (A3: P1 geometry PASS, P2 geometry FAIL on p = 6.41 > 6; A6 PASS) |
| KA5 manufactured saddle (D.P < 0, exact) | 1.7889e-30 vs 1.7904e-30 (8e-4). PASS in every reading |
| M1 tilt flipped | every stable label turns unstable. BITES |
| M2 planted s^-1 D.P (A3) | unbounded on all 24 backgrounds. BITES |
| M3 identity without 1/(1+u) | sympy BITES (cubics 1.6 relative); numerical half on the KA4 sphere does NOT bite (2.1 % < 5 %: u <= 0.10 there) |
| M4 Lean twin | 6 false versions, 6 errors, exit 1. BITES |
| Lean DCN1.lean | 6 theorems (rate_identity, slab_null, sphere_null, slab_null_neg, sphere_null_neg, raw_switch_zero), exit 0, axioms propext / Classical.choice / Quot.sound only |
| SCS3's global sequence | Gamma_L^2 R3-R6 canonical 1.35e-33, 6.41e-28, 1.33e-27, 5.62e-27: growing (as SCS3) |
| Reported: r_min 1e-6 R_d | every negative cell's inner edge follows r_min (thick variant C: shells 1-2 only; thin discs: from r_min out to <= 1e-3 R_d, shrinking with resolution); frozen thick deposits: 0 negative cells |

## Disclosures

- **A1** (after KA4's first run). KA4 failed. A1 put that down to the null cell's resolution-independent operator error, and
  added a factor-2 bracket and Q_8. The error is real (exact Phi through the operator: 0.45 x 4 pi G rho for s < 2h), but
  most of that first failure was A2's bug.
- **A2** (after KA5's first run). A sign slip in solve(): the Dirichlet term entered as src - radd, so the solve imposed
  -Phi_b. diagnostics() was right. KA4 and KA5 were rerun; KA5 then passed as frozen.
- **A3** (after the corrected KA4 and KA5). The graded rate moved to a fixed annulus (Q_A), and boundedness at the null to
  inward shell maxima; M2 became a planted s^-1 D.P. No P1 / P2 number had been seen.
- **A4** (after the first, invalid P1 / P2 runs).
  - The Picard residual was normalised by ||rhs||, which the potential's constant offset dominates. The solves stopped
    near the interpolated initial guess, whose D.P carries the global grid's kinks, and P1 came out erratic: Q_A positive
    at 1-25 Myr on 4 of 6 backgrounds.
  - Fixed: residual over ||src||, a gauge shift, at least 10 iterations, and an update test. A clamp fixed P2's crash.
  - The invalid runs are kept in the scratchpad, quoted only in A4, and not graded.
- **A5** (after seeing every P1 / P2 output). Restores the frozen criteria's own "no D.P < 0 cell on the finest two"
  clause, which A3's rewrite had dropped. It is post hoc on the outcome.
- **A6** (after seeing the first label output). KA3's test grid becomes the lane's own; exact known answers pass on direct
  agreement on the finest two grids. It is post hoc on the outcome.
- **Code fix to the frozen text.** The frozen unbounded(b) needs Part A to fail or Q_id to diverge too, and the first label
  pass tested only that Q diverges. After the fix, the frozen reading still shows one "unbounded": alt 10.7 / 0.1 a0. There
  Q (negative, -1.294 to -1.273e-28) creeps toward zero by 0.4-0.6 % per level, and Q_id creeps with it. That is a decay
  rate settling, not growth, but the frozen text calls it unbounded. That reading is NO VERDICT anyway (KA4 fails).
- **The null search window.** The frozen window (1e-3 to 0.3 R_d) misses the 0.01 a0 nulls of the heavier discs; see the
  table notes.
- **M3's numerical half does not bite.** Stated as it is.
- **Resources.** Every solve under 2 GB (global R6: 1.86 GB peak). Caches are in the scratchpad. Nothing was downloaded.
  At most two heavy processes at once.

## What was not graded

- **Discs other than these models.** Real centres with a cusp or a central black hole have no null (|grad Phi| does not go
  to 0) and are not covered here; neither are bars or non-axisymmetric centres.
- **Non-axisymmetric perturbations of the background, and the nonlinear outcome.** Route L is the local WKB symbol.
- **The stiffness's own term where D.P > 0.** That is the hand form (+k^2, stabilising), not solved.
- **The collapse (COL1) and the cosmological background.** As before.

## Files

- Criteria and amendments: FROZEN_CRITERIA.md, AMENDMENT_A1.md to AMENDMENT_A6.md.
- Part A: dcn1_symbol.py -> dcn1_symbol.json / .out.
- Globals: scs2_aqual.py (SCS3's copy, unchanged); dcn1_global.py -> dcn1_global_{KA1_R4, KA1_R5, KA1_R6, KA2, BC, P2G,
  P2R}.json / .out.
- Local solves: dcn1_local.py -> dcn1_local_{KA4, KA5, P1, P2}.json / .out.
- Null check (reported): dcn1_nullcheck.py -> dcn1_nullcheck.json / .out.
- Labels: dcn1_labels.py -> dcn1_labels.json / .out.
- Lean: DCN1.lean, DCN1_MUTATE.lean, compile.txt, compile_MUTATE.txt (built in fable_independent_2026/lean_2026, not left
  there).

Main script for a re-run: from this folder, with DCN1_CACHE set to a scratch directory, run in order:
- `DCN1_MODE=BC python3 dcn1_global.py`
- `DCN1_LSET=KA4 python3 dcn1_local.py`
- `DCN1_LSET=KA5 python3 dcn1_local.py`
- `DCN1_LSET=P1 python3 dcn1_local.py`
- `DCN1_LSET=P2 python3 dcn1_local.py`
- `python3 dcn1_labels.py`

The KA1 / KA2 / P2G / P2R modes are optional checks.

Commit ids, local / origin: criteria d603f1703c / -, A1 0a6e46fb52 / -, A2 15f6f993e4 / -, A3 f5e101ba9a / -,
A4 d08610695e / -, A5 00d6869022 / -, A6 830aeed427 / -, result (this commit) / - (origin ids recorded in the next commit).

Not registered. Does not edit fable52_push/README.md, CLOSURE.md, SCS1 / SCS2 / SCS3's files, the register, the decision
files or any paper.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
