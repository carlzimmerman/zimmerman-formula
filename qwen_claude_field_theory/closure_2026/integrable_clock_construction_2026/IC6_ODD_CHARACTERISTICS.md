# IC6 odd characteristics on anisotropic plane backgrounds

Base `0b75e72bf5797e451beb258847ade528cd9c4551`, 2026-09-08.
**Restricted odd-sector result; the full IC6 theory remains OPEN.**

The cross polarization has a positive kinetic coefficient and the physical
light cone on the regular IC6 expanding plateau for the diagonal background
class specified below. This includes genuinely anisotropic Bianchi I data,
and is conditional on existence of an on-shell background in the spatially
inhomogeneous class. The other polarization and the mixed scalar system are
not eliminated here. No new action, empirical fit, or all-background
causality claim is made.

## Domain and independently varied fields

Use the exact covariant phase action of [IC5_ACTION.md](IC5_ACTION.md), with
the sole IC6 change in [TENSOR_BALANCE.md](TENSOR_BALANCE.md). Work on

\[
\eta=1,\qquad m>0,\quad J_T>0,\quad K_6\ne0,\quad
N>0,\quad A_i>0,\quad 0<u<1.
\]

The unperturbed physical metric has zero shift and is

\[
ds^2=-N(t,z)^2dt^2+\sum_{i=1}^3 A_i(t,z)^2(dx^i)^2,
\qquad (x^1,x^2,x^3)=(x,y,z).
\]

All background clock/auxiliary scalars depend only on \((t,z)\). Matter is
absent in this gravity-clock calculation; the reference light cone is that
of the unchanged physical metric to which ordinary matter couples. No
additional principal metric operator from a nonminimal matter action is
included. Put

\[
H_i=\partial_t\ln A_i,\qquad L_i=\partial_z\ln A_i,
\qquad V=A_1A_2A_3.
\]

Here \(H_i\) are coordinate-time rates, not physical Hubble rates. There is
no small-background-shear or small-background-gradient expansion.

For a perturbation independent of \(x,y\), take the physical metric

\[
h=D\exp(\epsilon\gamma(t,z)E)D,\qquad
D=\operatorname{diag}(A_1,A_2,A_3),\qquad
E=\begin{pmatrix}0&1&0\\1&0&0\\0&0&0\end{pmatrix}.
\]

The two background reflections \(x\mapsto-x\), \(y\mapsto-y\) make
\(h_{xy}\) and its conjugate momentum odd under **both** reflections.
The fields \(\delta\xi,\delta u,\delta T\), the diagonal metric/trace
momenta and the longitudinal shift are even under both; each transverse
shift and each \(h_{xz},h_{yz}\) is odd under only one. Consequently no
other gravitational/clock perturbation lies in this odd representation.
The full invariant quadratic action cannot mix these inequivalent
representations. This is why their *linearized equations*, including lapse,
auxiliary and shift equations, permit zero first-order responses in this
sector. They are not replaced by arbitrary frozen auxiliary coefficients.

Second-order scalar/diagonal responses can be sourced. Their contribution
to the quadratic action multiplies the background Euler equations and
vanishes on a solution. The exponential completion has exactly fixed
spatial volume, \(\det h=V^2\).

## Geometry and phase elimination

The script constructs the Christoffel symbols and Ricci tensor through the
exact second perturbative jet, retaining all \(H_i,L_i,\partial_zL_i\).
Write \(Z=Z_0+\epsilon Z_1+\epsilon^2Z_2+O(\epsilon^3)\). It obtains

\[
Q=\frac{H_1+H_2+H_3-3\partial_tw}{N},\qquad
Q_1=Q_2=0,
\]
\[
(Q_{\rm TF}^2)_1=0,\qquad
(Q_{\rm TF}^2)_2=
\frac{(\partial_t\gamma)^2+(H_1-H_2)^2\gamma^2}{2N^2},
\]
\[
(R^{(3)})_1=0,\qquad
(R^{(3)})_2=-
\frac{(\partial_z\gamma)^2+(L_1-L_2)^2\gamma^2}{2A_3^2}.
\]

In particular, the algebraic shear terms are retained. Dropping them would
incorrectly identify the complete anisotropic equation with the FLRW
equation, even though it would leave its high-frequency cone unchanged.

The hatted curvature is also checked, rather than equated to physical
spatial curvature on an inhomogeneous background:

\[
\widehat R=R^{(3)}+4\Delta_hw-2|Dw|_h^2,
\]
\[
\Delta_hw=\frac{\partial_z^2w+(L_1+L_2-L_3)\partial_zw}{A_3^2},
\qquad |Dw|_h^2=\frac{(\partial_zw)^2}{A_3^2}.
\]

Both displayed clock expressions are unperturbed, because \(V\) and
\(h^{zz}\) are unperturbed. Thus \(\widehat R_1=0\) and
\(\widehat R_2=(R^{(3)})_2\), even though generally
\(\widehat R_0\ne R^{(3)}_0\). The potential, bare clock term and the
IC5/IC6 auxiliary gradient square likewise have no odd metric dependence.

The five traceless momenta are independently varied in the phase density.
The actual algebraic equations give

\[
P_{\rm TF}=\frac{mJ_T}{2}Q_{\rm TF},\qquad
p=-\frac{mQ}{K_6},\qquad
K_6=1+\frac{3FY}{2a_0^2},\quad Y=\widehat R+Q_{\rm TF}^2.
\]

The implementation checks all five momentum equations and the
envelope-theorem identity in the remaining \(p\) variation. Equivalently,
the momentum-dependent part reduces to

\[
f(Y,Q,F)=\frac m2Y-\frac{mQ^2}{3K_6}.
\]

Define background values

\[
K_0=1+\frac{3F_0Y_0}{2a_0^2},\qquad
J_0=1+\frac{F_0Q_0^2}{a_0^2K_0^2}
=1+\frac{p_0^2F_0}{m^2a_0^2}>0.
\]

Here \(Y_0\) includes actual background shear and hatted curvature.
Since \(Y_1=Q_1=F_1=0\) in the odd representation,

\[
f_2=f_Y Y_2,\qquad f_Y=\frac m2J_0.
\]

The trace momentum is not set to its isotropic value. Along the displayed
odd metric path, its actual second response is

\[
p_2=\frac{3mF_0Q_0}{2a_0^2K_0^2}Y_2,
\]

and its second-order Euler residual vanishes. Its action contribution
multiplies the stationary background trace equation. The odd momentum
Hessian has zero mixed entries with the trace and the other four traceless
momenta on diagonal background data.

## Physical quadratic action and characteristic

Without spatial averaging, the resulting action density is

\[
\boxed{
\mathcal L_{2,\rm odd}=\frac{mNVJ_0}{4}\left[
\frac{(\partial_t\gamma)^2}{N^2}
-\frac{(\partial_z\gamma)^2}{A_3^2}
+\left(\frac{(H_1-H_2)^2}{N^2}
-\frac{(L_1-L_2)^2}{A_3^2}\right)\gamma^2
\right].}
\]

The equation retains the derivatives of its variable coefficients:

\[
\partial_t\left(\frac{VJ_0}{N}\partial_t\gamma\right)
-\partial_z\left(\frac{NVJ_0}{A_3^2}\partial_z\gamma\right)
-NVJ_0\left[\frac{(H_1-H_2)^2}{N^2}
-\frac{(L_1-L_2)^2}{A_3^2}\right]\gamma=0.
\]

The principal symbol, up to a positive overall factor, is

\[
\boxed{\mathcal P_{\rm odd}(\omega,k_z)=
J_0\left(-\frac{\omega^2}{N^2}+\frac{k_z^2}{A_3^2}\right),
\qquad c_{\rm odd,physical}^2=1.}
\]

This is a statement about the propagating odd degree of freedom, after its
only same-representation auxiliary momentum is eliminated. Positivity of
both derivative coefficients uses \(J_0>0\); matching negative coefficients
would not establish health. The algebraic terms and coefficient derivatives
do not alter this high-frequency symbol. They do prevent an inference of
global energy positivity or finite-time stability from the symbol alone.

An independent constant-coefficient phase calculation varies \(P_{xy}\)
directly, using \(\operatorname{tr}P_{\rm TF}^2=2P_{xy}^2\). It reproduces
the same coefficients. A mutation replacing IC6's reciprocal tensor
Hamiltonian coefficient by IC5's coefficient returns
\(c^2=J_0\), not one; the tests detect the difference.

## Nonempty anisotropic homogeneous subfamily

This is not merely an assertion for arbitrary off-shell shear. In barred
canonical variables, set units \(m=V=h_0=1\), start with \(\bar h=I\),
and allow initial
\(\bar\pi_{\rm TF}=\operatorname{diag}(s,-s,0)\).
The homogeneous IC6 shear density is exactly

\[
\mathcal H_{\rm shear}=
\frac{4e^{(4-3u)\xi}s^2}{J_{T,\rm bar}},\qquad
J_{T,\rm bar}=1+
\frac{e^{-6(u-1)\xi}\bar\pi^2F}{a_0^2}.
\]

It and its auxiliary first jets vanish at \(s=0\). Independently
differentiating the full homogeneous zero-shear density at the frozen
witness gives, after normalization by \(e^{-1/2}\),

\[
\mathcal H_{qq}=-\begin{pmatrix}
24&-27\\-27&2\mathcal T+135/8
\end{pmatrix},\quad q=(\xi,u),\quad
\det\mathcal H_{qq}=12(4\mathcal T-27)>0.
\]

The two witness constraint residuals and this Hessian are verified exactly
from the frozen action constants. The determinant sign follows, for
example, from \(\ell=\ln(9/5)<4/5\), which implies
\(\mathcal T=-27/16+54/(5\ell)>189/16>27/4\).
The implicit-function theorem therefore solves the two auxiliary constraints
for all sufficiently small homogeneous shear data. The reduced finite
Hamiltonian is smooth, so its finite-dimensional evolution equations have
local solutions. The homogeneous momentum constraints vanish, diagonal data
remain diagonal, and \(s\ne0\) gives nonzero shear through
\(Q_{\rm TF}=2P_{\rm TF}/(mJ_T)\). The open branch conditions and the
interior of the activation plateau persist locally by continuity.

This supplies actual nearby Bianchi I solutions for the restricted tensor
statement. It does not construct inhomogeneous solutions or prove their
nonlinear evolution remains in the regular branch.

## What the even polarization still requires

At fixed \(F\), direct differentiation gives the exact identity

\[
\frac12(\delta Y,\delta Q)f''
\binom{\delta Y}{\delta Q}
=-\frac{m}{3K_6}
\left(\delta Q-\frac{3FQ}{2a_0^2K_6}\delta Y\right)^2.
\]

The \((Y,Q)\) Hessian has rank at most one. For the even polarization,
\(2Q_{\rm TF}:\delta Q_{\rm TF}\) need not vanish on sheared data.
This identity exposes the trace/shear coupling; it does not justify freezing
the trace, lapse or auxiliary field to calculate a physical tensor speed.

Moreover, \(F\) is itself varied. With

\[
\delta F=A_R\delta\xi+B_R\delta u,\qquad
\delta K=\frac{3}{2a_0^2}(F\delta Y+Y\delta F),
\]

the full \((Y,Q,F)\) Hessian quadratic is

\[
\boxed{
\frac12\delta^2_{\rm Hessian}f
=-\frac{m}{3K_6}\left(\delta Q-\frac{Q}{K_6}\delta K\right)^2
+\frac{mQ^2}{2a_0^2K_6^2}\delta F\,\delta Y.}
\]

The last term is not contained in the fixed-\(F\) rank-one square. A
separate symbolic check and mutation-sensitive test retain it.

A minimal next calculation on a diagonal Bianchi I background, at
\(k_z\ne0\), can use the barred spatial gauge

\[
\bar h=\operatorname{diag}
(B_1^2e^{2\zeta+\gamma_+},
 B_2^2e^{2\zeta-\gamma_+},B_3^2),\qquad
\xi=\xi_0+n,\quad u=u_0+v,\quad N^z=\beta.
\]

The dynamic candidates are \((\zeta,\gamma_+)\); the variables to vary
and eliminate are \((n,v,\beta)\), together with all appropriate phase
momenta. The longitudinal metric equation must be accounted for via the
spatial diffeomorphism identity when this gauge is imposed. Equivalently,
retain the ungauged \(\bar h_{zz}\) and longitudinal momentum until the
linearized momentum constraint is reduced. In particular:

- derive the auxiliary Hessian at the actual sheared solution, including
  the \(J_T^{-1}\) term;
- retain the auxiliary spatial square, the \(\delta F\delta\widehat R\)
  couplings, all shift/momentum constraints and the displayed mixed terms;
- form the reduced two-field principal determinant only after these
  variations and constraints; compare its roots with physical frequency
  \(\omega/N\) and physical wave number \(k_z/(e^wB_3)\).

The odd result has found no obstruction requiring an action correction.
A sufficient symmetry restriction protecting both tensor polarizations is
transverse rotational symmetry: locally \(A_1/A_2\) is constant, so
\(H_1=H_2\), \(L_1=L_2\), and the two transverse polarizations are related
by a background isometry. This restricts backgrounds, not the IC6 action.
Outside that restriction, this calculation neither proves a different even
cone nor supplies the full all-background characteristic result.

## Reproduction and verification boundary

Files: [ic6_odd_characteristics.py](ic6_odd_characteristics.py) and
[test_ic6_odd_characteristics.py](test_ic6_odd_characteristics.py).
The program hashes the five frozen action/source inputs before executing,
reports its own source hash, and emits JSON with exact residuals and explicit
unproved-status flags. No old executable is imported or modified.

From the repository root, each executed command used this cooperative
single-thread environment prefix:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
```

```text
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_ic6_odd_characteristics.py
  Exit 0: 13 tests pass; approximately 0.9 seconds.
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_odd_characteristics.py
  Exit 0: exact residual groups vanish; approximately 0.9 seconds.
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_odd_characteristics.py --require-all-background-causality
  Exit 2: restricted checks pass; the requested global result remains OPEN.
```

Environment: Python 3.9.6, SymPy 1.14.0, exact symbolic arithmetic over real
jet variables and the frozen \(\ln(9/5)\) constants. The displayed
determinant decimal is only a check; the determinant sign argument above is
analytic. No random sampling or numerical continuum approximation is used.
Every experiment is under the requested 180-second cap. The numerical-library
environment variables are cooperative, not operating-system CPU affinity.
The parent continuation records the bounded-run manifests centrally.

The computational assertion is the exact second-jet identity on the stated
symmetry class, not an exhaustive all-background enumeration. The reflection
argument identifies the independently varied physical sector to which that
identity applies. The proof is a self-reviewed derivation with independent
geometry and phase normalization checks, not an external theorem audit.
