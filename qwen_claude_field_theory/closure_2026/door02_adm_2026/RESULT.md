# Door 2: exact local ADM degeneracy and a homogeneous compatibility gate

The seven-velocity Hessian of the section 2 action is generically nonsingular.
There is no hidden kinetic mixing that can remove its scalar through a
determinant cancellation. The only exact rank-loss conditions are the separate
vanishing of the tensor, trace, or scalar blocks described below. This is a
local kinetic statement, **not a complete constraint count or a health proof**.

The source is `fable_independent_2026/THE_COMPLETE_THEORY_2026-09-08.md`, section 2,
at requested base `3e52670d048c6fb582d7eb7475d3100531e6bccc`. Its SHA-256 is
`4777fefb0847b6707033081715312c1be5f419d9a493da4ad17f7f45d4a84ade`.
The working repository advanced to `5d9bde097bdedca25ab21dff5de7b2cf54feac1b`
during this task, but the source hash agrees exactly with the requested base.
No commits or existing-file changes were made by this subtask.

## 1. Geometric reduction on arbitrary spatial data

Use signature \((-+++)\), a regular timelike clock, unitary gauge \(\tau=t\),
positive lapse \(N\), positive spatial metric \(h_{ij}\), and

\[
 K_{ij}=\frac{\dot h_{ij}-\mathcal L_{\vec N}h_{ij}}{2N},\qquad
 a_i=D_i\log N,\qquad Q=\frac{\dot\phi-N^iD_i\phi}{N}.
\]

The Einstein–Hilbert action is understood with its usual boundary term removed
before forming the first-order ADM Hessian. The coefficients in the printed
action are used literally: its \(c_i\) terms do not share an additional overall
Einstein–Hilbert prefactor. Set

\[
 F=\frac1{16\pi G},\quad b=2-K_B,\quad
 A=F-c_{13},\quad B=F+c_2,\quad D=A-3B=-2F-c_{13}-3c_2.
\]

In unitary gauge, \(V_i=D_i\phi\), \(V_0=N^iD_i\phi\), and
\(q^{00}=q^{0i}=0,\ q^{ij}=h^{ij}\). The identities

\[
 \Gamma^0_{ij}=K_{ij}/N,\qquad
 \Gamma^k_{ij}={}^{(3)}\Gamma^k_{ij}-N^kK_{ij}/N
\]

give \(\nabla_iV_j=D_iD_j\phi\): the two extrinsic-curvature contributions
cancel. Therefore

\[
 X=Y+\xi^2\lVert\nabla_\perp V\rVert^2
 =D_i\phi D^i\phi+\xi^2D_iD_j\phi D^iD^j\phi
\]

contains spatial derivatives, but no velocities, for arbitrary spatial
gradients, lapse and shift. The aether decomposition gives

\[
 \frac{\mathcal L}{N\sqrt h}
 =A K_{ij}K^{ij}-B K^2-K(Q)+W,
\]

\[
 W=F({}^{(3)}R-2\Lambda)+c_{14}a_i a^i
    +2b a_iD^i\phi-bJ(X).
\]

Smoothness of \(K\) at the evaluation point is assumed; for statements about a
generic branch, the same regularity and constant rank must hold on an open
region. An isolated zero of \(K''\) is not a regular removal of a field.

## 2. Full velocity Hessian and exact degeneracy loci

At any point choose an orthonormal basis of symmetric tensors with
\(B_0=h/\sqrt3\) and five traceless \(B_a\). This is an invertible linear
coordinate change for any positive spatial metric and makes no restriction on
the spatial data. Expand \(\dot h-\mathcal L_{\vec N}h=v_0B_0+v_aB_a\), and set
\(w=\dot\phi-N^iD_i\phi\). Direct differentiation gives

\[
 H_{(v_0,v_a,w)}=\frac{\sqrt h}{N}
 \operatorname{diag}\left(\frac D2,
       \frac A2\mathbf1_5,-K''(Q)\right).
\]

The full eleven-velocity matrix adds four zero rows and columns for
\(\dot N,\dot N^i\). Its rank is

\[
 r=5\mathbf1_{A\ne0}+\mathbf1_{D\ne0}+\mathbf1_{K''\ne0},\qquad
 \det\left(\frac N{\sqrt h}H_7\right)
 =-\frac{A^5D K''}{64}.
\]

Thus the exact generic rank-loss alternatives are:

| Condition | Lost Hessian directions | Immediate implication only |
|---|---:|---|
| \(c_{13}=F\) | five shear directions | Ordinary tensor kinetic term is absent |
| \(c_2=-(2F+c_{13})/3\) | one trace direction | Trace primary constraint |
| \(K''\equiv0\), hence \(K(Q)=\ell Q+K_0\) locally | one scalar direction | Scalar primary constraint |

Intersections add these rank losses. If \(c_{13}=0\), \(F>0\), \(c_2>0\),
and \(K(Q)=K_2Q^2\) with \(K_2\ne0\), as on the printed parameter branch,
then \(A=F\), \(D=-2F-3c_2\), and \(K''=2K_2\): rank seven. A relation
such as \(c_2|K_2|=b^2\) cannot make this Hessian degenerate. Retaining the
Einstein tensor kinetic coefficient requires \(A\ne0\); its positive sign
requires \(A>0\). The scalar block alone has positive sign if \(K''<0\),
but these signs alone do not establish health after constraints.

The canonical momenta are

\[
 \Pi^{ij}=\sqrt h(AK^{ij}-BK h^{ij}),\quad
 \Pi=h_{ij}\Pi^{ij}=\sqrt h D K,\quad
 p_\phi=-\sqrt h K'(Q).
\]

Hence \(D=0\) gives \(\Pi\approx0\), while affine \(K\) gives
\(C_\phi=p_\phi+\ell\sqrt h\approx0\). If both conditions hold and
\(\ell\ne0\), these primary constraints already have nonzero mutual bracket:

\[
 \{\Pi(x),C_\phi(y)\}=-\frac32\ell\sqrt h(x)\delta(x-y).
\]

Consequently one cannot assume that each null Hessian direction generates its
own independent secondary constraint. This also explains why replacing affine
\(K\) by constant \(K\) silently changes the constraint problem.

## 3. Homogeneous necessary conditions for the trace-degenerate branch

For FLRW, take \(h_{ij}=a(t)^2\gamma_{ij}\), constant sectional curvature
\(\kappa\), homogeneous \(N,\phi\), zero shift, and comoving spatial volume
one. Then \(a_i=V_i=D_iD_j\phi=0\), \(K=3\dot a/(Na)\). Let

\[
 C=2F\Lambda+K_0+bJ(0),\qquad K(Q)=\ell Q+K_0.
\]

Assume \(J(0)\) is finite and this homogeneous restriction is admitted by the
action. The reduced gravity-plus-scalar Lagrangian is

\[
 L=\frac{3D a\dot a^2}{N}+6F\kappa Na-Na^3C-\ell a^3\dot\phi.
\]

For minimally coupled perfect-fluid stress, use
\(\delta S_m/\delta N=-a^3\rho\) and
\(\delta S_m/\delta a=3Na^2p\). On \(D=0\), varying lapse and scale factor
gives

\[
 \rho=\frac{6F\kappa}{a^2}-C,\qquad
 p=C-\frac{2F\kappa}{a^2}+\ell Q,\qquad
 \rho+p=\frac{4F\kappa}{a^2}+\ell Q.
\]

For constant \(K\), \(\ell=0\), and spatially flat FLRW, \(\kappa=0\),
this forces \(\rho+p=0\). Ordinary positive-density dust or radiation alone
cannot satisfy this condition. It is a necessary-condition obstruction for
this doubly degenerate homogeneous branch; it is not a no-go for spatially
curved or inhomogeneous configurations, or for the trace-regular branch.

For affine \(K\) with \(\ell\ne0\), the scalar equation instead supplies

\[
 3\ell a^2\dot a=0.
\]

Thus a nonzero affine coefficient forbids homogeneous expansion in this
ansatz, even though \(\rho+p=\ell Q\) need not vanish when \(\kappa=0\).
The term \(-\ell a^3\dot\phi\) is not a removable boundary term for varying
\(a\): its symplectic two-form has component \(-3\ell a^2\,da\wedge d\phi\).

## 4. The discriminating next constraint

The tensor-preserving path that leaves the metric trace regular is
\(A\ne0, D\ne0, K=K_0\). Its scalar primary is \(p_\phi\approx0\).
Preserving it gives the spatial scalar equation

\[
 D_i\!\left[NJ'(X)D^i\phi\right]
 -\xi^2D_jD_i\!\left[NJ'(X)D^iD^j\phi\right]
 -D_i(Na^i)=0,
\]

for \(b\ne0\). The next useful calculation is the coupled functional
bracket matrix of the lapse and scalar primary/secondary constraints, including
its spatial differential operators and boundary conditions. That can determine
whether the scalar pair removes a local mode or instead produces an
underdetermined/irregular branch. A lapse-independent kinetic determinant does
not establish a first-class Hamiltonian constraint. The trace-degenerate path
also requires preserving \(\Pi\) and satisfying the matter restriction above.

No full Dirac algebra, Ward identity, no-slip relation, MOND law, or global
hyperbolicity result is claimed by this report. The construction remains open.

## 5. Computation, provenance, and self-review

`check_adm.py` constructs the exact Lagrangian and obtains its Hessian by
symbolic differentiation. It computes ranks on all eight exact combinations of
the three rank-loss conditions, verifies the arbitrary-shift cancellation in
the projected connection, differentiates the trace momentum, and obtains the
homogeneous lapse/scale equations. The general rank formula follows directly
from the displayed symbolic diagonal matrix, rather than from the sample ranks.
The geometric ADM reduction is also stated explicitly above; the code is not
an independent spacetime variation engine.

Run command (runner and child both exited 0; child runtime 0.720 seconds):

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/door02_adm_2026/contract.json --input qwen_claude_field_theory/closure_2026/door02_adm_2026/check_adm.py --input fable_independent_2026/THE_COMPLETE_THEORY_2026-09-08.md --output qwen_claude_field_theory/closure_2026/door02_adm_2026/run --result qwen_claude_field_theory/closure_2026/door02_adm_2026/run/result.json --timeout 120 --max-output-bytes 1048576 --max-cpu-seconds 110 --max-threads 1 -- python3 qwen_claude_field_theory/closure_2026/door02_adm_2026/check_adm.py
```

The runner requires a fresh output directory; reproducing the run requires
changing the script's result destination and the matching runner paths, or
working in a separate copy. Do not overwrite the recorded evidence.

Validation command (exit 0, `valid evidence record; mathematical interpretation requires review`):

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/door02_adm_2026/run/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

`run/manifest.json` records actual argv, commit, dirty state, software versions,
input/output hashes, runtime, exit status, and enforced limits. Mathematical
interpretation: implementation and exact symbolic assertion verified in the
stated seven-variable local model, with its uniform geometric reduction given
above. This evidence does not extend to the uncomputed full constraint algebra.

Skills used: computation-audit for the contract, exact checks and bounded
manifest; proofread-math for self-review of this report. Proofreading coverage:
this new report only; no unresolved notation issues or proofreading changes to
mathematical tokens. No external theorem or literature claim was needed.
