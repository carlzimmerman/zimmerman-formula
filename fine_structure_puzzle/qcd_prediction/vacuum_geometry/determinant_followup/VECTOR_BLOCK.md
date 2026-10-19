# Exact coupled static vector/A4 block

This addendum completes an additional determinant calculation after the scalar/ghost result in REPORT.md. It uses the same fixed small circle, exact static BPS saddle and dimensionless radius \(x=m_WR\). It is one real spherical block, with its own explicitly stated auxiliary reference.

## Actual Hessian and domain

The spherical static action, apart from the constant \(4\pi L/g^2\) and a common scale, is

\[
E=\int_0^x dt\left[K'^2+\frac{(K^2-1)^2}{2t^2}
+\frac{t^2h'^2}{2}+K^2h^2\right],
\quad K=t/\sinh t,\quad h=\coth t-1/t.
\]

Consider real variations \(p=\delta K\), \(v=t\delta h/\sqrt2\). The common rescaling \((u,w)=\sqrt2(p,v)\) puts the quadratic action in the conventional \(\tfrac12\int(u'^2+w'^2+\cdots)\) form; the operator is unchanged. With the boundary values of \(K,h\) fixed, \(p(x)=v(x)=0\). At the origin both regular reduced fields behave as \(t^2\); irregular \(t^{-1}\) fields are excluded.

Expanding the actual spherical action and integrating the \(v'v/t\) term by parts gives

\[
\mathcal H=-d^2/dt^2+U(t),\qquad
U=\begin{pmatrix}
h^2+(3K^2-1)/t^2&2\sqrt2Kh/t\\
2\sqrt2Kh/t&2K^2/t^2
\end{pmatrix}.\tag{M1}
\]

This is not a guessed scalar potential. It is the Hessian for the real spherical gauge-amplitude and \(A_4\) fluctuations. The phase/radial-gauge sector and all other angular/Fourier channels are omitted.

The real spherical variations already satisfy background gauge: their spatial connection variation has the same antisymmetric tensor structure as the background, so \(D_i\delta A_i=0\), while \([\Phi,\delta\Phi]=0\). Thus the background-gauge fixing term vanishes on this block. This is an actual invariant slice of the gauge-fixed static fluctuation problem.

Using \(K'=-Kh\), \(h'=(1-K^2)/t^2\), define

\[
Q=d/dt+W,\quad
W=\begin{pmatrix}h&\sqrt2K/t\\\sqrt2K/t&-1/t\end{pmatrix}.
\]

Then \(\mathcal H=Q^\dagger Q\) on the stated Dirichlet quadratic-form domain. Its kernel is empty: \(Qy=0\) together with \(y(x)=0\) implies the identically zero solution by first-order uniqueness. No collective zero eigenvalues are removed in this block determinant.

Let \(Y(t)\) be the regular zero-energy fundamental matrix, normalized by \(Y(t)/t^2\to I_2\). The matrix Gel'fand–Yaglom relation gives the relative determinant as \(\det Y(x)/\det Y_{\rm ref}(x)\). [Kirsten–McKane, math-ph/0403050v1, Section 4, equations (40)–(42) and the following unnumbered determinant-ratio formula, pages 12–13](https://arxiv.org/abs/math-ph/0403050v1) establishes the regular-interval matrix result for Hermitian potentials, the same leading coefficient, and matched self-adjoint boundary data. Apply it first on \([\epsilon,x]\). Here both matrix potentials have the same \(2I_2/t^2\) singular part; each unit-derivative regular-cutoff fundamental matrix has leading common factor \((3\epsilon)^{-1}Y(x)\). Its determinant factor cancels in the ratio, by the same regular/singular-basis argument as in REPORT.md. No direct application of a regular theorem at \(t=0\) is assumed.

## Exact reduction of the matrix determinant to one integral

The BPS mass-variation solution

\[
y_0(t)=\begin{pmatrix}tK'\\t(h+th')/\sqrt2\end{pmatrix}
\]

satisfies \(Qy_0=0\). At the origin \(y_0=t^2a+O(t^4)\), where
\(a=(-1/3,\sqrt2/3)^T\) and \(a^Ta=1/3\).

For another regular zero-energy solution \(y\), put \(z=Qy\). Since \(Q^\dagger z=0\), \(z'=Wz\), while \(y_0'=-Wy_0\); hence \(y_0^Tz\) is constant and vanishes at the origin. With \(J=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)\), it follows that

\[
z=C\frac{\sinh t}{t^2}Jy_0.
\]

This follows from \(WJ+JW=\operatorname{tr}(W)J\) and
\(\operatorname{tr}W=\coth t-2/t\). Writing \(d=\det[y_0,y]\) gives

\[
\left[d\frac{\sinh t}{t^2}\right]'
=C\left(\frac{\sinh t}{t^2}\right)^2y_0^Ty_0.
\]

If \(y=Yb\), its small-\(t\) behavior determines \(C=9\det[a,b]\). Dividing by that same \(\det[a,b]\) yields

\[
\boxed{\det Y(x)=\frac{9x^2}{\sinh x}
\int_0^x\!dt\left[
(\coth t-1/t)^2+
\frac12\left(\frac{\cosh t}{t}-\frac1{\sinh t}\right)^2
\right].}\tag{M2}
\]

The integrand is positive and behaves as \(t^2/3\) at zero, so \(\det Y\sim x^4\), verifying the fundamental normalization directly.

Choose the explicit diagonal comparison

\[
\mathcal H_{\rm ref}=\operatorname{diag}
(-d^2/dt^2+1+2/t^2,\;-d^2/dt^2+2/t^2),
\]

with the same origin and outer Dirichlet data. Its regular zero-energy determinant is
\(\det Y_{\rm ref}=3x^2(\cosh x-\sinh x/x)\). Thus (M2), divided by that expression, computes the entire relative determinant \(D_{\rm real}(x)\) of this coupled block; there is no unspecified numerical constant in this comparison.

## Calculated large-radius term

At large \(t\), the exponentially growing part of the integrand in (M2) is \(e^{2t}/(8t^2)\). Repeated integration by parts gives

\[
\int_0^x\!dt\,[\cdots]
\sim\frac{e^{2x}}{16x^2}
\left(1+\frac1x+\frac3{2x^2}+\cdots\right).
\]

The non-growing terms contribute only exponentially small relative corrections. Therefore

\[
\boxed{D_{\rm real}(x)=\frac3{4x^2}
\left[1+\frac2x+\frac7{2x^2}+O(x^{-3})\right],}\tag{M3}
\]

and

\[
\log D_{\rm real}(x)
=\log\frac3{4x^2}+\frac2x+\frac3{2x^2}+O(x^{-3}).\tag{M4}
\]

This real bosonic block contributes \(-\tfrac12\log D_{\rm real}\) to \(\log Z\), so its residual linear contribution is \(-1/(m_WR)\) relative to its stated comparison. Together with the static ghost slice's residual \(-1/(m_WR)\), the two computed pieces would total \(-2/(m_WR)\) **within these auxiliary comparisons**. This is bookkeeping for two computed slices, not the coefficient of the full gauge ensemble. In particular it does not cancel or validly add the previous four-coordinate Jacobian: the latter's mode/domain prescription differs, and the remaining spherical gauge sector can contribute.

## Independent numerical check and freeze

`check_vector.py` verifies (M1), \(Qy_0=0\), the determinant-integrand identity and all near-origin series symbolically. Independently it integrates the original coupled second-order matrix equation \(Y''=UY\) with DOP853. It uses two origin cutoffs, \(10^{-3}\) and \(5\times10^{-4}\), and the Frobenius start

\[
Y=t^2[I+At^2+Bt^4+O(t^6)],\quad
A=V_0/10,\quad B=(V_0A+V_2)/28,
\]

where \(U=2I/t^2+V_0+V_2t^2+\cdots\). The scalar integral in (M2) is evaluated separately at 60 decimal digits. All six comparisons at \(x=2,5,8\) agree within \(2.32\times10^{-13}\) relative discrepancy. The declared conservative tolerance is \(2\times10^{-7}\); no certified interval bound is claimed. Direct scalar quadrature at \(x=10,20,40\) also checks approach to (M3), without fitting any coefficient.

The v2 manifest `runs/vector-001/manifest.json` has status `completed` and validates against current code. `VECTOR_COMPUTATION_CONTRACT.json` records exact assertions, software, bounds and non-claims. The coordinator independently reconstructed the Hessian, BPS kernel, normalization and large-radius coefficient before seeing the numerical implementation. Mathematical proofreading self-review covers both follow-up reports.

**Frozen scope:** a scalar ghost block, its exact Fourier-frequency determinants, a real coupled vector/A4 block, and explicit boundary-domain obstructions are now calculated. The next required calculation is the remaining spherical phase/radial-gauge block with the vector boundary conditions compatible with the same ghost framing, followed by the angular/Fourier sum and physical-vacuum matching. The scalar auxiliary references used here do not bypass that task. Physical QCD \(c_H\), \(R(\alpha)\) and an alpha root remain uncomputed.
