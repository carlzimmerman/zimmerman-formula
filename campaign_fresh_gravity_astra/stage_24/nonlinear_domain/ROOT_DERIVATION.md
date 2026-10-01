# Exact Q energy is not controlled by the completed crossing form

2026-09-30 18:31 UTC pass. Proof-only, fixed before new worker/auditor proofs
or formula previews. Common task037 proposes singular/concentration tests.
Use the FGF035 crossing and FGF036 weighted form on one fixed selected short
interval I=(-l,l), with positive bounded a(x), bounded background g=phi_x,
positive bounded rho, and signed source B=sgn(g)b(|g|,a), B_x=C rho.
C=4piG. Scale and fluid density are fixed in the main counterexamples.

## Exact growth and finite-energy domain

For s>=0 and a>0 the actual Q inverse obeys

s-a/2 <= b(s,a)=(sqrt(a²+4s²)-a)/2 <= s.

Integrating from zero gives

s²/2-as/2 <= W(s,a) <= s²/2,
W(s,a) >= s²/4-a²/4, and W>=0.                               (1)

The second lower bound uses (s-a)²>=0. All are global bounds, not a deep-MOND
expansion extended to arbitrarily large gradients. Therefore on a finite
interval with bounded a, integral W(|v|,a) is finite iff v is L2. If g is
the fixed finite-energy background, then integral W(|g+psi_x|,a) is finite
iff psi_x is L2. On the absolutely continuous zero-wall weighted domain,
this means precisely psi in H1_0. This classification is for the fixed-a
potential slice, not an asserted classification of every full matter/scale
state. Other static terms are finite on that slice because rho and psi are
bounded and scale is unchanged.

For an arbitrary AC zero-trace psi in X_A, B psi_x is integrable: B is bounded
and psi_x is L1. Integration by parts with B_x=C rho gives

integral rho psi = -(1/C) integral B psi_x.

The EXACT full static energy increment on this fixed-density/fixed-scale slice
is consequently

DeltaE[psi]=(1/C) integral [W(|g+psi_x|,a)-W(|g|,a)-B psi_x].       (2)

This is also meaningful as an extended nonnegative value if the new field
energy is infinite. The even signed-gradient function W(|g|,a) is convex,
so its tangent-subtracted integrand is nonnegative. No cancellation of
infinities or omission of the matter interaction is used. This is the signed
MOND flux equation; substituting phi_xx=C rho would invalidate (2).

## A direction allowed by the linear form but not the nonlinear energy

By FGF035, A~A_* sqrt(|x|), A_*>0, so 1/A is integrable but 1/A² is not.
Choose smooth P equal to a nonzero constant near zero and adjust it away
from zero so integral P/A=0. Define psi(x)=integral_-l^x P/A. Then psi has
zero outer traces, is bounded and AC, and

integral A psi_x²=integral P²/A<infinity,
psi_x=P/A not in L2.

Thus (0,psi,0) belongs to the full LINEAR form domain V, whereas for EVERY
nonzero real epsilon, g+epsilon psi_x is not L2 and
DeltaE[epsilon psi]=+infinity by (1),(2). The weighted norm can be made
arbitrarily small by scaling epsilon. The full nonlinear energy is therefore
not a finite-valued function on any V-neighborhood of the background.

This example only requires the form domain. If the stronger operator-domain
control of FGF036 is used, choose d=rho(c-psi)/cs² with c the rho-weighted
mean of psi and xi=-rho^-1 integral d. It gives h=cs²d/rho+psi=c, eta=0
and the same P. The associated d is bounded and zero integral. The exact
Eulerian path rho_epsilon=rho+epsilon d remains positive and mass-preserving
for sufficiently small epsilon. Its matter/internal/interaction energies stay
finite, while its field energy is still infinite. This is not an assertion
that additive density is a finite material-displacement map. It is an allowed
positive fixed-mass density path with the prescribed tangent. In either
version the tangent's nonlinear finite-energy admissibility fails.

## Smooth concentration control: no infinite-gradient state is required

Fix dimensionful L_ref>0 and Psi_ref>0 (length and potential units), and a
nonzero smooth f compactly supported in (-1,1). Let delta>0 be dimensionless,
small enough that L_ref delta<l, and choose ONCE beta=3/8. Set

psi_delta(x)=Psi_ref delta^beta f(x/(L_ref delta)),
h_delta=psi_delta_x=(Psi_ref/L_ref)delta^(beta-1) f'(x/(L_ref delta)).

Every psi_delta is smooth, zero at the original walls, with unchanged positive
rho and unchanged scale. Mass is unchanged. Define I0=integral f'^2>0 and
I1=integral sqrt(|y|) f'^2>0. The exact asymptotics are

||h_delta||_2²=(Psi_ref²/L_ref) I0 delta^(2beta-1),
||psi_delta||_2²=Psi_ref² L_ref integral f² delta^(2beta+1),
Q[0,psi_delta,0]=(Psi_ref² A_*/(C sqrt(L_ref))) I1
                                      delta^(2beta-1/2)(1+o(1)). (3)

For the last formula use A(L_ref delta y)/sqrt(L_ref delta)->A_*sqrt(|y|)
with a dominating constant times sqrt(|y|) on the fixed support. This follows
from the crossing asymptotic and continuity; the single point y=0 has no
contribution. Thus the V norm tends to zero: Q scales as delta^(1/4), and
||psi_delta||_2² as delta^(7/4). The ordinary gradient square instead grows
as delta^(-1/4). Uniform potential smallness does not imply small gradients.

Use the global (1), specifically |W(s,a)-s²/2|<=as/2. Over the shrinking
support, bounded a and background g=O(sqrt(|x|)) give

integral a|h_delta|=O(delta^beta),
integral |g h_delta|=O(delta^(beta+1/2)),
integral g²=O(delta²), integral W(|g|,a)=O(delta^(5/2)),
integral |B h_delta|=O(delta^(beta+1)).

Outside the support the increment is zero. Comparing these terms with the
leading delta^(2beta-1) term at beta=3/8 proves

DeltaE[psi_delta]=(Psi_ref²/(2C L_ref)) I0 delta^(-1/4)(1+o(1))
                  -> +infinity.                                (4)

Each energy is nevertheless finite. This is an analytic limiting family,
not sampled data or a numerical asymptotic fit. Equation (2) retains the
exact matter contribution and equilibrium linear cancellation throughout.
Although the BACKGROUND is deep-MOND at the crossing, the concentrated
perturbation reaches large gradients: using W~s³/(3a) for it would be wrong.

The Taylor convention is Q=d²E and H2=Q/2. Combining (3),(4),
DeltaE/(Q/2) is asymptotic to a positive constant times delta^(-1/2).
Consequently neither continuity of exact energy in the V topology nor a
uniform remainder DeltaE-Q/2=o(||u||_V²) holds, even when restricted to smooth
finite-energy perturbations. No finite local inequality DeltaE<=K Q can
hold on that slice. These smooth perturbations are not small in H1 or in
exact energy, so the result does not demonstrate growth from physically
small-energy initial data or dynamical instability.

## Precise surviving result and stop rule

FGF036's positive closed linear form, transmission operator and conservative
linear evolution remain mathematically valid. What fails is using this entire
completed space as a nonlinear finite-action neighborhood or promoting its
quadratic control to nonlinear stability. The fixed-a potential slice needs
at least H1 for finite exact energy. This is not a proof of a twice-Frechet
Taylor theorem on H1, preservation of H1 under the weighted linear flow, a
nonlinear inverse theorem, or any nonlinear Cauchy result. No ghost or
ill-posedness conclusion is drawn from this topology mismatch.

Both positive reference a0 values, 9.3619e-11 and1.1279e-10 m/s², enter their
own fixed background and A_*; the proof does not fit or identify them. All
scaling uses signed Q flux, with C and physical bump units explicit.
Constant-vacuum reference, frozen a0 E(z), E²=.315(1+z)^3+.685, and actually
evolving H remain distinct. A varying reference still needs its physical
work reservoir; locally responsive a is an added diagnostic assumption.
No RAR/M/filtered-MONO, metric/photon/DOF, calibrated cluster or novelty claim.

This closes the attempted nonlinear interpretation of the bare weighted norm:
it is disproved, not merely numerically untested. No further concentration
exponent sweep or reproof of weighted positivity can remove it. Any continuation
must change the nonlinear topology or physical mechanism explicitly, and
must independently verify its domain and conservation before claiming stability.
