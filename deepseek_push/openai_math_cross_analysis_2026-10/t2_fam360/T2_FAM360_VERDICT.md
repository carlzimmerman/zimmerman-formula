# T2 — Family 360 (weak MTW): verdict

Manuscripts (read-only source, read in full, incl. Lean docs/360.md and build/sections/*.tex):
- *Global Support and Convex Injectivity Domains under Weak MTW* (Thm: weak MTW on a compact connected closed
  Riemannian manifold n>=2 -> convex tangent injectivity domains; global support; no density hypothesis).
- *Uniform Bi-Holder Transport from Weak MTW* (Thm: on a fixed compact connected closed weak-MTW manifold,
  densities lambda <= rho <= Lambda (a.e., probability wrt vol) -> a.e.-unique optimal map is bi-Holder,
  one (alpha, C) for the whole density class; alpha non-explicit, C depends on (M,g), lambda, Lambda.

Script: t2_fam360/t2_fam360.py (MUTATE: T2FAM360_MUTATE=1). All checks can fail; base rc=0, MUTATE rc=1.

## (i) What weak-MTW gives for OUR setting

- Euclidean R^3 with c = |x-y|^2/2 trivially satisfies weak MTW: geodesics are lines, so
  c(exp_x(t xi), exp_x(p+s eta)) = |t xi - p - s eta|^2/2 is QUADRATIC in (s,t); the cost quartic
  S = -(3/2) d^4_{s^2 t^2} c is IDENTICALLY ZERO (checked numerically: |S| < 1e-12). I(x) = T_x R^3
  (all velocities are minimizing forever) is convex. So the geometric half of 360 is empty in flat space.
- The theorem is stated for a fixed COMPACT CLOSED manifold; its constants depend on that manifold and on
  (lambda, Lambda) — no a0, no kappa, no universal scale (on a flat torus of side L the constants depend
  on L and blow up as L -> oo).
- The density half is the classical statement: densities bounded above and away from zero on flat convex
  domains -> optimal map is a bi-Holder homeomorphism (Caffarelli). In flat space 360 adds nothing to the
  classical result: its own hypotheses (closed compact manifold, a.e. bounds on ALL of M) do not hold for
  an annulus with target vanishing outside it (any torus extension forces lambda = 0).

## (ii)+(iii) Density-bound check and map regularity on the truncation annulus

rho_ph(Mb, a0) = div[(nu-1) g_N]/(4 pi G), point host: rho_ph(r) = (M_b/4 pi r^3) g(y), g(y) =
sqrt(y) e^{-sqrt y}/(1-e^{-sqrt y})^2, y = (r_M/r)^2, r_M = sqrt(G M_b/a0). g is strictly decreasing;
rho_ph has a UNIQUE interior maximum at sqrt(y) = t* = 3.822 (root of t coth(t/2) = 4), r_peak = r_M/t*,
and decays as ~ (1/4 pi) sqrt(a0 M_b/G) r^{-2} in the deep-MOND tail (the "1/r^2 cusp" is the TAIL, not
a centre singularity).

Hosts (declared): MW: M_b = 1e11 Msun point mass, r_in = 0.5 kpc, r_out = 818 kpc.
CL: M_500 = 5e14 Msun, f_b = 0.157 -> M_b = 7.85e13 Msun point mass, R500 = 1.3 Mpc, r_out = 2 R500 = 2.6 Mpc,
r_in = 10 kpc. Both footings, never pooled.

| footing  | host | r_MOND kpc | r_peak kpc | rho_min (lambda) kg/m^3 | rho_max (Lambda) kg/m^3 | Lambda/lambda | min at |
|----------|------|-----------:|-----------:|------------------------:|------------------------:|--------------:|--------|
| canonical| MW   |  12.203    |    3.186   | 2.6451e-27              | 1.4467e-21              | 5.47e5        | r_in   |
| canonical| CL   | 341.90     |   89.27    | 2.0484e-32              | 5.1634e-23              | 2.52e9        | r_in   |
| alt      | MW   |  11.100    |    2.898   | 2.1825e-26              | 1.9220e-21              | 8.81e4        | r_in   |
| alt      | CL   | 311.01     |   81.20    | 4.0910e-31              | 6.8597e-23              | 1.68e8        | r_in   |

- C2 (density bounds on the annulus): min > 0 and max finite for all 4 (host x footing) — PASS.
  min is at r_in (super-exponentially suppressed: rho_ph ~ (M_b/4 pi) t e^{-t}/r^3, t = r_M/r, NOT 1/r_in^2;
  the frozen criteria's "1/r_in^2 bound" is corrected), max at the interior peak r_peak = r_M/3.822.
  Mass integral reproduces the analytic enclosed mass to 1e-6.
- C4 (map regularity at the inner edge): radial equal-mass (monotone Brenier) map T from a uniform cold
  fluid on the annulus: dT/dr(r_in+) = rho_s/rho_ph(r_in) FINITE (rho_ph(r_in) > 0) -> T is Lipschitz at the
  inner boundary (L_edge = 9.9 (alt/MW) to 2.5e7 (canonical/CL)); map strictly monotone — PASS.
  The 1/r^2 tail and the cusp generate NO singular behaviour: with both densities bounded above and away
  from zero the map is bi-Holder (classical), and in this radial case Lipschitz at the edge.
  Caveat: the log-log slope over any resolved finite window is < 1 (0.12-0.65) because the map runs ahead
  of r by the factor rho_s/rho_ph(r_in) into a steep radial density gradient; the asymptotic delta -> 0
  slope is 1 (analytic).
- MUTATE (remove the inner truncation, r -> 0): rho_ph(0+) = 0 (super-exponential), so the away-from-zero
  bound FAILS (grid min = 0.0 exactly); the failure mode is inf = 0 — "not bounded away from zero", NOT
  "unbounded above" (the declared parenthetical is corrected: for a point host there is no centre cusp).
  The map then loses Lipschitz (L_edge = inf) and is only continuous at the centre: T ~ r_M/(3 ln(1/r)),
  i.e. NOT alpha-Holder for any alpha > 0 (resolved slope ~ 0.10 and -> 0). So the truncation does real
  work for the 360 hypothesis; if the SOURCE is also bounded appropriately at r_in (uniform annulus: yes),
  the truncated map is regular.

## (iv) Verdict and screen

- FORCES: no. Nothing determines a0 or kappa; the manifold-dependent constants give no scale.
- TOOL: only in the trivial sense — the truncated-annulus density bounds hold (measured above) and the map
  is regular there, but that IS the classical Euclidean Caffarelli/radial-rearrangement statement; 360's
  own theorem is formally inapplicable (needs closed compact M, a.e. bounds on all of M, non-explicit
  alpha). It re-proves nothing beyond classical flat-space transport regularity.
- Verdict: DOES NOT APPLY (classical content only; a hypothesis of the theorem — closed compact manifold —
  cannot hold and no declared truncation fixes it). Matches FROZEN_CRITERIA declared expectation.
- Screen: Q1 NO (360 accepts the density as data; a0 enters only through the profile); Q2 no coefficient
  (alpha non-explicit, by contradiction); Q3 NOT APPLICABLE (no numeric constant emerged); C3 record
  cross-check: base-rate family F (891 distinct values), 1%-window share for T = 1/sqrt(32 pi):
  0.2245% — consistent with the record's 0.2-0.3%.

Honest bottom line: 360 supplies no forcing content for the settling problem and no scale for a0 or kappa.
Its only contact is that the phantom IS marginally in the classical bounded-density class after inner
truncation — which is exactly the Caffarelli hypothesis the triage already flagged as classical. The new
number this lane contributes is the density-bound table above (lambda, Lambda per host per footing), which
is what any class-uniform constant would have to be built on.