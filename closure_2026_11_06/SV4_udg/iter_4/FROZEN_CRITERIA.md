# SV4 iter_4: Malin 1's inner bulge/bar mass model and the HI vs stellar distance (FROZEN)

Shared rules: ../FROZEN_CRITERIA.md. Committed before any script or number.

Baseline = QX4's Malin 1 density: gas and LSB as NNLS annuli (A2: inside the plotted range; A1 reported beside),
Gaussian h = 1 kpc; the HSB component as a sphere with M(<r) = V_HSB^2 r / G (Lelli+2010 DecoHL, M/L_R 3.3).
KA0 reproduces QX4 iter1.json Malin1_A2 V_exact.

## Variants (declared corners)

1. HSB geometry (bulge vs inner disc): G-s sphere (QX4 baseline) and G-d thin disc, the HSB curve inverted to
   Sigma_HSB by QX4's NNLS annuli (A2 edges), Gaussian h = 0.3 kpc; K4-type check: thin ring-sum V of the inverted
   Sigma vs the plotted HSB curve at the Table radii, 3 % line (a miss tags G-d).
2. HSB mass-to-light: s = M/L / 3.3 in {1, 3.7/3.3 (the paper's MOND fit), 5/3.3 (the paper's stated upper bound
   "cannot be higher than 5")} = in errors; s = 0.5 GENEROUS (UD2's end; no published lower bound).
3. Stellar vs HI distance: stars (HSB and LSB) placed at D_* = f D, gas at D. At fixed angular profiles:
   Sigma_*'(R) = Sigma_*(R/f) (disc), M_*'(<r) = f^2 M_*(<r/f) (sphere). f in {1, (1+z)^-2, (1+z)^2}, z = 0.0826
   (Malin 1's redshift, from memory, provisional): the full D_A vs D_L mix-up, the largest distance-convention
   mismatch between the HI and optical analyses. In errors (it brackets any convention error).
4. Bar (non-axisymmetric, analytic bound): a bar of mass <= M_HSB and half-length a <= 10 kpc (declared generous;
   no bar length is on disk, and the 12.5 kpc ring is the innermost graded point) changes V^2 at R by at most
   |dV^2/V^2| <= (M_bar/M_enc(R)) (a/R)^2 / 2 (quadrupole over monopole). Graded by lowering the exact-field
   V_model by that bound at every ring (the favourable direction).

Grid: every combination of 1 x 2 x 3 (2 x 4 x 3 = 24) on A2, both footings; item 4 on the baseline and on the best
in-errors corner. A1 at the baseline and the best corner, reported. Labels per the shared rule; the best corner is
reported whatever it is. This is an error envelope over published values, not a fit: no continuous parameter is
optimised.

MUTATE: the wrong-direction corner (G-s, s = 5/3.3, f = (1+z)^2, bar term raising V) must give chi2 above the
baseline exact-field chi2 on both footings.

## Not graded here

AGC 114905 has no bulge or bar in its published model (UD1: poly-exponential stars, 6 % of the baryons) and a
single published distance: item n/a for it.
