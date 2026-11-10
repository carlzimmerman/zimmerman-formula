# MK1 AMENDMENT A1 (before any graded number; committed alone)

Written after a solver test of the capped profile (no row, gate or known answer had been computed; nothing graded exists).
The criteria (b1fbded1e2) say the capped state is found "self-consistently (shooting on the potential's central offset)"
and that a missing state FAILS the row. They do not say which state to take when several exist. The test showed that
they can.

**What the test showed.** For a point mass with X = 59.486, the shooting function (dust at the centre, as a function of
the cap radius x_c) has one root for m = mu_K r_M below about 0.024. Above that, extra roots appear near the dust-free cap
radius x_t (m x_t above about 1.4). On those extra roots the potential oscillates inside the cap. The root that continues
from m = 0 keeps phi < 0 and a positive, rising dust mass everywhere. Its cap radius shrinks smoothly (x_c = 57.5, 31.5,
9.8, 1.6 at m = 1e-3, 1e-2, 0.1, 1). Here m x_c tends to about 1.55, so the whole share ends up in a dust core of radius
about pi/(2 mu_K). With the dust's sign flipped (MUTATE M-SIGN), the continuous root ends at m of about 1.3e-3. The
shooting already uses the inward form (start at x_c, where the law fixes the dust, and require zero dust at the centre).
That is the same condition as shooting on the central offset; only the shooting variable differs.

**Rule (frozen now).**
1. The capped state used everywhere is the branch continuous from m = 0. It is followed by continuation in ascending m,
   with steps of at most 0.05 dex. At each step the root is searched in [0.5, 1] times the previous x_c (in [1, 2] times
   for M-SIGN).
2. Where the continuation finds no root, the branch has folded. There is no capped state there, and per the criteria that
   value FAILS the row for that lens set (and for every larger m).
3. The other roots are counted and reported at the row grids, never used.
4. On the branch, phi < 0 everywhere and the dust mass is monotone. Both are checked and printed for every table entry;
   a violation is reported.

No line, gate, grid or known answer changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
