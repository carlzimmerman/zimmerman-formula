# Reconstructed scalar function, followed by the actual zero-field gate

2026-09-05. Follow-up to REPORT.md. Relevant HEAD: `90dab18b8`.

## Outcome

1. **Constructed:** an explicit single-valued J for each of the two alternative
   exponential kernels, at J_N=3. This passes the preceding monotonicity gate
   and reproduces the spherical law in the unscreened, charge-free static
   limit, using the large-scale Newton constant.
2. **Refuted in the stated sector:** the original inside-J operator has a
   gradient instability at the exact deep-MOND endpoint. This follows from
   the actual time-dependent quadratic action after varying and eliminating
   lapse and shift, not from a frozen-metric guess. It holds for every k>0
   when K=-K2>0, c2>0, 0<c14<K_B<2, xi>0.
3. **An explicit alternative passes this particular gate:** putting a positive
   independent fourth-order term outside J gives positive kinetic and spatial
   matrices for every k>0 on this same zero-field background. This is a
   DIFFERENT action. No finite-gradient, full PPN, nonlinear Dirac, k=0,
   cosmological stability, empirical or causal completion is asserted.

The new wide-binary commit withdraws the unmeasured 3% ceiling. It does not
exclude J_N=3 under its proxy statistic. Thus the earlier J_N=30 exclusion
was never an exclusion of every possible normalization, as REPORT.md said.

## 1. Explicit candidate actions being distinguished

Set c=1 and define n_mu=-partial_mu T/sqrt(-partial T squared),
q_mu_nu=g_mu_nu+n_mu n_nu, a_mu=n^nu nabla_nu n_mu,
F_mu_nu=2 nabla_[mu n_nu], Q=n^mu partial_mu chi,
V_mu=q_mu^nu partial_nu chi, Y=V_mu V^mu, and
Hcal=q^(alpha beta) q^(mu nu) nabla_alpha V_mu nabla_beta V_nu.
With A=2-K_B, the two actions share

\[
S={1\over16\pi\widetilde G}\int\sqrt{-g}\,d^4x
\left[R-2\Lambda-{K_B\over2}F_{\mu\nu}F^{\mu\nu}
-c_2(\nabla_\mu n^\mu)^2+c_4a_\mu a^\mu
+2A a^\mu\nabla_\mu\chi-A Y+K(Q-Q_0)^2-A\mathcal U\right]+S_m[g].
\]

Here K>0, c14=K_B+c4, and the alternative scalar functionals are

\[
\mathcal U_{\rm in}=a_0^2J((Y+\xi^2\mathcal H)/a_0^2),\qquad
\mathcal U_{\rm out}=a_0^2J(Y/a_0^2)+\xi^2\mathcal H.
\]

This writes the source operators and their two placements explicitly; it
does not claim a full nonlinear variation has been carried out here.
The computation expands about Minkowski, Q0=0, constant chi, clock rest,
Lambda=0. It independently reproduces this sector from ADM variables.
The gravitational conventions are those of f34; matter coupling is written
but a new matter Ward computation is not part of this follow-up.
The scale relation a0=(c/2)sqrt(G rho_DE) is still an input, not derived.

## 2. The scalar function is now specified, not just 'chosen appropriately'

Let B=2-c14, eta=A/B, f=eta/(1+J_N-eta), q=1+f.
For K_B=1/5, c14=1/100000, J_N=3, this gives f approximately 0.290324,
above both thresholds proved in REPORT.md. G_infinity=q G0,
G0=2 G_tilde/B. Put X=Y/a0^2 and normalize J(0)=0.

For the exact **mu_exp target**, use the parameter x=g/a0 and e=exp(-x):

\[
\boxed{X(x)={x^2(f+e^{-x})^2\over\eta^2q^2},\qquad
J(X(x))={f x^2+2[e^{-x}(x^2+x+1)-1]\over\eta q}-X(x).}
\]

Differentiating, rather than imposing a field equation, gives

\[
J'(X(x))={\eta q\over f+e^{-x}}-1.
\]

The static action's scalar variation gives F(s)s=g0, where
s=|grad(eta chi)| and F=(1+J'-eta)/eta. Substituting the reconstructed
function yields s/a0=x(f+e^-x)/q and g0/a0=x(1-e^-x)/q. Their sum is x.
Consequently g_b=q g0 satisfies g_b=g(1-exp(-g/a0)).

For the framework's **nu_RAR target**, let u=sqrt(g_b/a0),
r(u)=u^2/(1-exp(-u)), and I3(u)=integral_0^u t^3/(1-exp(-t)) dt. Then

\[
X(u)={u^4(f+e^{-u})^2\over\eta^2q^2(1-e^{-u})^2},\qquad
J(X(u))={r(u)^2\over\eta}-{4I_3(u)\over\eta q}-X(u).
\]

Again J'=eta q/(f+e^-u)-1. The derivative of the definite integral is
checked symbolically; its primitive is independently tested by quadrature
and finite differences. It is a local free function of X, not a nonlocal
spacetime integral. These are two alternative actions, not one action
claimed to reproduce two different laws.

The previous minimum-slope theorem guarantees X is strictly increasing
for each chosen branch at every positive parameter value; J is therefore
single-valued. Both functions obey J'(infinity)=3 and

\[
\boxed{J'(0)=\eta-1={c_{14}-K_B\over2-c_{14}}<0.}
\]

This last result, forced by deep MOND, is the next gate. It is independent
of J_N and is not repaired by increasing the scalar's Newtonian share.
Specifically J'(X)=eta-1+[eta^2/q]sqrt(X)+O(X), so J is C1 but not C2
at X=0. The composite field action nevertheless has a quadratic expansion:
J(W)=j0 W+O(W^(3/2)), where W is quadratic in perturbations. We claim
regularity at X>0 and this quadratic endpoint, not a uniform nonlinear
strong-coupling bound.

## 3. Actual time-dependent quadratic action

`zero_field_source_audit.py` rebuilds f34's scalar sector from its source AST,
with w_i=Q0=0 inserted before expansion. It excises all cache reads/writes.
An independent ADM construction is compared exactly with that source result.
No reported determinant, kinetic rank or mode count is inserted as an answer.

Use clock-unitary lapse n, shift N_i=partial_i T_s, and spatial metric
gamma_ij=(1-2P) delta_ij. In the source's Newton-gauge notation the
invertible change of variables is Psi=n+dot(T_s). The lapse and scalar
shift block is algebraic, with computed determinant -4 c14 c2 k^6.
It is eliminated only for k!=0 and c14,c2 nonzero. The spatial E=0 gauge
does not discard the retained shift equation.

After elimination the kernel on (P,chi), apart from an overall positive
factor, is

\[
R=\begin{pmatrix}
a\omega^2-bk^2&dk^2\\
dk^2&K\omega^2-e k^2-Ah\xi^2 k^4
\end{pmatrix},\quad
a=2(3+2/c_2),\ b=2B/c_{14},\ d=2A/c_{14},\ e=2A^2/(Bc_{14}).
\]

Here h=J'(0) for the inside action; h=1 for the outside action. The computed
identity be=d^2 yields

\[
\det R=aK\omega^4-
\{a[e k^2+Ah\xi^2 k^4]+bKk^2\}\omega^2+bAh\xi^2 k^6.
\]

For h<0 the product of the two omega^2 roots is negative, since aK>0.
Their discriminant is positive (the constant term is negative). Exactly
one root is negative: an exponentially growing physical scalar mode in
this reduced sector, not a negative-norm kinetic ghost. This proof holds
for every nonzero k under the stated assumptions, not just the sample.

For h=1 the kinetic matrix diag(a,K) is positive definite. The spatial
matrix has leading minor b k^2>0 and determinant bA xi^2 k^6>0, so it too
is positive definite. Both generalized eigenvalues omega^2 are therefore
positive for every k>0. This is only a quadratic zero-field result.

At K_B=.2,c14=1e-5,c2=.01,K=10,k=xi=1, the source gives:

| Operator | omega^2 roots |
|---|---|
| Inside J | -0.00053116404219, 33385.36128155 |
| Outside J | +0.00531184888425, 33385.55343773 |

The computed kinetic matrix is diag(406,10), rank 2. This counts the two
scalar modes of this reduced quadratic sector, NOT the gravitational DOFs
of the full nonlinear theory. The homogeneous k=0 problem is unanalysed
here; dividing out powers of k cannot certify it.

## 4. What the new binary result can and cannot contribute

Commit `90dab18b8` adds g03f. Its proxy data comparison does not reject
f approximately .290324 at the tested .03-.05 pc ranges. This is not a
detection, and not a completed test of either action above. In particular:

- The asserted negligible-MOND cut uses mu_exp. For nu_RAR at g_b/a0=8,
  nu-1 is about 6.28%, not 0.03%; the proxy cannot be transferred unchanged.
- In a constant-j regime the inside action has screening range
  lambda=xi sqrt(j/(1+j-eta)); the outside action instead has
  lambda=xi/sqrt(1+j-eta). g03f sets lambda=xi. At j=3 these factors are
  about .984 and .568. Changing operator placement requires a new comparison.
- Upper limits at the fit-grid endpoint 1.5 are censored, not finite
  measured bounds. Its subsample systematics check is hard-coded True.
- The proxy uses projected separations and a velocity rescaling, not orbit
  integration in the same action. The numerical fit is not a full likelihood.

These caveats justify testing the escape; they do not certify it empirically.
The f~.29 reconstruction uses G_infinity, whereas the screened local limit
uses G0. A single universal measured Newton constant is still unmatched.

## 5. Remaining requirements, without transferring passes

The outside action's static equations include

\[
\Delta\Phi_0=4\pi G_0\rho,\qquad
\nabla\cdot[F(|\nabla\psi|)\nabla\psi]
-{\xi^2\over\eta}\Delta^2\psi=4\pi G_0\rho,\qquad
\Phi=\Phi_0+\psi.
\]

This is not the already-tested g03d equation. Even at xi=0, agreement with
the target algebraic law in spherical symmetry is not equivalence to the
full nonspherical AQUAL PDE. The independent static spatial metric
variation gives no slip with the stated harmonic boundary conditions, but
no full PPN coefficient set is awarded from that alone.

The positive outside-J operator retains a branch with omega proportional
to k^2 at sufficiently large k: positivity is not finite-speed causality.
The clock and scalar propagation, cutoff and strong-coupling scales require
a separate physical analysis. No front-speed claim is inferred from a
group-velocity number here. Full Dirac closure, k=0, charged FLRW
perturbations and finite-gradient stability remain uncomputed for this
explicit reconstructed function.

**Disposition:** original inside-J candidate DEAD in the specified
zero-field branch. The outside-J action passes that narrower stability gate
but has NOT achieved the original full target: at this normalization its
large-scale Newtonian coupling is 199999/154999 times its local coupling,
so its exact G_infinity-normalized law is not the requested universal-G
law. That mismatch is already established, not an unperformed test. The
broader construction programme remains OPEN. Further work must supply an
action-level repair of the physical Newton normalization and the
nonspherical metric equation before reusing any solar/PPN result.

## 6. Reproduction and changed files

New files in this directory: `escape_audit.py`, `test_escape_audit.py`,
`zero_field_source_audit.py`, `escape_results.json`,
`zero_field_source_results.json`, `escape_manifest.json`, `ESCAPE_REPORT.md`.
No prior source modified; no commit/push performed.

Commands from the repository root:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/zero_field_source_audit.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/zero_field_source_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/zero_field_source_audit.py --strict-inside
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/escape_audit.py
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/escape_audit.py --strict-inside
python3 -B qwen_claude_field_theory/closure_2026/g03c_zero_field_limit_outside_J.py
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_clock_constraint_2026 -p 'test_*.py' -v
git diff --check
```

The completed combined suite has 17 tests. Audit producers exit 0 on internal
consistency; the strict inside-J tests exit 2 on the mathematical failure.
The initial construction test exited 1 before implementation (six dependent
tests skipped); the completed construction/source suite passes without skips.
The source output records its f34 hash and all excluded AST operations.
The manifest records input/output hashes, environment and computational scope.
The existing g03c test exits 0 (eight checks), and the C-H constraint suite
exits 0 (nine tests). Neither is an extra certification of this action.
The default Python 3.9 environment lacks Astropy (import probe exit 1);
no dependency was installed. The existing binary test was reproduced with
the available Astropy-enabled interpreter:

```sh
/opt/homebrew/Caskroom/miniconda/base/bin/python3 -B qwen_claude_field_theory/closure_2026/g03f_wb_fifth_force_bound.py
```

Runtime: Python 3.13.9, NumPy 1.26.4, Astropy 7.2.0. The catalogue hash reported
by the read-only data audit is
`6d67d12bf15f6c579e4072aecbb995e8ce13f057ba1dc83115e7046d9c13bacf`.
The catalogue is external/untracked; its historical provenance was not
reauthenticated against its download host. The mathematical construction
does not require this catalogue.
Mathbox self-review is limited to these new derivations and their scope;
no global novelty, observational detection or completed-theory claim is made.
