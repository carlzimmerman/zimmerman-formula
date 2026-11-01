# Uniform entropy-floor target

Checkpoint **X48-FLOOR-2026-11-01-A**, descended from
X48-TRANSPORT-2026-11-01-B. Initial HEAD observed by the coordinator:
`6c4693396308a12233b88445d6aab9451b49ab6e`; the shared checkout changes
concurrently, so exact source hashes identify the mathematical inputs.

For the unchanged exact semidiscrete shell ODE and virgin initial sphere,
prove constants `t_s<infinity` and `epsilon>0` independent of N such that

\[
 \inf_{t\ge t_s}\min_{1\le i\le\lceil N/20\rceil}K_i^{(N)}(t)
 \ge\epsilon\qquad\text{for every }N\ge32.
\]

The initial sphere, material scales and all coefficients are exactly those
in `../README.md`: rho=.25, R=1, u=-.25r, K=0,
G=rho_q=Kstar=1, tau=.5, D=.1, alpha=1,
chi_d=chi_g=.01, ell_g=.1. No law changes, inserted floor, sorting,
energy reset, seed perturbation, coefficient rescaling or numerical
accepted-state projection can establish this target. Continuum passage
requires a separate stated convergence notion; a point value at m=0 needs
regularity beyond an almost-everywhere material bound.

The required conjunction is actual uniform seeding plus unconditional
long-term preservation for the exact finite-mesh solutions. Exact energy
conservation and quiet-domain inactivity must be retained. A conditional
seed-to-floor theorem alone is partial progress; finite grids alone do not
establish the universal quantifier.

Routes owned separately:

1. Direct startup seeding: analytic cold homology, activation expansion and
   a fixed-prefix compression lower bound with a remainder uniform in N.
2. Preservation: ordered auxiliary heat flow, entropy production, comparison
   and fixed-N geometric continuation.
3. Obstruction: test free-surface effects and quantifiers, distinguishing
   failures of proof methods from a counterexample for these initial data.
4. Startup energy route: localized discrete relative-energy/semigroup bounds
   for the parabolic stress layer, instead of a finite propagation cone.
5. Literature transfer: check exact hypotheses of free-boundary results;
   none can be imported merely because it concerns a gaseous star.

New mathematical notes live here. Previous pinned code, results and analysis
records remain immutable. New finite computations use declared bounded
contracts and explicitly test the remaining startup hypothesis rather than
being labeled a proof of it.
