# IC33: restore the independent tracefree metric evolution

Base: 42716b2a63d10f8bcdd5bbbd4c7c49647bedbd73, 2026-09-09.
Original full-theory target: **OPEN**. Self-review; not a novelty or formal proof certificate.
Credit: Carl Zimmerman's exponential constitutive law, vacuum-scale relation,
and primordial-clock direction motivate this same-action construction.

## 1. Why a passing constraint test was insufficient

IC32 tested a tangent to the constraints and used shdot(2)=0 as boundary data.
It did not independently vary the anisotropic spatial metric. In a spherical
exterior, momentum preservation fixes the shear rate only up to C(T)/r^3
on the initial spatially constant-Q slice. A free choice of that integration
constant need not solve the tracefree metric Euler equation.

IC33 retains independent barred radial and angular metric fields BEFORE variation:

    hbar_ij = diag(exp(2a), r^2 exp(2b), r^2 sin(theta)^2 exp(2b)),
    J = r^2 exp(a+2b),
    pi^i_j / volume = diag((q+2sh)/3, (q-sh)/3, (q-sh)/3).

All remaining fields and coefficient functions are the IC29/30 action's fields.
In particular v=m exp(S+2w)/2, t=exp(2S)/v, xi=S+w,
u=(S+2w)/(S+w). The complete radial density, omitting the angular factor 4pi, is

    L/J =
      2(q+2sh) adot/3 + 4(q-sh) bdot/3
      -2t sh^2/3 + t q^2/6 + A q z + exp(S) P0 + D z^2 + E4 z^4
      + eta exp(S) ell(w-wc)
      -2(q+2sh)(beta' + beta a')/3
      -4(q-sh) beta(b'+1/r)/3
      + v Rbar + 2v exp(-2a)[2u xi xi' u' + xi^2 u'^2].

P0 and the activation eta are unchanged from ic30_radial_bridge.radial_action.
The curvature is

    Rbar = exp(-2a)[-4b''-6b'^2+4a'b'+4a'/r-12b'/r-2/r^2]
             +2 exp(-2b)/r^2.

The code checks this against IC30's independently constructed Christoffel/Ricci
calculation. Substitution a=b=Q reduces this full action to IC30's action up to
the explicitly checked radial boundary derivative. Agreement of actions after
gauge fixing alone is not used as proof that no metric equation was lost.

## 2. Independent metric equations

The time Euler terms, not just spatial variations, are

    d/dT (dL/dadot) = 2J[qdot+2shdot+(adot+2bdot)(q+2sh)]/3,
    d/dT (dL/dbdot) = 4J[qdot-shdot+(adot+2bdot)(q-sh)]/3.

After varying, impose a=b=Q and the active pin w=wc, eta=1. Define

    h = -t q^2/6 - A q z - exp(S) P0 - D z^2 - E4 z^4,
    HQ = h_q/2,
    B = 2v(1-u^2),
    div_beta = beta' + 3 beta Q' + 2 beta/r.

The q variation gives Qdot=HQ+div_beta/3. The shear variation gives
beta'-beta/r=-t sh. With that shear gauge equation, the metric trace gives

    qdot = beta q' -3h/2 + t sh^2
      + exp(-2Q)/2 [
          -2v Q'^2 -4v S' Q' +(B-4v)S'^2
          -4v(Q''+S''+2(Q'+S')/r)
        ]
      + matter_trace.

The independently obtained tracefree equation is

    shdot = beta sh' -3 HQ sh
      + exp(-2Q) [
          v(Q''+S''-(Q'+S')/r-Q'^2-2Q'S')
          +(v-B)S'^2
        ]
      + matter_tracefree.

These expressions retain Q', q', and Q''. They are not IC32's homogeneous-in-space
initial equations reused at later times. The numerical evaluator uses the actual
varied equations; the displayed simplified trace formula is compared only after
using the shear gauge equation. An initial check without that restriction found
the omitted residual -2 sh(beta'-beta/r+t sh); the hypothesis is now explicit.

## 3. Matter stress is varied independently

For one minimally coupled fluid write its lapse-weighted Hamiltonian per barred
volume as H(j,k), where j=Pi/J and k=exp(-2a)(sigma')^2. Here k denotes the squared
spatial gradient, not a Fourier wavenumber. Variation at fixed Pi and sigma gives

    Ea_m/J = -H+j H_j+2k H_k,
    Eb_m/J = 2(-H+j H_j).

Consequently

    matter_trace     = 3(j H_j-H)/2 + k H_k,
    matter_tracefree = k H_k.

For the same constant-equation-of-state fluid as IC32,
H_j=exp(S) v_f and H_k=exp(S)j/(2v_f), where v_f is its normal velocity,
not the gravitational coefficient v. Thus a generated fluid spatial gradient
contributes anisotropic stress; it cannot be dropped in a later-time evolution.
Both general Hamiltonian variation identities are tested symbolically.
The ordinary covariant matter Ward identity is not replaced by these radial equations.

## 4. Evidence and constructive repair

The frozen IC32 calculation is preserved, not overwritten. Its numerical control
is rerun here with the repaired fixed 81-node coefficient function.

For the standard initial exterior, the independently varied action requires
shdot(2) approximately -1.87221877524, while IC32 chose zero. At twice the
tail amplitude the action gives approximately -3.79172304752. Model units only.
The difference between the two shear rates is numerically C/r^3: it is precisely
the integration constant that differentiated momentum preservation could not fix.
The homogeneous zero-tail control has no significant discrepancy.

The repair is to derive shdot(2) from the full metric equation and carry that
value through momentum preservation. Re-solve lapse preservation with this new
shear source; propagate z, ell, and beta with their differentiated equations.
Keep the action, coefficient function, sources, and spatial boundary conventions
otherwise unchanged. No source refit or new free coupling is introduced.

The new driver compares its entire shear-rate profile with the full metric
Euler equation at nodes AND midpoints. It then tests lapse and momentum
preservation and unprojected Euler kicks dt=.001,.0005,.00025. The full fluid
Legendre transform includes the gradients produced by those kicks. Constraint
errors after the kicks are evaluated without solving the gravitational
constraints again. Actual outcomes belong to ic33_run_001, not to this pre-run
contract.

The 1601-node amplitude-1 repair missed the 1e-7 shear-equation tolerance:
its maximum node/midpoint defect was 1.3735771631218086e-7. It remains a coarse
control. The selected refined tests use 3201 nodes for amplitudes 1 and 2,
and 6401 nodes for the amplitude-2 refinement. The tolerance is not relaxed;
refinement must reduce the independently evaluated shear-equation defect.

The lapse boundary conditions Sdot'(2)=0 and Sdot(8)=Sbar_dot are still diagnostic
exterior boundary choices, not derived galaxy-to-cosmology matching conditions.
Their replacement by physical matching data remains necessary.

## 5. Audit verdict and remaining goal

Claim reviewed: IC32's chosen tangent is a solution of all metric evolution equations.
Verdict: **refuted in its nonzero-tail tests**. The narrower claim of a tested
constraint-preserving tangent survives. IC32 itself did not certify a full theory;
this audit prevents that narrower result from being promoted incorrectly.

Dependency chain:
full phase action -> independent a,b variation -> isotropic active-pin equations
-> comparison with IC32 boundary rate -> action-determined repair -> finite tests.
Exact symbolic equalities establish the local algebraic implications. Numerical
BVPs and finite-kick ratios remain finite floating-point evidence.

The corrected tangent is still not a many-step spacetime solution. The next step
is general inhomogeneous evolution using BOTH independently varied metric
equations and generated matter stress, checking constraints at every stage and
against refinement. Thereafter the active-pin/unpinned-MOND connection, global
coefficient regularity, full functional Dirac closure including k=0 and y=0,
all-mode health/causality/strong coupling, full PPN, and empirical cosmology,
galaxies, binaries and clusters remain obligations from the original target.

No Lean toolchain is on the checked PATH; no formal certificate is claimed.
No new empirical data were fitted and the factor 1/2 in the scale relation
remains input, not a derived prediction.
