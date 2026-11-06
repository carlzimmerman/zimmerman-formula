# Independent review: mean-only gravitational momentum

**Outcome:** the reduced state and differentiated momentum equation are
correct. The canonical mean momentum rate is retained; the nonconstant
rate is reconstructed and checked against the native rate, not simply
discarded. This is a new constrained discretization, valid where the
periodic reconstruction exists on the selected regular branch and its
canonical-rate discrepancy converges. It does not retroactively validate
old runs beyond their former stopping criterion.

Read-only review of reduced_system.py, CONSTRAINT_RATE_CONTRACT.md,
MEAN_MOMENTUM_CONTRACT.md, the inherited reconstruction, and recorded
validation outputs. No solver files changed. A small independent t=1
reconstruction probe was run without evolving a trajectory.

## State and equation accounting

The saved state has length 2n+2 and contains lambda, n beta values,
mean(p_lambda), and n r_mom values. The slicing in unpack/reduce is
consistent. reduce takes the actual fine-grid mean of the canonical
p_lambda rate, while it Fourier-restricts beta_t and r_t. Thus the global
canonical momentum equation remains an evolved equation.

At every stage expand prolongs beta and r, recenters the cached p_lambda
guess to the requested mean, and solves the native spatial momentum
constraint. The initial family has beta=0 and constant p_lambda, so
the initial mean mapping is exact. Initial beta/r truncation is the same
spectral approximation already used by the padded formulation; no new
arbitrary initial mean is introduced.

With C=2M^2 exp(4beta)/p and S=2beta_xx+3beta_x^2,

    p_beta=r+C S,
    (p_beta)_t=r_t+4C beta_t S-C S p_t/p
                 +C(2 beta_xxt+6beta_x beta_xt).

Differentiating p_x=beta_x p_beta therefore gives

    (partial_x+beta_x C S/p)p_t
      =beta_xt p_beta
        +beta_x[r_t+4C beta_t S+C(2 beta_xxt+6beta_x beta_xt)].

The sign and every chain term in the implemented operator/source are
correct. Using the restricted coarse beta_t,r_t and then prolonging them
is essential: this is the tangent equation for the independently evolved
state, rather than for discarded fine-grid derivatives. The reference
p_t comes from the full native canonical RHS on the reconstructed state.
Both represented and full discrepancies are reported.

At finite resolution the differentiated constraint and canonical p_t need
not agree. The explicit represented-rate test is precisely the check that
the reconstructed nonconstant momentum has not replaced a physical
equation by an unrelated evolution. A passing finite tolerance establishes
numerical consistency at that tolerance, not exact equivalence or continuum
accuracy by itself.

## Global compatibility and mean enforcement

Periodic reconstruction still requires the global momentum compatibility

    integral beta_x p_beta dx=0.

Arbitrary beta,r,mean(p) are not automatically admissible. In particular
the rank-one mean augmentation does not eliminate that physical condition.
The inherited check of the unaugmented momentum residual is necessary
and remains present.

The nonlinear solver actually solves

    Cmom+(mean(p)-target)=0.

It subsequently allows maximum |Cmom|<=1e-8. Hence exact preservation of
the requested mean does not follow algebraically from the augmented solve
alone: a small constant residual can balance a small mean shift. The
differentiated augmented solve has the analogous issue. Its low-mode
canonical-rate comparison includes the zero mode and therefore bounds
this mismatch indirectly, but separate mean and compatibility diagnostics
make its interpretation unambiguous.

Recommended recorded quantities are mean(p_reconstructed)-mean(p_saved),
mean(p_t_solved)-mean(p_t_canonical), the unaugmented tangent residual,
and mean(beta_x p_beta). They distinguish an acceptable tolerance error
from failure of the global reconstruction.

## Cache and independent probe

The cache is explicitly recentered before each solve. It is only a Newton
initial guess if the solver remains on the same local solution branch.
The code does not prove global nonlinear reconstruction uniqueness; branch
continuation, nonzero p, convergence checks, and occasional perturbed-cache
comparisons are the appropriate local safeguards.

I mapped the existing n127/evaluation255 t=1 state to the reduced variables,
reconstructed from a constant guess, then perturbed the cache by a 1e-5
sinusoid and reconstructed again. Results:

| Probe | Maximum/error |
| --- | ---: |
| reconstructed-state difference after cache perturbation | 1.58207e-15 |
| reconstructed mean minus saved mean | -8.88178e-16 |
| tangent mean minus canonical mean rate | 1.38778e-17 |
| unaugmented differentiated-constraint residual | 6.28729e-14 |
| reduce(expand(y))-y | 8.88178e-16 |

This supports cache independence and mean preservation for that resolved
state. It is not a universal branch-uniqueness proof. The input was
`pf07/chunk127_m255_t1/result.json`; the probe used the manifest-compatible
python3 interpreter with single-thread BLAS settings. Plain `python` in
this environment selects a different SciPy installation and rejects the
old gmres `tol` keyword; the recorded python3 environment works. No code
change was needed for the probe.

For numerically exact restart claims, preserve the cached reconstructed
p as well as independent state and polarization gvar, or demonstrate
that rebuilding the cache reproduces the desired tolerance. The cache
is not independent physical data, but nonlinear stopping roundoff and
branch initialization can depend on it.

## Recorded validation and acceptance interpretation

The inspected new t=.5 reduced-versus-former comparison reports maximum
q difference 5.19e-13, lapse difference 1.37e-13, beta difference 5.76e-16,
and p_beta difference 8.57e-9. Its represented/full rate errors are
1.37e-10 and 3.13e-10. These are successful declared equivalence checks.
The validation function presently exercises t=.5; the contract's requested
t=1 comparison is a separate obligation if not recorded elsewhere.

The legacy-stop diagnostics show represented rate errors 1.53e-7 and
1.12e-7, compared with 1.59e-12 at the old t=1 reference. Those numbers
motivate a new explicitly declared formulation and its 1e-6 threshold.
They do not alter the acceptance status of a step that failed its original
raw-momentum criterion. New trajectories must satisfy the new criterion
and inherited physical spectra/domain criteria at their own accepted steps.

The rate normalization uses the maximum full canonical p_t. It should be
reported alongside absolute discrepancies so that changes in scale or
fine-only rates do not obscure the physical error. A full-grid discrepancy
need not share the represented threshold, but it must be monitored and
decrease appropriately with resolution. A growing fine-grid discrepancy
cannot be called harmless solely because p is auxiliary.

The current spectra include q,N,beta,r,p_beta. The broad phrase "every
physical field" should either be narrowed to that explicit monitored set
or supplemented with p_lambda and P/its derivative, especially when the
purpose is to assess reconstructed auxiliary tails. The expanded rate's
continuum product-rule and constraint assumptions remain in force.

## Final scope

No momentum evolution is incorrectly omitted in the proposed constrained
architecture provided the canonical tangent-rate check, periodic
compatibility, branch control, and physical convergence requirements are
retained. This review supports the formulation and its resolved validation;
it does not certify later states before their checks run. It is not a
formation, avoidance, or singular-selection result.

Independent delegated review, 2026-11-06. Reviewed reduced_system.py SHA-256:

    265aae7d039a4e4e3d14f67944421519f3d3a03bd0d6592623e126c21061bc41

## Addendum: v2/v3 and current claims

Reviewed reduced_system_v2.py and evolve_reduced_v2.py/v3.py without a new
evolution suite. The new explicit mean and unaugmented tangent checks use
the correct quantities. Six checks in reduced_validation002 pass. Restart
requires a valid checkpoint, so a stopped failing state cannot silently
be promoted into accepted data. Prolongation preserves represented modes
and the saved mean, carries gvar and the p cache, and immediately rechecks
the reconstructed state. Optional larger evaluation padding changes the
quadrature approximation and needs its declared sensitivity comparison;
it is not new independent initial data.

The inspected r511, r1023_a and r2047_b outputs fail the p_beta spectrum
criterion at their quoted times, with mean/tangent residuals still small.
r511_half passes the requested t=1.4 endpoint. STATUS.md correctly calls
these accuracy stops and identifies checkpoint-prolonged trajectories
rather than independent fine initial-data evolutions. Its open initial-
family item should now distinguish the audited small-amplitude auxiliary/
ADM construction from the still-unproved coupled local-evolution theorem.

Two minor robustness gaps remain outside the observed runs: explicitly
reject even independent n or evaluation size below n, and make failure
serialization tolerate an initial solve that fails before gvar/cached_pl
exist. The current unconditional .tolist accesses could otherwise mask
the original numerical exception. Neither changes the successful recorded
comparisons or the mathematical equation audit.

Reviewed SHA-256 revisions:

    reduced_system_v2.py 0f6d3ef85b2b147688a78f34654f1ad1f6e1d68efee65a26daa01b664d58f75f
    evolve_reduced_v2.py cc0cb6a3c555d0512c0eaef3d755cd184cc146cbaead331bb68afd01e0803229
    evolve_reduced_v3.py 535874d429520f70a6f4089cf3a06bd018a8e7b50bc168193f54b24426b66dff
