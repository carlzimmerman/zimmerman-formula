# OPUS_49 BRIDGE CLOSURE -- registering the spectral-spine handoff (2026-09-22)

Parent: `spectral_spine_closure_2026_09_22/REPORT.md` (committed 93bc3420a).
This file registers what the bridge closes, what it kills, and the three
remaining obstructions -- in the repo's append-only, no-delete style.

## 1. C_gr is now PINNED, cross-checked two ways (supersedes the [2.25, 3.35] band)

The I13 certificate (31e5eafd8... ca2f8fd0d) registered the virial Coulomb
factor only as a literature band. The bridge's n=3 polytrope computation gives

    C_gr(n=3) = 3.373422935937

and the independent door-A Lane-Emden recomputation gives

    C_gr(n=3) = 3.373422934888   (relative agreement 5e-10)

Both reproduce the published 1.1245 benchmark in the conventional
(Gamma_1 - 4/3) coefficient (1.124474 / 3.373423 ~ 1/3). The band
[2.25, 3.35] is superseded; the n=3 value 3.37342 is the committed one.

## 2. KILLED: the I14 source bridge (the spectral-rigidity route to kappa = 1/2)

The bridge's SOURCE_BRIDGE.md supplies explicit algebraic obstructions to
identifying I14's t-lattice Hardy operator with the framework's scalar
action (G155):

- directly varying G155's kinetic action yields a different radial weight;
  its deep log-coordinate weight is constant, not the weight underlying
  I14's sqrt(r) dressing;
- the cited action supplies no independently derived negative kappa^2
  potential;
- the full interpolant does not admit the quoted logarithmic background
  exactly.

CONSEQUENCE (registered, no hedging): I14's 12 Lean theorems remain TRUE as
mathematics of the t-lattice Hardy-marginal model -- the trichotomy
(gapped stable / marginal at kappa^2 = 1/4 / explicit negative modes) is
machine-checked. But the PHYSICAL identification -- "the phantom's radial
fluctuation operator reduces to this family with the framework's kappa,
hence kappa = 1/2 is the stability boundary" -- is VOIDED AS STATED. The
claim "spectral-rigidity route to kappa = 1/2" (opus_49b/c messages,
memory) is retracted from the framework side and re-registered as: a model
theorem awaiting a real derivation from the framework's actual constrained
quadratic action. The wall is "shifted by confinement; not universally
kappa = 1/2" (bridge, I14 DERIVATION). kappa = 1/2 remains derived by the
PD08/PD22 composition route; the I14 route does not add a fourth path.

## 3. Not closeable: I15 many-plaquette X_d is obstructed, not merely unevaluated

The bridge reduced the volume-uniform strong-coupling window to
x >= X_d, X_d = max(1, sqrt(2 A_d/c1), sqrt(2 c2 A_d)), A_d = (32/3) d(d-1)/2,
with c1, c2 from Yarotsky, math-ph/0411042. Audit: c1, c2 are EXISTENCE
constants in that source (Theorem 1: "There exists a constant c1 ...");
their values come from the 2004 JMP predecessor (10.1063/1.1705718,
paywalled, no arXiv version with explicit constants located). Evaluating
X_d therefore requires reproducing the full cluster expansion -- a research
paper, not a numerical evaluation. The obstruction is exact: the cited
source does not contain the constants numerically.

So the honest state of the real-YM rung: single-plaquette operator gap
certified (>= 1 at x >= 2 via min-max); many-plaquette gap proven to EXIST
uniform in N and volume for x >= X_d with X_d finite-but-unknown;
x >= 2 uniformly in volume NOT obtained; continuum limit (R5/R6) untouched
and named. No Clay claim.

## 4. Door-A result (independent, parallel lane)

pulsational crossing from the I13 spine + n=3 polytrope + C_gr = 3.37342:
     x* ~ 1.32e-4,  M_puls ~ 6.6e7 Msun (T_rec = 5000 K),
     band [4.6e7, 1.03e8] over T_rec in [4000, 6000] K.
Read against the index's double ceiling: this lands on the GLOBAL
equilibrium ceiling [5.09e7, 1.21e8], NOT the pulsational band 1e5-1e6.
The pre-registered kill for the pulsational reading fires (FAIL on the
pulsational landing); the global-ceiling coincidence is a separate,
registered finding pending door-A's own verdict and the MESA profile
import that would distinguish the two bands.

## 5. What remains open (unchanged, named)

- MESA Gamma_1(beta(r)) profile import -- the only way to split the two
  ceilings observationally (door A REGISTERED).
- The I14 source derivation -- a NEW lane: Hessian of the framework's
  actual constrained action at its actual background. Required before any
  kappa stability claim is framework-level again.
- X_d (Yarotsky c1, c2) -- blocked by a paywalled cluster-expansion paper.
- The Clay wall R5/R6 -- unchanged, world-open.