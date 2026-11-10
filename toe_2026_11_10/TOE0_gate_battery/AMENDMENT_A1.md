# TOE0 AMENDMENT A1 (post hoc, committed alone after the criteria 8a99cb7c34 and before any script or number)

Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What the frozen text gets wrong.** TOE0-P, P2 grades c_X n_X(c_X) on "exact Fermi-Dirac and Bose-Einstein number
densities (massless and massive, m/T in {0, 1, 5}, mu/T over [-0.5, 0.5] on a fixed 41-point grid)". A Bose-Einstein gas
needs |mu| <= m: for m = 0 and mu != 0 one of the two occupation numbers has a pole on the integration range, so the
number density does not exist. On the frozen grid that row (bosons, m/T = 0) has 40 undefined points out of 41. Read
literally they are neither "c_X n_X >= 0" nor "< 0", so the frozen reading of P2 is UNDECIDED whatever the other rows say.
This was written before any number; it is a slip in the grid, found while writing the script.

**Amendment.** P2 is graded on the rows where the density exists: Fermi-Dirac at m/T = 0, 1, 5 and Bose-Einstein at
m/T = 1, 5 (all |mu|/T <= 0.5 < m/T there), 41 points each, 205 points in all. The Bose-Einstein m/T = 0 row is reported
as undefined, point by point, and not graded. The labels DRAINS / CREATES / UNDECIDED and the TOE0-P label rule are
unchanged.

**Reporting order.** RESULT.md gives the frozen reading first (expected UNDECIDED, from the undefined row) and the
amended reading second, both from the same script run.

**One limit added to the report, not to the grade.** P2's sign statement is for an asymmetry that starts at zero (or,
more generally, any start with c_X n_init <= c_X n_eq). A plasma that starts with more asymmetry than equilibrium, of the
same sign as c_X, relaxes back and returns charge to the clock. RESULT.md states what that would require; it does not
change P2's grade, which the frozen text defines from zero.
