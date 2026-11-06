# QX12 iter_3 Amendment A1, before any graded iter_3 number

Kappa = 1/2 FITTED; not theory closed. Written after ungraded smoke tests of the solver. Their outputs were not
saved and no file under this lane holds a graded number. Lines, gates and the c_min rule are unchanged.

## What the smoke tests showed

1. **The sea must not gravitate.** The uniform cosmic sea is the background; only the excess over it is a local
   source (as in KiDS, which measures excess surface density). The solver now sources g with M_X - (4 pi/3)
   rho_sea r^3 and reports that excess everywhere.
2. **Singular host centres make the Boltzmann profile collapse.** It is exponentially sensitive to the central depth.
   Two hosts the criteria inherited from QX10 have an infinite central depth:
   - KiDS point masses: GM/r diverges.
   - QX10's inner extrapolation M ∝ r^max(s0, 0.5): the depth diverges for s0 <= 1.
   With those hosts, at c_s0 = 2000 km/s the whole capped mass (4.2 M_b) collapses inside 1 pc of a point-mass lens.
   That is an artefact of the host model, not physics: the n = 1 polytrope that QX10 graded is not exponentially
   sensitive.

## Fix (frozen now)

- KiDS hosts become sphericalised exponential discs (QX10's expdisc) with R_opt = 3.2 r_d. r_d comes from a
  log-log least-squares fit of SPARC's own Rdisk against M_b = 0.5 L[3.6] + 1.33 M_HI (Q <= 2, inc >= 30), so it
  is non-cluster data already on disk.
- X-COP and group hosts: below the innermost data point, M(r) = M_1 (r/r_1)^3 (a uniform core, finite central
  depth). Reported variant: M ∝ r^max(s0, 1.2).
- The label holds only if the main and variant hosts agree on PASS/FAIL. If they disagree, it is NO VERDICT (host
  sensitive).
