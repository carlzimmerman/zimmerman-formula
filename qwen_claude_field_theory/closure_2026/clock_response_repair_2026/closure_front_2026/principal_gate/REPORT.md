# Same-action response gate: what is established, and what fails

Base checkpoint: `f59fad6c7`; subsequently reviewed `473860435` (L211/L212).
Before this checkpoint was committed, `425a28355` added L213/L214 and withdrew
L212's verdict. The historical audit in section 6 is not a claim that the
withdrawn numerical verdict is still current. A bounded L214 dependency check
is recorded at the end of that section; its whole new branch is not certified.
The frozen action and its coefficient functions are not changed. This is a
continuation of Carl Zimmerman's primordial-clock research programme, not a
new empirical discovery or a claim that every gravity gate has passed.

## 1. Exact target and research decision

The benchmark here is the user's explicit isolated-system exponential law

\[
g[1-e^{-g/a_0}]=g_N,\qquad a_0>0.
\]

This must not be conflated with the different, commonly used expression
\(\nu(x)=1/(1-e^{-\sqrt{x}})\), \(x=g_N/a_0\). They have the same leading
deep-MOND power but are not exact inverses. The formal exponential certificate
below applies to the benchmark as written. No local or environmental
redefinition of \(a_0\) is used. Its relation to vacuum density remains input.

Three routes were executed: independent metric variation; a complete Dirac
chain for the frozen two-field principal truncation; and a nonlinear radial
first integral. The metric route derives a genuine source and no leading
static slip. The regular-response route fails the exact isolated MOND gate.
The radial route identifies why a cubic scalar interaction alone cannot be
identified with that MOND law. The uncomputed step is a complete nonlinear,
on-shell branch with controlled loss of uniform response (possibly a
degeneracy), not another coefficient fit.

## 2. Same action and Euler–Lagrange equations

Use signature \(-+++\), positive constant \(M^2\), constant \(\gamma\), and
one minimally coupled physical metric:

\[
S=\int\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
+P(X,\tau)-V(\tau)+sW(Y,\tau)+\gamma X\Box\chi\right]d^4x+S_m[g,\psi],
\]

\[
s=\sqrt{-\nabla\tau\cdot\nabla\tau}>0,\quad
n_\mu=-\partial_\mu\tau/s,\quad Q=n^\mu\partial_\mu\chi,
\quad X=-\nabla\chi\cdot\nabla\chi,\quad
u_\mu=\partial_\mu\chi+Qn_\mu,\quad Y=u_\mu u^\mu.
\]

Let \(v_\mu=\partial_\mu\chi\), \(H_{\mu\nu}=\nabla_\mu\nabla_\nu\chi\).
The scalar and clock variations are

\[
E_\chi=2\nabla_\mu(P_Xv^\mu-sW_Yu^\mu)
+2\gamma[(\Box\chi)^2-H_{\mu\nu}H^{\mu\nu}
-R_{\mu\nu}v^\mu v^\nu]=0,
\]

\[
E_\tau=P_\tau-V_\tau+sW_\tau
-\nabla_\mu(Wn^\mu-2QW_Yu^\mu)=0.
\]

Partial clock derivatives here hold \(X,Y\) fixed. The cubic equation follows
by varying \(X\Box\chi\), integrating both derivative variations by parts,
and commuting covariant derivatives on \(v_\mu\). The metric equation is

\[
M^2(G_{\mu\nu}+\Lambda g_{\mu\nu})=T^{(m)}_{\mu\nu}
+T^{(0)}_{\mu\nu}+T^{(3)}_{\mu\nu},
\]

\[
T^{(0)}_{\mu\nu}=(P-V+sW)g_{\mu\nu}+2P_Xv_\mu v_\nu
+sWn_\mu n_\nu-2sW_Yu_\mu u_\nu,
\]

\[
T^{(3)}_{\mu\nu}=2\gamma[
(\Box\chi)v_\mu v_\nu-2v_{(\mu}H_{\nu)\alpha}v^\alpha
+g_{\mu\nu}H_{\alpha\beta}v^\alpha v^\beta].
\]

`first_derivative_variation.py` differentiates the exact metric and gradient
invariants before evaluating a clock-rest orthonormal frame, checking all ten
independent non-cubic stress components and both four-component variational
currents. A canonical scalar energy control fixes the sign. The cubic static
metric variation and Einstein response are independently computed in
`../metric_response/derive_static_metric.py`; the cubic scalar variation is
also tested by the radial action in `../spherical_branch/derive_spherical.py`.
These checks do not constitute a formal Lean proof of general covariance or
the full Euler–Lagrange system.

Ordinary matter conservation is independent of whether the scalar is forced
through the metric. For a separately diffeomorphism-invariant \(S_m[g,\psi]\),
its metric variation is \(-\frac12\sqrt{-g}T_{\mu\nu}\delta g^{\mu\nu}\).
A compactly supported diffeomorphism, integration by parts, and the matter
Euler–Lagrange equations give \(\nabla_\mu T_m^{\mu\nu}=0\). No scalar
equation is used in this matter-only identity. Conversely,
\(\delta S_m/\delta\chi=0\) does not imply zero scalar forcing after the
Einstein equation is inserted into the curvature term of \(E_\chi\).

## 3. Physical static metric, not an assigned scalar force

Take an aligned affine local jet, \(\chi=qt+\pi\),
\(\tau=st+\sigma\), freeze coefficients, and keep leading spatial derivatives
of static perturbations. Define

\[
K_0=2P_X+4q^2P_{XX},\quad
G_0=2P_X-\frac{2sW_YW_0}{W_0-2q^2W_Y},\quad
b=\gamma q^2,\quad B_g=2b^2/M^2,
\quad G=G_0-B_g,\quad K=K_0+3B_g.
\]

The clock elimination requires \(k\ne0\) and \(W_0\ne2q^2W_Y\).
The static action derived independently by the metric route is

\[
\mathcal L_{\rm stat}=M^2[(\nabla\Psi)^2
-2\nabla\Phi\cdot\nabla\Psi]
-\tfrac12G_0(\nabla\pi)^2+2b\nabla\Phi\cdot\nabla\pi-\rho\Phi.
\]

Its equations, with the independent spatial Einstein equation, give

\[
2M^2\Delta\Psi=\rho+2b\Delta\pi,\quad
(\partial_i\partial_j-\delta_{ij}\Delta)(\Psi-\Phi)=0,
\quad G_0\Delta\pi=2b\Delta\Phi.
\]

With the stated nonzero Fourier mode and no added homogeneous solutions,

\[
\boxed{\widehat\Phi=\widehat\Psi
=-\frac{\widehat\rho}{2M^2k^2}\left(1+\frac{B_g}{G}\right),
\qquad \widehat\pi=-\frac{b\widehat\rho}{M^2Gk^2}.}
\]

Both potentials are derived. Their static ratio is one when the potential is
nonzero. This is **not a full PPN calculation** of \(\gamma,\beta,\alpha_i\).
At this order the measured static coupling would be
\(G_{\rm stat}=G_{\rm bare}(1+B_g/G)\), with
\(G_{\rm bare}=1/(8\pi M^2)\). Solar-System recovery still requires the
appropriate background and nonlinear matching. Replacing a bare coupling by
a measured constant does not change the source-amplitude argument below.

For positive \(G,K\), the local scalar speed and enhancement obey

\[
\boxed{\mathcal R\,c_s^2=\frac{G_0}{K},\qquad
\mathcal R=1+\frac{B_g}{G},\qquad c_s^2=G/K.}
\]

These formulas assume a zero background Hessian. On a general FLRW or
inhomogeneous jet the previously derived Hessian terms must be restored;
they cannot be dropped just by calling an expansion quasistatic. In the
restricted formula, fixed nonzero finite \(B_g\) and finite positive \(K\)
make diverging enhancement approach a vanishing gradient coefficient and
sound speed. This does not prove an instability at every such endpoint.

At exactly \(G=0\), the two displayed static field equations imply
\(b\rho=0\). Thus for nonzero braiding a nonzero source cannot be supported
by that linear operator. `critical_static_source_compatibility` formalizes
this compatibility condition directly from the two equations, without a
division by \(G\). Nonlinear terms may become leading there; ignoring them
does not turn the divergent response into a MOND solution.

## 4. A rigorous obstruction to bounded isolated response

For any real \(y\), \(1-e^{-y}\le y\). Hence the exact target, with \(g\ge0\),
implies

\[
\boxed{g^2\ge a_0g_N.}
\]

Suppose an isolated branch has a uniform finite gain \(g\le Cg_N\),
\(C>0\), while source amplitude is reduced at fixed location and boundary
conditions. Then the two statements are incompatible whenever

\[
\boxed{0<g_N<a_0/C^2.}
\]

`ResponseGate.lean` proves this exact implication with the exponential
function itself, not a fitted power or an assumed MOND coefficient. It also
proves the bracket determinant positivity and the response/speed identity.
The seventh statement treats the critical static source compatibility above.

The regular constant-coefficient metric calculation has just such a finite
gain. A nonlinear solution with zero acceleration at zero source, differentiable
in source amplitude with bounded derivative near zero, would also have one.
**This conditional differentiability
statement is not an existence theorem for the nonlinear PDE.** Degenerate,
nonanalytic, nonuniform, charged, nonzero-external-field, or changed-boundary
branches are not ruled out by this argument. In particular, an external-field
linear regime is not being tested against an isolated MOND requirement.

Thus this rules out certifying the regular linear branch as exact isolated
MOND. It is not a no-go theorem for all relativistic MOND constructions.

## 5. Full preservation in the finite-mode principal truncation

This section is deliberately restricted to the frozen fixed-metric
two-field quadratic action. For one real Fourier amplitude write

\[
L_k=\tfrac12K_0\dot\pi^2-\tfrac12k^2
(A\pi^2+2B\pi\sigma+C\sigma^2),
\]

\[
A=2P_X-2sW_Y,\quad B=2qW_Y,\quad C=(W_0-2q^2W_Y)/s.
\]

The script obtains the momentum map and its Hessian, Legendre transforms
the invertible velocity, and continues each constraint's Poisson bracket
with the total Hamiltonian until closure or multiplier fixation. Ranks,
first-/second-class counts, and canonical-pair counts are computed, not
inserted as expected results.

For \(K_0\ne0,k\ne0,C\ne0\), the chain is

\[
p_\sigma=0,\quad -k^2(B\pi+C\sigma)=0,\qquad
\{\phi_a,\phi_b\}=\begin{pmatrix}0&Ck^2\\-Ck^2&0\end{pmatrix}.
\]

Preservation fixes the primary multiplier to
\(-Bp_\pi/(CK_0)\). The determinant is \(C^2k^4\): two second-class
constraints and one remaining scalar canonical pair in this truncation.
The constrained clock does not remove \(\chi\)'s canonical pair.

For \(C=0,B\ne0,k\ne0\), preservation continues through four constraints,
proportional to \(p_\sigma,\pi,p_\pi,\sigma\), fixes the multiplier, and
the computed matrix has rank four. The finite-mode scalar pair is absent
there. Dividing the regular solution by \(C\) cannot describe this branch.

For \(k=0\) before any division, only \(p_\sigma\) is a principal constraint:
it is first-class in this truncation and the homogeneous \(\chi\) canonical
pair remains. Explicit clock dependence, expansion and all lower derivative
terms are omitted, so that first-class classification is **not** a statement
about the full homogeneous action. \(B=C=0,k\ne0\) likewise has a decoupled
clock. \(K_0=0\) is excluded and requires a new momentum analysis. Lapse,
shift, tensor and full nonlinear constraints are not counted in this section.

## 6. L211/L212: the specific shortcut that does not work

L211's assigned zero direct scalar source does not calculate the curvature
source. Inserting minimal dust in the trace-reversed Einstein equation gives
\(2\gamma v^\mu v^\nu R^{(m)}_{\mu\nu}
=\gamma q^2\rho/M^2\), nonzero generically. This is the source in section 3.

L212's correct identity is \(G_0|_{W_0=0}=2P_X\). At that same locus,
however,

\[
\sigma/\pi=s/q,\qquad C=-2q^2W_Y/s\ne0
\]

when \(q,W_Y\ne0\). The clock aligns with the scalar; it does not stop
responding. The cubic source and \(B_g\) survive. Preferred-frame safety is
not proved by eliminating a \(W_Y\) term from one reduced coefficient.

Furthermore the current positive-\(\gamma\) canonical reference patch has
\(U>0\) and \(\bar q'<0\), so
\(W_0=U-2\gamma\bar q^2\bar q'>U>0\). This follows from the explicit
positive \(a,m,v\) reference flow in `nonlinear_evolution_2026/constitutive.py`.
It is not a claim that \(v\) stays positive for arbitrary evolution. On the
stated patch, L212 has not exhibited a \(W_0=0\) solution of this fixed action.
Under its separate power-law ansatz \(\bar q'=-3wHq/s\), a zero requires
\(\gamma=-Us/(6wHq^3)\), including the sign and clock-rate factor omitted
from its magnitude-only estimate. No new coefficients are reconstructed here.

Latest dependency check: L214 (`425a28355`), lines 40–49, adds a direct
leading-order term `lambda phi rho` and solves a separately truncated
`s beta Y^(3/2)` gradient equation. Its own limitations at lines 230–236
acknowledge that a full covariant matter coupling and the coupled gates have
not been supplied. This is a changed coupling/operator, not a result from
the unchanged minimal-matter action examined here. The matter Ward identity,
physical photon metric, lapse/curvature potentials, clock constraint and
energy signs must all be re-derived before transferring any earlier gate.
The existing exact spherical calculation already demonstrates that clock
variation cannot simply be omitted in a radial ansatz. We have not run L214
or treated its emitted PASS labels or newly appended Lean declarations as
certification of that missing covariant completion.

## 7. All-gates ledger for this same candidate

| Requirement | What the evidence supports |
|---|---|
| Exact exponential MOND, deep law, BTFR | Regular finite-gain branch fails the isolated weak-source limit; nonlinear degenerate branch not established |
| Only two tensor gravitational modes; no hidden auxiliary | Two tensor polarizations in earlier homogeneous calculation; a scalar canonical pair remains in the regular principal system and must be openly counted; full nonlinear Dirac closure open |
| \(\Phi=\Psi\), lensing | Derived at leading static affine-jet order here; finite-gradient galactic branch open |
| \(\beta,\gamma,\alpha_1,\alpha_2,\alpha_3\) | Static potential ratio one is not a full PPN solution; complete matching open |
| Ordinary matter conservation | Follows from separately covariant minimal \(S_m\) on matter equations, as above |
| Tensor speed/energy | Earlier same-action homogeneous tensor calculation: common photon/tensor cone and positive energy for \(M^2>0\); general backgrounds not certified |
| Scalar/vector stability, strong coupling | Conditional principal coefficients derived; no uniform nonlinear health theorem, no full strong-coupling bound |
| Expanding FLRW and CMB | Homogeneous equations and reference solutions exist; CMB viability and nonlinear galaxy/cluster allocation not established by this work |
| \(k=0,y=0\) limits | Separate finite-mode analysis performed; required nonlinear degenerate limit not controlled |
| Newtonian/GR recovery and measured \(G\) | Static source-normalized \(G_{\rm stat}\) derived; full high-acceleration recovery open |
| One physical metric | Retained for matter and photons; no direct/disformal coupling added |
| \(a_0\)–\(\Lambda\) and fitted one-half | No derivation of the coefficient; relation remains input |
| Empirical confirmation | No new dataset or likelihood was analyzed in this checkpoint |

**Whole-theory status: OPEN.** The regular finite-susceptibility route to the
exact isolated law is excluded under the stated assumptions. The next
unavoidable calculation is the full, uneliminated nonlinear metric/clock
system on a branch with degeneracy or another controlled loss of uniform
response, with the fixed cosmological
boundary/charge data, both metric potentials, constraint rank and interaction
scales evaluated together. The radial first integral alone is not that solution.
If no healthy branch exists there, this particular action fails; neither Lean
nor a larger parameter scan can replace that missing implication.

## 8. Attribution and verification scope

The general scalar–metric kinetic-mixing mechanism is known, not a new force
mechanism claimed here: Deffayet, Pujolàs, Sawicki and Vikman, *Imperfect Dark
Energy from Kinetic Gravity Braiding*, arXiv:1008.0048v2 (24 September 2010),
section 1, explicitly discusses coupling to external matter through gravity
without a direct scalar–matter term. [Primary paper](https://arxiv.org/pdf/1008.0048v2),
checked 12 September 2026. This is attribution for the mechanism only; its
single-scalar results are not imported as certification of the extra clock.
The source uses a different signature/kinetic normalization; the coefficients
in section 3 are independently differentiated in this repository's convention.
No global novelty search or claim is made for the elementary inequalities.

Independent read-only review re-derived the principal coefficients, complete
finite-mode chains and the finite-response contradiction. Mathematical
proofreading is limited to these new notes and equations. Exact commands,
exit statuses, compiler axiom output, input hashes and limits are recorded by
the bounded verification run described in `VERIFICATION.md`.
