# ONE1 pre-freeze note: the cold component counted once (2026-11-09, written before any ONE1 criteria)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered. This is not a result and carries no label. It records
(1) the reading ONE1 will grade, (2) what was looked at before the criteria exist, and (3) one prediction for lane KO2,
committed before KO2 has any lensing number on disk.

## 1. The reading

The a0 law is not a second force added to gravity. It is the gravity of the cold component itself. Each galaxy holds one
share of the cold component, and inside the galaxy that share is arranged as the law's own "phantom" halo. Where the share
runs out, the halo ends and the field falls as a point mass. Nothing is counted twice and nothing has to be cleared.

Why this reading and no other (each line is a verdict already in the record):

1. The CMB needs a cold clustering component of about 5.4 times the baryons (F1). Clusters need 4.18 M_b and the cosmic
   amount delivers 4.11. The Bullet's lensing peaks sit on the galaxies.
2. The law plus that component, both acting in discs, fails the rotation curves (route E's wall, 2026-11-01).
3. Removing the component from galaxies fails on every route: kicks, heating, conversion, and every action-based switch
   (SWT1, EMV1, GAL1, KO1, SNP1, and HE1's static construction, all 2026-11-09).
4. Hiding it from baryons where the law acts fails its consistency gate.
5. What is left is counting it once. The record graded two forms of that (PD1, PD2). Their fails are amounts (KiDS's
   outer points, groups, the Bullet subcluster's mass), not structure.

## 2. What was looked at before any criteria (disclosure)

`one1_prefreeze_look.py` -> `one1_prefreeze_look.out`. Post hoc. It reads no shear: only KO1's pair weights, the law's
cells and KO1's published per-bin amplitudes. No neighbours are modelled.

Model: enclosed mass M(x) / M_b = nu(1 / x^2) for x = r / r_M below x_t, where nu = 1 + X, and constant 1 + X beyond;
projected exactly. Checks: the untruncated profile is the isothermal form to 1.3 % and 0.2 % at x = 50 and 300; the far
field equals the point-mass form to 3e-4; KO1's host-free samples are rebuilt at their published sizes.

Shape ratio R_s = outer bins / inner bins, host-free lenses, canonical (alt in brackets). X = 59.5 is PD1's own share
(the dust inside the turnaround shell's Lagrangian sphere), not fitted here.

| Veto radius | Measured (KO1) | Halo ends at X = 59.5 | Halo ends at X = 80 | Law as its own field (no end) |
|---|---|---|---|---|
| 1.0 R_h | 0.607 +- 0.094 | 0.510 (+1.0 sigma) [0.464, +1.5] | 0.685 (-0.8) [0.623, -0.2] | 1 (-4.2) [-4.2] |
| 1.3 R_h | 0.714 +- 0.116 | 0.515 (+1.7) [0.468, +2.1] | 0.691 (+0.2) [0.629, +0.7] | 1 (-2.5) [-2.5] |
| 1.6 R_h | 0.811 +- 0.134 | 0.525 (+2.1) [0.477, +2.5] | 0.704 (+0.8) [0.641, +1.3] | 1 (-1.4) [-1.4] |

(sigma = (measured - model) / error.) KO1's E8 puts the neighbours' term near 0.01 of the law at a share of 5.56; scaled
to 59.5 it is about 0.1, which would move the X = 59.5 column up by about that much. That scaling is a hand estimate.

Read plainly:

- PD1's first failing gate (KiDS, graded on B21's pooled points) does not fail on KO1's host-free lenses with PD1's own
  share: 1 to 2.5 sigma low without neighbours.
- The law continuing as the lens's own field is further from the host-free bins at two of three veto radii.
- KiDS still does not separate the two at the widest veto (2.1 against 1.4 sigma), and the veto's edge effect biases
  the narrower ones. Nothing here is a verdict.
- **By type it does not close.** Late types sit below the X = 59.5 model (outer -0.19 +- 0.39 against about 0.8) and
  early types above it (1.34 +- 0.18 against about 0.94). One share for both types does not fit both.

## 3. A prediction for KO2, made blind

KO2 (`closure_2026_11_09/KO2_kids_own_field_by_type/`, criteria 59e3c9ee9a, another session) models every neighbour and
fits each type's own extended amplitude, R_ext. When this note was committed its folder held the criteria, two amendments,
the script and one failed kernel check; no lensing number.

- If the cold component is counted once and a disc's halo ends at its share, **R_ext for late types is below the law's
  floor: at most about 0.5. KO2's label for late types is ABSENT or REDUCED (or no power), not PRESENT.**
- If the law is the lens's own field with no end, R_ext is 1 and the label is PRESENT.
- So late types PRESENT in KO2 falsifies this reading for discs. Early types are not predicted here (section 2 shows they
  carry more outer signal than one share gives).

Hand estimate behind the number: with the inner amplitude fixed at 1, a halo ending at x_t = 60 leaves an extended
amplitude of 0.32 at the inner edge of KO2's outer band, 0.14 at its middle and 0.07 at its outer edge; X = 80 gives
0.69, 0.29 and 0.15.

## 4. What ONE1 has to grade (for its criteria, not decided here)

Every gate in one table, for one stated share rule fixed before any number: SPARC, KiDS (host-free shape, neighbours
modelled, by type), X-COP, groups, the Bullet (offset and amount), Coma's diffuse galaxies, the CMB, growth and CMB
lensing, the Solar System and wide binaries (Newtonian in this reading: there is no second force to screen), and the
filling line (not applicable if nothing is added on top). And one row that is not a gate: the reading has no derivation.
PD1 (P7) already records that the halo's profile needs an assumed relation, the component's dispersion locked to
sigma^2 = (1/2) sqrt(G M_b a0). No action in the record produces it.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
