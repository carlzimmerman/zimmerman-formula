# Partial audit — exact gaps; six-tile regrade still in progress

Kappa = 1/2 FITTED; not theory closed. Criteria825835993f. Main structural
run passes15/17 checks and exits1: the two original quadrature checks fail.
Strong-coupling/BH recomputations and board integration remain pending.

## The switched energy does not provide H(div) coercivity

In one dimension set K=a0=1, fixed Dirichlet potential at x=+-1, and
g(u)=-u-log(1-u)-u^2/2. Let0<a<1 and

    p_n(x) = -a tanh(nx),
    Phi_n(x) = a[log cosh(n)-log cosh(nx)]/n.

Then Phi'_n=p_n, Phi_n(+-1)=0, |p_n|<a and p'_n<0. For the switched
functional with zero source,

    E_n = integral[(Phi'_n-p_n)^2/2 + g(|p_n|)
                   + gamma max(p'_n,0)^2/2] dx
        = integral g(|p_n|) dx <= 2g(a).

Yet exact integration gives

    integral (p'_n)^2 dx
      = 2a^2 n[tanh(n)-tanh(n)^3/3] ~ (4a^2/3)n.

Thus its energy sublevel is unbounded in H(div), even with a uniform cap
margin and zero boundary potential. The symbolic primitive and all these
identities are checked in `structural.py`. The sequence approaches a downward
jump in p. It shows that a downward jump is not excluded by an infinite
energy barrier in the relaxed limit. It does not assert that the original
functional is defined on every distribution, or that this limiting profile
is a minimizer or a solution.

This exposes a missing compactness/existence step when transferring C8's
full-divergence-penalty direct-method argument to X3's positive-part penalty.
The convex dual representation proves lower semicontinuity in an appropriate
topology; it does not supply the missing H(div) bound. A measure-divergence
relaxation may be viable, but its domain, boundary traces and regularity need
their own proof. Noncoercivity here is not a theorem of nonexistence.

Conditional uniqueness remains justified: g(|P|) is strictly convex inside
the cap; the squared Phi-gradient term and fixed Dirichlet data then make
two distinct finite-energy minimizers impossible. That is an at-most-one
statement, not a proof that a classical minimizer exists for every source.

The original512/1024 global Gauss quadrature under-resolves the increasingly
narrow transition. Main energy-pair disagreement at n128 is2.10e-5 versus
the frozen1e-6 line; the norm check misses by7.86e-8 versus1e-8. The symbolic
identities are exact independently of these quadratures. Both numeric
failures remain in `main/structural_results.json`.

The separately frozen POST-RESULT A1 diagnostic uses y=n|x|, with16/32
Gauss nodes per unit interval. It passes the same tolerances on all eight
main/mutant cases: maximum norm error4.44e-16, energy-pair change2.22e-16.
This confirms the resolution diagnosis without replacing the initial failures.

## The board's off-shell conservation statement is false

For minimally coupled scalar matter,

    nabla_mu T^mu_nu = (Box chi - V'(chi)) partial_nu chi.

This is the off-shell Noether identity. Conservation follows on the matter
equations. The script derives it on an arbitrary diagonal1+1 curved metric;
both symbolic residuals vanish. In flat spacetime, with V=0 and chi=t^2,
the divergence is(-4t,0), not zero. The on-shell control chi=t+x gives zero.
This corrects the board wording; CFG329's README itself already distinguishes
the off-shell identity from on-shell conservation.

Either orientation of the v3s stiffness switch remains a scalar function
of D.P, so changing its orientation does not break diffeomorphism invariance.
The required switch-inverted control instead fails the nonnegative principal
sound-speed test on negative-divergence states. It should not be engineered
to fail the valid matter identity.

## Pulsar and causality claims need a wider scope audit

The C8 conservative binary arithmetic reproduces at24pc and is tiny over
both declared L intervals. But C8's 'no radiative channel' premise conflicts
with P3's background-gradient propagating mode. Conservative force estimates
alone cannot certify the full radiation prediction.

Likewise an elliptic leaf equation alone does not establish observable
acausality: GR has elliptic constraints and retarded physical observables.
The inherited instantaneous-force numbers are recomputed as illustrative
estimates, not accepted as a full gauge-invariant response calculation.
These two full claims remain NO VERDICT pending the remaining analysis.

## Reproduce this partial audit

From the repository root:

```sh
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/structural.py
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/structural.py --mutate
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ34_switched_relativity/quadrature_diagnostic.py
```

Expected exits1,1,0. Main15/17; mutant13/17, additionally failing principal
sound-speed positivity and the original sequence's uniform energy bound.
These subsecond calculations write separate atomic main/mutant outputs.
The final lane README and board changes await the declared BH and coupling
checks. This document is a partial finding, not lane-completion certification.
