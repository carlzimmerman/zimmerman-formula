# Fixed-action initial-data extension

2026-09-12. Owner: `/root/fixed_action_escape`. Requested base was
`1f0306787`; the actual shared checkout at first inspection and all archived
executions was `5a87447af258ec132f6cedb5170dc8dd4c03f038`, dirty. Old source
files and existing records were preserved; exact actual input hashes are in
each run manifest. No commit was made by this work package.

**The complete theory remains OPEN.** Additional physical initial data yield
three distinct early-clock histories with a longer positive numerical
gradient-screen interval. They nevertheless fail the future gradient gate.
This is a finite result, not an exclusion of every initial condition of this
action or a no-go for clock-based MOND theories.

## Contract and frozen ingredients

The calculation retains the existing EH + P(X,tau) - V(tau) +
sqrt(Xtau) W(Y,tau) + gamma X Box(chi) action and ordinary baryons/radiation.
M2=1, Lambda=.7, gamma=1e-6, the coefficient ODE, and its initial data
(coefficient a=1,m=.1,v=.5) are unchanged. Backward and forward evaluations
join two integrations of that same IVP; there is no extrapolation outside
the integrated interval tau in [-2.344261575...,2].

Physical a=1 is a normalization epoch, not calibrated today. The grid varies
physical initial tau, rho_b, and rho_r. For each tuple, the actual clock
constraint eliminates H as (P_tau-V_tau)/(3W), then the Friedmann residual
is solved for q. Both q orientations are searched. The resulting scalar
current is determined by the constraints; an incompatible current is never
imposed independently. During evolution rho_b and rho_r obey their exact
a^-3 and a^-4 first integrals, while a^3 j_chi and the original constraints
are monitored independently.

The 54 tuples are the Cartesian product of:

- tau = [-2.1650061542309937, -1.5726764780714775,
  -0.9006685507781443, 0, .5, 1]. The first four are the coefficient
  ln(a)=-2,-1,-.5,0 epochs of the unchanged IVP.
- rho_b = [.0001,.001,.01].
- rho_r = [.0001,.01,1].

Sign-change grids of 1601 and 3201 points, each augmented by 100 logarithmic
boundary points on each side, find the same number of roots for every tuple.
Maximum matched q difference is 3.22e-15. Tangential roots and other unsampled
initial data are not excluded. An earlier 801-grid scout is retained as
`exploratory.json`; the archived runs below carry the load-bearing evidence.

## Results and the discrimination supplied

The two inventories each find 186 constraint roots: 126 fail the initial
gradient screen and 60 pass the necessary initial gradient/partial-kinetic
screens. Every passing positive-q root is continued, giving 30 distinct
initial-data continuations. Of these, 27 develop a resolved negative gradient
backward. The other three require an extended wavenumber check.

The three exceptions have tau=-2.1650061542309937 and rho_r=1. Their initial
q is approximately .998002 and H approximately 3.16. Their different baryon
charges are retained, and the negative-q counterpart at rho_b=.001 is also
checked. At the originally used k=3000,30000, finite-k corrections cause a
sign-resolution stop near ln(a)=-.675 despite positive k=30000 estimates.
Adding k=300000 moves that diagnostic stop to approximately -1.75. Explicit
evaluation at k=3e6 and 3e7 resolves the sampled operator estimates further;
these values are computed from the actual six-state finite-gamma operator,
not assigned from an expected sound speed.

The refined continuation uses step .0125, rtol=5e-12, and a requested range
of -2.3 to +2.3 physical e-folds. The middle positive-q case illustrates it:

| Point | ln(a) | tau_dot | clock c_s^2 at k=3e7 | relative log margin | background condition |
|---|---:|---:|---:|---:|---:|
| Initial | 0 | .931404 | about 8.09e-5 | .00234781 | 3.92e4 |
| Backward bound | -2.3 | .774706 | +2.74739e-7 | 2.39867e-6 | 1.17123e10 |
| Future failure | +.2625 | 1.002660 | -6.32797e-6 | about .00505 | 2.25427e4 |

All four extended cases reach the backward bound with positive numerical
operator estimates. Radiation fraction there is only .2605, so no
radiation-dominated era was reached. All four subsequently show a future
gradient sign change bracketed by ln(a) in [.25,.2625]. Their negative
endpoint values range from -3.90e-6 to -6.57e-6, compared with the recorded
finite-k convergence diagnostic of 1e-10. The coarser .025 run first samples
the failure at .275. These brackets locate sampled sign changes, not exact
transition times.

Thus the extended candidates fail for a different time direction from the
tau=0 high-|q| candidates: they survive the specified past screen but fail
forward. None of the 30 positive-q initially passing roots supplies the
requested tested two-direction history. Only one negative-q early counterpart
received the new long continuation; the other negative-q grid histories
were not universally classified.

## Numerical and physical limits of the longer past screen

The larger k values establish neither a UV completion nor stability at
arbitrarily high frequency. At the backward endpoints the background matrix
has condition about 1.17e10 and determinant about -1.387e14. The eigenvector
matrix of the similarity-balanced k=3e7 operator has condition as large as
8.04e9. This whole-basis condition alone would not establish sensitivity of
the clock pair. A separate left/right eigenvector check finds clock-specific
first-order eigenvalue condition numbers of 3.04e9--3.05e9 at those backward
endpoints. A small eigen-equation residual alone is not a rigorous eigenvalue
error bound for such a non-normal matrix. The positive past result must
therefore remain conditional floating-point evidence, even though independent
step refinement and the approximate principal formulas agree on its sign.

The future failure occurs under substantially better conditioning: background
conditions 2.23e4--2.26e4, determinant approximately -2.33e3, and kmax
eigenvector conditions 1.31e5--1.70e5. Clock-specific eigenvalue conditions
are 5.90e4--7.66e4. These are coordinate-dependent sensitivity diagnostics,
not interval error certificates. The future failure is not a logarithm-boundary stop.

Across 828 refined extended samples, the largest scaled constraint residual
is 4.50e-10 and the largest relative scalar-current drift is 3.78e-10. None
has a partial-kinetic eigenvalue below its recorded scale-aware negative
tolerance. This uses the original quadratic action, with lapse and shift
eliminated through A-B C^-1 B^T. Dust density and remaining constraints are
unreduced: no physical rank, Hamiltonian degree count, or full no-ghost result
is inferred. The full spectra and per-sample conditions are retained.

The L186 gamma->0 principal formulas are cross-checks, not substitutes for
the finite-gamma operator. At the middle backward endpoint the general
formula evaluated on the finite-gamma jets gives 2.74739354e-7 against the
operator's 2.74738990e-7. The simplified closure formula gives 2.70203796e-7,
about 1.65% lower, demonstrating why its equality must not be imposed at
finite gamma. Direct closed-form density and clock identities including
cubic terms agree with the original numerical jets to scaled differences
at most 1.03e-10 and 8.99e-10 respectively.

## These are physically different histories

For the conserved charges Q_chi=a^3 j_chi, Q_b=a^3 rho_b, and
Q_r=a^4 rho_r, Q_chi/Q_b and Q_chi/Q_r^(3/4) are invariant under shifting
the normalization epoch or rescaling a. They distinguish the early candidates
from the previously archived original history:

| History | Q_chi/Q_b | Q_chi/Q_r^(3/4) |
|---|---:|---:|
| Previous original branch | 97.1724 | 3.07286 |
| New early, rho_b=.0001 | 283182.36 | 28.31824 |
| New early, rho_b=.001 | 28312.51 | 28.31251 |
| New early, rho_b=.01 | 2825.54 | 28.25541 |

The new histories are therefore not merely the old history with a relabeled
scale factor. This does not supply an observational normalization or establish
their cosmological suitability.

## Existing tau functions do not automatically require extra fields

Tau is already varied in this action. Evaluating its fixed functions U(tau),
d(tau), and V(tau) at a different initial tau adds no field. More generally,
choosing a different fixed function of an existing scalar changes its coupling
and field equations but does not, by that fact alone, introduce an independent
field. Additional fields arise only if independent dynamical coefficient
variables are actually introduced. No new coefficient function was chosen
in this experiment. This distinction does not make arbitrary post hoc
coefficient reconstruction admissible under the user's requested scope.

## Route status and next useful implication

This bounded same-action initial-data extension is completed as a research
discriminator. Its candidates fail the required time-history gradient gate;
the broader action and intended theory remain open. No CMB transfer,
recombination mapping, primordial mode choice, galaxy phenomenology, or
observational likelihood was computed.

The next mathematical discriminator would reduce the fixed-action
constraint/current system to a relation in tau and the scale-invariant
conserved-charge ratios, then determine whether an admissible path can avoid
the clock-rate crossing surface in both time directions. A proof would need
the finite-gamma principal condition and global hypotheses; this finite grid
does not provide them. Untested continuous initial data and tangential roots
remain open, rather than being discarded by numerical non-detection.

The computation-audit and research-program skills shaped the separation of
finite numerical evidence, unresolved conditioning, and the unchanged global
goal. Four focused tests passed. All seven archived numerical executions and
their manifest validations returned exit 0. See [commands and provenance](COMMANDS.md).
