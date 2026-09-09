# IC37: finite multiplier acceleration at the activation interface

Base c23c1d7ec34f32b1c982648a27ae25ce88243115. Original full theory OPEN.
Credit: Carl Zimmerman's exponential constitutive law, vacuum-scale proposal,
and primordial-clock direction motivate this same-action construction.

## Bounded design and execution plan

Retain the IC36 results and action unchanged. Do not just repeat its RMS fit.
This turn tests the different condition Wddot+eta exp(S) ellddot=0 with finite
ellddot at the moving activation interface. The full target still includes
Dirac closure, healthy clock/tensors, PPN, cosmology, and empirical tests.

1. Build analytic directional derivatives of the existing independently varied
   metric equations and the lapse/w constraints. Evaluate the actual local
   third derivative of the fixed Hermite coefficient; do not assume a globally
   C3 coefficient. Check analytic time jets against finite differences.
2. Derive the moving-interface second derivative when W=Wdot=0 initially,
   and the exact exponentially flat activation asymptotic. A finite response
   requires Wddot=O(eta), not just a small absolute residual.
3. Integrate the lapse-acceleration equation, then use its two homogeneous
   constants to set Wddot and its first spatial derivative to zero AT the
   interface. Compute the actual response matrix and the remaining spatial
   jets independently of an assigned rank or desired determinant.
4. Test baseline and IC36-selected data, spatial degree and interval changes.
   Try selecting the remaining initial clock-rate gradient by zero interface
   curvature, then immediately inspect the next spatial jet. Preserve failures.
5. Run new scripts and relevant closure regressions; store exact commands,
   input hashes, outputs, domain/regularity caveats and terminal statuses.

No empirical fitting, altered MOND kernel, or imposed PPN/DOF result. Float64
numerical evidence is not an exact continuum no-go. An analytic-sector statement
must explicitly assume the requisite one-sided analytic extension; a C2
coefficient alone does not provide it. Lean/lake were absent from PATH at IC36.

## Exact interface obligation

Let the moving interface be r=R(t). If W(0,r)=0 and W_t(0,r)=0 on an open
initial collar, the ordinary chain rule gives

    d^2 W(t,R(t))/dt^2 |t=0 = W_tt(0,R(0)).

The other terms are 2 Rdot W_tr, Rdot^2 W_rr and Rddot W_r, all zero under
these stated hypotheses. Boundary motion therefore does not remove this
particular second-time source. This does not assume a stationary boundary.

At ell=ell_t=0 the differentiated multiplier equation is

    E(r) + eta(r) exp(S(r)) L(r) = 0,
    E=W_tt, L=ell_tt.

Set x=alpha^2-1/2 on the active side, 0<x<1/4. The actual switch satisfies

    1/eta = 1 + exp(1/x - 1/(1/4-x)),
    lim[x->0+] eta/x^p = 0 for every real p>0.

For finite S and bounded L, E=O(eta). If E has a nonzero finite Taylor jet
E(x)=a x^n+o(x^n), a!=0, this is impossible because eta/x^n ->0. In particular,
after E=E_r=0 have been matched at a regular interface with dx/dr!=0,
a nonzero one-sided E_rr rules out bounded L for those initial data.

This implication is an elementary conditional theorem; the actual field-jet
values below require numerical/regularity validation, not just that theorem.
If E has a convergent power series at the interface, bounded L forces every
coefficient to vanish, hence E identically zero locally. Do not apply this
analytic-sector statement to arbitrary smooth or merely C2 fields.

Flatness alone is NOT sufficient outside the analytic sector. The explicit
counterexample E=exp[-1/(2x)] has all power-flat limits but E/eta -> infinity.
Conversely E=-eta exp(S) L0 has the finite response L=L0. Neither example is
asserted to be a solution of the gravity action; they test the regularity logic.

## High-precision local construction and its limits

The first float64 experiment (`ic37_interface_flatness.py`) differentiates
polynomial fits of the analytic time sources. Its higher interface derivatives
are not stable under changes of degree/interval; small value-fit errors do not
certify derivative accuracy. Retain those rows as a failed numerical method,
not as the load-bearing interface result. The wider interval [2,2.003] also
crosses a coefficient join. The interface itself is inside cell 23, not on a
join; smaller one-cell audits still expose differentiation sensitivity.

`ic37_local_taylor.py` therefore constructs spatial Taylor coefficients by the
ODE recurrence, differentiates the independently varied physical time flows,
and assembles the constraint sources with high-precision mpmath arithmetic.
It does not fit sampled field values. The analytic source implementation is
checked against finite kicks of the earlier, separately compiled field flow.
The lapse boundary system is checked against hand-solved manufactured cases.

All binary-float action constants, fixed Hermite data and initial fluid c,j,w
are lifted exactly into mpmath. Redundant derived energy is recomputed as
h=exp(S)c j^(1+w), and the interface momentum is recomputed from alpha^2=1/2.
This removes inconsistent rounding of dependent quantities; it is not an
action-parameter refit. No global C3 coefficient is claimed. The local routine
rejects arguments outside the interior of its fixed coefficient cell.

Baseline and selected profiles are audited at 50 and 80 decimal digits with
four spatial derivatives of E. Initial spatial series extend through order 8.
The shift-acceleration convention is beta_t(2)=0. Boundary homogeneous data
are (A,A')=(1,0),(0,1) in physical r units; the float diagnostic instead scales
the second datum by inverse interval length. Their raw singular values therefore
use different units; neither matrix is a Poisson-bracket matrix.

The constructive search first selects U1=S_tr(2) with U0=S_t(2)=0 to cancel
E_rr. It then jointly selects U0,U1 to cancel E_rr and E_rrr. It never assigns
their values, the boundary determinant, or the remaining derivative. Both
root branches are retained, with actual search histories, numerical Jacobians
and precision checks. A remaining nonzero quartic jet still obstructs bounded
multiplier acceleration under this initial-data ansatz. The decimal residuals
are numerical evidence, not interval-certified nonzero constants.

Full outputs and the final self-review accompany the frozen execution record.
`IC38_FUNCTIONAL_COMPATIBILITY.md` goes beyond this finite-jet selection by
deriving a function-level necessary-and-sufficient operator compatibility test
on its explicitly regular domain. It does not claim that the full field
equations have thereby been solved.
