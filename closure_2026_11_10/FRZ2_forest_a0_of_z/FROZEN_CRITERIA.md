# FRZ2 FROZEN CRITERIA: the forest row with a0 allowed to change with z

Committed alone, before any FRZ2 script or number. TEST lane. Footings canonical / alt graded separately, never pooled.
Cold dark energy is a gravitating field component; no particle is added.

## Question
FRZ1 (criteria 1835d8fb7d) fails the forest with a0 constant in physical units: Delta chi^2 9916.2 / 9008.7. Its MZ3
(a0 unscaled in comoving units) flips the sign. For which a0(z) does the forest gate pass, and does any a0(z) the
framework offers get there?

## Method
FRZ1's `frz1_hm.py` and `frz1_forest.py` copied; one change: a factor f(z) = a0_phys(z) / a0_phys(0) multiplies a0
wherever FRZ1 applies a0 / (1+z)^2. Only FRZ1's primary layout (reading L), both footings, all 12 DESI bins.

## Cases (frozen)
- P0, P0.5, P1, P1.5, P2: f = (1+z)^n, n = 0, 0.5, 1, 1.5, 2.
- D-Pan, D-DES5, D-Uni: f = sqrt(F(z)), F = (1+z)^(3(1+w0+wa)) exp(-3 wa z/(1+z)); (w0, wa) = (-0.838, -0.62),
  (-0.752, -0.86), (-0.667, -1.09).
- Q-Pan, Q-DES5, Q-Uni: f = sqrt(w(z) F(z) / w0), w(z) = w0 + wa z/(1+z), same sets.
- H: f = H(z)/H0 = sqrt(Om (1+z)^3 + 1 - Om) with the Om of frz1_hm.py (CFG556's library).

## Gate and labels
Per case and footing: PASSES if Delta chi^2 <= 4 (FRZ1's forest gate unchanged), else FAILS.
Lane: "NO FRAMEWORK a0(z) PASSES" if every D, Q and H case fails on both footings; "A FRAMEWORK a0(z) PASSES" if any
of them passes on both (not a pass for the theory; needs an independent re-grade); NO VERDICT if a known answer fails.
A D/Q/H case passing on one footing only is reported as such and does not make the second label.

## Known answers
- KA-P0: P0 reproduces FRZ1's primary R_cold (frz1_hm.json) at every z and k to 1e-10 relative, and Delta chi^2
  9916.2 / 9008.7 to 0.1.
- KA-P2: P2 reproduces FRZ1's MZ3 change of R_cold(k 3, z 3), +0.502 canonical, to 0.01 (P2 minus P0).
## Mutation (must bite)
- MZ1: frz1_forest.py's 3 keV warm cutoff arm, run on this lane's copy (FRZ1's arm as written): Delta chi^2 > 4.

## Reported, not graded
The power-law n (of the five) with the smallest Delta chi^2 per footing, and whether it is under the gate.
Hand estimate before any number: at z 3, D cases give f ~0.75-0.8 (worse than P0), Q cases ~0.95-1.0 (about P0),
H gives f ~4.5 ~ (1+z)^1.1, near where MZ3's sign flip should cross; a pass needs the crossing to land within the
gate's narrow window at all 12 bins at once, so I expect every case to fail.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
