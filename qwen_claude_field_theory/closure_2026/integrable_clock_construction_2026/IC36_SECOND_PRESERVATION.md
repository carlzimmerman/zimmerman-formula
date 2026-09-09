# IC36: second-preservation compatibility of the IC35 collar

Base: fef9aa6ca058522ae8e6c846f1df0fd53c86d99b. Full theory OPEN.
Carl Zimmerman's exponential kernel, vacuum-scale proposal, and primordial-clock
direction motivate this construction. No novelty or empirical-fit claim.

## Authorized bounded design and execution plan

Continue the existing IC35 experiment without changing its action or coefficients.
The research question is whether its selected first time jet extends to a second
time jet with w=wc and ell=elldot=ellddot=0. Failure is restricted to these data
and this multiplier ansatz, not a no-go theorem for the action.

1. Test polynomial spatial differentiation, a manufactured compatible and an
   incompatible pair of second-order equations, and the generated fluid flux.
2. Reconstruct the IC35 dense initial fields and first-preservation-selected
   profile. Retain independently varied IC33 physical metric velocities.
3. Differentiate these physical velocities along the actual first jet, including
   shift-gauge preservation and ordinary-fluid density/gradient response. Do not
   freely assign qddot or project physical momenta back onto the constraints.
4. With lapse acceleration initially zero, evaluate the second directional
   constraints along the resulting quadratic time curve. Compare time-difference
   steps and spatial polynomial orders; explicitly inspect coefficient cells.
5. Solve the lapse second-preservation equation for a particular solution and
   its two homogeneous solutions. Test the independent w equation against that
   two-parameter family. Compute singular values/rank, never assign them.
6. Preserve results and failures with provenance, run relevant regressions, and
   record the next implication. This is not full nonlinear evolution or Dirac
   closure, and no test exit status certifies the full gravity target.

Float64 exploratory computation, fixed 81-node C2 coefficient representation;
no assumption of globally existing third derivatives at coefficient joins.
Resource intent: bounded individual runs, one numerical-library thread, no
external data or parameter fit. Lean/lake were not found on PATH this turn.

## 1. Exact second-jet obligation

Write C for the total lapse constraint and W=W_vac-p_w for the unmultiplied
clock-sector equation. The latter obeys

    W + eta exp(S) ell = 0.

At the IC35 initial data w=wc, wdot=0, ell=elldot=0, its second time derivative
on the active branch is

    Wddot + eta exp(S) ellddot = 0.

This experiment imposes the additional restriction ellddot=0. The inactive
side is also held at w=wc through second order. Neither restriction is
necessary for every solution of the action. A finite nonzero multiplier
acceleration instead requires Wddot=O(eta), with the undivided equation used
near eta=0. No floating residual divided by tiny eta is a regularity proof.

Eliminate z by its actual convex cubic Aq+2D(S)z+4E4z^3=0. For either reduced
constraint F and a physical quadratic time curve, the chain rule gives

    Fddot = DF[Xddot] + D^2F[Xdot,Xdot].

Only A(r)=Sddot(r) is undetermined at this order. Qddot, qddot and shddot are
directional derivatives of the independently varied IC33 equations along
the IC35 first jet. They are NOT free profiles or fitted constraint data.
Consequently the simultaneous second-preservation equations take the form

    c2 A'' + c1 A' + c0 A + FC = 0,
    w2 A'' + w1 A' + w0 A + FW = 0.

The coefficients c_i,w_i are exactly the coefficients multiplying Sdot and
its derivatives in IC35 after eliminating zdot. Sources FC,FW are computed
from the quadratic time curve with A=0, including physical accelerations.
The symbol A in this section means lapse acceleration, not the action's
fixed mixing coefficient named A in the implementation.

On a regular interval c2!=0, any two solutions of the first equation differ
by a solution of its homogeneous second-order equation. Thus its solution
family consists of a particular solution plus two independent initial-data
directions. The script integrates all three and evaluates the second equation
on them. Its two homogeneous constants are fitted with all audit points,
without imposing preferred lapse-acceleration boundary values. Singular
values and rank are computed on the column-normalized response matrix with
relative least-squares cutoff 1e-11. This matrix is NOT a Poisson matrix.

This is a necessary compatibility test in the continuum formulation. Its
floating, polynomially interpolated implementation supplies bounded numerical
evidence, not an exact nonexistence proof.

## 2. The ordinary-fluid contribution cannot be frozen

For each same-action fluid, let j=Pi/J, g=sigma', J=r^2 exp(3Q), and let v_f
be its normal field velocity. The canonical equations imply

    jdot = beta j' - 3HQ j + J^-1 [J exp(S-2Q) j g/v_f]',
    gdot = [exp(S) v_f + beta g]',
    HQ = Qdot - (beta'+3 beta Q'+2 beta/r)/3.

Initially j is spatially constant and g=0, so jdot=-3HQ j, but gdot generally
does not vanish. Differentiate BEFORE imposing those initial conditions:

    jddot = beta (jdot)' - 3 HQdot j - 3 HQ jdot
          + exp(S-2Q) j/v_f [gdot' + (2/r+Q'+S') gdot].

The script verifies this identity symbolically, including the initially
vanishing contributions from time derivatives of the flux coefficients.
It then uses the full timelike Legendre transform at the kicked states.
Because the fluid constraint terms are even in g and g=0 initially, gddot
does not contribute to their second time derivatives; the gdot^2 terms DO.

The differentiated shear gauge is

    betadot' - betadot/r = -t (shdot + sh Sdot),
    t = 2 exp(S-2wc)/m.

Its integration constant sets betadot=0 at the audit interval midpoint.
This is a coordinate convention, not a physical source or fitted coefficient.

## 3. Accuracy and constructive repair checks

The baseline is the IC35 width .006 collar, slope q'(2)=-100,
Sdot(2)=Sdot'(2)=0. Compare polynomial degrees 8,12,16 on 65 Chebyshev audit
points; second-directional steps 2e-4,1e-4,5e-5; physical-flow differentiation
steps 1e-4 and 5e-5. A quadratic time curve with the solved lapse acceleration
independently checks the inferred second-constraint response. This is not
many-step evolution and is not an interval error enclosure.

Record coefficient cells and crossings for BOTH uncorrected and corrected
time kicks. The fixed coefficient is globally C2; do not assign global third
derivatives. One-sided subintervals (1.9972,1.999) and (2.001,2.0028) test
whether a discrepancy survives away from coefficient joins.

Retain baseline failures. Explore unused initial data Sdot'(2)=-100,-10,10,100
without changing the action, and minimize the second-preservation RMS residual
over each of [-10,0] and [0,10]. The search uses degree 8 and 33 nodes, at most
18 bounded-optimizer iterations and x tolerance 1e-3. Recheck selected data
at degrees 8/12, 65 nodes and smaller directional steps. Initial-data tuning
is a construction search, not an empirical fit, a novelty claim or proof of
an exact solution. A finite minimum is not a universal lower bound.

## 4. Gates not replaced by this experiment

Full functional Dirac closure; a healthy explicitly counted clock; zero-field
and homogeneous modes; PPN and measured G; tensor/scalar/vector stability and
causality; a physical galaxy-to-FLRW match; pre-recombination perturbations and
empirical CMB, galaxy, binary and cluster tests all remain obligations. The
vacuum-scale coefficient 1/2 is still imposed. No claim is transferred from
another candidate to fill a missing gate.
