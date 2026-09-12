# Independent audit: nonlinear static clock response

**Normalized claim.** The unchanged covariant action has a well-defined
zero-spatial-clock-flux projection at a frozen coefficient state. Eliminating
that clock response modifies the scalar's quartic spatial coefficient and can
produce a nonzero stationary gradient. Does this establish a healthy nonlinear
state of the same full action?

**Primary verdict: correct only after a stated restriction.** The projected
coefficient and stationary gradient are action-derived static diagnostics.
They do not establish a solution of the nonlinear Einstein, scalar and clock
equations. More decisively, the regular nonzero stationary gradient has zero
transverse restoring coefficient in the P/W projection. For a covariantly
affine chi jet, the unchanged cubic interaction's Einstein response changes
that zero to a strictly negative transverse principal coefficient when
gamma is nonzero, X>0 and M²>0. This excludes a healthy affine realization
under the positive-kinetic hypothesis. It does not exclude a non-affine
solution with its actual covariant Hessian and curvature response.

The audit used mathbox proof-audit and computation-audit, followed by
proofread-math self-review. It did not change an old file or coefficient.
The source revision supplied to this independent pass was `1be42350b`.

## Exact claim domain and dependencies

The action is

\[
S=\int d^4x\sqrt{-g}\,[M^2(R-2\Lambda)/2+P(X,\tau)-V(\tau)
 +sW(Y,\tau)+\gamma X\Box\chi]+S_m,
\]

with signature -+++, X=-∇χ·∇χ, s=√(-∇τ·∇τ)>0,
\(n_\mu=-\partial_\mu\tau/s\), \(q=n^\mu\partial_\mu\chi\)
and Y=q²-X. In formulas below q is the physical
clock-frame chi rate; Q is the constant coordinate coefficient in χ=Qt+f(x).
They differ after tilting the clock.

Dependency graph:

1. Vary the unrestricted covariant action to obtain the clock current and
   cubic stress: internal action identities.
2. Impose the local static metric and coefficient projection: an explicit
   restriction, not a derived solution or gauge-independent reduction.
3. Use a nonzero clock Hessian to eliminate the zero-flux root: conditional
   implicit-function argument plus the clock agent's stronger branch analysis.
4. Differentiate the actual 3D invariant to test transverse perturbations:
   internal algebra, independently checked by rotational identities.
5. Eliminate the Einstein curvature term in the cubic scalar equation:
   internal covariant trace-reversal identity, with actual chi Hessian retained
   unless the affine restriction is explicitly imposed.
6. Select the archived first physical state and unchanged Model jets:
   numerical input, not a new solution after adding gradients.

All Schur statements exclude a vanishing relevant clock block. The scalar
plane-wave statements require nonzero spatial momentum. No homogeneous
constraint was inferred by dividing through momentum. Smoothness of P and W
is required through their stated derivative orders and all constitutive
logarithm and square-root domains must hold.

## 1. What the full clock equation actually says

Writing \(D^\mu\chi=(g^{\mu\nu}+n^\mu n^\nu)\partial_\nu\chi\),
unrestricted variation gives

\[
J_\tau^\mu=Wn^\mu-2qW_Y D^\mu\chi,
\qquad
E_\tau=P_\tau-V_\tau+sW_\tau-\nabla_\mu J_\tau^\mu=0.
\]

Constant gamma contributes no direct tau variation. For the flat static
ansatz χ=Qt+f(x), τ=s0t+π(x), write u=f', z=π'/s0,
r=√(1-z²), v=u-Qz and q=(Q-uz)/r. Then

\[
L=P(Q^2-u^2,\tau)+s_0rW(v^2/r^2,\tau),
\quad
J_\tau^x=-Wz/r-2qW_Yv/r^2=L_z/s_0,
\]
\[
J_\tau^0=W/r+2qW_Yzv/r^2,
\qquad J_\tau^0+zJ_\tau^x=rW.
\]

Thus a frozen-time flux equation is not itself the full tau equation. For
constant Q,s0 and static u,z, retaining the actual explicit coefficient
derivatives gives the time-current source

\[
P_\tau-V_\tau+s_0rW_\tau-s_0\partial_\tau J_\tau^0
 =P_\tau-V_\tau+s_0z\partial_\tau J_\tau^x.
\]

The partial tau derivatives on this line hold u,z fixed. The full flat
clock Euler equation can also be written

\[
E_\tau=P_\tau-V_\tau
 -(\partial_uJ_\tau^x)u'-(\partial_zJ_\tau^x)z',
\]

because the explicit coefficient part of ∂xJx cancels the displayed
s0z∂τJx term. Consequently it would be incorrect to count Wτ as an
independent unavoidable obstruction without its time-current cancellation.
If zero flux holds for the whole static spacetime rather than just one
snapshot, its explicit tau derivative must vanish too; Eτ then additionally
requires Pτ=Vτ. A shift-symmetric stationary sector with zero boundary flux
is a sufficient restricted setting in which the flux elimination solves
the clock equation. It still need not solve the scalar or metric equations.

For the archived state the origin has Pτ-Vτ=0.0141577019830257.
This is the expected homogeneous value 3H W, cancelled by cosmological
expansion in the full homogeneous equation. At the nonzero stationary
snapshot the retained time-current source is 0.0141578906219717 and
∂τJx=-6.80939785832e-6. The difference from the origin is approximately
1.88639e-7. These numbers identify the terms a full continuation must
balance. The nonzero flat source is not a counterexample to the original
FLRW solution.

## 2. Independent quartic response

At u=z=0, set p=P_X, p2=P_XX, w=W(0), d=W_Y(0), e=W_YY(0)
and S=w-2Q²d≠0. Freezing the explicit tau coefficients gives

\[
z=-\frac{2Qd}{S}u+O(u^3),
\qquad
L_{\rm eff}=L_0+c_2u^2+c_4u^4+O(u^6),
\]
\[
c_2=-p+\frac{s_0dw}{S},
\qquad
c_4=\frac{p2}{2}
 +\frac{s_0}{S^4}\left[\frac{e w^4}{2}
              +2Q^2d^3w(w-Q^2d)\right].
\]

The cubic coefficient of z(u) cancels from c4 by quadratic clock
stationarity. This independently reproduces the clock elimination route;
the bare fixed-clock quartic is a different coefficient. A sign of c4
alone does not specify a physical Hamiltonian, a constraint-compatible
background, a kinetic matrix or a characteristic cone.

## 3. The genuine 3D transverse gate

For vector gradients u and z the invariant is

\[
Y=|\mathbf u|^2-Q^2+
 \frac{(Q-\mathbf u\cdot\mathbf z)^2}{1-|\mathbf z|^2},
\qquad L=P(Q^2-|\mathbf u|^2)+s_0\sqrt{1-|\mathbf z|^2}W(Y).
\]

At an aligned background u=u e1, z=z e1, every transverse direction has
the independently differentiated 2×2 scalar/clock gradient Hessian

\[
H_{uu}^{\perp}=-2P_X+2s_0rW_Y,\quad
H_{uz}^{\perp}=-2s_0qW_Y,\quad
H_{zz}^{\perp}=-\frac{s_0}{r}(W-2q^2W_Y).
\]

When Hzz⊥≠0, its actual transverse plane-wave Schur coefficient is

\[
h_\perp=-2P_X+
 \frac{2s_0rW_YW}{W-2q^2W_Y}.
\]

Rotating both gradients gives two identities before imposing either
stationarity equation:

\[
H_{uz}^{\perp}u+H_{zz}^{\perp}z=L_z,
\qquad
H_{uu}^{\perp}u+H_{uz}^{\perp}z=L_u.
\]

Hence h⊥u=Lu-Huz⊥Lz/Hzz⊥. At any nonzero simultaneous stationary point
Lu=Lz=0 on the regular clock branch, h⊥=0 exactly. Equivalently an O(3)
pointwise reduced function F(|u|²) has transverse Hessian 2F', which vanishes
at a nonzero stationary gradient. This means two transverse spatial
stiffness eigenvalues, not two extra propagating scalar degrees of freedom.

There is a necessary integrability restriction. Pointwise vector zero flux
Jτ^i=0 is stronger than the scalar clock equation ∂iJτ^i=0, and a pointwise
map z=κ(|u|²)u need not remain curl-free for arbitrary spatial χ. For an
arbitrary wavevector k the physical scalar-clock elimination uses

\[
k^T H_{uu}k-
 \frac{(k^T H_{uz}k)^2}{k^T H_{zz}k},
\]

which is generally different from contracting k with a pointwise matrix
Schur complement. The transverse gate above survives this restriction:
for k perpendicular to the background gradient the perturbation gradients
lie in a common transverse eigendirection, so the actual clock divergence
equation gives exactly the displayed 2×2 Schur coefficient.

An independent direct-density solve locates
u=0.00153986429484530, z=-0.0159526364648014. There,

| Diagnostic | Value |
| --- | ---: |
| Longitudinal static Schur | -0.00621946148187773 |
| Transverse clock block | -0.000901498364481796 |
| Transverse static Schur | 2.46e-15, numerical zero |
| X | 0.824156842439634 |
| Y | 0.000256775615983518 |

The zero follows from the exact identities; the finite root locates one
instance and is not an interval or exhaustive root certificate.

## 4. What the unchanged cubic metric response does

The fact that γX□χ=∂x[γ(Q²u-u³/3)] under the flat 1D restriction does
not make its metric variation a boundary. Direct covariant variation yields

\[
T^{(3)}_{\mu\nu}=2\gamma\Box\chi\,\chi_\mu\chi_\nu
 +\gamma(\chi_\mu\partial_\nu X+\chi_\nu\partial_\mu X)
 -\gamma g_{\mu\nu}\nabla\chi\cdot\nabla X.
\]

On that static restriction, T00=2γ(Q²-u²)u', Tyy=Tzz=2γu²u',
and T0x=Txx=0. Restricting the density before variation would lose these
sources. Constant u makes their background values zero; perturbations
still carry the scalar-metric mixing.

Eliminating the Ricci term in
E3=2γ[(□χ)²-(∇∇χ)²-Rμν∇μχ∇νχ] using Einstein trace reversal adds

\[
\Delta Z^{\mu\nu}=-\frac{2\gamma^2X}{M^2}
 (Xg^{\mu\nu}+4\nabla^\mu\chi\nabla^\nu\chi).
\]

The script independently recomputes the transverse contraction from the
stress, rather than importing the previous debraiding implementation.
In the clock rest frame, use q=(Q-uz)/r, s=s0r and Y=v²/r². For a wavevector
perpendicular to the spatial chi gradient and a vanishing background
covariant chi Hessian,

\[
K_0=2P_X+4q^2P_{XX},\quad G_0=-h_\perp=0,\quad B_0=0,
\]
\[
\Delta K=\frac{2\gamma^2X}{M^2}(4q^2-X),\quad
\Delta G_\perp=-\frac{2\gamma^2X^2}{M^2},\quad \Delta B=0.
\]

Thus γ≠0, X>0, M²>0 and K0+ΔK>0 imply G⊥<0 and an imaginary transverse
principal phase speed. The same-root values are K0≈2.18490894553523,
ΔK≈4.07709999e-12 and ΔG≈-1.35846900188014e-12. Using the exact stationary
identity, c⊥²≈-6.21751e-13. Direct double-precision root residuals affect
the last few digits of a raw numerical G0+ΔG cancellation; they do not
decide the sign established by the algebraic identity.

No order-two P/W clock-metric contribution was omitted in this affine
principal argument: their metric terms have one derivative of the metric,
while the leading Einstein equation relates its two-derivative term to
the cubic two-derivative scalar source. Their substituted contribution
remains lower derivative order. Explicit tau jets similarly enter the
lower-order equations. This order count does not license dropping those
terms in a finite-wavelength evolution or near a cutoff.

For a nonzero background covariant Hessian Hμν=∇μ∇νχ, the scalar principal
tensor also receives

\[
Z_H^{\mu\nu}=4\gamma[(\Box\chi)g^{\mu\nu}-H^{\mu\nu}].
\]

These terms are first order in gamma and can dominate the displayed
gamma-squared shift. The stationary snapshot has not solved for Hμν,
metric responses, matter responses or the nonzero harmonic constraints.
The affine conditional exclusion cannot be promoted to a no-go for the
full FLRW continuation, or to an instability below a known EFT cutoff.

## Obligation matrix and remaining gap

| Obligation | Audit status |
| --- | --- |
| Exact static projected quartic | Passed |
| Full clock current and explicit-tau cancellation | Passed |
| 3D transverse Hessian and legitimate transverse plane-wave reduction | Passed |
| Finite nonzero stationary root and nonzero transverse clock block | Numerical, one archived state |
| Affine Einstein feedback sign at a regular stationary root | Passed, conditional on the stated affine/kinetic hypotheses |
| Arbitrary-angle pointwise local reduced action | Not established; curl-free/clock-divergence distinction is necessary |
| Coupled background and nonlinear constraint solution at the root | Not addressed by the static projection |
| Actual non-affine finite-wavelength characteristic cone | Incomplete |
| Nonlinear stability, cutoff and observational law | Out of scope |

The smallest next implication is to solve the same-action constraint and
preservation equations for a finite-gradient continuation, retaining the
actual homogeneous and second-harmonic responses and its covariant chi
Hessian, then insert that Hessian into the full principal tensor. A new
quartic fit or another static root scan does not supply that implication.

Reproduction: `python3 -B review/derive_audit.py` from this experiment's
directory. The script performs 32 exact checks and one independent
double-precision numerical stationary-root diagnostic. Its optional
`--output` records JSON. Inputs are the unchanged `constitutive.py` and
the archived `inhomogeneous_charge_2026/exterior/run_001/result.json`.
The parent experiment's bounded run supplies the final argv, software,
hashes, logs and resource record. No external theorem or empirical input
was required for these identities.

Proofread scope: this report only; routine notation clarification during
drafting; no unresolved local mathematical-token or cross-reference issue.
