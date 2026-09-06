# Constraint-first metric MOND: construction and unresolved causal gate

Date: 2026-09-05. Status: **OPEN, not a completed relativistic theory.**

This study keeps the exact exponential law and puts MOND in the metric lapse
constraint, rather than in an additional force-carrying scalar. It adds an
explicit volume-preserving trace-momentum constraint. All results below use
this one Hamiltonian. No PPN or stability results are imported from AeST,
f34, g03j, or the repository's separately written `THE_ACTION`.

`metric_constraint.py` is the executable calculation; its JSON includes the
actual constraint generations, Poisson matrices, source solutions, and
checks. A successful ordinary run means algebraic checks passed, not that the
theory passed the physical requirements. The strict principal-causality run
returns **2**.

## 1. Explicit Hamiltonian and its variation

Set c=1. Normalize the ADM momentum by factoring out 1/(16 pi G).
On a compact spatial leaf Sigma, define

\[
V=\int_\Sigma\sqrt h\,d^3x,\qquad
\bar\pi=V^{-1}\int_\Sigma\pi\,d^3x,\qquad
\pi=h_{ij}\pi^{ij},\quad a_i=D_i\ln N.
\]

The candidate is the first-order action

\[
S={1\over16\pi G}\int dt\,d^3x\,[\pi^{ij}\dot h_{ij}-\mathcal H]
  +S_m[g,\psi],
\]
\[
\boxed{\mathcal H=N\mathcal H_{\rm GR}+N^i\mathcal H_i
-2N\sqrt h\,a_0^2F(z)+\lambda(\pi-\sqrt h\bar\pi)},
\quad z={a_i a^i\over a_0^2},
\]
\[
F(z)=2[1-(1+\sqrt z)e^{-\sqrt z}],\qquad
\mathcal H_{\rm GR}={\pi^{ij}\pi_{ij}-\pi^2/2\over\sqrt h}
-\sqrt h(R^{(3)}-2\Lambda),\quad
\mathcal H_i=-2h_{ij}D_k\pi^{jk}.
\]

Matter couples minimally to the ADM spacetime metric. This is a
preferred-foliation Hamiltonian, **not yet a generally covariant clock-field
completion**. An infinite-volume average has not been silently defined.

Write H_m for the matter Hamiltonian in the same normalization. Variation of
N, N^i, and lambda gives, respectively,

\[
0=\mathcal H_{\rm GR}-2\sqrt h\,a_0^2(F-2zF_z)
 +4\sqrt h D_i(F_z a^i)+{\delta H_m\over\delta N},
\]
\[
0=\mathcal H_i+{\delta H_m\over\delta N^i},\qquad
0=\pi-\sqrt h\bar\pi.
\]

For example, the lapse variation uses
delta a_i=D_i(delta N/N); its integration by parts generates the displayed
divergence. It is not a phenomenologically inserted Poisson equation.
Let \(\bar\lambda=V^{-1}\int\sqrt h\lambda\,d^3x\). The remaining Hamilton
equations are

\[
\dot h_{ij}={2N\over\sqrt h}(\pi_{ij}-\tfrac12\pi h_{ij})
 +\mathcal L_{\mathbf N}h_{ij}+(\lambda-\bar\lambda)h_{ij},
\]
\[
\begin{split}
\dot\pi^{ij}={}&-N\sqrt h(R^{ij}-\tfrac12h^{ij}R^{(3)}+\Lambda h^{ij})
 +\sqrt h(D^iD^jN-h^{ij}\Delta N)\\
&+{N h^{ij}\over2\sqrt h}(\pi^{kl}\pi_{kl}-\tfrac12\pi^2)
 -{2N\over\sqrt h}(\pi^{ik}\pi_k{}^j-\tfrac12\pi\pi^{ij})
 +\mathcal L_{\mathbf N}\pi^{ij}\\
&+N\sqrt h(a_0^2F h^{ij}-2F_z a^i a^j)
 -(\lambda-\bar\lambda)(\pi^{ij}-\tfrac12\bar\pi\sqrt h h^{ij})
 -{\delta H_m\over\delta h_{ij}}.
\end{split}
\]

The mean-subtraction terms follow by varying both the numerator and
denominator of bar-pi. These equations specify the candidate; their
**nonlinear constraint-preservation closure is not established here**.

## 2. Independent static potentials and the exact kernel

Take a weak, static, zero-momentum branch with homogeneous lambda and
\(g_{00}=-(1+2\Phi)\), \(h_{ij}=(1-2\Psi)\delta_{ij}\).
At leading weak-field order, keeping all orders in |grad Phi|/a0, the action
density multiplied by 16 pi G is

\[
L_{\rm stat}=2|\nabla\Psi|^2-4\nabla\Phi\cdot\nabla\Psi
 +2a_0^2F(|\nabla\Phi|^2/a_0^2)-16\pi G\rho_b\Phi.
\]

Independent variations, not an assigned slip condition, give

\[
\Delta(\Psi-\Phi)=0,\qquad
\nabla\cdot(\nabla\Psi-F_z\nabla\Phi)=4\pi G\rho_b.
\]

With boundary data removing the harmonic difference, F_z=exp(-y) gives

\[
\boxed{\Psi=\Phi,\qquad
\nabla\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]=4\pi G\rho_b.}
\]

Thus the leading static metric ratio is one, the measured high-acceleration
Newton coefficient is G at this order, and spherical Gauss integration gives
\(\mu(g/a_0)g=GM_b(r)/r^2\). Consequently
\(v_\infty^4=Ga_0M_b\) for a finite spherical mass. This is the familiar MOND
BTFR consequence, not a new empirical law. Full PPN gamma, beta and all three
alpha parameters are **not certified** by this static calculation.

The cosmological relation a0^2=Lambda/(32 pi) may be imposed in c=1 units;
it is not derived. Both project acceleration footings are permitted because
these gates are dimensionless. F(0)=0 and F(infinity)=2 also imply a
high-acceleration vacuum offset Lambda_high=Lambda-2a0^2; this is not silently
identified with the homogeneous cosmological constant.

### Controlled static zero field, not controlled dynamics

Eliminating Psi yields the positive static energy primitive

\[
\mathcal G(y)=y^2-F(y^2)
=y^2+2(1+y)e^{-y}-2
=\tfrac23y^3-\tfrac14y^4+O(y^5).
\]

The code derives G'/(2y)=mu, G(y)>y^2-2, and
lambda_parallel-lambda_perp=y exp(-y)>0. Since mu>0 for y>0,
the radial energy is strictly convex, although its Hessian vanishes at zero.
For a bounded Lipschitz static patch with fixed Dirichlet data and
rho_b in H^-1, consider

\[
E[\Phi]={a_0^2\over8\pi G}\int\mathcal G(|\nabla\Phi|/a_0)\,d^3x
 +\langle\rho_b,\Phi\rangle.
\]

The quadratic lower bound and Poincare inequality bound every minimizing
sequence in H^1; a weakly convergent subsequence exists. Convexity supplies
weak lower semicontinuity, so the limit minimizes E. Strict convexity of the
gradient energy and fixed boundary data give uniqueness. Its first variation
is exactly the MOND equation. This is an analytic weak-solution argument,
with its algebraic identities checked computationally, not a numerical
existence proof. It does not imply uniform ellipticity, a differentiable
linear response at zero, or healthy nonlinear time evolution. A static patch
is not a globally static compact universe containing uncompensated positive
mass; cosmological matching remains necessary.

## 3. Actual local quadratic Dirac calculation

For q=k^2>0 retain the scalar spatial gauge coordinate E until after the
Legendre transform. The velocity part and lapse potential are

\[
L_2=-6\dot P^2+4q\dot P(B-\dot E)+2qP^2-4qnP+2\alpha qn^2.
\]

The candidate's trace constraint becomes p_P=0, with a rescaling of lambda.
The computed Hamiltonian is

\[
H_2=-{p_Pp_E\over4q}+{3p_E^2\over8q^2}+Bp_E
-2qP^2+4qnP-2\alpha qn^2+\lambda p_P.
\]

The algorithm starts with p_n,p_B,p_lambda, computes their brackets with H,
and continues consistency using left null vectors of the multiplier matrix.
For generic alpha !=0,1 the successive independent generations are

1. p_n, p_B, p_lambda (primary).
2. n-P/alpha, p_E, p_P (secondary).
3. P.
4. lambda.

All remaining preservation residuals vanish after solving the primary
multipliers; only the shift multiplier remains free. In precisely that
constraint order the actual Poisson matrix is

\[
\begin{pmatrix}
0&0&0&-1&0&0&0&0\\
0&0&0&0&0&0&0&0\\
0&0&0&0&0&0&0&-1\\
1&0&0&0&0&-1/\alpha&0&0\\
0&0&0&0&0&0&0&0\\
0&0&0&1/\alpha&0&0&-1&0\\
0&0&0&0&0&1&0&0\\
0&0&1&0&0&0&0&0
\end{pmatrix}.
\]

Its rank is computed symbolically, not supplied to the algorithm.

| Local quadratic branch | Independent constraints | First class | Second class | Scalar pairs |
|---|---:|---:|---:|---:|
| Generic symbolic alpha, q>0 | 8 | 2 | 6 | 0 |
| alpha=0, recomputed | 8 | 2 | 6 | 0 |
| alpha=1, recomputed | 6 | 4 | 2 | 0 |

At alpha=0 the higher constraints are lambda,n. At alpha=1 the chain stops
after the second generation, with n-P replacing n-P/alpha; the primary
multiplier solution changes to (lambda, free, free). Its rank is **2, not 6**.
This is enhanced linear degeneracy, not evidence that nonlinear evolution is
regular. In particular a generic source cannot be inverted by dividing by
1-alpha at that point. The JSON contains all three full matrices and a
rational witness alpha=1/2, q=1 in addition to the symbolic branch.

These are complete constraints of the **specified quadratic scalar model**,
not all constraints of the nonlinear field theory. The principal transverse
vector block remains the GR constraint block; a full finite-background vector
calculation is outstanding. The TT block is derived from
L_TT=[tr(dot H_TT^2)-q tr(H_TT^2)]/4. The computed kinetic eigenvalues are
1,1 and both tensor frequencies obey omega^2=q. This supports two healthy
luminal tensors at principal order, not an all-background stability theorem.

## 4. k=0 is not discarded or constrained to be static

On a homogeneous isotropic configuration, with homogeneous lambda,
the volume-preserving trace term and its first variation vanish. The code
checks the weighted projection on constant configurations independently.
The homogeneous Lagrangian is

\[
L_0=-6A\dot A^2/N-2\Lambda NA^3-NM_d,
\qquad H^2=\Lambda/3+M_d/(6A^3).
\]

Here M_d=16 pi G times the comoving dust mass density. For an explicit canonical
matter clock take minimally coupled irrotational dust,
S_d=-1/2 int sqrt(-g) rho_d[(partial T)^2+1]. Its future-directed homogeneous
branch has H_d=N p_T, p_T>0, with dot T=N. This is ordinary matter, not a
hidden gravitational auxiliary. This uses a legitimate reduced matter phase
space: before eliminating its density r, H_d=N[p_T^2/(2A^3 r)+A^3 r/2],
with primary p_r=0 and secondary
chi_r=A^3/2-p_T^2/(2A^3 r^2)=0. Their bracket is
{p_r,chi_r}=-p_T^2/(A^3 r^3), nonzero on the positive-density branch.
This second-class pair eliminates r=p_T/A^3 and p_r, not the dust clock.
The exact minisuperspace Legendre transform in that reduced matter space gives

\[
H_0=N[-p_A^2/(24A)+2\Lambda A^3+p_T].
\]

Primary constraints p_N,p_lambda generate one secondary Hamiltonian
constraint; its next preservation vanishes. The computed 3 by 3 Poisson
matrix is zero: three first-class constraints, no second-class constraints.
Four configuration variables (A,N,lambda,T) leave **one homogeneous physical
pair including the matter clock**, separately from the zero local scalar
pairs above. On an expanding branch,

\[
p_A^2=24A(2\Lambda A^3+p_T)\ne0.
\]

The rational witness Lambda=3, M_d=6, A=1 gives H^2=2. We have not imposed
K=0, p_A=0, or H=0. Dust perturbation health, caustics and cosmological data
are not settled by a background existence calculation.

## 5. Physical curvature, not just an instantaneous lapse

Around an acceleration directed along z, direct differentiation of F gives

\[
M_{ij}=e^{-y}(\delta_{ij}-y\hat a_i\hat a_j),\quad
\alpha(\hat k)=e^{-y}(1-y\cos^2\theta),
\]
\[
q(1-\alpha)=\mu_t(k_x^2+k_y^2)+\mu_l k_z^2,
\quad\mu_t=1-e^{-y},\quad\mu_l=1+(y-1)e^{-y}.
\]

This anisotropy is retained; a finite-field exponential background is not
replaced by an isotropic constant alpha. With normalized sources rho=T00,
S=Tii and flat conservation, minimal metric coupling gives

\[
H_s=H_2+n\rho+PS-B\dot\rho-E\ddot\rho.
\]

Solving the sourced constraints, and only then fixing E=dot E=0, gives

\[
P=-{\rho+\alpha S\over4q(1-\alpha)},\quad
n=-{\rho+S\over4q(1-\alpha)},\quad
B=-{3\dot\rho\over4q^2},\quad p_E=\dot\rho,\quad p_P=0.
\]

Relative to alpha=0, delta P=delta n=-alpha(rho+S)/[4q(1-alpha)]
and delta B=0. The observable correction is therefore

\[
\delta R_{0i0j}=(\partial_i\partial_j+\delta_{ij}\partial_t^2)\delta P.
\]

Let G_A solve the anisotropic elliptic operator and G_I solve Delta:

\[
G_A=-{1\over4\pi\mu_t\sqrt{\mu_l}}
\left({X^2+Y^2\over\mu_t}+{Z^2\over\mu_l}\right)^{-1/2},
\quad G_I=-{1\over4\pi r},\quad V=G_A-G_I.
\]

Coordinate rescaling fixes its delta-function normalization; the code
independently checks the differential equation off the source.
An explicitly conserved probe is T00=f partial_z^2 sigma,
T0z=-f' partial_z sigma, Tzz=f'' sigma, with other components zero.
The script verifies both conservation equations for arbitrary smooth sigma.
For the point-profile limit and f(t)=t^6 for t>0, zero for t<0,

\[
\delta P=\tfrac14[f\partial_z^2V+f''V].
\]

At y=ln 2, (X,Y,Z)=(1,0,0), t=1/10, the computed curvature difference is

\[
\delta R_{0x0x}=-0.03853164394383143
\]

in normalized units, before the GR light cone reaches the probe. Setting
mu_t=mu_l=1 makes the same expression identically zero. This is an actual
curvature-response warning, not a conclusion from an elliptic gauge potential.

**Scope is crucial:** this is the anisotropic frozen highest-spatial-derivative
quadratic model. A solved finite-gradient background, lower-derivative
lapse/metric terms, induced sector mixing, global boundary conditions and a
physical positive-energy matter realization of the formal probe have not all
been included. It is consequently **not yet a full nonlinear acausality
no-go**. The strict clean-principal-causality gate fails; whether the complete
candidate has an uncancelled physical instantaneous channel remains the next
decisive calculation. The formal infinite-volume Green probe is also distinct
from a solved compact-leaf boundary problem.

## 6. Ward identity and unearned certificates

For ordinary minimally coupled matter, with
delta S_m=int sqrt(-g)[(1/2)T^{mu nu}delta g_mu nu+E_psi delta psi],
an infinitesimal diffeomorphism and integration by parts give

\[
\nabla_\mu T^{\mu\nu}=E_\psi\nabla^\nu\psi
\]

for scalar matter; the tensor-field version includes its corresponding
Euler derivatives. Thus ordinary matter is separately conserved on its own
equations of motion, not merely after adding auxiliary stress. This follows
from S_m's metric covariance. It does **not** establish compatibility of all
gravitational constraints with arbitrary matter histories in this
preferred-foliation theory; the nonlinear Dirac calculation must test that.

Still unproved: full nonlinear DOF/constraint closure; finite-background
causality; strong coupling through y=0; complete scalar/vector/tensor
perturbations; boosted and second-order PPN beta, gamma, alpha_1, alpha_2,
alpha_3; cosmological perturbations and fits; a covariant clock completion.
No expected PPN parameter, Poisson rank, determinant or DOF count is used as
an input to the derivation. Test expectations only check computed results.

## 7. Attribution and the latest commits

The lapse-acceleration mechanism itself is known. Blanchet and Marsat,
*Modified gravity approach based on a preferred time foliation*, Physical
Review D 84, 044056 (published 26 August 2011), equations (2.4), (4.5)-(4.6),
derive leading no-slip MOND from a preferred-foliation f(a) action.
Our notation maps as f(a)=Lambda-a0^2 F(a^2/a0^2), hence their
chi=f'(a)/(2a)=-F_z and mu=1+chi. This source supports the base static
mechanism, **not the additional trace constraint or its consistency**.
[Primary published PDF](https://www2.iap.fr/users/blanchet/images/PhysRevD.84.044056.pdf),
DOI 10.1103/PhysRevD.84.044056; inspected 2026-09-05. No novelty certificate
is asserted for this Hamiltonian variant. Search scope was the named
Blanchet-Marsat preferred-foliation mechanism, not all constrained gravity.

HEAD advanced during work from 0d846a52a to 9ff805406, adding g03k and g03l.
Those are useful static/empirical developments, not a resolution of the
action/constraint issue:

- g03k derives s_cross=xi x_cross(y_e) from its assumed screened AQUAL PDE.
  Its code still uses the pure exponential at y_e>1, not g03j's monotone
  completion. Its crossing numbers cannot be transferred without recomputing
  the background coefficients for that completion.
- g03l compares the supplied monotone kernels with paired, profiled SPARC
  fits. Its committed outputs do not distinguish them from the exponential
  in that design. This turn inspected the files, not a fresh empirical rerun.
- The literal action in `THE_ACTION_2026-09-05.md` omits f34's acceleration
  mixing/source coupling, yet its static section assumes a matter-sourced
  MOND scalar. On a static, zero-current, positive-J' branch, minimal matter
  coupling does not insert such a source. Multiplication of the homogeneous
  scalar equation by phi and integration with vanishing boundary terms gives
  an integral proportional to J'(X)[|D phi|^2+xi^2|DD phi|^2]=0 for the
  inside-J placement. This forces constant phi on that branch. A different
  branch or added coupling needs its own variation. Neither new commit
  changes that action. This restricted mismatch is not a no-go for every
  scalar carrier; in particular measured-G renormalization changes g03j's
  zero-floor additive-force assumptions (see `REPORT.md` in this directory).

## 8. Reproduction and next calculation

Created in this study, without altering other research files:

1. `metric_constraint.py`
2. `test_metric_constraint.py`
3. `metric_constraint_results.json`
4. `METRIC_CONSTRAINT.md`
5. `metric_constraint_manifest.json`

Run from repository root:

```bash
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_constraint.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_constraint_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_constraint.py --require-clean-principal-causality
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_constraint_manifest.json
git diff --check
```

The manifest records actual exit statuses, the failing-before-implementation
tests, the symbolic-expression comparison bug and its fix, software, input
hashes, bounds and non-claims. No commit or push was performed in this study.
Final measured runs: 22 algebraic checks, exit 0; strict principal-causality
gate, exit 2; all 39 tests in this research directory, exit 0. The latter
include the existing bridge, source-dynamics, selective-screen and
causal-screen regressions, not the entire repository's closure suite.

**Strongest result:** the explicit constrained metric Hamiltonian gives the
exact requested static law and independent no-slip equation, a controlled
static variational zero-field limit, no local scalar pair in its complete
principal quadratic Dirac calculation, and an expanding homogeneous sector
whose matter clock is explicitly counted. These do not establish a full
relativistic theory.

**Next unavoidable calculation:** expand this same Hamiltonian about a solved
nonzero-gradient background, preserving the full mean-subtracted constraint
chain and all metric sectors, then compute the complete retarded curvature
response to admissible conserved matter. If the principal tail survives,
this candidate fails the user's causality requirement even if its exact
local gravitational DOF count is two. If it cancels, nonlinear Dirac closure
and boosted PPN become the next gates. Status remains **OPEN**.
