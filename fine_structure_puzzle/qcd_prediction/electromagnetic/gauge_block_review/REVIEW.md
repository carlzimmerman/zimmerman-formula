# Static spherical gauge block: independent boundary and determinant review

**Primary verdict: correct only after a stated restriction.** The static spherical phase/radial-gauge Hessian admits a scalar/ghost spectral reduction with **relative mixed vector data**, framed Dirichlet ghosts, smooth-origin domains and a physical scalar **Robin** condition. All-vector Dirichlet data do not admit that pairing with framed Dirichlet ghosts. The resulting auxiliary determinant ratio can be calculated exactly and has no residual inverse-radius powers, but this is neither full vector/ghost cancellation nor the physical finite-ball monopole measure.

The raw derivation in INDEPENDENT_DERIVATION.md was saved before reading the vacuum agent's new phase block, which was not read for this review. The coordinator subsequently supplied candidate Robin solutions and an auxiliary ratio; the identities below were then checked independently by hand. A separate read-only child derived the boundary and operator relations from the stated ansatz without reading that new phase block.

## 1. Actual phase sector and operator complex

Use the frozen fixed-small-circle static BPS conventions
\[
K={mr\over\sinh(mr)},\quad H=m\coth(mr)-1/r,\quad
K'=-KH,\quad H'=(1-K^2)/r^2.
\]
In the spherical ansatz with complex \(w=K+iv\), radial connection \(b\), and radial adjoint Higgs, the quadratic energy is
\[
E_2=\int dr\left[(v'-Kb)^2+2K'bv+
\left(H^2+{K^2-1\over r^2}\right)v^2\right].
\]
The mixed \(2K'bv\) term is essential. Residual gauge variations are
\((v,b)=(K\lambda,\lambda')\).
The norm is \(\int(2v^2+r^2b^2)dr\), and background gauge is
\[
G=b'+2b/r-2Kv/r^2.
\]

In canonical variables \(Y=(u,w)^T=(\sqrt2v,rb)^T\), \(s=r\lambda\), \(a=\sqrt2K/r\), define
\[
\mathcal R=\binom{a}{\partial_r-1/r},\quad
\mathcal R^\dagger=(a,-\partial_r-1/r),\quad
\mathcal T=(\partial_r+H,-a).
\]
Then
\[
\mathcal T\mathcal R=0,\quad rG=-\mathcal R^\dagger Y,\quad
\mathcal L_{\rm gh}=\mathcal R^\dagger\mathcal R
=-\partial_r^2+2K^2/r^2,
\]
\[
\mathcal H_{\rm phase}
=\mathcal T^\dagger\mathcal T+\mathcal R\mathcal R^\dagger,
\qquad
\mathcal P=\mathcal T\mathcal T^\dagger
=-\partial_r^2+H^2+(1+K^2)/r^2.
\]
Expanding the matrix gives the raw derivation's explicit potential. In particular \(\mathcal P\) is not the ghost operator.

The canonical phase potential has origin eigenvalues \(0/r^2\) and \(6/r^2\), giving the smooth modes \(r(\sqrt2,1)^T\) and \(r^3(1,-\sqrt2)^T\). It does **not** have the two \(r^2\) origin modes of the frozen real-amplitude/Higgs block. The scalar ghost and \(\mathcal P\) have regular \(r^2\) behavior. Smooth/Friedrichs data exclude point-defect extensions.

The gauge-invariant static combination \(b-(v/K)'\) has algebraic energy \(K^2[b-(v/K)']^2\), up to a surface term. A second-order scalar partner in the gauge-fixed calculation does not establish an extra propagating static degree of freedom.

## 2. All-vector Dirichlet fails the gauge-domain test

Framing means \(\lambda(R)=0\). All-vector Dirichlet would also require \(v(R)=b(R)=0\). But a framed transformation has \(v(R)=K(R)\lambda(R)=0\) and \(b(R)=\lambda'(R)\), which is generally nonzero.

For an explicit smooth counterexample,
\[
\lambda(r)=r(1-r^2/R^2),\qquad
\lambda(R)=0,\qquad \lambda'(R)=-2.
\]
The transformation is smooth at the origin and framed at the wall, but violates radial-vector Dirichlet. Imposing both \(\lambda(R)=\lambda'(R)=0\) overdetermines the second-order ghost eigenproblem. Thus formal bulk identities cannot cancel that vector Dirichlet determinant against the quoted Dirichlet ghost determinant.

## 3. Relative data give a self-adjoint spectral pairing

Fix the induced connection and Higgs/holonomy fluctuation at the wall, leaving the normal connection fluctuation free. In this phase block the relative vector conditions are
\[
u(R)=0,\qquad(\mathcal R^\dagger Y)(R)=0,
\]
or \(v(R)=0\), \(b'(R)+2b(R)/R=0\). The scalar ghost has \(s(R)=0\).

The first-order operator
\(\mathcal D Y=(\mathcal TY,\mathcal R^\dagger Y)\)
has wall form \(t^*u-z^*w\). Taking its form domain to have \(u(R)=0\) gives adjoint data \(z(R)=0\). Consequently
\[
\mathcal D^\dagger\mathcal D=\mathcal H_{\rm phase,rel},
\qquad
\mathcal D\mathcal D^\dagger
=\operatorname{diag}(\mathcal P_{\rm Robin},\mathcal L_{\rm gh,D}),
\]
\[
t'(R)-H(R)t(R)=0,\qquad s(R)=0.
\]
This proves the nonzero eigenfunction pairing with these domains. It is not a pairing to two scalar Dirichlet problems. For finite \(R\), \(K>0\); the ghost form is positive, and
\[
\langle t,\mathcal P_{\rm Robin}t\rangle
=\|\mathcal T^\dagger t\|^2
\]
has no zero eigenvector because \(\mathcal T^\dagger t=(-t'+Ht,-at)\) would force \(t=0\). The two scalar spectra therefore give the vector spectrum without an exact zero subtraction.

With the conventional complex Faddeev–Popov ghost and two real vector fields, the formal contribution is
\[
Z_{\rm phase+gh}\ \propto\
\left({\det\mathcal L_{\rm gh,D}\over
\det\mathcal P_{\rm Robin}}\right)^{1/2}.
\]
Gauge-volume and other-field bookkeeping must still be matched; the full ghost determinant does not literally cancel a single longitudinal real-boson square root.

## 4. BRST statement and alternative wall conditions

The relative essential conditions have a concrete off-shell auxiliary-field formulation:
\[
a_t=\phi=c=\bar c=B=0\quad\hbox{at the wall},\qquad
s a_\mu=D_\mu c,\quad s\bar c=B,\quad sB=0,
\]
with the usual nonlinear ghost rule when required. At linear order this kinematic set is BRST closed. The induced boundary connection and Higgs are fixed, and framing makes their variations vanish. Integrating out \(B\) yields the natural gauge-fixing condition \(G=0\).

That eliminated formulation has a restricted invariance statement:
\[
sG=-\mathcal M_{\rm gh}c.
\]
An arbitrary smooth Dirichlet ghost need not have \(\mathcal M_{\rm gh}c=0\) at the wall. Ghost eigenfunctions do, since \(\mathcal M_{\rm gh}c=\lambda_{\rm eig}c\). Thus the determinant problem is BRST invariant on its compatible eigenfunction/spectral complex; one must not replace that fact with an unrestricted off-shell claim about the eliminated \(G=0\) condition.

This distinction is explicitly made in [Moss, arXiv:1301.0717v2, section II, equations (28)–(31)](https://arxiv.org/abs/1301.0717v2). The source supplies the auxiliary-field/eigenvalue distinction, not a theorem about the full nonlinear monopole wall theory. The static radial problem above has an ordinary self-adjoint mixed Laplace-type principal part. It does not address all angular/Fourier boundary symbols.

Ordinary geometric absolute data instead fix \(b(R)=0\) and \((v'-Kb)(R)=0\), hence \(v'(R)=0\). Neumann ghosts \(\lambda'(R)=0\) fail to preserve the latter when \(K'(R)\lambda(R)\ne0\). This is the background-curvature obstruction \(d_A D_A\epsilon=[F_A,\epsilon]\). It is absent in vacuum Maxwell theory but cannot be discarded for the finite-wall monopole.

The profile-adapted alternative
\[
b(R)=0,\qquad v'(R)-[K'(R)/K(R)]v(R)=0
\]
does pair with a Neumann ghost and would give a Dirichlet physical scalar partner. It changes the framing and is not ordinary geometric absolute data. Moreover
\[
E_2=\int|\mathcal TY|^2/2+[K'v^2/K]_0^R.
\]
Since \(v(R)\) is free in that alternative, a corresponding boundary action/gauge-fixing completion must be specified to remove or vary this surface term. For example the factorized quadratic form requires subtracting the displayed \(K'v^2/K\) wall term. A self-adjoint Robin condition alone does not authorize that physical boundary action. The relative \(v(R)=0\) problem avoids this additional term.

## 5. Exact auxiliary Robin determinant check

Set \(m=1\) and \(x=mR\) for the dimensionless equations; write \(h=\coth x-1/x\), \(K=x/\sinh x\). Choose the explicitly auxiliary comparison
\[
\mathcal P_{\rm ref}=-\partial_x^2+1+2/x^2
\]
with the **same** wall Robin functional \(\mathcal B=\partial_x-h(x)\), and the same normalized regular origin data. Direct use of the BPS identities gives
\[
\mathcal P K={2K\over x^2},\qquad
\mathcal P(1/K)={2K\over x^2}.
\]
Therefore the normalized regular zero-energy solution and its Robin functional are
\[
t_A=3(1/K-K)=3(\sinh x/x-x/\sinh x),\quad
t_A/x^2\to1,\quad \mathcal B t_A=6Kh.
\]
The reference solution is
\[
t_{\rm ref}=3(\cosh x-\sinh x/x),\qquad
\mathcal B t_{\rm ref}=3(\cosh x/x-\operatorname{csch}x).
\]
It is positive at the wall. The reference operator is positive with this Robin condition: \(0<h(x)<1\), and completing the square with the fixed value \(h(x)\) bounds its form below by the positive bulk term \((1-h(x)^2+2/r^2)t^2\).

For regular-cutoff scalar Sturm–Liouville problems with identical self-adjoint boundary matrices and leading derivative coefficient, the determinant ratio is the zero-energy boundary-functional ratio; see [Kirsten–McKane, arXiv:math-ph/0403050v1, sections 2–4](https://arxiv.org/abs/math-ph/0403050v1). As in the frozen ghost derivation, take a common origin cutoff first: the shared regular \(r^2\)/singular \(r^{-1}\) pair gives the common normalization factor \(1/(3\epsilon)\), which cancels before the cutoff is removed. Thus
\[
D_A={6Kh\over3(\cosh x/x-\operatorname{csch}x)}.
\]
Combining it with the frozen auxiliary ghost ratio
\(D_g=3(x\coth x-1)/x^2\) gives the exact identity
\[
\boxed{\quad {D_g\over D_A}
={3(\sinh x\cosh x-x)\over2x^3}.\quad}
\]
Consequently this auxiliary static phase-plus-ghost contribution is
\[
\log Z_{\rm phase+gh}^{\rm rel}
={1\over2}\log{D_g\over D_A}
=x-\frac32\log x+\frac12\log(3/8)
+\frac12\log[1-4xe^{-2x}-e^{-4x}].
\]
All algebraic inverse-radius terms cancel in **this** weighted comparison. The remaining linear/exponential and logarithmic normalizations cannot be discarded without a specified reference/subtraction contract. The two scalar reference operators have not been shown to arise from one physical vacuum gauge complex with the same wall data; their cancellation is not the physical full determinant.

## 6. A near-zero mode makes the wall limit nonuniform

There is no exact finite-wall zero mode in this relative problem, but the Robin functional of \(t_A\) is exponentially small. Its relation to the old global rotation is exact. Let \(s_0=xh\); then
\[
\mathcal L_{\rm gh}s_0=0,\qquad
\mathcal T^\dagger t_A=-3\sqrt2\,\mathcal R s_0.
\]
The scalar gauge parameter \(s_0\) is not framed, since \(s_0(x)\ne0\). The corresponding vector is the ordinary normalizable infinite-space rotation variation. Its tangential finite-wall value is small but nonzero, so it is lifted rather than an exact finite-wall collective coordinate.

The physical scalar form permits \(t_A\) as a Rayleigh trial function, yielding
\[
0<\lambda_{\min}(\mathcal P_{\rm Robin})
\le {t_A(x)\,[6K(x)h(x)]\over\int_0^x t_A(t)^2dt}
=16x^2e^{-2x}[1+O(x^{-1})].
\]
Here the last expression is the trial bound's asymptotic value, not a claimed independently determined eigenvalue asymptotic. It proves a nonuniform vanishing gap. Removing this state as though it were an exact zero at every finite wall, or adding the infinite-space four-coordinate Jacobian to a determinant which retains its lifted version, changes the measure. A collective-coordinate/near-zero prescription must be specified and matched.

## 7. What is and is not settled

Passed: direct phase ansatz/action, canonical Hessian, gauge complex, smooth-origin data, explicit failure of all-vector Dirichlet pairing, relative scalar/ghost boundary reduction, auxiliary Robin zero solutions and determinant identity, and the near-zero Rayleigh bound. These are hand derivations, independently checked in the indicated ways. No numerical or symbolic experiment was executed in this review; there is no new computation manifest.

Conditional: promoting the scalar determinant ratios to a physical monopole measure requires a single boundary action, induced connection/holonomy data, framed gauge group and antighost/auxiliary-field prescription, reference gauge complex and UV subtraction, and treatment of the lifted rotation mode. The full angular/Fourier sum and any matter determinants remain outside this static block.

The exact missing physical boundary prescription is therefore not an arbitrary scalar Robin constant: it is the complete, common gauge boundary problem and collective-coordinate measure. Choosing relative data supplies one coherent one-loop candidate. It does not establish that this candidate is the boundary prescription intended by the earlier truncated zero-mode calculation, nor does the auxiliary cancellation establish a QCD cosmological coefficient.
