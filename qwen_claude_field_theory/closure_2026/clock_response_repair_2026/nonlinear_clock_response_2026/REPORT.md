# Nonlinear clock response: construction and obstruction

Status: **OPEN**, not a complete or Lean-certified theory of gravity.
This checkpoint constructs second-order constrained initial data from the
unchanged action, and falsifies a restricted affine saturation mechanism.
It does not fit new coefficient functions or import another model's successes.

## Same action and actual state

With signature (-+++), the tested action is

\[
S=\int d^4x\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
 +P(X,\tau)-V(\tau)+sW(Y,\tau)+\gamma X\Box\chi\right]+S_m,
\]

where \(X=-\nabla\chi\cdot\nabla\chi\),
\(s=\sqrt{-\nabla\tau\cdot\nabla\tau}\),
\(n_\mu=-\nabla_\mu\tau/s\), and
\(Y=(g^{\mu\nu}+n^\mu n^\nu)\nabla_\mu\chi\nabla_\nu\chi\).
The original logarithmic P, square-root W and V are loaded from
`../nonlinear_evolution_2026/constitutive.py`; no coefficients are reconstructed.

All reported numerical witnesses use the archived first sourced state:
\(Q=0.9078321505772312\), \(s_0=1.0317810692809903\),
\(H=0.5191118192004086\), \(a=M^2=1\), \(\gamma=10^{-6}\),
\(\Lambda=0.7\). This is a dimensionless test history, **not a calibrated
recombination background**. The physical Q is not the constitutive reference
history \(\bar q\).

## 1. Clock response really reverses the bare quartic sign

For the restricted frozen-metric, frozen-coefficient static experiment,
\(\chi=Qt+f(x)\), \(\tau=s_0t+\pi(x)\), let
\(u=f'\), \(z=\pi'/s_0\), \(|z|<1\). Then

\[
L=P(Q^2-u^2)+s_0\sqrt{1-z^2}\,
 W\!\left(\frac{(u-Qz)^2}{1-z^2}\right).
\]

Variation gives \(\partial_xL_z=0\); the tested zero-flux branch has
\(L_z=0\). Write \(p=P_X\), \(d=W_Y\), \(w=W\), \(e=W_{YY}\),
\(F=w-2Q^2d\), with all jets evaluated at \((X,Y)=(Q^2,0)\).
For \(z=\alpha u+\beta u^3+\cdots\),

\[
\alpha=-\frac{2Qd}{F},\qquad
L_{\rm red}=L_0+c_2u^2+c_4u^4+O(u^6),
\]

\[
c_2=-p+\frac{s_0dw}{F},\qquad
c_4=\frac{P_{XX}}2+
\frac{s_0}{F^4}\left[\frac{ew^4}{2}+2Q^2d^3w(w-Q^2d)\right].
\]

The cubic clock-response coefficient beta cancels by stationarity; it is
not set to zero. Numerically, \(c_2=0.00169543468\),
\(c_4=-390.80759694\), versus the frozen-clock bare
\(c_4=+0.2838591180\). Thus bare vertices alone gave the wrong sign for
this reduced quartic. A maximum of the static L is not a full healthy
Hamiltonian or an attractor certificate.

The exact zero-flux branch has a nonzero stationary point
\((u,z)=(0.00153986429485,-0.01595263646481)\), with a regular clock
block and longitudinal Schur curvature \(-0.00621946148\).
`clock/README.md` gives an analytic uniqueness argument for the negative-z
clock root on the stated interval, separate from the sampled tests. Numerical
scalar stationary-root counts are not claimed exhaustive.

## 2. Its apparent saturation does not pass the full directional gate

Independent differentiation of the three-dimensional invariants gives,
at \(L_u=L_z=0\), zero static Schur stiffness in both directions
transverse to the aligned gradients. The scalar clock's curl-free condition
prevents treating arbitrary pointwise vector elimination as a general local
three-dimensional action. The transverse plane-wave check used here respects
that condition; the degeneracy is not an artifact of ignoring it.

For the conditional **affine** local background \(\nabla_\mu\nabla_\nu\chi=0\),
restoring the Einstein response to the cubic scalar interaction yields

\[
G_\perp=G_{\perp,0}-\frac{2\gamma^2X^2}{M^2}<0,
\qquad K_\perp>0,
\]

at the stationary point where \(G_{\perp,0}=0\). A calculation at 80-digit
precision using the same rounded primitive inputs finds
\(G_{\perp,0}\simeq1.58\times10^{-81}\),
\(G_\perp=-1.35846900\times10^{-12}\),
\(K_\perp\simeq2.18490895\), and
\(c_\perp^2=-6.21750854\times10^{-13}\).
The zero and negative sign are computed, not assigned. This is not an
80-digit physical measurement or interval enclosure.

For a nonaffine background the omitted Hessian terms must be restored.
For a wave along y in the clock rest frame, write
\(B_H=-\chi_{;00}+\chi_{;xx}+\chi_{;zz}\). At zero bare transverse G,

\[
G_y=4\gamma B_H-\frac{2\gamma^2X^2}{M^2}.
\]

Therefore positive diagonal G requires

\[
\boxed{2M^2 B_H>\gamma X^2},\qquad
B_H>3.39617250\times10^{-7}\quad\text{at the tested root}.
\]

This is a necessary condition for **positive G**, not a full nonaffine
hyperbolicity criterion: time-space mixed Hessians can produce mixed
frequency/wavenumber terms. No Hessian is selected to force this inequality.
An actual FLRW/sourced Hessian cannot be dropped as though it were affine.
The affine saturation proposal fails its stated stability gate; this does
not falsify all nonaffine solutions of the action.

## 3. A further construction: nonlinear initial constraints through order two

`action/adm_action.py` derives the unreduced plane ADM action through order
four, including radiation, dust, shear, lapse, shift, and the full
\(\gamma[ -2Q^3K/3+2QK_xY+2Q^2D^2\chi+\chi^x\partial_xY]\).
The final term starts at cubic order. Varying before Fourier projection
retains mean/2k sources at second order and k/3k sources at third order.
The covariant/ADM boundary identity is independently checked with nonzero shift.

The clock current is
\(J_\tau^\mu=Wn^\mu-2QW_Yh^{\mu\nu}\nabla_\nu\chi\), and
\(E_\tau=P_\tau-V_\tau+sW_\tau-\nabla_\mu J_\tau^\mu\).
On a unitary clock slice its exact plane form is

\[
E_\tau=P_\tau-V_\tau-WK+2W_YK_xY
       +2Q(W_YD^2\chi+W_{YY}\chi^x\partial_xY).
\]

`action/initial_response.py` solves the Hamiltonian, momentum and clock
initial constraints at order epsilon squared for one linearly admissible
k=3 seed. The mean sector solves the common mean diagonal curvature and
mean Q correction; the 2k sector solves spatial curvature and two diagonal
extrinsic curvatures. These are physical initial jets represented with
dummy lapse 1 and shift 0, **not** a preserved-lapse solution.

| Coefficient of epsilon squared | Computed value |
|---|---:|
| Mean Kx and Ky, each | 2.0941712953 |
| Mean Q | 2.3972469835 |
| Spatial z, cos(2kx) | 0.2915963815 |
| Kx, cos(2kx) | -10.0164237633 |
| Ky, cos(2kx) | -1.2521273562 |

Q is the normal scalar velocity, **not by itself a conserved clock charge
or dust density**. The trace mean curvature correction is three times the
listed common value. The free second-order choices are stated explicitly
in `action/README.md`; they select initial data, not new coefficient functions.

The response matrix is calculated from varied equations; determinant
\(-1.85898604\), condition number \(7924.98\). It is **not a Dirac
Poisson-bracket matrix or a DOF count**. The local quadratic constraint
residual falls from 15.0255 to \(2.81\times10^{-14}\).
Unexpanded logarithm/square-root constraints at epsilon 0.002, 0.001,
0.0005 converge with orders 3.0108, 3.0054; their even parts converge with
orders 4.00021, 4.00006. This is nontrivial conditional numerical evidence
for second-order initial constraints, not exact nonlinear existence.

## Formalization, next calculation, and limits

`ClockElimination.lean` proves ten exact conditional algebraic lemmas.
Its Schur identities still require a nonzero block for actual elimination;
they do not formalize the covariant variation, PDE existence or Dirac closure.
The compiler's axiom reports contain no custom axioms or sorryAx.
Computation/proof-audit skills required independent transverse and metric
checks, exposing the restricted saturation failure after the quartic sign flip.
Mathematical self-review covered this report and the Lean statements.

The next unavoidable calculation is **nonlinear preservation of E_tau and
the metric/scalar evolution equations on the constructed mean/2k slice**,
determining lapse and the covariant chi Hessian rather than choosing them.
Then test the complete principal symbol, including mixed terms, and compute
the constraint-reduced quartic feedback. Amplitude refinement here does not
repair or certify the earlier spatial evolution convergence problem.

No new all-gates PASS is asserted for MOND, lensing, PPN, CMB, dark-sector
depletion, the acceleration-scale coefficient, or a two-gravitational-DOF
theory. Neither this mathematical checkpoint nor the DF2 observation in the
companion note supplies empirical closure.
