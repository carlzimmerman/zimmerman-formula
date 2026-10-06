# CFG357 — FROZEN CRITERIA: does the chassis's heat filter suppress the EFE solar-system quadrupole Q2 (Cassini)?

Frozen before any script in this lane was written or run.

## Question
p58 (`sonnet55_push/puzzle_32pi/p58_cassini_kappa_bound.py`) finds, for plain QUMOND with nu = sqrt(1+1/y)
(simple kernel) and the Galactic field 2.146e-10 m/s^2, Q2(kappa = 1/2) = 2.195e-26 s^-2, against Cassini
(Hees+ 2014) Q2 = (3 +- 3)e-27 s^-2: about +6.3 sigma. The published version of this tension is
Desmond, Hees & Famaey 2024, MNRAS 530, 1781 (cited from abstract-level knowledge only; PROVISIONAL).
Does the chassis (L340, filtered C-H/K) evade it through its heat filter?

## The filter (reused, not re-invented)
- Definition: MASTER_LAGRANGIAN.md, W_b = S U, S = exp((xi^2/2) Delta) (heat slice, b = xi^2/2); the MOND
  kernel acts on the filtered field grad W_b; the Newtonian part of the Sun is unfiltered.
- Implementation reused exactly: L340 S1 (`real_research/g03_audit_2026/L340_filtered_khronon_completion.py`,
  `phantom()`): the Sun's mass is a Gaussian of width wd = xi (M_enc = M[erf(r/(sqrt2 xi)) - sqrt(2/pi)(r/xi)
  exp(-r^2/2xi^2)], with its small-r series); the phantom is built from G_f = g_sun,filtered + g_Ne.
- In p58's solver this is the single substitution G -> G_f in D = (nu(|G|/a0) - 1) G - (nu_e - 1) g_Ne.
  Q2 is then computed by p58's own multipole formula (Q2 = -3/5 Int s_2 r^-1 dr).
- Kernel nu_mono reimplemented exactly from L340 lines 104-118 (RAR below y_p, floor 0.05 h_p/(y + y_p)).

## Configuration
- kappa = 1/2 on both footings: a0 = 9.3603e-11 (canonical) and 1.13e-10 (alt). External field 2.146e-10 m/s^2
  (p58's value; held fixed as the observed field, nu_e solved as in p58). Sun = point mass (then filtered).
- xi grid (declared, reported in full; no fitting): 0.030 (declared floor), 0.031, 0.033 (L340 S1 Q2 floors),
  0.045, 0.049 (Saturn-monopole floors), 0.07, 0.10, 0.15 (g03x carried-kernel floors), 0.3, 1, 3 pc,
  plus 1e-6, 1e-4, 1e-3, 0.01 pc to show the approach to the unfiltered limit.
- The decision window is [0.030, 0.15] pc: the record's declared floor to the largest committed xi floor.
  Larger xi is reported as context only (the record has no committed upper edge; galaxies need xi << kpc,
  wide binaries at 2-30 kAU lose the MOND boost once xi exceeds ~0.1 pc, f29's knee 15-20 kAU).

## Decision (sigma = (Q2 - 3e-27)/3e-27; pass at 2 sigma means |sigma| <= 2)
- **kappa = 1/2 SURVIVES CASSINI:** filtered Q2 within 2 sigma for the whole decision window on both footings.
- **CONDITIONAL:** within 2 sigma for only part of the window (on either footing); the passing xi range is stated.
- **FAILS:** outside 2 sigma across the whole window on either footing.
- Also reported: 3 sigma ranges; whether Q2(xi) is steep enough near the floor to pin xi (a NEW constraint is
  claimed only if the 2-sigma crossing lies inside the window and is resolved by the grid).

## Controls (load-bearing)
- C1 filter off (xi -> 0 / no filter), simple nu, canonical: Q2 = 2.195e-26 to 1% (p58).
- C2 no external field: |Q2| < 1e-3 of the field-on value.
- C3 filtered at xi = 1e-6 pc equals the unfiltered nu_mono Q2 to 1%.
- C4 grid convergence: Q2 at the window floor changes < 2% when Nr and Nmu are raised.
- MUTATE (CFG357_MUTATE=1; separate outputs *_MUTATE.*): external field at 10%; Q2 must differ from the main run
  (unfiltered and at the floor), so the C1 identity check FAILS and rc = 1.
- Cross-check (informative): at the floor the filtered Q2 should be near L340 S1's ceiling 5.2e-27, which S1 used
  to define the floor (different field 2.32e-10 and quadrature; agreement within a factor 2 expected, not required).

## Lean
Rational interval bounds on filtered Q2 at the window edges vs the 2-sigma bound 9e-27 (and the 3-sigma 1.2e-26),
Lean 4 + Mathlib, no sorry. The Lean certifies the arithmetic of the inequalities on the computed numbers,
not the PDE solution.

## Scope
kappa = 1/2 fixed (fitted). No knob scans beyond the declared xi grid. No downloads. Bare static QUMOND-type
response with the L340 filter; the khronon sector is not included in Q2 (L340: it renormalises G by ~1e-9).
