# A finite wall needs a different constraint transition

2026-10-15. This continues the [infinite-medium wall theorem](../cold_3d_wall_2026_10_14/PROOF.md). It rules out a particular simple localization and gives exact tensor matching conditions. A physical cold-energy carrier, finite vacuum interface, and powered spacecraft solution remain unestablished.

## Precisely specified localization

Place the phase boundary in a flat collar outside the curvature-supporting wall. In a local rest chart set b=0, H_AB=0. Multiply **all** non-Einstein stabilizers of the previous construction by a smooth material-coordinate window p(Φ), with 0≤p≤1: the strain mass terms, normalized expansion square, acceleration square, and κ=4 derivative elasticity (spatial coefficient 1/2). Keep the Einstein term unchanged. At p=1 this recovers the flat limit of that medium; at p=0 it is ordinary Einstein gravity in this sector. The window is a prescribed constitutive profile, not a new independently stabilized phase field. Adding such a field would require another analysis.

This collar remains an exact flat background: all multiplied densities and their first variations vanish there. Spatial variation of p does not by itself create a background surface stress. It does affect perturbation equations. This observation is insufficient for stability.

Units below are Mp=1 and D=1, so k is dimensionless momentum in inverse medium length units. Restoring dimensions replaces k² by D times physical momentum squared in the homogeneous formulas. These are statements about a postulated continuum action; no microscopic cutoff or material realization has been supplied.

## Scalar constraint calculation

For a homogeneous collar value 0<p≤1 choose propagation along z and scalar metric velocity Qdot=diag(a,a,c). Choose the real Fourier phase of the longitudinal shift v so that its contribution to the extrinsic-curvature numerator is −2kv. The quadratic kinetic/shift Lagrangian is

\[
L_{\rm kin}={2a^2+(c-2kv)^2-(2a+c-2kv)^2\over8}
+{p\over8}(2a+c-2kv)^2
+{p\over2}(2a^2+c^2)+2pv^2.
\]

The lapse has positive quadratic coefficient p(1+k²)/2 and no velocity coupling on this flat background. Eliminating it cannot repair a negative velocity eigenvalue. The longitudinal shift is a positive auxiliary with coefficient p(k²+4)/2. Its minimizer is

\[
v_*={k[2(p-1)a+pc]\over2p(k^2+4)}.
\]

Define the reduced scalar kinetic matrix by Lred=(a,c)K(a,c)^T/2. Direct differentiation gives

\[
K=\begin{pmatrix}
{2k^2p^2+\frac32k^2p-k^2+12p^2-2p\over p(k^2+4)}&{2(p-1)\over k^2+4}\\
{2(p-1)\over k^2+4}&{p(k^2+5)\over k^2+4}
\end{pmatrix},
\]

\[
\det K={k^2(4p^2+3p-2)+28p^2-p-2\over2(k^2+4)}.
\]

Since Kcc>0, negative determinant proves one physical scalar velocity has negative kinetic energy in the homogeneous medium. At k=0 positivity requires p>2/7. At arbitrarily large momentum the stricter necessary threshold is

\[
p\ge p_{\rm UV}={\sqrt{41}-3\over8}=0.425390529679106\ldots .
\]

For p<pUV the determinant is negative at sufficiently large finite k. At p=1/4 it is exactly −(2k²+1)/[4(k²+4)], negative for every k. This is a kinetic failure, not merely an unfavorable static potential.

The limiting coefficient for c=0 is Kaa→(4p²+3p−2)/(2p). Thus the problem is local in a smooth taper, rather than a consequence of imposing a large periodic box. In an open collar patch with p bounded strictly between zero and pUV, take a compact smooth velocity envelope times cos(kz), c=0, and a compact longitudinal shift with the local leading minimizer v=(p−1)a/(pk), with its corresponding sine phase. Envelope and coefficient derivatives in the shift gradient are O(1/k). The leading quadratic integral is negative and remains negative for sufficiently large k. Transverse shift derivatives vanish in this limit. The lapse can be set to zero in this kinetic trial.

The integrated shift-only quadratic form is nonnegative: the Einstein contribution is the nonnegative transverse-gradient form after integration by parts, and the added terms are p(div v)²/2+2p|v|². Hence minimizing over auxiliaries cannot make this negative trial positive. Wherever a reduced kinetic form exists, it has a negative direction. The exterior can have gauge null directions at p=0; that degeneracy supplies no positive-energy estimate and must be handled by constraints rather than division by p. The wave-packet argument applies in the continuum and inside a genuinely flat collar. A finite microscopic momentum cutoff could prevent access to the asymptotic regime in a thin collar; no such cutoff or ultraviolet completion has been constructed here.

**Conclusion:** simultaneously and continuously tapering the old stabilizers to zero in a flat collar fails the positive kinetic-energy requirement. This does not refute every finite medium or every alternate covariant action.

## Why changing the taper schedule alone is difficult

More generally let θ multiply the normalized expansion square and κ multiply the derivative elastic kinetic term. At zero momentum an isotropic velocity Qdot=sI has

\[
L_{\rm kin,iso}={3\over8}(\kappa+3\theta-2)s^2.
\]

While a positive lapse/shift mass keeps those fields auxiliary rather than restoring Einstein constraints, κ+3θ<2 gives a negative homogeneous trace kinetic direction. A continuous route from (θ,κ)=(1,4) to (0,0) crosses this threshold. Thus the strain mass cannot simply stay positive until after the regulators are switched off. This is a necessary local condition, not a complete classification: a proposed route must restore the relevant constraint before the negative trace becomes physical, or retain another healthy kinetic construction. At zero mass the rank and gauge structure change, and the above positive-mass Schur formulas must not be continued by division through zero.

An abrupt material boundary is another separate possibility. It needs variational boundary conditions and a joint scalar/vector/tensor boundary energy analysis. The tensor calculation below cannot supply that missing proof.

## Tensor matching actually works in isolation

For a planar collar p=p(z), the tangential off-diagonal tensor h=Qxy(t,z) decouples at quadratic order. Its action is

\[
L_T={1\over2}[A(z)\dot h^2-B(z)(h')^2-C(z)h^2],\qquad
A={1+4p\over2},\quad B={1+2p\over2},\quad C={2p\over D}.
\]

The field equation is A hddot−(Bh′)′+Ch=0. For stationary 0≤p≤1,

\[
E_T={1\over2}\int[A\dot h^2+B(h')^2+Ch^2]dz
\]

is positive and conserved with vanishing boundary flux. At a sharp interface without an additional surface action, finite-energy weak solutions satisfy continuity of h and Bh′. For a propagating monochromatic wave, ki²=(Ai ω²−Ci)/Bi and Zi=Bi ki. Reflection and transmission amplitudes are r=(Z1−Z2)/(Z1+Z2), t=2Z1/(Z1+Z2), and r²+(Z2/Z1)t²=1. The flux formula assumes real positive ki on both sides; below a gap one must treat evanescent waves instead. Exterior p=0 has luminal tensor propagation; p=1 gives the previously derived speed squared 3/5 and gap 4/(5D).

This supplies a healthy tensor-only interface, while the simultaneous taper still fails in its scalar sector. A successful polarization check is not a full gravitational constraint audit.

## What localized control would physically do

In a flat patch the postulated canonical controller obeys Fc²(Λddot−∇²Λ)=J. Multiplying by Λdot and integrating gives dEΛ/dt=∫JΛdot minus outward scalar-wave energy flux. The optical portal supplies a contribution J=gp W E²/2, as derived in the [previous pump construction](../cold_3d_wall_2026_10_14/PUMP.md). This is an energy input, not a speed command. A pump confined to a cavity necessarily creates gradients and outward disturbances unless separately confined. A spatially uniform finite-time change across infinite space still costs infinite energy.

With the optional postulated payload mass m(Λ), the payload force is −(gμν+uμuν)∂νm. The same interaction contributes the reciprocal localized scalar source. The field, source apparatus and payload exchange momentum. A symmetric pump around a centered, initially stationary test payload gives no direct scalar-gradient acceleration at its symmetry center. Directed control must break that symmetry and include the source/field reaction. For an isolated complete system, a net final craft momentum requires opposite momentum in escaping radiation/matter or another external system; internal state changes alone do not supply it. This statement assumes an acceptable asymptotic conserved momentum and includes the entire device. That charge has not been derived for the present exotic wall action.

A geometrically comoving test worldline in an assigned bubble metric remains a kinematic construction. It becomes a propulsion mechanism only after the finite interface, powered time-dependent field equations, and payload backreaction are solved together. This checkpoint has not done that.

## Evidence and next decisive construction

The exact SymPy run [v2 results](run_v2/calculation/results.json) verifies 14 algebraic identities, including an independent completed-square check of the shift elimination and tensor flux conservation. [v1 stderr](run_v1/stderr.txt) preserves a failed hand-entered p=1/4 benchmark; the reduced matrix and determinant were unchanged, and v2 corrects that benchmark arithmetic. This is a self-review, not an independent referee report. Symbolic checks do not establish a physical material or replace the separately stated wave-packet argument.

The next useful candidate must specify a constraint-restoring boundary or a different finite-phase action; then its full reduced quadratic kinetic and boundary flux forms must be evaluated. Reusing the old coefficients with a smooth common window is now excluded in the stated continuum collar setting. The research goal remains open, with a more precise construction requirement rather than a claimed engine.
