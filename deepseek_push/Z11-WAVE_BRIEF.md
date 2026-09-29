# Z11-WAVE BRIEF (conductor, 2026-09-29 tick ~15:5x EDT - pre-registered BEFORE any exact run)

Spawn trigger: 0 deepseek lanes running (ps aux: hermes gateway, one orphaned
`python3 -` stdin process from 06:50 - not a deepseek lane script, and one
cfg158_referee.py live-lab referee, untouched per house rule 8). All Z9/Z10
verdicts committed (9be87161e, 4754ea411, 400e7919a). Open doors from the
register: W2 candidate (unregistered) and OA1 WG high-z (data-gated on eRASS:3
WG products, not on disk - no padding lane, Z5-ops/Z9 rule). W2 REGISTERED NOW
as this wave's single lane; delegate_task re-confirmed absent in prior ticks -
conductor-run lane per Z6/Z7/Z8/Z9 precedent. Wave size 1: that is every
runnable registered door.

## Door W2 (registered): exact thin-window law c00(q) = A0 + A1*q

Background (on-disk): MC7 (exit 0, 4754ea411) measured c00(q) = lim E[D]/tau0
by extrapolation and found the MC4 line refuted at q in {0,1,6,10}; its
extrapolation model stayed UNSETTLED (quadratic tau0-coefficient selected only
at q=10). W1/LR7 banked the NUMERATOR side exactly. The DENOMINATOR side has
no exact form. This door derives one.

Conductor pre-audit (numeric, recorded in the tick transcript BEFORE this
brief was written; MC7_results.json loaded-not-transcribed): D = elapsed - Q
= sum_j l_j (1 - u_j . u_final) (telescoping identity, engine algebra). To
leading order in tau0 only single-scatter photons contribute (prob O(tau0)),
the first segment contributes l_1(1 - E[mu_Thomson]) = l_1 (E[mu]=0 by the odd
kernel), and the segment ends at the wall distance W. So

    c00(q) = E[ int_0^W s k(s) ds ],
    k(s) = 1 + q r(s)^2 = 1 + q(r^2 + 2 (p.u) s + s^2),

i.e.  c00(q) = A0 + A1*q with
    A0 = E[W^2/2],
    A1 = E[r^2 W^2/2 + 2 (p.u) W^3/3 + W^4/4],
p volume-uniform in the unit ball, u isotropic, W = -(p.u) + sqrt((p.u)^2 +
1 - r^2) (the disc simplifies: disc = 1 - rho^2 in cylindrical form).
First pre-audit pass used the WRONG k(s) (the integrated rate, not its
integrand) and missed MC7 at z~55 on the q-slope - recorded verbatim in the
transcript, fixed before any lane run. Second pass (n=2e7, seed 20260929):
A0_num = 0.400015, A1_num = 0.228584 vs MC7 measured c00 = 0.401977+-0.001434
(q=0), 0.627066 (q=1), 1.085406 (q=3), 1.786688 (q=6), 2.651924 (q=10,
quadratic-selected). Hand check: A0 = 2/5 exactly (E[1-rho^2]=3/5, E[z^2]=1/5,
odd term vanishes).

## Lane W2_c00_tau0_expansion (owner: conductor; prefix W2_*)

Deliverables: W2_c00_tau0_expansion.py/.out/.json (exit code real), register
row, commit (work+math only).

Gates (pre-registered):
- K1 EXACTNESS: sympy exact A0, A1 (cylindrical (rho,z) reduction, density
  3/(4pi), z in [-sqrt(1-rho^2), sqrt(1-rho^2)]) must match TWO independent
  numerical quadratures (mpmath quad + Gauss-Legendre) to <= 1e-11 rel.
  Mismatch -> exit 1.
- K2 PARITY: exact c00(q) = A0 + A1 q vs MC7 measured c00 at q in {0,1,3}:
  any |z| > 3 -> exact-law candidate REJECTED, honest record, exit 1.
- K3 SCOPE TEST (records, does not gate exit): q=6 residual explained as
  O(tau0) extrapolation bias in MC7's linear model? Refit MC7's stored 8-point
  c0(tau0) at q=6 on the 4 smallest-tau0 points with c0 = A + B tau0; the
  intercept should agree with exact A0 + 6*A1 within 3 SE. Fire recorded
  either way; q=10 (quadratic-selected) excluded from all gates.
- Honest scope: c1(q) (the O(tau0) coefficient) NOT derived this lane -
  successor door W3 candidate; Lean certificates of the exact A0/A1 rationals
  - successor door LR8 candidate (own algebra audit first, LR7 precedent).

Exit 0 iff K1 and K2 pass. Kill conditions honored per house rule 5; all run
blocks preserved verbatim in .out.
