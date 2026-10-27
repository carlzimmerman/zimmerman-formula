# QCD-V determinant follow-up: an actual BPS ghost block

FSP-003 / QCD-V. All earlier vacuum_geometry artifacts are preserved. This follow-up computes one nonzero-mode determinant slice and its finite-radius dependence; it does not assign a value to the remaining full determinant.

**Result.** A framed Dirichlet adjoint ghost channel has the exact relative determinant

\[
\boxed{D_0(x)=\frac{3[x\coth x-1]}{x^2},\qquad x=m_WR.}\tag{D1}
\]

After its explicit \(\log(3/x)\) infrared normalization, its logarithm contains \(-1/(m_WR)\). The nonzero Fourier-frequency channels have the opposite sign \(+1/(|\omega_n|R)\). This is a concrete counterexample to ignoring nonzero-mode finite-size terms merely because a determinant uses spectral phases. It is an admissible diagnostic channel with an explicitly auxiliary reference, not a complete gauge partition function. Its boundary domain excludes the global rotation parameter used in the earlier collective-coordinate Jacobian.

## 1. Action, background and a closed radial channel

Take the static BPS sector of Euclidean \(SU(2)\) Yang–Mills on \(B_R^3\times S_L^1\), with \(L\) fixed and \(\Phi=A_4\). Equivalently its static action is

\[
S_{\rm static}=\frac{L}{2g^2}\int_{B_R}\!d^3r\,
[B_i^aB_i^a+(D_i\Phi)^a(D_i\Phi)^a].
\]

Fix the classical boundary holonomy data and use the exact BPS hedgehog

\[
\Phi^a=n^aH(r),\quad H=m[\coth(mr)-(mr)^{-1}],\quad
A_i^a=\epsilon_{aij}\frac{n_j}{r}[1-K(r)],\quad
K=\frac{mr}{\sinh(mr)},\quad m=m_W.
\]

Conventions are \(D_i c^a=\partial_i c^a+\epsilon^{abc}A_i^b c^c\); changing signs consistently gives the same radial operator. The BPS action specifies the saddle used here. A center-stabilizing holonomy potential in a full deformed theory can change its profile and the vector Hessian; that potential is not silently omitted from a claimed full-theory result.

In background gauge the complex Faddeev–Popov ghosts have

\[
\mathcal M_{\rm gh}=-D_iD_i-(\partial_4+\operatorname{ad}\Phi)^2.
\]

The adjoint channel

\[
c^a(\tau,r,\Omega)=e^{i\omega_n\tau}n^a f(r),\quad
\omega_n=2\pi n/L
\]

is invariant under this operator. It has grand spin zero under simultaneous spatial/isospin rotations. In particular \([\Phi,c]=0\), and

\[
D_i(n^af)=n_in^af'+\frac{Kf}{r}(\delta_{ia}-n_in^a).
\]

Taking its quadratic norm or a second covariant derivative gives

\[
\mathcal M_{\rm gh}(n^af)
=n^a[-f''-2f'/r+2K^2f/r^2+\omega_n^2 f].
\]

The unitary radial change \(u=rf\), up to the common angular/circle normalization, produces the actual block

\[
\boxed{\mathcal L_q=m^2\left[-\frac{d^2}{dx^2}
+\frac2{\sinh^2x}+q^2\right],\quad
q=|\omega_n|/m.}\tag{D2}
\]

Smooth adjoint fields at the origin require \(f=O(r)\), hence \(u=O(r^2)\). The other solution \(u\sim r^{-1}\) is not square-integrable in the reduced measure. This is the unique Friedrichs/limit-point condition. For framed small gauge transformations, require **\(c(R)=0\)**, giving \(u(x)=0\) at the outer endpoint. These conditions specify a positive self-adjoint ghost block with no ghost zero eigenvalue.

## 2. Determinants, including the endpoint issue

Define the comparison operator

\[
\mathcal L^{\rm ref}_q=m^2[-d^2/dx^2+2/x^2+q^2]
\]

with the same origin behavior and outer Dirichlet condition. This reference is explicit and fixes the relative determinant normalization. It is **auxiliary**: an untwisted vacuum with a fixed isospin \(A_4\) does not preserve this monopole grand-spin decomposition. One must not call this single ratio the physical vacuum subtraction for all adjoint fields.

The regular solutions of \(\mathcal L_q u=0\), normalized to \(u/x^2\to1\), are

\[
u_q(x)=\frac{3[q\cosh(qx)-\coth x\sinh(qx)]}{q(q^2-1)},\qquad
u_q^{\rm ref}(x)=\frac3{q^2}\left[\cosh(qx)-\frac{\sinh(qx)}{qx}\right].\tag{D3}
\]

For \(q=0\), \(u_0=3(x\coth x-1)\), \(u_0^{\rm ref}=x^2\). At \(q=1\), the removable limit is \(u_1=\tfrac32(\cosh x-x/\sinh x)\). Each expression has been substituted into its differential equation symbolically.

The ordinary Gel'fand–Yaglom formula applies first on \([\epsilon,x]\), where both potentials are continuous, with identical initial Dirichlet data and unit derivative. [Kirsten–McKane, hep-th/0507005v1, Section 3, equations (9)–(14)](https://arxiv.org/abs/hep-th/0507005v1) establishes that regular-interval formula. It must not be applied directly to the singular endpoint without an extra step.

Here that step is elementary. Normalize regular/singular bases as \(a(y)\sim y^2\), \(b(y)\sim y^{-1}\), so their Wronskian tends to \(-3\). The unit-derivative solution at \(\epsilon\) is

\[
y_\epsilon(y)=\frac{a(\epsilon)b(y)-b(\epsilon)a(y)}
{a(\epsilon)b'(\epsilon)-a'(\epsilon)b(\epsilon)}
=\frac{a(y)}{3\epsilon}+o(\epsilon^{-1}).
\]

The common divergent factor cancels in the ratio. Thus the cutoff-limit relative determinant, equivalently the convergent relative eigenvalue product, is

\[
\boxed{D_q(x)=\frac{u_q(x)}{u_q^{\rm ref}(x)}
=\frac{q}{q^2-1}\frac{q\cosh(qx)-\coth x\sinh(qx)}
{\cosh(qx)-\sinh(qx)/(qx)}.}\tag{D4}
\]

For \(q=1\),
\(D_1=(\cosh x-x/\sinh x)/[2(\cosh x-\sinh x/x)]\).
Equation (D1) is its \(q=0\) limit. No zero eigenvalue is removed from these Dirichlet ghost determinants.

## 3. Actual finite-size terms and their limits

At zero frequency,

\[
\log D_0(x)=\log(3/x)-\frac1x-\frac1{2x^2}
+O(x^{-3})+O(e^{-2x}).\tag{D5}
\]

For each fixed \(q>0\),

\[
\log D_q(x)=\log\frac q{q+1}+\frac1{qx}
+\frac1{2q^2x^2}+O(x^{-3})
+O\!\left({\rm poly}(x)e^{-2\min(1,q)x}\right).\tag{D6}
\]

The \(q=1\) limit follows from its separate expression. These asymptotics are nonuniform as \(q\to0\); taking that limit in (D6) is invalid. A complex ghost contributes \(+\log\det\mathcal M_{\rm gh}\) to \(\log Z\), so the static slice has a negative linear coefficient, whereas each positive-frequency slice has a positive one relative to the stated reference.

This does not settle cancellation of the earlier \(-1/(2mR)\) collective-coordinate term. The latter uses modes not obeying the present outer boundary condition. Nor can one sum (D6) as a full result: at center-symmetric \(SU(2)\) holonomy \(m=\pi/L\), \(q_n=2|n|\), and summing this isolated channel's \(1/(q_nx)\) over nonzero Fourier modes is harmonic. The large-\(q\) expansion at fixed \(x\) also gives \(\log D_q\sim(1/x-\coth x)/q\). UV subtraction and the remaining angular/vector channels are required before interpreting a full coefficient. No finite cutoff or arbitrary subtraction constant is chosen here to make a desired cancellation.

## 4. Factorization changes the boundary domain

The exact first-order operator

\[
T=d/dx-\coth x,\qquad T^\dagger=-d/dx-\coth x
\]

satisfies the formal identities

\[
T^\dagger T=-d^2/dx^2+1,\qquad
TT^\dagger=-d^2/dx^2+1+2\operatorname{csch}^2x.
\tag{D7}
\]

Consequently a free solution \(y\) is mapped by \(T\) to the BPS radial solution. But \(v=Ty\) obeys the BPS Dirichlet condition \(v(x)=0\) precisely when

\[
y'(x)-\coth x\,y(x)=0,\tag{D8}
\]

which is Robin, not Dirichlet. At the origin \(y(0)=0\) maps to the regular \(v=O(x^2)\). The free Dirichlet/Robin operator has one additional eigenfunction \(y=\sinh x\) with eigenvalue \(-1\), killed by \(T\). Its removal is essential. For all other eigenvalues the inverse is \(y=T^\dagger v/(\lambda+1)\), proving the domain pairing rather than guessing it.

The positive BPS Dirichlet eigenvalues satisfy

\[
\tan z=\frac{z\tanh x}{x},\qquad z\in(n\pi,n\pi+\pi/2),\quad n\ge1,\tag{D9}
\]

whereas the comparison \(l=1\) eigenvalues satisfy \(\tan z=z\). Their inequivalence is measured by (D4). Thus a bulk self-duality/factorization identity cannot pair two arbitrarily chosen finite-ball Dirichlet spectra.

For the full monopole Hessian, [Dorey et al., hep-th/9703228v2, Section 3.1, equations (13), (21)–(26)](https://arxiv.org/abs/hep-th/9703228v2) relates vector, scalar and ghost operators to the two chiral Dirac squares. The paper explicitly retains a continuum spectral-density mismatch, obtaining a nontrivial determinant ratio even in its supersymmetric theory. Its supersymmetric field content and infinite-volume prescription are different from the present target; the factorization supplies neither finite-ball boundary pairing nor the desired QCD coefficient.

## 5. The former rotation mode is outside this ghost domain

The regular static gauge parameter \(c^a=\Phi^a/m=n^a H/m\) solves the ghost differential equation, but

\[
c^a(R)=n^a[\coth x-1/x]\ne0.
\]

It is the unbroken global rotation parameter, not a small framed Dirichlet ghost. Removing it as a zero eigenvalue from (D1) would be incorrect. The corresponding vector variation \(D_i\Phi\) also has finite-wall tangential components \(HK/r\); they are exponentially small at large radius but not zero. Translation variations change the fixed wall data as well. Therefore a boundary problem that fixes the boundary connection does not have the same exact four collective zero modes as the infinite-space saddle. Their lifting, admissible gauge group and induced vector boundary conditions must be handled before adding a finite-ball Jacobian and a finite-ball determinant.

This is the demonstrated domain obstruction: the previously reproduced normalization term and the present determinant belong to distinguishable prescriptions. Their arithmetic sum is not an answer to the physical finite-size question.

## 6. Independent spectral check and provenance

`check_radial.py` checks (D3), its origin normalization and (D7)–(D9), and computes the first 256 eigenvalues from (D9) and its reference using bracketing, independently of the zero-energy initial-value solutions. It compares the finite products

\[
P_N=\prod_{n=1}^N\frac{z_n^2+q^2x^2}{(z_n^{\rm ref})^2+q^2x^2}
\]

to (D4), for \(x=2,5,10\) and \(q=0,1,2\). The first two explicit large-\(n\) tail terms improve convergence; after that correction, the largest observed log discrepancy is \(5.50\times10^{-10}\), below the declared \(2\times10^{-8}\) tolerance. Tail correction is numerical evidence, not a claimed interval certificate.

There is also a separate conservative analytic bracket. The potential difference satisfies \(-2/3\le2\operatorname{csch}^2y-2/y^2\le0\). To see its lower bound, \(1/y^2-\operatorname{csch}^2y\) decreases from \(1/3\): its derivative has the required sign because \(\sinh^3 y\ge y^3\cosh y\), obtained by differentiating \(3\log(\sinh y/y)-\log\cosh y\). Monotonicity of that last expression follows from \(y(3+2\sinh^2y)-3\sinh y\cosh y\ge0\), whose derivative is \(4\sinh y(y\cosh y-\sinh y)\ge0\).

Min–max comparison then bounds the omitted logarithmic product by

\[
-B_N\le\log D_q-\log P_N\le0,\quad
B_N=\frac{\gamma}{N[1-\gamma/(N+1)^2]},\quad
\gamma=\frac{2x^2}{3\pi^2},\tag{D10}
\]

when \((N+1)^2>\gamma\). The code checks these brackets too. This bound follows from \(\lambda_n^{\rm ref}\ge(n\pi/x)^2\), \(\log(1-z)\ge-z/(1-z)\), and \(\sum_{n>N}n^{-2}\le1/N\), independently of the tail asymptotics. Computed roots are high-precision approximations, so the script's bracket comparison itself is numerical; (D10) is the hand analytic statement.

Contract: `COMPUTATION_CONTRACT.json`. Current run: `runs/radial-001/manifest.json`, v2 schema, status `completed`, current input hash verified. Nine cases, 60 decimal digits, 110 bisections per root, no random sampling. No earlier artifacts changed. `SOURCES.json` and `INPUTS.json` pin source versions and hashes. The coordinator independently derived the static radial block and (D1) before seeing this implementation; the spectral-product implementation is an additional independent check, not an audit of the complete vector Hessian.

Validate from the repository root:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_prediction/vacuum_geometry/determinant_followup/runs/radial-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

For an exact new execution, use the runner argv in that manifest with a fresh output directory and matching `--result` argument.

**Further calculation completed:** VECTOR_BLOCK.md now derives a real coupled spherical vector/A4 Hessian and evaluates its full relative matrix determinant as an explicit one-dimensional integral, independently checked against the original matrix ODE. Its logarithmic residual is \(+2/(m_WR)\), giving \(-1/(m_WR)\) in the bosonic \(\log Z\) contribution. That addendum records the exact slice and remaining domain/reference limitations. The next required block is the spherical phase/radial-gauge sector with vector boundary data compatible with the same ghost framing, followed by the complete angular/Fourier sum and physical-vacuum matching. No physical \(c_H\), \(R(\alpha)\), or alpha root is obtained here.
