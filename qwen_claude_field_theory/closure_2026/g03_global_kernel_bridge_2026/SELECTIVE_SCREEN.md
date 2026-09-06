# Selective screening: Newtonian normalization repaired, stability lost

Status: **DEAD on the tested flat, constant-scalar branch**, not a universal
MOND no-go and not a completed field theory. No empirical discovery or novelty
claim. Current inspected HEAD: `90dab18b8`; the live working tree was dirty.

## Bounded question and explicit alternative action

Can the higher-spatial-derivative screen act only on the nonlinear excess,
leaving the scalar's Newtonian contribution intact? This is a NEW operator,
not the action already subjected to the repository's Solar-System fit.
In units c=1 and signature (-+++), consider

\[
 S={1\over16\pi\widetilde G}\int\!\sqrt{-g}\,[R-2\Lambda
 -{K_B\over2}F_{\mu\nu}F^{\mu\nu}-c_2(\nabla_\mu n^\mu)^2+c_4a_\mu a^\mu
 +2A a^\mu\partial_\mu\chi-A Y+K(Q-Q_0)^2
 -A a_0^2J(Y/a_0^2)-A\xi^2\mathcal H_W]+S_m[g,\psi].
\]

Here \(n_\mu=-\partial_\mu T/\sqrt{-(\partial T)^2}\),
\(q_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu\),
\(a_\mu=n^\nu\nabla_\nu n_\mu\), \(F_{\mu\nu}=2\nabla_{[\mu}n_{\nu]}\),
\(Q=n^\mu\partial_\mu\chi\), \(V_\mu=q_\mu{}^\nu\partial_\nu\chi\),
\(Y=V_\mu V^\mu\), and

\[
 W_\mu=V_\mu-\beta a_\mu,\qquad
 \mathcal H_W=q^{\alpha\beta}q^{\mu\nu}
 (\nabla_\alpha W_\mu)(\nabla_\beta W_\nu),\qquad
 \beta={1\over1+j_N}.
\]

\(A=2-K_B>0\), \(c_{14}=K_B+c_4\), \(K=-K_2>0\),
\(0<c_{14}<K_B<2\), \(c_2,\xi>0\). Here beta is an operator coefficient,
**not** the PPN beta. For the requested exponential law use the parametric
J reconstruction in `ESCAPE_REPORT.md` (mu_exp branch), with j_N=3.
Only its necessary limits enter this audit:
\(J'(\infty)=j_N\), \(J'(0)=j_0=A/(2-c_{14})-1\).
The a0--Lambda relation remains input, not a derivation.

Scope: scalar perturbations in clock-unitary gauge about the flat,
constant-chi, Q0=0 branch; Lambda=0 for the exact flat-background calculation.
No inference here that a nonzero-Lambda, nonzero-Q0 cosmological branch has
been fully varied or tested. All displayed instability inequalities concern
this explicit quadratic limit. a0 drops out, so the dimensionless result
is identical on both repository acceleration-scale footings.

## Variation, with the lapse and shift retained

For a real spatial Fourier mode, let q=k^2, x=xi^2 k^2,
N=1+n, N_i=partial_i t, gamma_ij=(1-2P)delta_ij. Write j=J' on the
constant-gradient limit. The action gives

\[
 L_2=-6\dot P^2+4q\dot P t-c_2(-3\dot P+qt)^2+K\dot\chi^2
 +q[2P^2-4nP+c_{14}n^2+2An\chi-A(1+j)\chi^2]
 -A\xi^2q^2(\chi-\beta n)^2.
\]

The script differentiates this expression and independently compares its
full bra/ket matrix against a fresh, cache-free build of f34 with precisely
the stated operator replacement. It does not import a numerical verdict.
Define C=6+4/c2, D=c14-A beta^2 x, E=A(1+beta x), F=A(1+j+x).
The two auxiliary equations and two evolution equations are

\[
 Dn-2P+E\chi=0,\qquad qt=(3+2/c_2)\dot P,
\]
\[
 (12+18c_2)\ddot P-(4+6c_2)q\dot t+4q(P-n)=0,
 \qquad K\ddot\chi+q(F\chi-En)=0.
\]

For static matter, the spatial-potential equation gives P=n independently.
The scalar equation at j=jN then gives chi=n/(1+jN); the higher-derivative
term and its first variation vanish on that solution. The lapse equation
with matter source 16 pi Gtilde rho consequently yields

\[
 \Phi=n=\Psi=P,\qquad
 G_{\rm measured}={2\widetilde G\over2-c_{14}-A/(1+j_N)}.
\]

This G is independent of k on the particular sourced Newtonian solution.
It is not assigned to the bare coupling. Possible homogeneous static
solutions require boundary conditions; uniqueness at every momentum is
not asserted. This result is a Newtonian static gate, not a full PPN result
or a finite-xi exact AQUAL derivation. Spherical xi=0 reconstruction is
not a proof of the requested nonspherical PDE.

## Exact stability obstruction

For k!=0 and D!=0, elimination gives kinetic matrix diag(C,K)>0 and

\[
 L_{\rm red}=C\dot P^2+K\dot\chi^2
 -q(P,\chi)\mathsf W(P,\chi)^T,
 \quad
 \mathsf W=\begin{pmatrix}4/D-2&-2E/D\\-2E/D&F+E^2/D\end{pmatrix}.
\]

Thus **D<0 implies negative stiffness**, since W11<0. With positive
kinetic energy a negative eigenvalue of the kinetic-normalized stiffness
gives an actual omega^2<0 mode. This argument holds independently of j.
At the deep-MOND value j0, the stronger exact identity is

\[
 \boxed{\det\mathsf W=
 {2Ax[\,2-c_{14}-A\beta\,]^2\over(2-c_{14})(c_{14}-A\beta^2x)}}.
\]

For nonzero beta and an unrestricted continuum of momenta, D eventually
becomes negative. For the witness KB=1/5, c14=1e-5, c2=1/100, K=10,
jN=3, xi=1:

\[
 k_*\xi=\sqrt{{c_{14}\over A\beta^2}}=0.0094280904.
\]

At k^2=2k_*^2 the exact polynomial has roots displayed numerically as
omega^2=(1.008258048e-10, -5.935634601). The instability is already present
below k xi=1, the intended fourth-order screening scale. These frequencies
use xi=1 units, not measured physical rates.

This is not a ghost inferred from changing a lapse sign: the reduced
kinetic matrix remains positive. It is a gradient instability.

## The singular momentum and actual Dirac preservation

Do not divide through D=0. After the nonsingular shift reduction, retain
the lapse in the full descriptor, with lambda=omega^2/q:

\[
 \det\begin{pmatrix}C\lambda+2&0&-2\\0&K\lambda-F&E\\-2&E&D\end{pmatrix}
 =DCK\lambda^2-[C(DF+E^2)+K(4-2D)]\lambda+2[(2-D)F-E^2].
\]

At D=0 the determinant is linear, not identically zero. The constraint
2P=Echi leaves the finite branch
lambda=(4F-2E^2)/(CE^2+4K). The other branch runs through infinity and is
unstable on the D<0 side. It is not removed at neighboring momenta.

The script Legendre-transforms L2 before eliminating n,t. Primary
constraints are p_n=p_t=0. At generic D, convenient secondaries are
Cn=2q(Dn-2P+Echi), Ct=(4q^2 t-q p_P)/3. Their actual Poisson matrix in
the order (p_n,p_t,Cn,Ct) is

\[
 \begin{pmatrix}
 0&0&-2qD&0\\0&0&0&-4q^2/3\\
 2qD&0&0&4q^2/3\\0&4q^2/3&-4q^2/3&0
 \end{pmatrix}.
\]

Preservation fixes the primary multipliers for D!=0. At D=0 it generates
a tertiary momentum constraint and a quaternary lapse constraint instead.
The algorithm computes left-null consistency conditions, adds independent
constraints until closure, evaluates all Poisson brackets, and solves
the remaining multiplier equations. The complete generated constraints,
bracket matrices and multipliers are in `selective_screen_results.json`.

| Exact rational witness sector | Constraints | PB rank | FC / SC | Scalar modes |
|---|---:|---:|---:|---:|
| k^2=k_*^2/2 | 4 | 4 | 0 / 4 | 2 |
| k^2=k_*^2 | 6 | 6 | 0 / 6 | 1 |
| k^2=2k_*^2 | 4 | 4 | 0 / 4 | 2 |

Ranks and counts are computed, not supplied to the algorithm. These are
gauge-fixed **quadratic scalar** counts, not a full nonlinear Dirac theorem
or N_grav=2. The homogeneous sector is evaluated separately: the screen
vanishes, the shift parametrization itself vanishes, and
L0=-(6+9c2) Pdot^2+K chidot^2. Its velocity Hessian has rank two, but the
nonlinear global lapse constraint is absent at this perturbative order.
No homogeneous physical count, homogeneous ghost, or FLRW certificate is
inferred from it.

## What this settles and what it does not

The simplest matched local Hessian screen repairs measured G but fails
stability on the tested branch. An EFT cutoff k<k_* avoids this counterexample
only by excluding the intended k xi~1 screening regime. It is not a full
resolution. Changing only the lapse coefficient cannot fix all momenta:
positive stiffness would require 0<D<=2 and E^2<=(2-D)F<=2F, whereas
E^2/F grows as A beta^2 x at large x.

The next architectural calculation, if this route is continued, is an
explicit bounded or frequency-dependent response replacing the polynomial
spatial screen, with its complete pole/constraint accounting. It must
preserve the measured-G relation without hidden modes or instantaneous
physical signaling. No such completion is supplied here. Adding another
static fit cannot answer that question.

Matter's minimal metric coupling in the stated action preserves its own
diffeomorphism Ward identity on matter shell: under a compactly supported
infinitesimal diffeomorphism zeta,
\(0=\delta_\zeta S_m=\int\sqrt{-g}\,T^{\mu\nu}\nabla_\mu\zeta_\nu\)
after imposing the matter Euler--Lagrange equations. Integration by parts
and arbitrary zeta give \(\nabla_\mu T^{\mu\nu}=0\), independently of the
auxiliary stress. That identity does
not repair the exhibited gravitational instability. Full covariant field
variation, nonlinear constraints, nonzero-Q0 FLRW, finite-gradient modes,
vector/tensor sectors and acceptable PPN values remain uncomputed for this
new action. No earlier action's pass is transferred to it.

## Reproduction and exact changes

This turn creates only `selective_screen.py`, `test_selective_screen.py`,
`selective_screen_results.json`, `selective_screen_manifest.json`, and this
report in the existing `g03_global_kernel_bridge_2026` directory. No existing
research file was edited; no commit or push was performed.

Run from the repository root:

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_selective_screen.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/selective_screen.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/selective_screen_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/selective_screen.py --require-stable
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03c_zero_field_limit_outside_J.py
git diff --check
```

The first test-first run intentionally exited 1 (missing calculation).
After implementation, the focused six tests and nine internal identities
exit 0. `--require-stable` exits **2**, the physical counterexample; exit 0
on algebra checks does not certify the theory. The full local suite passed
23 tests (exit 0), and g03c passed its eight checks (exit 0). g03c concerns
a different static operator, so its pass is a regression result, not a
certificate for this action. `git diff --check` exited 0. An in-memory
mutation doubling the ADM screen coefficient was rejected by the independent
source-comparison check; the original files were not changed. Manifest
validation is recorded separately after execution.

Self-review: the new report's equations, notation and scope were checked
using Mathbox mathematical proofreading; no typographical mathematical-token
changes were needed. An independent algebra review also reproduced the
stiffness, threshold and lapse-inclusive crossing polynomial. That review
does not replace the executable checks.
