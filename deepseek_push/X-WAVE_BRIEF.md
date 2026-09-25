# X-WAVE BRIEF (conductor tick 2026-09-25, spawned from the landed W-wave)

Successor wave to W01/W02/W03. 3 conductor-run lanes (delegate_task absent from
this session's toolchain; Q/R/S/T/U/V/W precedent). Distinct OPEN doors only —
the M05 "symmetry puzzle" (the uncertified ladder rungs above m=8, incl. T01's
K1-fired r^10 NON-CLOSED) and the lattice of exact exposure-moment values
around the volume window (N02's 4/5 & 8/35, M05's 3/4 & 5/12). KILLED-column
consulted: none of the killed doors are touched. Files claimed: X01_* / X02_* /
X03_* in deepseek_push/, plus NEW files fable_independent_2026/lean_2026/X01_*.
lean (append-only rule: NO existing file is edited — Q01_r6_core.lean and
friends stay bit-identical; supersession is recorded as new rows/files on top).

## X01 — the first-flight EXPOSURE LADDER, closed form + m=4 audit + extension

Door: M05 left the ladder open ("4th moment sequence is a symmetry puzzle"),
P/Q/R certified rungs m=2..8, T01's r=10 rung is NON-CLOSED under the
registered K1 (q=97020>1e4). This lane derives, in exact rational arithmetic
and THREE independent routes, the closed form of the whole even ladder:

    M_n := E[ int_0^chord (R^2 + 2 R mu s + s^2)^n ds ]  (R~3R^2, mu~U(-1,1),
           chord = -R mu + sqrt(1 - R^2 + R^2 mu^2);  measure EXACTLY as P01)
    M_n = (3/(2(n+1)(n+2))) * sum_{k=0}^n (k+1)/(2k+1)          (X01-I)
        = (3/4) * [(n+1) + H_{2n+1} - H_n/2] / ((n+1)(n+2))

Routes: (A) closed form X01-I, (B) sympy-EXACT mu->t change-of-variables with
the antiderivative computed by sp.integrate of the FULL power (NOT the
hand-written expansion used by M05_geometric_anchors/P01/Q01 g_m(4) — the
hand expansion is the audit target), (C) 40-dps original-variable nested
quadrature of the definition.

- K1 (m=4 audit, BOTH-WAYS): if route B == route C == X01-I to <1e-30 abs AND
  all three differ from the landed 1/4 by >1e-9 -> verdict CORRECTED-TO-17/60,
  bug trail named (halved s^3/s^4 coefficients of (R^2+2Rmu s+s^2)^2 in
  M05_geometric_anchors.py I2, P01 I2, Q01 g_m(4); m=4 absent from every K0
  replication gate; q01CoreR4 certified the buggy polynomial). If any route
  agrees with 1/4 -> verdict LANDED-STANDS, correction NOT issued, and the
  closed form is re-checked for a modeling error (recorded either way).
- K2 (closure): X01-I == route B exactly (sympy rational arithmetic) for
  n = 1..6 AND |X01-I - route C| < 1e-30 for n = 0..6 AND MC 1e7 z <= 5 at
  n = 2, 6 -> LADDER-CLOSED; else OPEN with the exact failure recorded.
- K3 (extension): M_6 = ?, M_7 = ?, M_8 = ? (closed form) each verified by
  route C < 1e-30 and MC 1e7 z <= 5 -> rungs m=12/14/16 LANDED (new).
- K4 (odd rungs, informational): E[int r ds] (m=1 odd) rational reconstruction
  fails at 1e-12 with q <= 1e6 -> ODD-RUNGS-NOT-RATIONAL (expected: the
  u-substitution leaves an asinh/elliptic integral; evidence only, no proof).
- K5: scope — math-only lane (K3 of the wave), no new physics claim here;
  the physics payload is X02.

## X02 — the exact window atom to O(tau^3): finite-thickness law

Door: M05-I gives the thin-limit window R_v(0,q) = (3/4 + 5q/12)/c0(q) from
the FIRST-order exposure only; the atom A_v = E exp(-tau0 (L + q I1)) has no
second/third-order exact coefficients on record, and N02's anchors (E[L^2]=4/5,
E[int s r^2 ds]=8/35) are the first two 1D cores. This lane computes the exact
cumulant expansion of -ln A_v to O(tau^3):

    -ln A_v = tau E[X] - tau^2 k2/2 + tau^3 k3/6 + O(tau^4),  X = L + q I1
    E[X] = 3/4 + 5q/12 (landed),  k2 = Var(L) + 2q Cov(L,I1) + q^2 Var(I1),
    k3 = E[(X-E[X])^3]  —   ALL coefficients exact rationals.

- K1 (anchors, reproductions): E[L^2] = 4/5, E[int s r^2 ds] = 8/35 (N02
  storage) reproduced by definitional 40-dps quadrature < 1e-30; plus NEW
  exact values E[L*I1] = 2/5, E[L^3] = 1, E[I1^2] = 208/945 (sympy-exact +
  quadrature < 1e-30); E[L^2 I1], E[L I1^2], E[I1^3] on the same route.
- K2 (both-ways, pre-registered): MC 1e7 of A_v at the 3 x 3 grid
  tau0 in {0.25, 0.5, 1.0}, q in {0, 3, 10}; compare ln A_v(MC) against the
  exact polynomial P3(tau,q) = -tau E[X] + tau^2 k2/2 - tau^3 k3/6:
  |ln A_v(MC) - P3| <= 3 SE at ALL 9 points (abs) -> FINITE-THICKNESS-EXACT
  (the window atom is exact through O(tau^3)); any point > 3 SE -> recorded
  with the exact measured discrepancy (no re-tuning, both-ways).
- K3: scope — window channel only; no new astrophysics law; c0(q) itself
  (K07's measured column, ratio vs (3/4+5q/12)/2 unexplained: 1.0565 /
  1.089 / 1.0854 at q=0/3/10) is left OPEN for a successor wave, explicitly
  NOT touched.

## AMENDMENT 1 (2026-09-25, fix-forward recorded BEFORE the X02 rerun — house rule 3)

X02 run-1: the lane's k4 polynomial used the formula for the central 4th MOMENT
(E4 - 4 mu E3 + 6 mu^2 E2 - 3 mu^4) instead of the 4th CUMULANT (k4 = m4 - 3 m2^2);
k2 and k3 are unaffected (they coincide with their central moments).  The 9-point
pre-registered gate failed on the wrong k4 (residuals matched 3 Var^2 tau^4/24
exactly: 4.4e-4 at (0.5,0), 6.8e-4 at (0.25,3) vs measured 4.46e-4 / 6.95e-4).
Run-1 output kept verbatim in X02_atom_exact.out/.json history.  Amendment:
- K2a unchanged K1 (moment lattice — all ran clean, exit 0 in run-1).
- K2b (re-registered): corrected P4 (k4 as cumulant) at the same 9-point grid;
  PLUS the exact-tower check P7 = P4 + tau^5 k5/120 - tau^6 k6/720 + tau^7 k7/5040
  (k5..k7 from the standard cumulant formulas in terms of E[X^1..7]; moments from
  the same exact (x,y) machinery, quadrature-verified).  Verdict rules: all 9 at
  P4 -> CUMULANT-4-EXACT; all 9 at P7 -> CUMULANT-TOWER-7; else the pointwise
  residuals are recorded verbatim (both-ways, no re-tuning).
- K2c (NEW, registered): the exact q=0 atom closed form
  E[e^{-tau L}] = (3/(2 tau)) [1/2 - (1 - e^{-2 tau}(1 + 2 tau))/(4 tau^2)]
  checked against MC at tau in {0.25, 0.5, 1.0, 2.0}, gate |..| <= 3 SE.
  (This is exact geometry, closed-form; the q>0 atom is NOT of this closed
  class — the I1 exponent does not Fubini-flip — the cumulant tower is the
  exact object there.)

## X03 — Lean: corrected m=4 core + first m=10 certificate + m=12 extension

Door: q01CoreR4 (int P~_4 = 1/4) certifies the buggy polynomial (X01 K1);
m=10 was NEVER Lean-certified (T01's K2 gated on the failed K1); m=12 has no
core at all. This lane writes NEW files only:

- X01_ladder_core.lean: corrected r4 theorem (17/60, core from route B),
  r10 theorem (13649/97020 — first certificate of the T01 rung, justified now
  by the closed form X01-I, not by the denominator gate), r12 theorem
  (50423/420420), each as an exact 1D polynomial integral (FTC idiom of
  N03/Q01/S01), plus a header comment recording the supersession of
  Q01's q01CoreR4 (file untouched, append-only).
- K1 (cores): each core integrates EXACTLY (sympy) to the claimed rational.
- K2 (Lean): lake compile exit 0, zero sorry, #print axioms exactly
  {propext, Classical.choice, Quot.sound} on EVERY new theorem.
- K3: scope — 1D polynomial certification only (the 2D->1D reduction stays
  sympy-analytic, exactly as Q01/S01 recorded).

House rules 1-10 (LOOP_CONDUCTOR.md) bind: kills pre-registered above BEFORE
any run; exit 0 only on real passes; honest FAILs preserved verbatim; no lane
commits (conductor commits the wave); raw data never committed; append-only
record (register rows + this brief + lane files, no edits to landed files).
