# COL1 AMENDMENT A1 (post hoc; committed alone, before any graded run)

**What changes.** The node layout of section 4/5 of FROZEN_CRITERIA.md. Frozen: "nodes log-spaced" from X_in to X_out with
node 0 at the centre, so the gap [0, X_in] is a single linear element at every resolution. A1: the same J log-spaced nodes
plus linear nodes inside X_in at the log spacing found there (spacing X_in * dln, dln = ln(X_out/X_in)/(J - 1); about 200
extra nodes at J = 1200 and 400 at J = 2400), so the centre refines with J. Nothing else changes: same J labels (1200 /
2400 log nodes), same X_in, X_out, events, labels, reads, MUTATE.

**Why, and what was seen first (post hoc).**
- KA4 (static law state, mu_K 0.1 and 3.71) failed its first run: residual |dv/dt|/g = 0.19 at both resolutions. A probe
  located it at the first node only (0.192 there; 1e-6 to 2e-5 at every other node). The central ball [0, 0.5 kpc] is one
  element with a linear h, which cannot carry the softened core's profile, and log spacing never refines it. KA6 and KA5
  failed for the same reason (shells crossed at the first node within 1-2 Myr; no oscillation to measure).
- KA3's first run failed on a bug in the known answer itself: its n = 1 polytrope mass profile carried a misplaced factor
  (sin x/mu^2 - r cos x/mu instead of sin x - x cos x). Fixed in col1_ka.py; not a criteria change. Disclosed here.
- Before any known answer ran, two development probes of the primary row (mu_K 3.71, log M_b 10.45, canonical, J 1200 and
  2400, the frozen layout) were made to time the solver and fix the h solve's Newton tolerance (round-off floor; solved in
  u = h - hbar). They ended in E1 at 0.1315 / 0.1314 Gyr after z_i at r = 0.062 / 0.051 kpc. They are not graded and are
  kept outside the repo; the graded runs are made after the known answers pass, with A1's layout.
- The development probes also showed the explicit step resolving the law's flux-cap wall (X14's r_w = sqrt(G m/a0)) only
  with a step floor far below 1e-9 of the time unit; the driver uses 1e-20 and calls a stop below it STALL (numerical, not a
  frozen event; a STALL row is NO VERDICT).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
