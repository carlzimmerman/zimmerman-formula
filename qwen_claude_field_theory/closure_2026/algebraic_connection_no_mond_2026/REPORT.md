# Algebraic connections cannot supply the MOND source in this action class

Date: 2026-09-04. Starting revision: `164a5e1e0b1e2d186bd7696b49cde1eec9d7ce63`.
The live tree also contains unrelated changes; they are not part of this work.

**Outcome:** the action class in section 1 is **DEAD as a MOND construction**.
The full fried-chicken goal is **OPEN**. This is a scoped variational no-go, not
a universal no-go for relativistic MOND and not a complete theory.

The core framework stays fixed: mu_exp(y)=1-exp(-y), y=g/a0; ordinary matter and
photons use one physical metric; a0=(c/2)sqrt(G_N rho_Lambda) remains a proposed
input unless derived. The different exponential-RAR nu function is not substituted.

## 1. The explicit action and exact scope

In c=1 units, with signature (-+++), consider

\[
 S=\frac{M^2}{2}\int d^4x\sqrt{-g}\,
 [g^{\mu\nu}R_{\mu\nu}(\Gamma)-2\Lambda_0+F(g,C)]
 +S_m[g,\psi],\qquad
 C^\alpha{}_{\mu\nu}=\Gamma^\alpha{}_{\mu\nu}-\{g\}^\alpha{}_{\mu\nu}.
\]

Hypotheses:

1. M^2>0 is constant, and Gamma is an unrestricted independent torsion-free
   connection: all 40 components C^alpha_(mu nu) may be varied.
2. F is a differentiable, covariant local scalar made only from g and algebraic C.
   It may be nonlinear and non-polynomial, and its stationary points may be degenerate.
   Its parameters, including any a0, are constants.
3. There are no derivatives of C, additional differentiated fields, external tensors,
   or additional curvature dependence. Matter is independent of Gamma and minimally
   coupled to g. Metric dependence hidden in C is explicitly retained in the variation.
4. The claim concerns smooth connected bulk solutions with ordinary compactly supported
   variations; discarded boundary divergences do not introduce new bulk degrees of freedom.

Define

\[
 B=g^{\mu\nu}(C^\alpha{}_{\alpha\beta}C^\beta{}_{\mu\nu}
                   -C^\alpha{}_{\nu\beta}C^\beta{}_{\mu\alpha}),\qquad U=B+F.
\]

The curvature decomposition, with the same Ricci convention as the executable
metric calculation, is

\[
 g^{\mu\nu}R_{\mu\nu}(\Gamma)=R(g)+\nabla_\alpha V^\alpha+B,
 \quad V^\alpha=g^{\mu\nu}C^\alpha{}_{\mu\nu}
                  -g^{\mu\alpha}C^\beta{}_{\mu\beta}.
\]

Thus the bulk action in independent variables (g,C) is EH plus sqrt(-g) U.
This change of variables contains metric derivatives; it is NOT silently treated
as a canonical point transformation. Its Euler-derivative chain rule is

\[
 E_C=E_\Gamma,\qquad
 E_g\big|_C=E_g\big|_\Gamma+(D\{g\})^*E_\Gamma.
\]

Consequently the two metric equations agree on the connection shell. This is sufficient
for the bulk-metric theorem and does not establish a regular Hamiltonian equivalence
on every singular branch.

## 2. General variational theorem, including degenerate branches

**Claim.** Every solution obeying the hypotheses has

\[
 \boxed{G_{\mu\nu}+\Lambda_{\rm eff}g_{\mu\nu}=M^{-2}T_{\mu\nu},
 \qquad \Lambda_{\rm eff}=\Lambda_0-U_*/2,\qquad \partial_\rho U_*=0.}
\]

**Proof.** Independent connection variation gives U_C=0. For an arbitrary
infinitesimal change of frame H^a_b, scalar covariance gives the algebraic identity

\[
 0=U_g\!\cdot\delta_Hg+U_C\!\cdot\delta_H C,
\]

where

\[
 \delta_Hg^{ij}=H^i{}_k g^{kj}+H^j{}_k g^{ik},
\quad
 \delta_HC^a{}_{bc}=H^a{}_d C^d{}_{bc}
                -H^d{}_b C^a{}_{dc}-H^d{}_c C^a{}_{bd}.
\]

The induced C variation remains symmetric in its lower indices and hence is allowed.
On U_C=0, U_g dot delta_H g=0 for every H. For any symmetric prescribed variation
X^{ij}, take H^i_j=(1/2)X^{ik}g_kj; then delta_H g=X. Therefore **U_g=0 on shell**.
No Hessian inversion, isolated critical point, polynomial assumption, or enumeration
of invariants has been used.

Varying the metric at fixed C now gives

\[
 G_{\mu\nu}+\Lambda_0g_{\mu\nu}
 +U_{g^{\mu\nu}}-\tfrac12Ug_{\mu\nu}=M^{-2}T_{\mu\nu}.
\]

The metric derivative vanishes by the preceding argument. Since the Levi-Civita
derivative obeys nabla g=0, naturality and constant parameters also imply
partial_rho U=U_C dot nabla_rho C=0 on shell. This proves the claim. Different
connected branches may have different constants U_*; a smooth branch cannot make
a spatially varying phantom density. QED.

This is stronger than finding C=0 in a quadratic example: even an undetermined,
nonzero C branch cannot evade the metric conclusion under these hypotheses.

**Exclusions matter.** The theorem does not apply to Palatini f(R) with nonlinear
curvature, a field-dependent EH coefficient, derivatives of C, direct matter-connection
couplings, extra differentiated clocks, nonlocal operators, or a flatness-restricted
connection such as symmetric teleparallel constructions. Flatness is a differential
constraint, so its connection equation is not the unrestricted U_C=0 used here.
Non-differentiable actions require a specified alternative variational formulation.

For example, an algebraic vector coupled to a differentiated scalar,
L=A_mu A^mu/2-A^mu partial_mu phi, eliminates to -partial_phi^2/2, not a
cosmological term. It lies outside the hypotheses, illustrating a real exception.

## 3. Full-component computation and what its ranks mean

`connection_checks.py` constructs all torsion-free components and a fully symbolic
inverse metric. The contraction B is differentiated, not inserted as a matrix.
An independent vector restriction C^a_bc=delta^a_b A_c+delta^a_c A_b returns
B=3 A_mu A^mu in 4D. All 16 frame generators are tested on B and a second invariant,
g^{mu nu} C^a_(a mu) C^b_(b nu). All 32 polynomial residuals vanish. Omitting metric
variation gives nonzero residuals for all 16 B generators. The metric-variation map
has computed rank 10. These are finite algebraic checks of the conventions; section 2,
not invariant sampling, proves the arbitrary-potential statement.

Computed flat-frame Hessians H_B:

| Spacetime dimension | Independent C components | rank(H_B) | det(H_B) |
| --- | ---: | ---: | ---: |
| 1 | 1 | 0 | 0 |
| 2 | 6 | 4 | 0 |
| 3 | 18 | 18 | 65536 |
| 4 | 40 | 40 | 89060441849856 |

For the regular frozen-metric auxiliary L=B block (nonzero constant overall factor
normalized to one), the code derives:

- Primary constraints pi_A=partial L/partial dot C_A=0, A=1,...,40.
- Canonical Hamiltonian H_c=-B, and secondary constraints E_A={pi_A,H_c}=B_,A.
- Their actual canonical Poisson matrix, using these constraint functions, is
  Delta=[[0,-H_B],[H_B,0]]. The full basis, every secondary constraint, and all
  nonzero matrix entries are saved in `connection_results.json`.
- Preservation gives dot E=H_B u=0. The computed inverse fixes every u=0;
  substitution into the preservation equations gives zero, so no tertiary appears
  in this frozen block.
- The constraint Jacobian and Poisson matrix both have rank 80;
  det(Delta)=7931762302491582015247220736. Thus 0 first-class and 80 second-class
  constraints leave 0 auxiliary phase-space dimensions in this block.

There are no spatial C derivatives, so this auxiliary block is identical for
k=0 and k!=0. **This is not a full gravitational Dirac count.** It omits the
metric lapse, shift, diffeomorphism constraints and their mixed brackets. Nor is it
the canonical analysis of the exponential singular action below. No full-theory
N_grav value or perturbative-health certificate is generated from this block.

## 4. Put the framework's exact exponential primitive into the action

Choose the explicit member F=-B+U_exp(B), where

\[
 U_{\exp}(B)=a_0^2\mathcal G(\sqrt{|B|}/a_0),\qquad
 \mathcal G(y)=y^2+2(1+y)e^{-y}-2.
\]

This makes the bulk action EH plus U_exp. Here a0 is expressed in geometric c=1 units;
this is a candidate insertion of the framework's primitive, not a derivation of MOND.
Exact differentiation gives

\[
 \mathcal G'(y)/(2y)=1-e^{-y},\qquad
 U_B=\operatorname{sgn}(B)(1-e^{-\sqrt{|B|}/a_0}).
\]

For B!=0 the multiplier U_B is nonzero. The connection equation U_B H_B C=0
and the computed invertibility of H_B in 4D force C=0, contradicting B!=0.
For B=0, however, U_B=0: **the entire quadratic null cone survives**, not only C=0.
The explicit nonzero configuration C^0_00=1 with every other component zero has
B=0 but B_,C!=0. Both statements are computed.

The controlled first-variation limit is U_exp=2|B|^(3/2)/(3a0)+O(B^2),
so U and U_B extend continuously to zero. Every null-branch solution has U=0
and U_g=0 and therefore the metric equation is exactly Einstein's with Lambda_0.
The exponential kernel supplies no MOND force here.

The second derivative U_BB diverges as 1/(2a0 sqrt(|B|)) at nonzero null points.
One must not report a regular Dirac rank there. At C=0, by contrast,
|B(C)|=O(||C||^2) and U(C)=O(||C||^3), so the second variation at that point
vanishes; the executable directional check agrees. This does not make the action
C^2 on a neighborhood containing nonzero null points, and does not certify absence
of strong coupling. The action already fails MOND, irrespective of that unresolved health issue.

## 5. Independently derived physical metric and the missing MOND source

`metric_branch_checks.py` constructs Christoffel, Ricci and Einstein tensors from
ds^2=-(1+2 epsilon Phi)dt^2+(1-2 epsilon Psi)(dr^2+r^2 dOmega^2), keeping the
potentials independent throughout. At first order it obtains

\[
 G_{00}=2(\Psi''+2\Psi'/r),\quad
 G_{rr}=2(\Phi'-\Psi')/r,\quad
 G_{\theta\theta}/r^2=\Phi''-\Psi''+(\Phi'-\Psi')/r,
 \quad R_{00}=\Phi''+2\Phi'/r.
\]

In the locally Lambda-negligible, source-free spherical exterior, independently
integrating G00=Grr=0 and matching G00=kappa rho_b gives

\[
 \Phi=C_\Phi-\frac{\kappa M_b}{8\pi r},\qquad
 \Psi=C_\Psi-\frac{\kappa M_b}{8\pi r},\qquad
 G_N=\frac{\kappa}{8\pi}=\frac1{8\pi M^2}.
\]

After coordinate normalizations remove the additive constants, their derived
coefficient ratio is gamma=1. This is a static linear result, not a calculation
of beta or alpha_1, alpha_2, alpha_3; those are not assigned numerical values here.

Now impose the REQUIRED mu_exp law on an isolated finite spherical baryonic mass:

\[
 a_0 y(1-e^{-y})=G_NM_b/r^2,\qquad g=\Phi'=a_0y.
\]

Implicit differentiation and substitution into the separately generated R00 yields

\[
 \boxed{R_{00}^{(1)}=\nabla^2\Phi
 =\frac{2a_0y^2}{r(e^y-1+y)}>0\quad(r,a_0,y>0).}
\]

This is also the first-order static-observer Ricci contraction and does not depend
on Psi. No choice of a separate lensing potential can make this MOND exterior
Ricci-flat. A constant cosmological term cannot reproduce it on an open radial
interval: along the implicit fixed-mass branch the expression is real analytic,
and its derivative at y=1 is

\[
 -\frac{2a_0(3e^2-4e+2)}{r^2 e^3}\ne0.
\]

If it were constant on an open interval, analytic continuation would force its
derivative to vanish everywhere on the connected positive-y branch, a contradiction.
This argument does not assert that the derivative has one sign at all y.

Equivalently, any no-slip weak-field Einstein-source realization MUST supply the
exterior effective density

\[
 \rho_{\rm required}(r)=\frac{a_0y^2}{2\pi G_Nr(e^y-1+y)}.
\]

This is a conditional constitutive prediction, not observed new physics or a
globally novel law. Section 2 proves the algebraic connection cannot supply it.
The inference concerns the controlled weak-field static limit demanded by the spec,
not an exact strong-field equality involving this linearized R00.

## 6. Matter Ward identity and cosmology

Ordinary matter conservation follows from S_m alone. For illustration, for matter
scalars define E_A=(1/sqrt(-g))delta S_m/delta psi_A. Under a compactly supported
diffeomorphism, delta g_mu nu=2 nabla_(mu xi_nu) and delta psi_A=xi^nu partial_nu psi_A.
Integration by parts in
delta S_m=int sqrt(-g)[T^{mu nu}delta g_mu nu/2+sum_A E_A delta psi_A] gives
nabla_mu T^mu_nu=sum_A E_A partial_nu psi_A. Thus on the ordinary matter equations,
nabla_mu T^{mu nu}=0 separately. For tensor/spinor matter the corresponding Lie or
local-frame variations add matter-Euler terms, which also vanish on matter shell.
No auxiliary stress has been bundled into this T, and no new baryonic force is used.

The exact curved-FLRW metric calculation, with arbitrary scale factor a(t) and
spatial curvature k_sp, gives

\[
 \kappa\rho=3(H^2+k_{\rm sp}/a^2)-\Lambda_{\rm eff},\qquad
 \kappa p=\Lambda_{\rm eff}-2\ddot a/a-H^2-k_{\rm sp}/a^2.
\]

These are expanding-capable Einstein backgrounds; nothing here imposes K=0 or H=0.
Spatial curvature k_sp is NOT the Fourier wave number k in the auxiliary audit.
Admitting FLRW does not fix the absence of MOND. Full scalar/vector/tensor perturbations,
GW speed, nonlinear well-posedness and the homogeneous gravitational constraint algebra
are not certified by this work. The failed MOND gate already decisively rejects the candidate.
No a0–Lambda relation is derived: a0 drops out of the exponential branch metric equation.

## 7. Where the surviving elliptic/nonlocal route must do genuinely new work

The algebraic-connection shortcut is closed under the stated assumptions. A metric-only
spectral projector is outside this theorem, but has its own obstructions. The companion
`spectral_escape_checks.py` tests them with Lorentzian rather than Euclidean matrices.

For R=lambda I+[[d,b],[-b,-d]], eta=diag(-1,1), d>0 and Delta=d^2-b^2>0, its
timelike projector and contravariant spatial operator are

\[
 Q_t=\tfrac12(I+(R-\lambda I)/\sqrt\Delta),\qquad
 P=(I-Q_t)\eta=\tfrac12
 \begin{pmatrix}d/\sqrt\Delta-1&-b/\sqrt\Delta\\
 -b/\sqrt\Delta&d/\sqrt\Delta+1\end{pmatrix}.
\]

The limit at R=lambda I depends on the approach direction; at the nonzero
null/Jordan boundary it diverges. Multiplying by a vanishing weight may control
regularity but changes rank and the sourced response; it is not automatically excluded
or certified. A nonlocal frame with boundary/history data is also not ruled out by
the pointwise normalized-projector failure.

There is a separate source-design obstruction. For p>0, a static no-slip isotropic Hessian
Phi_,ij=(p/3)delta_ij has R0i0j=p delta_ij/3 and Rijij=2p/3, and zero Weyl tensor
at linear order. These algebraic curvature values match flat dust FLRW at
dot H=-p, H^2=2p/3. A pointwise curvature-algebraic source which vanishes on every
such FLRW curvature tensor cannot also return p on every such static curvature jet.
This is a statement about curvature jets at the weak-field order, not a global
identification of static and expanding spacetimes.

A possible distinguishing quantity is J_acc=R_uu+L_u K+K_ij K^ij=div(a)=D^2N/N
for a hypersurface-normal unit u. It vanishes on FLRW and is Laplacian Phi statically.
But a Ricci-defined u depends on second metric derivatives and generically makes
J_acc fourth-order in the metric; hypersurface orthogonality is also not guaranteed.
An independent normal clock instead reopens the clock's constraint/health problem.

## 8. Exact remaining calculation list — in kill-order, from ONE action

This is a research program, not a claim that a completion exists. The efficient next
step is NOT another reparametrization of v_flat^4=G_N M_b a0. It is items 1–3 below.

| Order | Calculation and required output | Stop condition / why it is needed |
| --- | --- | --- |
| 1 | Freeze ONE differentiable covariant auxiliary action: specify projector P[g] or clock, scalar source J, boundary/state prescription, every multiplier and physical matter coupling. A schematic lambda(P nabla nabla chi-J) is not yet a theory. Derive delta P and delta J, not just delta chi. | If P/source is undefined on FLRW or its regularization erases the required static response, reject this action. The curvature-jet degeneracy above is a mandatory test. |
| 2 | Expand that action with lapse N, shift N^i, h_ij and all auxiliaries on an inhomogeneous background with off-diagonal Ricci R^0_1!=0. Construct the highest-time-derivative Hessian. Include all regularizer/source terms. | A diagonal static or Bianchi-I calculation misses eigenframe derivatives. The computed spectral subblock partial_d^2[lambda C P11]=3 lambda C b^2 d/[2(d^2-b^2)^(5/2)] is a trigger, NOT a complete DOF proof. |
| 3 | Full Legendre/Dirac algorithm: momenta, primary constraints, secondary and higher preservation, exact smeared Poisson operator, constraint independence and closure. Separate k=0, k!=0, zero-gradient, eigenvalue-gap-zero and generic branches. | Need N_grav=2 plus explicitly healthy allowed matter/clock. No ranks borrowed from the frozen auxiliary block or a different action. A hidden physical scalar/ghost rejects the action. |
| 4 | Vary the same action to obtain both 00 and spatial weak-field equations, independently solve Phi and Psi, and derive the density source coefficient G_N. Verify the full nonlinear divergence law, not only spherical force matching. | Need div[(1-exp(-|grad Phi|/a0))grad Phi]=4pi G_N rho_b AND Phi=Psi. Check the required exterior Ricci/density in section 5. |
| 5 | Derive the ordinary matter Ward identity from the same physical-metric matter action, and compute the constrained, gauge-invariant matter-to-matter response/retarded Green function. | Separate ordinary conservation from total-stress conservation. An elliptic equation with no scalar initial data can still carry an instantaneous physical channel. |
| 6 | Scalar/vector/tensor quadratic action and physical propagator on static nonzero-gradient and expanding backgrounds, followed by the leading nonlinear interactions as y->0. | Compute residues, poles, characteristic speeds, tensor kinetic sign and c_T. Prove a controlled degenerate limit; a zero quadratic coefficient is not absence of strong coupling. |
| 7 | Homogeneous action with lapse retained, all multiplier equations and their k=0 preservation; solve expanding FLRW with baryons/radiation/Lambda, then perturb it. | H!=0 and consistent expansion history must coexist with the local branch; do not import GR cosmology from another model or impose K=0. |
| 8 | Boosted 1PN physical metric: g00 through O(v^4), g0i through O(v^3), gij through O(v^2); transform to standard PPN gauge and match beta, gamma, alpha1, alpha2, alpha3. | These coefficients cannot be assigned from covariance or rest-frame slip. Derive measured G_N and its relation to the bare action coefficient. |
| 9 | Recompute the Solar-System external-field boundary-value problem for this same action and exact kernel; fit nuisance parameters with stated covariance and current data. | Existing QUMOND bounds do not automatically apply to every AQUAL/nonlocal realization; changing mu to clear a gate changes the requested theory. |
| 10 | Vary with respect to any field responsible for a0 and Lambda. Derive or explicitly posit a0=(c/2)sqrt(G_N rho_Lambda); if dynamical, derive its evolution and stress/extra modes. | Dimensional analysis fixes neither the 1/2 coefficient nor the dynamical linkage. Input normalization is acceptable under the spec, fabricated derivation is not. |
| 11 | Obtain at least one observable not algebraically equivalent to the already-fitted mass–acceleration relation; propagate nuisance parameters and compare independent data. | Existing conditional orbital-shape discriminators are candidates. Do not count the BTFR substitution as another independent Kepler law or infer novelty from absence of a search hit. |

The first unavoidable new calculation is the **full off-diagonal, lapse-and-shift-retaining
highest-derivative/constraint analysis of one defined regularized projector-and-source action**.
The source and its global definition must be specified before that calculation has a meaning.
There is currently no certified choice satisfying all of these obligations. A new matter/clock
completion remains another avenue, but it is not proved healthy simply by counting it separately.

## 9. Primary-source overlap and novelty boundary

Checked 2026-09-04; exact PDFs inspected, not merely search snippets.

- Shimada, Aoki, Maeda, *Metric-Affine Gravity and Inflation*,
  [arXiv:1812.03420v2](https://arxiv.org/pdf/1812.03420v2), header 21 December 2018:
  section II, equations (2.1)–(2.4), (2.12). Their distortion kappa is this report's C;
  their constant M_Pl is M. They supply the curvature decomposition and ordinary
  Palatini EH reduction, not an arbitrary nonlinear F theorem. **Adjacent established result.**
- Iosifidis, *The Full Quadratic Metric-Affine Gravity (Including Parity Odd Terms):
  Exact solutions for the Affine-Connection*,
  [arXiv:2112.09154v1](https://arxiv.org/pdf/2112.09154v1), 16 December 2021:
  equation (41), Corollaries 2–3, pp. 11–12. Vanishing hypermomentum means matter
  independent of the connection. The GR-equivalence statement assumes two nonzero
  matrix determinants and a 17-parameter quadratic action. It does not prove the
  arbitrary nonlinear, degenerate-branch claim here. **Adjacent established result.**

This was a bounded comparison of two primary metric-affine papers plus the repo's
vector/degenerate examples, not an exhaustive literature search. The project-level
extension is the direct covariance argument covering arbitrary differentiable algebraic
F without invertibility. It may be a known general auxiliary-field consequence in
other terminology. **No global originality, priority, or new law of nature is claimed.**

## 10. Verification and reproducibility

`run_audit.py` reruns every calculation script in this folder, its unittest suite,
and the listed related repository gates in isolated temporary output directories.
It writes the exact commands, exit codes, software versions, timing, captured output
and hashes to `computation_manifest.json` and `audit_output.txt`. The matrix and
constraint functions are regenerated in `connection_results.json`.

The connection tests were first run without the implementation: five assertion
failures (exit 1). After implementation all five passed (exit 0, 3.443 s).
The metric worker reported six passing tests and successful direct execution;
the aggregate run is the authoritative fresh verification of the integrated files.
Negative controls reject logarithmic MOND potentials as Einstein vacuum, unequal
vacuum potentials, and omission of the metric term in the frame identity.

Independent adversarial review found no mathematical blocker in the theorem or the
singular-branch scope. Its two findings were addressed: the Poisson test now explicitly
fixes the cross-block sign (skewness/rank alone do not), and the curvature-jet match
explicitly assumes p>0. Mathematical proofreading covered the new report only; no
equation was altered merely to improve style.

The provenance-runner's two tests also failed before its implementation, then passed.
An actual in-memory replacement Delta -> -Delta is rejected by the strengthened
Poisson cross-block test (one intended assertion failure, no test error). This mutation
did not edit any source file. Integration review corrected the aggregate randomness
record: the NEW checks are symbolic without sampling, while the old Palatini gate
uses seeds 11, 23, 37, 101 and the old degenerate gate uses seed 5. The imported legacy
`hunt_2026/hunt_lib.py` is fingerprinted too. Input hashes are taken before execution
and compared afterward so concurrent executable edits cannot silently certify a new version.
Missing input files become explicit failed records rather than aborting before a failure
manifest is written; a regression test first reproduced this stale-manifest risk and then passed.

The two earlier local aggregate runs also executed the existing untracked
`dw_intrinsic_elliptic_gate_2026/dw_intrinsic_elliptic_gate_2026.py` successfully
(19/19, exit 0). It is excluded from the final published runner: the reproducible
new result must not depend on unrelated files absent from a fresh checkout.
The final aggregate therefore runs nine commands: the 24-test new suite, three new
calculation executables, and five committed legacy gates. Exit statuses and exact
arguments are recorded rather than assumed.

The old vector Palatini script checks a restricted ansatz, not section 2's theorem.
The old degenerate-branch script also contains broader checks using hard-coded True;
its green total cannot certify those broader claims. Neither is promoted to a
full-theory certificate by being rerun here.

**Interpretation:** execution success verifies the reported algebra and test controls.
The MOND verdict is failure for the explicit action class, supported by the variational
proof and the independently derived nonzero exterior Ricci source. Uncomputed full
PPN/Dirac/stability gates are explicitly left uncomputed, not assigned a PASS.

## 11. Exact deliverables

All files created by this work are in
`qwen_claude_field_theory/closure_2026/algebraic_connection_no_mond_2026/`:

- `PLAN.md`
- `REPORT.md`
- `connection_checks.py`
- `test_connection_checks.py`
- `metric_branch_checks.py`
- `test_metric_branch_checks.py`
- `spectral_escape_checks.py`
- `test_spectral_escape_checks.py`
- `run_audit.py`
- `test_run_audit.py`
- `connection_results.json`
- `computation_manifest.json`
- `audit_output.txt`

No existing physics source, user data or unrelated dirty file is modified. Regenerate
the complete recorded audit from the repository root with

```sh
python3 qwen_claude_field_theory/closure_2026/algebraic_connection_no_mond_2026/run_audit.py
```

The manifest stores each actual subprocess command, working directory, exit status,
timeout flag and execution duration. Temporary working directories are regenerated
on each run; all calculation paths resolve from the repository root.
