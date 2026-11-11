# AKS1 AMENDMENT A1 (post hoc; committed alone, before any A1 row or graded number)

Frozen criteria: local 5b35674191. This amendment changes the method in two places, for the two method failures listed
below. Every line, gate, label and known-answer map of FROZEN_CRITERIA.md is unchanged. Adopts nothing. kappa = 1/2
FITTED; not theory closed.

## What was seen before A1 (disclosed)

- Symbolic part (`aks1_sym.py`): KA1, KA2, H1-H4 all PASS (as committed later; nothing in A1 touches them).
- Known answers run under the frozen integrator: KA3 Bertschinger PASS (slope -2.274, line -2.25 +- 0.15); KA4 PASS (all
  eight focusing times within 5.1e-4 of COL1); KA9 PASS (r_e* within 1.3 % of CFG461); KA6 reported (the law's phantom over
  [0.1, 1] r_e*: slope -1.90 to -1.94, R2 amplitude -0.03 to -0.06 dex).
- **KA5 FAILED.** (a) sink off: max |Delta E/E| = 2.22e-3 (line 1e-3). (b) Gamma = 1000 |g|/c: max |E + E_diss - E0|/|E0|
  = 6.06e2. Cause, found in scratch diagnostics: the centre mirror (r -> 2 RS - r, v -> |v|) moves a shell to a position of
  different potential without paying for it. A damped shell resting against the mirror is lifted on every step, and the
  drag dissipates the free energy: a perpetual source. In the undamped case it is the 2.2e-3.
- Scratch diagnostics of change 1 below (kept outside the repo): KA5a 7.0e-4 at the frozen step size (passes its line).
  KA5b 5.3e-2 / 9.0e-2 / 1.7e-2 at step factors 1 / 0.5 / 0.25: not monotone in the step, so it is not step error. In
  this test the cold collapse onto the centre floor dissipates 206 |E0|, and thousands of shells pile and cross at the
  floor. Relative to the energy that went through the sink, the books balance to 2.6e-4 / 4.4e-4 / 8.1e-5. **KA5b is
  therefore expected to FAIL its frozen line (1e-3 of |E0|) under A1 too; the line is NOT changed.**
- **Graded rows finished under the frozen method before A1** (canonical; log M_b 9 and 10.5; keys P, Pc, MU1, MU2, B1;
  the rest of the grid was running): the frozen settled-region scan stopped in the centre, r_edge = 0 to 1.3 kpc for P, Pc,
  MU1 and MU2 (B1 at 10.5: 126 kpc), although the multi-stream region reached 62-284 kpc. Radial orbits through the centre
  make each inner bin's mass-weighted mean velocity the velocity of a few heavy shells crossing it at the snapshot times.
  Other readings seen: P's median N_Gamma at r_e* 1.2e-6 / 1.5e-6, B1's 0.008 / 0.017; B1 at 10.5: slope -2.28, R2
  amplitude -2.43 dex. All pre-A1 rows are moved outside the repo, not graded, and mentioned in RESULT.md only as pre-A1.

## The changes

1. **Energy-consistent centre reflection (integrator; for KA5).** After a mirror event at RS, the shell's outgoing speed
   is set by energy conservation in its exact potential: all other shells sorted at their post-step positions, the
   Plummer baryons and the smooth background (-g_bg r^2/2), between its pre-step and its mirrored position:
   v_out = sqrt(v_prev^2 - 2 [phi(r_mirrored) - phi(r_prev)]). If that is negative (the shell's energy cannot pay for
   the mirrored position), the shell is reflected in place: r = r_prev, v = +|v_prev|. Nothing else in the integrator
   changes (step rule, drag split, pressure, forces).
2. **Edge reading (for the scan's centre noise).** (i) Snapshots every 0.01 Gyr over the last 0.5 Gyr (51 instead of 11).
   (ii) The outward scan starts at the first populated bin whose lower edge is >= 3 kpc (3 eps: outside the softened
   baryon core, 10 RS) instead of 1 kpc. The settled test itself is unchanged: mass-weighted, |<v_r>| <= 0.25
   max(sigma_r, 0.1 v_c), >= 5 shell-snapshots, stop at the first two consecutive unsettled or empty bins, r_edge = 0 if
   the first two are unsettled. The R window is unchanged ([0.1, 1] r_edge, >= 4 bins).

3. **KA5's map, stated before any A1 row (no line changes).** The frozen text reads "KA5 (S1 and the dynamics): (a) ...;
   (b) ...". A1 grades it part by part: KA5(a) (sink off: conservation through crossings and centre passages) underpins
   the dynamics (R, E, T1); KA5(b) (the sink's energy identity) underpins S1 only. If KA5(b) fails its frozen line, S1 is
   NO VERDICT by the frozen map, and its numbers are reported with the bookkeeping accuracy relative to the dissipated
   energy. The step rule stays the frozen one (step factor 1).

## What is re-run

All graded rows, the homogeneous rows, KA5 (its frozen lines), KA7 and KA8 under A1. KA1-KA4, KA6, KA9 do not depend on
either change and are re-run unchanged in the final consolidated KA run. If A1's KA5 still fails its line, the frozen
KA map applies (NO VERDICT for the gate parts it underpins).
