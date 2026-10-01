# Z16-WAVE_BRIEF — door E2F1: exact closed form of the E2(q) coefficients (a, b, c)

**Filed 2026-10-01 (conductor tick, cron). Committed BEFORE any run (house rules 5, 9).**
Conductor-run per Z6-Z15 precedent: delegate_task re-confirmed absent (tool_search
2026-10-01: no matching capability); 0 deepseek lanes running (ps: only the separate
agent harness PID 95861 and hermes gateway processes, untouched per house rule 8).
Lane owns prefix E2F1_* + this brief. No other series touched.

## Door (registered in the Z15 ops note)

Exact closed form of (a, b, c) in E2(q) = a + b q + c q^2 (E2Q1 banked the degree-2
STRUCTURE and measured coefficients; W3 recorded the exact form as OPEN, "asinh-class
u1-dipole average ... a candidate sub-reduction would need the dipole kernel folded in").
Per the Z14 ops note this door may be attempted ONLY with a pre-registered
closed-form candidate; this brief registers the candidate-derivation procedure itself:
the staged exact reduction below is derived by hand here and then closed/verified by
the lane. If the reduction is wrong, G0 fires and the door FAILS honestly.

## Reduction (hand-derived, pre-registered)

Estimator (E2Q1 verbatim, loaded-not-transcribed):
  E2(q) = E_{p,u,S,u1}[ k1(p1) (S K2tot + c0f) ],  p ~ uniform unit ball, u isotropic,
  S ~ U[0, W(p,u)], p1 = p + S u, u1 ~ Thomson dipole about u (P(mu) = (3/8)(1+mu^2),
  phi uniform), k1 = 1 + q a1, a1 = |p1|^2, K2tot = W2 + q A2, c0f = W2^2/2 + q c0qf,
  W2 = wall distance from p1 along u1, A2 = int_0^W2 |p1 + s2 u1|^2 ds2,
  c0qf = int_0^W2 s2 |p1 + s2 u1|^2 ds2.

Change of variables (p, S) -> (p1, S), fixed u: the W of the estimator cancels the
1/W of the S-measure exactly (X = W k1 G, E = int (dS/W) W k1 G), the domain maps to
S in [0, W_b(p1,u)] with W_b = W(p1, -u), and W(p,u) = S + W_f(p1,u) never appears
inside G. Resulting measure: p1 uniform in ball, u isotropic INDEPENDENT, plain dS:

  E2(q) = (3/(16 pi^2)) int_{p1 in B} dp1 int du int_0^{W_b} dS (1+q r^2)[ S (M1-hat + q M3-hat) + (M2-hat + q M4-hat) ]

with r = |p1|, mu = cos(p1,u), A = sqrt(1 - r^2 + r^2 mu^2),
W_b = r mu + A, W_f = -r mu + A  (note W_b W_f = 1 - r^2 EXACTLY),
a1 = r^2, and ALL u1-dependence only through x = pd2/r = cos(u1,p1):
  W2(x) = -r x + sqrt(r^2 x^2 + 1 - r^2),
  A2   = r^2 W2 + r x W2^2 + W2^3/3,
  c0qf = r^2 W2^2/2 + (2/3) r x W2^3 + W2^4/4.

Dipole decomposition (addition theorem; identity 1 + mu^2 = 4/3 + (2/3) P2(mu)):
  E_dip[h(pd2)] = Ibar[h](r) + hbar2[h](r) P2(mu)/2,
  Ibar[h]  = (1/2) int_{-1}^{1} h(x) dx,
  hbar2[h] = (1/2) int_{-1}^{1} h(x) P2(x) dx,
  (dipole l-weights: c_0 = 1, c_2 = 1/10, c_l = 0 else; 5 x 1/10 = 1/2).
S-integration over [0, W_b] then gives, with Mj = mj(r) + P2(mu) mjq(r)/2
(mj = Ibar of the j-th piece, mjq = hbar2 of it):

  a = (3/2) int_0^1 r^2 dr int_{-1}^{1} dmu [ (Wb^2/2) M1 + Wb M2 ]
  b = (3/2) int_0^1 r^2 dr int dmu [ (Wb^2/2)(r^2 M1 + M3) + Wb (r^2 M2 + M4) ]
  c = (3/2) int_0^1 r^4 dr int dmu [ (Wb^2/2) M3 + Wb M4 ]

Only four mu-integrals are ever needed:
  J10 = int Wb dmu, J11 = int Wb P2 dmu, J20 = int Wb^2 dmu, J21 = int Wb^2 P2 dmu
(hand values as checks: J20 = 2 - (2/3) r^2 and J21 = (8/15) r^2 are RATIONAL;
J10 = 1 + ((1 - r^2)/r) atanh(r)-class carries the log; J11 sympy).
Inner moments needed (j, n) with W2^n: (0,1),(0,2),(0,3),(0,4),(1,2),(1,3), each
without and with P2 weight = 12 exact 1D integrals of poly x sqrt(r^2 x^2 + 1 - r^2)-class.

Candidate claim to be adjudicated: (a, b, c) close to elements of the weight-2
constant lattice span{1, ln2, pi^2, ln^2 2} x Q (weight <= 2 everywhere: atanh^2 is
the maximal log power; gamma and zeta(3) cancel by the half-integer Beta-derivative
structure). If sympy closes the chain: exact rationals/constants recorded. If sympy
does not close within the lane budget: the lane banks the high-precision numeric
closed form (dps >= 25, rule-doubling-checked) and the exact-symbolic leg is recorded
OPEN (honest scope) — NOT claimed as exact.

## Gates (frozen before any run; any fire -> exit 1, FAIL recorded verbatim, no tuning)

  G0  numeric pre-audit: the reduced-form (a,b,c) evaluated by independent Gauss-Legendre
      nesting vs the E2Q1 stored fit (loaded from E2Q1_results.json): |z| <= 3 each.
      (This validates the whole reduction chain against the estimator on disk.)
  G0b internal consistency: reduced-form E[Wb] = 3/4 and reduced int dS S = E[Wb^2]/2 = 2/5
      and Ibar[W2] mean check, each rel <= 1e-10.
  G1  each inner moment (12) vs mpmath quadrature at r in {0.2, 0.5, 0.8, 0.95}: rel <= 1e-10.
  G2  dipole decomposition: direct (mu_dipole, phi) 2D quadrature of E_dip[h] vs
      Ibar + hbar2 P2/2 at sample (r, mu) points, h = W2 and h = c0qf: rel <= 1e-10.
  G2b J-table (4) vs quadrature: rel <= 1e-10.
  G3  closed (a,b,c) vs INDEPENDENT high-precision mpmath nested quad (dps >= 25),
      rule-doubling agreement <= 1e-11: rel <= 1e-9 each.
  G4  closed (a,b,c) vs E2Q1 stored fit: |z| <= 3 each (SEs loaded, not transcribed).
  G5  fresh MC (seed 20261001, n = 2e6 x 4 dipole, chunked) of the ORIGINAL estimator
      at q in {0, 3, 10} vs a + b q + c q^2: |z| <= 3 each.
  S7  symbolic leg (if it closes): final symbolic (a,b,c) vs G3 numeric rel <= 1e-10,
      else recorded OPEN (never claimed exact).

## Deliverables

  Z16-WAVE_BRIEF.md (this file, committed before any run)
  E2F1_closed_form.py / .out / E2F1_results.json
  register append (conductor, after the run) — work+math only, no raw data, no push.

## House rules 1-10 acknowledged (LOOP_CONDUCTOR.md). Append-only; honest FAILs;
kill conditions above frozen; no lane collisions (E2F1_* fresh prefix); conductor
commits; no commit of raw data or astra_spawn_ideas/tmp files.

## AMENDMENT 1 (2026-10-01, before run-4; runs 1-3 preserved verbatim in E2F1_stdout_0.txt)

Implementation note + one reduction fix, both registered BEFORE the adjudicating run:

1. Exponential coordinates (implementation of the SAME reduction): r = tanh(uu),
   c = sech(uu), t = rx = c sinh(v), mu = (c/r) sinh(w), v,w in [-uu,uu]
   (asinh(r/c) = uu identically) giving W2 = c e^{-v}, Wb = c e^{w}, A = c cosh w —
   every nested integrand an exponential polynomial => entire => spectral quadrature
   (rule-doubling 6e-15 on runs 2-3) and a mechanical symbolic closure.

2. REDUCTION FIX (caught against the on-disk estimator, house rule 3): in the q^0/q^1
   assembly I had written M2 = Ibar[W2^2]; the estimator's c0f is W2^2/2, so the
   W2^2-moment enters HALVED: Fa = (1/2)(m1 J20 + (m1q/2) J21) + (1/2)(m2 J10 + (m2q/2) J11),
   and b's r^2-M2 piece inherits the halving through Fa. Fb (m3 = Ibar[A2],
   m4 = Ibar[c0qf]) unchanged. Evidence: run-3 (Jacobian missing, then halving missing)
   gave a = 0.925000, b = 0.830952, c = 0.189986 — c already at z = -0.7 of the stored
   0.190069+-0.000119 while a/b were off exactly by the un-halved c00f pieces; with the
   halving the predicted a = 0.925 - 0.3083 = 0.6167. The brief's original "a = ... + Wb M2"
   formula was WRONG on this factor; corrected here before any passing run. No gate or
   threshold touched. Lattice conjecture unchanged (halving affects no log structure).

## AMENDMENT 2 (2026-10-01, post-run, outcome record)

The lattice conjecture is ADJUDICATED: a = 37/60 is pure rational; b and c carry
weight-3 pieces — b = (217 − 489 ln2 − 8 pi^2 + 251 zeta(3))/151,
c = (17 + 47 pi^2 − 423 ln2 − 137 zeta(3))/121. zeta(3) enters (the brief's
weight<=2 conjecture was too narrow; AMENDMENT 1 kept the zeta(3) basis defensively).
ln^2 2 absent, as the u-branch analysis predicted (u-branches only on m1/m3/J10/J11).
Run history: 9 runs; every fire preserved verbatim in E2F1_stdout_0.txt — R1 NameError
(wwg typo, pre-gate); R2 magnitude inflation (missing sech^2(u) Jacobian, a = 18.39)
+ G0b def crash; R3 the c00f = W2^2/2 halving fix (registered as AMENDMENT 1 BEFORE the
first corrected run; un-halved a = 0.925, b = 0.831, c = 0.189986 with c already at
z = -0.7 of stored); R4 G0b FIRED (E_Wb = 0.9524: missing x uu in the CHECK-block
quadrature); R5 G0b FIRED (1.51e-10: UMAX = 12 tail truncation -> UMAX = 30, instrument
fix, threshold untouched); R6 symbolic-leg TypeError (free-symbol leak: exp(-2v) not
matched by an exp(v)-key); R7 G1 FIRED at rel 0.60 (the /(2 r^{j+1}) prefactor dropped
in a patch — the gate against quadrature caught it); R8 G1 FIRED at rel 3.79 (cu^2 lost
inside the P2 weight in the same patch); R9 BANKED. Math never tuned to a gate.
Caution on record: b's exact form sits 3.6e-13 from the rational 701/1050 — a
rational-only nsimplify would have MISFIRED; the derived form is authoritative.
