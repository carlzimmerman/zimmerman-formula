# MK2 AMENDMENT A1 (before any graded number; committed alone)

Written after solver tests, before any row, gate or known answer was computed. The tests: one X-COP cluster (A1795,
canonical) and Hernquist-softened point masses at log M_b 10 and 11. No known answer and no gate was evaluated.

## 1. Galaxies need a finite central potential

With exponential dust a point baryon mass gives exp(beta/x) near the centre, so the dust inside any radius is infinite.
The criteria's galaxy rows (e, f, h) take ONE1's point mass. So:

- **The potential that sets the dust** is that of a Hernquist sphere of scale x_a = a/r_M = 0.2. Its baryon profile is
  M_b x^2/(x + x_a)^2, solved on the law with the dust and the cap, like the clusters.
- **The dust's effect is applied as a difference** so that with no dust every galaxy row equals ONE1 / QX8 exactly:
  - own halo: DeltaSigma = ONE1's capped point-mass DeltaSigma(X) + [DeltaSigma_Hern,dust - DeltaSigma_Hern,no dust];
  - neighbours: ONE1's phantom profile plus the same difference in dM/dx;
  - SPARC: the outer potential Phi(R_last) is the Hernquist state's at M_b(R_last), and the data field inside R_last is
    unchanged.
- **x_a = 0.2** is about a disc's half-mass radius over r_M for log M_b 10-11 (0.15-0.25). Reported, not graded: rows
  e and h at x_a = 0.1 and 0.4.
- Clusters and groups use their own extended baryon profiles, as frozen. The groups' two-point power law is replaced by
  M proportional to r^3 inside 0.1 R2500, so the centre is finite.

## 2. Which static state (the branch rule; the criteria said "continuous from no dust")

- Clusters and groups: continuation in decreasing c_s from 1e4 km/s, steps of 0.025 dex (the frozen grid).
- Galaxy tables: at each c_s, continuation in increasing mass from log M_b 6 (no dust) in steps of 0.05 dex. The two
  paths reach the same branch wherever neither folds.
- At each step the central potential is searched in [0.98, 1.6] times the previous one, and the root nearest it is
  taken.
- The no-dust start comes from a wide scan.
- No root means the branch has folded. Then there is no static capped state and the value FAILS (criteria).
  Tests showed such folds: A1795 near c_s 630 km/s; log M_b 11 near 120 km/s.

## 3. M-NOCAP's zero point

Without the cap the law's potential grows as s ln r and has no finite value at infinity. So "Phi -> 0 at infinity"
cannot be imposed. M-NOCAP sets Phi = 0 at 3 R200 (QX2's zero point) and integrates without the cap, with
self-gravity. The central potential is found by outward shooting so that Phi(3 R200) = 0.

## 4. Implementation only

Baryon profiles are tabulated on a log grid. The far-field potential uses a precomputed cumulative integral. Both are
for speed; no number changes.

No line, gate, grid or known answer changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
