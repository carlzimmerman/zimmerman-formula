# The clock caustic is canonically admitted, not removed by closure

2026-09-05. **Same C-H action; full theory OPEN.** This closes one specific
loophole left by the [caustic study](../g03_clock_caustic_2026/REPORT.md):
the smooth pre-caustic trajectory satisfies the canonical constraints and
their full metric evolution. Equivalent preservation constraints cannot
exclude it. Its zero stress does not establish that it is gauge.

The exact flux representation below also permits an actual fixed-k scalar
Poisson calculation at zero field, without assigning a finite q'(0).
That representation does not establish a generic smooth-field equivalence,
regular nonlinear Dirac rank, or post-caustic continuation.

## 1. Canonical equations before restricting the branch

Keep the [action](../g03_covariant_action_2026/ACTION.md) and its
[complete variations](../g03_covariant_action_2026/FULL_VARIATION.md).
Use c=1, suppress the common c^3/(16 pi G), and take K_ij=+h_ij,dot/(2N)
when the shift is zero. In clock gauge tau=s, let

\[
V_i=D_iU-D_i\ln N,\quad w_i=D_i(S_hU),\quad
F=2V^2+2\alpha^2q(w^2/\alpha^2).
\]

After solving the heat endpoint equations, the action is
integral N sqrt(h)[R3+K_ij K^ij-K^2-2Lambda+F]. Its momenta are

\[
\pi^{ij}=\sqrt h(K^{ij}-Kh^{ij}),\qquad
p_N=p_{N^i}=p_U=0.
\]

The last equations are primaries, not an assumed mode count. In the
original heat-localized representation one additionally has
p_W(z)=p_L(z)=p_lambda0=0 at every heat coordinate z: no displayed heat
term contains physical-time velocities. Their preservation gives the heat
equation, adjoint heat equation, matching W0=U, and both varied endpoint
conditions already listed in FULL_VARIATION.md. This inventory is in
clock gauge; it is not an ungauged covariant clock-momentum derivation.

The canonical Hamiltonian after heat elimination is

\[
H_c=\int d^3x\,[N\mathcal H_{\rm GR}-N\sqrt hF+N^i\mathcal H_i],
\quad
\mathcal H_{\rm GR}=\frac{\pi^{ij}\pi_{ij}-\pi^2/2}{\sqrt h}
-\sqrt h(R^{(3)}-2\Lambda),\quad
\mathcal H_i=-2D_j\pi_i{}^j.
\]

The total Hamiltonian adds all primary multipliers. Spatial gauge
generators include primary-momentum terms as well. Preservation yields

\[
\mathcal C_N=\mathcal H_{\rm GR}-\sqrt h\mathscr A_N=0,\qquad
\mathscr A_N=2V^2+4V\cdot a+4D_iV^i+2\alpha^2q,
\]
\[
\mathcal C_U=D_i(NV^i)+S_h[D_i(Nf^i)]=0,\qquad
f_i=q'(w^2/\alpha^2)w_i,\qquad \mathcal H_i=0.
\]

The continuous value f=0 is used at w=0. The displayed S_h is
self-adjoint in sqrt(h); the N factors reproduce the original weighted
adjoint. Setting N=1 before deriving C_N would discard an equation.
Clock gauge is legitimate here because all metric and auxiliary equations
are retained: their covariant diffeomorphism identity implies the clock
equation when d tau is nonzero. Generic constraint classification is not
inferred from this argument.

The program checks the Legendre transform for three independent diagonal
scale velocities, retaining lapse variation, and checks the auxiliary
lapse variation by a one-dimensional Euler-Lagrange calculation with
nonconstant volume measure. These are falsifiable checks of the general
index derivation, not a second complete off-shell tensor derivation.

## 2. Exact canonical trajectory on the tilted compact leaves

On N=1, U=W=constant, L=lambda0=0, every auxiliary Hamiltonian first
derivative vanishes. The metric Hamilton equations therefore reduce to
vacuum GR. Recover the previously reconstructed unit-gradient clock and
use s=tau, with q the geodesic label. Put

\[
A=e^{Ht},\quad E=A^{-2},\quad \gamma=\sqrt{1+P(q)^2E},\quad
J=1+P'D_P,
\]

where P=-p0 sin(kq) for the explicit caustic family. The coordinate
derivatives from the exact characteristic and clock formulas are

\[
t_s=\gamma,\quad x_s=PE,\quad t_q|_s=P\gamma J,\quad
x_q|_s=\gamma^2J.
\]

Consequently the exact metric in clock-adapted Gaussian coordinates is

\[
ds_4^2=-ds^2+A^2[\gamma^2J^2dq^2+dy^2+dz^2].
\]

The lapse is one and the shift zero. Directly differentiating this metric
and computing its intrinsic connection and Ricci tensor gives

\[
\kappa_1=\frac H\gamma+\frac{EP'}{\gamma^2J},\qquad
\kappa_2=\kappa_3=H\gamma,\qquad
R^{(3)}=-2H^2P^2E-\frac{4HEP'}{\gamma J}.
\]

These are not assumed flat clock slices. Substitution gives identically

\[
R^{(3)}+K^2-K_{ij}K^{ij}=6H^2=2\Lambda,\qquad
D_jK_i{}^j-D_iK=0.
\]

The code obtains all momentum components by tensor divergence. It also
checks every component of the vacuum ADM evolution equation

\[
\partial_sK_{ij}=-R^{(3)}_{ij}+2K_{ik}K^k{}_j-KK_{ij}
+\Lambda h_{ij},\qquad \partial_sh_{ij}=2K_{ij}.
\]

The clock-coordinate derivatives are E_s=-2HE gamma and
J_s=EP'/gamma^2. Equivalently, partial_s kappa_i=H^2-kappa_i^2.
The Hamiltonian constraint and its derivative, all momentum components,
all nine metric-evolution residuals, and reconstructed auxiliary equations
are exactly zero. These identities hold for the whole smooth admitted
family, not merely q=0 or a finite grid. Compact clock caps remain those
proved in the previous report; the calculation is restricted to J>0.

Thus there exists a canonical trajectory of the same equations approaching
the previously established invariant clock singularity. Any preservation
condition genuinely implied by these equations must vanish on that
trajectory. Rejecting it by division by a vanishing coefficient or by an
additional regularity restriction is not exclusion by the original action.
This establishes admission and preservation, not uniqueness of evolution.

## 3. A pointwise exact flux representation

Let G(y)=y^2+2(1+y)exp(-y)-2. Introduce an algebraic spatial covector v_i
and replace the kernel term by its stationary expression

\[
\boxed{2\alpha^2q(w^2/\alpha^2)
=\underset{v}{\operatorname{stat}}\left[
4w\cdot v-2\alpha^2G(|v|/\alpha)-2w^2\right].}
\]

Variation of v, before eliminating it, gives

\[
w_i=(1-e^{-|v|/\alpha})v_i.
\]

The radial map is continuous and bijective: its tangential and radial
derivatives are mu(y)>0 and 1+(y-1)exp(-y)>0 for y>0. The stationary
point is the unique maximum of the displayed concave function of v;
direct substitution reproduces the exact q, with all factors of two.
No physical-time derivative for v has been introduced.

Since G(y)=2y^3/3-y^4/4+O(y^5), the lifted potential is C2 at v=0;
its Hessian there is zero. In contrast the eliminated q has a divergent
second derivative. This is a useful representation, **not** a regular
field redefinition: v(w) is asymptotic to sqrt(alpha|w|) times its unit
direction. Smooth w with simple zeros can give only Holder-1/2 v.
Demanding globally smooth lifted v would therefore shrink the original
field domain. Exact equivalence on the constant branch and the pointwise
stationary identity are secure; generic smooth-function-space equivalence
is not asserted.

## 4. Actual fixed-k scalar Poisson matrix and preservation

For one nonzero scalar Fourier mode about the compact de Sitter background,
let the lapse perturbation be n cos(kx), U=u cos(kx), and v_x=-v sin(kx).
Use the already derived GR scalar block from the previous FLRW study,
retaining the scalar spatial-coordinate variable E_sg and shift b. Set
sigma=exp[-xi^2 k^2/(2A^2)]>0 and eta=xi^2 k^2/A^2. The new auxiliary
quadratic density, with the average sin^2=1/2, is independently obtained as

\[
L_{\rm aux}^{(2)}=A[k^2(u-n)^2-k^2\sigma^2u^2+2k\sigma uv].
\]

The full velocity Hessian has computed rank two, in zeta and E_sg.
The four computed primaries are p_n,p_b,p_u,p_v. Preserving them gives,
in that order,

\[
C_n=2Ak^2(n-u+\zeta)-Hp_\zeta,\qquad C_b=-p_E,
\]
\[
C_u=-2Ak[k n+k(\sigma^2-1)u-\sigma v],\qquad
C_v=2Ak\sigma u.
\]

For the six constraints (p_n,p_u,p_v,C_n,C_u,C_v) the actual matrix is
[[0,B],[-B^T,0]], with

\[
B=2A\begin{pmatrix}
-k^2&k^2&0\\
k^2&k^2(\sigma^2-1)&-k\sigma\\
0&-k\sigma&0
\end{pmatrix},\qquad
\det B=8A^3k^4\sigma^2.
\]

Both B and its determinant are computed from canonical brackets in the
script, not assigned. The full eight-constraint matrix is in results.json.
It has computed rank six; the other two constraints p_b and -p_E are first
class in this scalar quadratic system. Thus the calculated subsector count
is (12-2*2-6)/2=1. No number is used as an input to the classification.

The actual algebraic surface is

\[
u=0,\quad p_E=0,\quad
n=-\zeta+\frac{Hp_\zeta}{2Ak^2},\quad v=\frac{k n}{\sigma}.
\]

Preservation uses the explicit time derivative sigma_dot=H eta sigma.
It determines lambda_n=-Hn, lambda_u=0 and lambda_v=-H(1+eta)v;
lambda_b remains free. All eight preservation residuals then vanish, and
differentiating the solved surface agrees independently with Hamilton flow.
There are no tertiary constraints in this fixed-k quadratic system.

Eliminating u and v directly in the Lagrangian reproduces the previous
scalar action and its reduced kinetic term A k^2 zeta_dot^2/H^2. This is
an independent auxiliary elimination, not an independently rebuilt GR
block. The scalar is the earlier clock sector; this calculation adds no
propagating algebraic auxiliary within the tested scalar subsector.

## 5. Exceptional sectors are not continuations of that count

At exactly zero Gaussian gain the raw bracket matrix rank falls to two.
That is an artificial spectral deletion, not finite xi and k: the exact
heat kernel has strictly positive gain. No count is continued through this
changed system. The constraint v=k n/sigma displays the unbounded inverse
heat response as k increases. Finite-k invertibility is not a bounded
continuum inverse or a nonlinear existence theorem.

For homogeneous k=0 there is no scalar gradient source w. The exact
algebraic flux equation is mu(|v|/alpha)v=0, whose only solution is v=0.
Its derivative at zero vanishes, however; linearizing it incorrectly
allows every delta v. These are not nonlinear gauge orbits. The script
returns no full homogeneous flux Dirac count. The separate GR homogeneous
block reproduces the previous zero local scalar count, not a count of this
irregular extended system. Transverse flux variables at nonzero k are
likewise not certified by the longitudinal scalar calculation. Their absent
quadratic potential must not be confused with an exact gauge symmetry.

## 6. Zero stress does not make arbitrary refoliation gauge

An off-shell gauge symmetry must leave the action invariant for allowed
off-shell configurations. Keep a Minkowski metric on a compact T3 slab,
all original auxiliaries constant/zero, and choose

\[
\tau=t+\epsilon f(t)\cos(kx),
\]

where f is smooth with support away from the caps and epsilon is small
enough that X>0. The q term is identically zero throughout this test.
Direct differentiation of the normalized clock gives
a_x=epsilon k f_dot sin(kx)+O(epsilon^2). Hence

\[
S[\tau]-S[t]=\frac{c^3}{16\pi G}\epsilon^2
\operatorname{Vol}(T^3)k^2\int\dot f^2dt+O(\epsilon^3)>0
\]

for nonconstant f and sufficiently small nonzero epsilon. The code checks
the normalization, acceleration and averaged coefficient; positive
integrated action follows from the compact-support argument. The metric
need not solve its equation for this off-shell symmetry test.

Ordinary diffeomorphisms and increasing clock relabelings cannot remove
the invariant caustic. The above also disproves arbitrary fixed-metric
clock refoliation invariance. It does not exclude every conceivable extra
metric-changing symmetry or a special identification restricted to the
geodesic branch. Such an identification still requires an actual generator
or equivalence construction. A vanishing first variation or presymplectic
form pulled back only to the branch does not provide one.

## 7. Decision and next construction gate

The previous question “could full constraints simply exclude this smooth
caustic-producing solution?” now has a negative answer for any canonical
formulation equivalent to the same equations and domain. We have exhibited
the canonical trajectory and its preservation. This is more specific than
a generic stability warning, but not a universal MOND no-go.

**Full geometric closure is not obtained.** A smooth post-caustic clock and
heat-leaf continuation is still missing; a generic nonlinear Dirac analysis,
physical gauge classification and cosmological matter evolution are not
supplied by a quadratic mode count. C-H remains the screened extension,
not the original exact AQUAL equation for general sources.

The next construction must either define a legitimate same-action
continuation/identification through the clock singularity, or modify clock
dynamics so the exact focusing branch is no longer a solution. Adjusting
alpha or xi does not do that. A proposed modification must be varied and
must retain the static exponential law while its own DOF, preferred-frame,
tensor-speed and stability gates are recalculated. No modified theory is
silently introduced here, and no primordial abundance is derived.

## 8. Reproduction and provenance

Only this new directory was authored: CONTRACT.md, constraint_gate.py,
test_constraint_gate.py, REPORT.md, results.json and computation_manifest.json.
The final two files are generated. No commit/push or other contributors'
changes are included. Initial and latest inspected HEAD: 8e9d8c601; exact
dirty input hashes identify the executed dependencies. No external
literature result or novelty claim is needed for the derivations above.

From repository root:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_clock_constraint_2026 -v
python3 -B qwen_claude_field_theory/closure_2026/g03_clock_constraint_2026/constraint_gate.py
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_clock_caustic_2026 -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_flrw_scalar_2026 -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_nonlinear_lift_2026 -v
```

The strict --require-closed run is executed by the unit suite with a private
temporary output directory; it must return 2 (OPEN), not a theory PASS.
The initial eight tests failed before implementation (exit 1). A ninth
determinant regression was also observed failing before that output was
implemented. The report records mathematical claims separately from finite
checks; full nonlinear or continuum closure is not certified by exit 0.

Final runs: new constraint suite 9/9 (exit 0), caustic suite 8/8 (exit 0),
FLRW suite 10/10 (exit 0), nonlinear-lift suite 11/11 (exit 0): **38 tests**.
The producer's ten diagnostic groups passed (exit 0). Strict certification
returned the expected exit 2 inside the new suite. A scoped git whitespace
check returned 0; these new untracked files additionally need a direct
whitespace check, since git diff alone omits them.

Independent read-only review found no important gap within the stated
scope. It reproduced the intrinsic scalar curvature through a separate
warped-product calculation, checked the exact six-by-six determinant
64 A^6 k^8 sigma^4, and evaluated rational bracket ranks at
(A,k,sigma)=(1,1,1),(2,3,1/3),(3,2,1/1000), all six. The symbolic
determinant, not these three examples, establishes the fixed-mode rank.
Mathbox self-proofreading covered this report: no further mathematical-token
changes or local notation issues were required. The nonlinear/gauge/domain
limitations above remain substantive open questions, not editorial gaps.
