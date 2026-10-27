# C-H: expanding compact background and its reduced clock scalar

2026-09-05. **OPEN, not a completed relativistic MOND theory.**

The same C-H action in `../g03_covariant_action_2026/ACTION.md` admits a
vacuum expanding flat three-torus. On its minimum-selected auxiliary branch,
the fixed-smooth-direction quadratic action has two tensor polarizations,
no physical vector modes, and **one additional scalar at nonzero spatial
wave number**. Its quadratic kinetic energy is positive and its effective
density dilutes like dust. This is not a nonlinear health certificate or a
full nonlinear Dirac count. A separately counted healthy clock is allowed
by the user's specification; this calculation does not establish its health.

## 1. Same action and background

Use c=1 until restoring dimensions. Suppress the positive prefactor
\(\mathcal C=c^3/(16\pi G)\) in perturbation actions. After solving the
heat-extension endpoint equations, the auxiliary action is exactly

\[
S_{\rm aux}=\mathcal C\int N\sqrt h\,
 [2|DU-D\ln N|_h^2+2\alpha^2q(|D S_hU|_h^2/\alpha^2)],
\quad S_h=e^{\xi^2\Delta_h/2},\quad\alpha=a_0/c^2>0.
\]

The varied clock defines the leaves; it is not an externally fixed vector.
Here \(s=y(1-e^{-y})\) and
\(q(s^2)=2-2(1+y)e^{-y}-y^2e^{-2y}\). In particular,
\(q(s^2)\sim(4/3)s^{3/2}\): the composite in the gradient is C1, not C2,
at zero. The script computes this limit and the divergent constitutive
tangent. No finite value is assigned to that tangent.

Set matter fields to zero, \(U\) spatially constant, \(\tau=t\), and
\(ds^2=-dt^2+A(t)^2d\mathbf x^2\) on T3. Auxiliary first variations vanish.
The lapse and scale equations are obtained by varying

\[
L_{\rm mini}=-6A\dot A^2/N-2\Lambda NA^3.
\]

Only afterward substitute \(N=1,A=e^{Ht},H^2=\Lambda/3>0\). Both residuals
vanish; the wrong relation \(H^2=\Lambda\) does not. In physical time,
\(H^2=c^2\Lambda/3\). This establishes an allowed expanding vacuum
background, not a viable radiation/matter/acceleration history.

## 2. Zero field: eliminate before expanding

Here is the continuum argument underlying the quadratic action. Fix a
smooth lapse direction \(N_\varepsilon=e^{\varepsilon\nu(x)}\), a positive
heat width, a compact flat leaf, and the mean-zero representative of U.
Define

\[
F_\varepsilon[U]=\int N_\varepsilon\{
2|DU-\varepsilon D\nu|^2+
2\alpha^2q(|D S_hU|^2/\alpha^2)\}\,dV_h.
\]

For global minimizers on H1 modulo constants, or minimizing sequences
with error o(\(\varepsilon^2\)),

\[
\inf_U F_\varepsilon[U]
=2\varepsilon^2\int|D\nu|^2dV_h+o(\varepsilon^2),
\qquad DU_\varepsilon=o(\varepsilon)\quad\hbox{in L2}.
\tag{1}
\]

Proof. The kernel is nonnegative: \(q(0)=0\) and
\(q'(s^2)=y/s-1>0\) for s>0. The trial U=0 gives an O(\(\varepsilon^2\))
upper bound. The squared-gradient term and Poincare inequality give
\(DU_\varepsilon=O(\varepsilon)\) in L2 and a mean-fixed H1 bound.
Heat smoothing at fixed positive width maps that bound to
\(\|D S_hU_\varepsilon\|_\infty=O(\varepsilon)\).
The local lower bound \(q(|p|^2/\alpha^2)\ge c_\alpha|p|^{3/2}\) then implies

\[
\|D S_h(U_\varepsilon/\varepsilon)\|_{3/2}
=O(|\varepsilon|^{1/3})\longrightarrow0.
\]

Any weak H1 subsequential limit V of \(U_\varepsilon/\varepsilon\)
satisfies \(D S_hV=0\). Every nonconstant heat eigenvalue is strictly
positive, so V is constant and its mean is zero. Thus
\(DU_\varepsilon/\varepsilon\rightharpoonup0\). The cross term against the
fixed smooth Dnu tends to zero. Comparing the squared-gradient lower bound
with the U=0 upper bound forces strong L2 convergence of
\(DU_\varepsilon/\varepsilon\) to zero and proves (1).
Existence follows by the direct method: the first term is coercive and
weakly lower semicontinuous; compact heat smoothing makes the q term
continuous along weakly converging bounded H1 sequences.

The same argument applies to a fixed smooth family
\(h_\varepsilon=h_0+O(\varepsilon)\) on the compact leaf. Norms and volume
forms are uniformly equivalent; the positive-time heat maps vary
continuously in smoothing norms for this smooth uniformly elliptic family.
For bounded mean-fixed \(U_\varepsilon/\varepsilon\), the difference
\(D S_{h_\varepsilon}-D S_{h_0}\) tends to zero in operator norm from H1
to C0. Consequently the limiting injectivity argument is unchanged, and
the coefficient in (1) uses h0. On a finite time interval the same bounds
apply uniformly to a fixed smooth perturbation of the de Sitter family.

This selects a minimum branch, not every nonlinear stationary branch.
It proves a fixed-direction reduced action limit, **not** uniform
control when perturbation amplitude and wavelength approach zero together,
nor convergence of its first variations sufficient to establish nonlinear
linearization stability. Small heat eigenvalues make this distinction
essential. It does not enumerate constraints of the original singular
localized heat/multiplier action.

Independent numerical checks vary the exact nonlinear functional, including
the lapse weight and the outer adjoint heat filter. They use alpha=A=1,
widths 0.2/0.5, 4/8 cosine modes, 192 nodes and amplitudes
0.02/0.01/0.005/0.0025. A 384-node check refines one case.
The analytic-gradient/finite-difference relative discrepancy is
9.81e-11; the largest scaled stationary residual is 8.96e-9.
The ratios F[U]/F[0] tend toward one (0.984--0.988 at amplitude 0.02,
0.99795--0.99850 at 0.0025). The quadrature refinement changes a ratio by
3.95e-9. These are bounded stationary minimization checks, not a proof
that the optimizer found the continuum global minimum.

## 3. Scalar action from ADM curvature

Use one real mode with k>0,
\(h_{ij}=A^2e^{2\varepsilon\zeta\cos(kx)}\delta_{ij}\),
\(N=e^{\varepsilon n\cos(kx)}\), and
\(N^x=\varepsilon b\sin(kx)\). The script expands the actual ADM curvature,
averages the trigonometric factors, and removes the time derivative of
\(-9HA^3\zeta^2\). Equation (1) supplies the auxiliary contribution
\(Ak^2n^2\), not a guessed q Hessian.

Restore the scalar spatial coordinate E through the pullback
\(x\mapsto x+\varepsilon E(t)\sin(kx)\). It replaces b by
\(b-\dot E\). Thus the momentum constraint has not been discarded by
fixing the spatial metric gauge before variation. In clock gauge tau=t,

\[
L_S=-3A^3(\dot\zeta-Hn)^2+
2A^3k(b-\dot E)(\dot\zeta-Hn)+Ak^2(\zeta+n)^2.
\tag{2}
\]

Spatial gauge transformations are E -> E+eta, b -> b+dot eta.
Using the clock gauge is valid for X>0 and does not remove a physical
clock excitation: it is then carried by the metric variables.

## 4. Computed quadratic Dirac chain

Coordinates are (zeta,n,b,E), momenta (p,p_n,p_b,p_E). Differentiating
(2) gives a velocity Hessian of rank two. Its two primaries are p_n and
p_b. The Legendre transform yields

\[
H_c=-Ak^2(n+\zeta)^2+Hnp+bp_E-
\frac{p_Ep}{2A^3k}+\frac{3p_E^2}{4A^3k^2}.
\]

Preservation generates the secondaries
\(C_n=2Ak^2(n+\zeta)-Hp\) and \(C_b=-p_E\). In order
\((p_n,p_b,C_n,C_b)\), the actual Poisson-bracket matrix is

\[
\begin{pmatrix}
0&0&-2Ak^2&0\\
0&0&0&0\\
2Ak^2&0&0&0\\
0&0&0&0
\end{pmatrix}.
\]

SymPy computes rank two. Including explicit time dependence
dot A=HA, preservation fixes
\(\lambda_n=H\zeta-H^2p/(2Ak^2)\), leaves lambda_b free, and produces
zero residuals for all four constraints. There are no tertiaries in
this quadratic chain: two second-class and two first-class constraints,
giving (8-2*2-2)/2 = **one scalar**. Independent numerical ranks at two
positive parameter tuples are checked by the tests.

Independently, the shift equation gives n=dot zeta/H. Substitution and
removal of \(d_t(Ak^2\zeta^2/H)\) give

\[
\boxed{L_{S,\mathrm{red}}=\frac{Ak^2}{H^2}\dot\zeta^2,
\qquad \ddot\zeta+H\dot\zeta=0.}
\tag{3}
\]

The kinetic Hessian has rank one and is positive. Removing the auxiliary
lapse-gradient contribution instead gives the empty GR scalar action,
an independent control. The effective density from lapse variation is

\[
\delta\epsilon=-\frac{2k^2}{A^2H}\dot\zeta,
\qquad \dot{\delta\epsilon}+3H\delta\epsilon=0.
\tag{4}
\]

The background auxiliary density is zero, so this linear density is
coordinate-gauge invariant. The solutions are constant zeta and
zeta proportional to exp(-Ht). There is no k-dependent restoring term:
the scalar is dust-like at this order. Zero sound speed and positive
quadratic kinetic energy do not settle caustics, nonlinear strong coupling,
high-frequency limits, or whether these modes integrate to full solutions.

## 5. Homogeneous, vector and tensor sectors

For k=0 restart rather than substitute into an inverse k. The sine shift
and spatial-displacement mode vanish; the constant-mode action is
\(L_0=-6A^3(\dot\zeta-Hn)^2\), without the cosine-average factor.
The primary p_n generates secondary -Hp. Their brackets and further
preservation vanish. The computed count is two first-class constraints,
zero second-class constraints, and zero local homogeneous scalar modes.
This is the H>0 vacuum quadratic calculation, not an assertion about
global moduli, matter backgrounds or the H=0 branch.

For each transverse vector polarization at k>0, expanding off-diagonal K gives
\(L_V=A^3k^2(b-\dot E)^2/4\). The primary p_b generates -p_E;
both are first class and the chain closes weakly. There are no physical
vector modes. During development an initial bookkeeping error tested
dot p_b=-p_E without imposing its secondary constraint; fixing the
constraint-surface evaluation resolved two test failures.

For a tensor polarization at k>0, the script independently computes the intrinsic
curvature of diag(A2 exp(w), A2 exp(-w), A2):
\(R^{(3)}=-(w')^2/(2A^2)\). Together with the ADM kinetic term this gives
\(L_T=(A^3\dot h^2-Ak^2h^2)/4\). Its kinetic coefficient is positive
and its computed speed is c after restoring units. The transverse-traceless
condition matrix has rank four on six symmetric components, leaving two
polarizations. This is a background-specific quadratic result. Homogeneous
torus anisotropies/moduli are not covered by this nonzero-k tensor count.

## 6. Latest concurrent commits: do not combine theories

HEAD advanced during this study from 301b15454 to 129311b8e, through
a8ed70bcf. The latter proposes a **different** clock plus dynamical MOND
scalar action. The newest g03c script tests a fourth-order static operator
with its coherence term outside J, whereas the displayed candidate action
still places that term inside J. Those placements are not interchangeable.
I inspected both commits and reran g03c: its eight diagnostics exit zero.
I did not audit f33's complete PPN calculation in this study.

The positive fourth-order principal symbol is useful, but does not prove
causal propagation, settle the constant mode, or restore the exact
second-order exponential AQUAL equation at finite xi. The computed force
deviations are themselves evidence that this is a modified static law.
The saddle suppression printed by g03c is a scaling estimate, not a solved
three-dimensional saddle boundary-value problem. Its interior Newtonian
check is a bounded numerical approximation, not exact exponential-kernel
equality at finite acceleration. None of these results is imported into C-H.

## 7. Reproduction and status

Created only this directory's CONTRACT.md, flrw_gate.py, test_flrw_gate.py,
REPORT.md, results.json and computation_manifest.json. No existing action
or other contributor's files were changed; no commit or push was made.

Commands from the repository root:

```sh
git status --short
git log -3 --oneline
git show --stat -2
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_flrw_scalar_2026 -v
python3 -B qwen_claude_field_theory/closure_2026/g03_flrw_scalar_2026/flrw_gate.py
python3 -B qwen_claude_field_theory/closure_2026/g03c_zero_field_limit_outside_J.py
```

The new unit suite passes 10/10, exit 0; the producer passes 13/13 diagnostic
groups, exit 0; its `--require-closed` mode is tested to exit **2 (OPEN)**.
The eight existing g03c diagnostics pass, exit 0. Tests were written before
implementation and initially failed; two later negative-control tests also
failed before their implementation. Script success means these calculations
ran consistently, not that the theory satisfies the specification.

Existing suites were rerun from byte-for-byte source copies in a private
fixture, so their CLI tests could regenerate evidence without overwriting
the live working tree. The fixture was created with
`mktemp -d /private/tmp/ch-flrw-regression-XXXXXX`; the three directories
below were copied preserving their repository-relative paths, along with
`hunt_2026/f29_coherence_length_law.py` and `hunt_2026/f30_ppn_screening_door.py`.
GIT_DIR and GIT_WORK_TREE referred to the original repository only for
read-only provenance queries. Actual verification commands and results:

```sh
python3 -B -m unittest discover -s /private/tmp/ch-flrw-regression-ChBE9i/qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026 -v
# 10/10, exit 0
python3 -B -m unittest discover -s /private/tmp/ch-flrw-regression-ChBE9i/qwen_claude_field_theory/closure_2026/two_body_frequency_2026 -v
# 9/9, exit 0
python3 -B -m unittest discover -s /private/tmp/ch-flrw-regression-ChBE9i/qwen_claude_field_theory/closure_2026/filtered_tidal_relation_2026 -v
# 6/6, exit 0
```

Together with the new suite, **35 unit tests pass**. A fresh read-only
review independently recomputed the scalar action, bracket matrix,
preservation and reduced equation, and checked the continuum argument.
Its scope/provenance suggestions were applied: nonzero-k tensor/vector
counts explicitly exclude homogeneous torus moduli; the manifest now
hashes this proof and the parent full-variation document. Mathematical
proofreading covered this report; the forced notation typo Hzeta was
corrected to H zeta, without changing the argument.
The homogeneous/vector test oracles were then strengthened to compare
their Dirac counts against kinetic ranks of actions reduced by their
own lapse/shift Euler equations, rather than a preset empty action.
Those two new output-contract assertions first failed, then passed after
implementing the independent reductions; the mathematical counts did not change.

The strongest result is (1)--(4), conditional on the minimum-selected
fixed-direction reduction. C-H cannot be advertised as having only two
total modes on the basis of this reduced action. Its general nonlinear
count and the health of the separately counted clock remain OPEN. The
original exact general-source AQUAL requirement was already not met by
this screened candidate; no requirement has been weakened into a PASS.

**Next unavoidable calculation:** determine whether the reduced clock
solutions are tangent to actual solutions of the original nonlinear
clock/heat equations, with uniform amplitude/wavelength control. This
requires the singular auxiliary constraint structure and nonlinear
interactions, not another quadratic assumed scalar Lagrangian. Only then
can nonlinear clock health, causal response with admissible matter,
realistic FLRW evolution and full PPN be certified or falsified.
