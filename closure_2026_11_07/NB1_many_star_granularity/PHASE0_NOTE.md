# NB1 Phase 0 result (criteria 308bf8c6b0): NO POWER for the frozen 3D test

Script nb1_phase0.py, outputs nb1_phase0.json / nb1_phase0.out. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**Rule outcome.** Largest min-over-footings power P = 0.0014 at (M 1e4 Msun, R 1 Lstar), far under the 0.15 line.
Per the frozen criteria the label is **NO POWER**; Phase 1 (3D) still owes a run and is not yet done.

**What Phase 0 shows (recorded, not gated).** At equal total mass, a point and a smooth ball (R 1-8 Lstar) give the same
far field: |G_point/G_ball - 1| <= 0.054 at 2R, <= 0.008 at 5R, <= 0.005 at 10R, every cell, both footings. The distance
from law S depends on the TOTAL mass, not on whether it is a point:
- 1e4 Msun: ball and point both reach only 0.34 / 0.54 / 0.72 of law S at 2 / 5 / 10 Lstar (canonical);
- 1e6 Msun: 0.96-0.99;
- 1e8 and 1e10 Msun: 1.000.
So the isolated Sun's deficit (QX17C: 0.71 at 1e3 Lstar) is a low-mass effect, not a point-source effect. What Phase 0
cannot see is the 3D question proper: whether ~1e10 separate 1 Msun stars act as one 1e10 Msun source (regions with
D.P < 0 between stars, where the switch turns off, exist only in 3D).

**Disclosures.**
1. Point solves at M 1e6 (canonical) and 1e8 (both) stopped above the Newton line (err 6.5e-3, 0.24, 0.26); their P
   values (<= 0.007) are not converged. Every ball solve and every other point solve converged (<= 1e-10).
2. Rows at M 1e4 have min Z 8.6e-9 / 8.2e-9 below the blend scale b~ 3.5e-8 / 4.5e-8: there the raw-branch solve is
   not exactly the blend solve (far tail). The other masses sit above b~ everywhere (blend = raw exactly, TC1).
3. Importing qx17c.py re-ran QX17C's own gate block first; its lines head nb1_phase0.out and reproduce QX17C (PASS).
4. Chosen-cell convergence: grid x2 changes P by <= 6e-7, s_out x10 by <= 4e-8.
