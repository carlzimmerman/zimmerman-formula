# Independent whole-domain geometric Mellin audit

**Verdict: proved conditional on the parent's exact QUMOND quadrupole functional.** The entire positive external-field continuum has a nonzero moment, not a blind moment:

\[
\int_0^\infty e^{-1/2}w_e(y)\,de=-\frac{4\pi}{35}y,\qquad y>0.
\]

This conclusion was reconstructed from the triangle-domain angular integral, independently of the author's beta-function continuation. Exact inspected source hashes and observed Git HEAD are recorded in `independent_mellin/provenance.json`. The source functional and physical normalization remain named inputs; this is not an independent derivation of QUMOND from a covariant action.

## Full domain and convergence

Write `w_e(y)=sqrt(y) F(e/y)`, `q=e/y`, and

\[
A(q)=2q^3+q^2+6q+12,\quad B(q)=-2q^3+q^2-6q+12.
\]

The exact two branches are

\[
F(q)=-\frac2{35q^3}\left[\frac{A(q)}{\sqrt{1+q}}-\frac{B(q)}{\sqrt{1-q}}\right]\quad(0<q<1),
\]
\[
F(q)=-\frac2{35q^3}\left[\frac{A(q)}{\sqrt{1+q}}+\frac{B(q)}{\sqrt{q-1}}\right]\quad(q>1).
\]

Expanding these actual branches gives `F(q)=q²/10+O(q⁴)` at zero and `F(q)=−q^(−7/2)[1+11/(40q²)+O(q^(−4))]` at infinity. At the shell the signed coefficients are `+2/7` below and `−2/7` above, multiplying `|q−1|^(−1/2)`. Therefore `q^(−1/2)F(q)` is absolutely integrable: powers `q^(3/2)`, `q^(−4)`, and an integrable square-root shell. Dropping the upper branch changes the moment and its sign.

## Direct geometric calculation

In the parent's raw angular transform put `t=u²`,

\[
\xi=\frac{y^2-e^2-t^2}{2et},\quad A_\xi=3\xi-5\xi^3,\quad B_\xi=1-3\xi^2.
\]

The integration domain is the symmetric triangle `e,t>0`, `|e−t|<y<e+t`. Its moment is

\[
M(y)=\frac y2\iint e^{-3/2}t^{-3/2}[e A_\xi+tB_\xi],de,dt.
\]

Fubini and exchange `e↔t` are legitimate even before cancellation. The polynomials are bounded on `−1≤xi≤1`. Near the axis `e=0`, `t` is near `y` in a strip of width `2e`, so the absolute integral is bounded by a constant times `integral e^(−1/2)de`; the other axis is identical. In the large diagonal strip, `e,t` are comparable, its width is at most `2y`, and the integrand is `O((e+t)^(−2))`. The remaining compact domain is bounded away from the axes. Hence the raw double integral is absolutely convergent.

Symmetrization replaces the bracket by `(e+t)P(xi)/2`, where `P=1+3xi−3xi²−5xi³`. Set `s=e+t`, `v=e−t` (Jacobian `1/2`). Then

\[
M(y)=y\int_y^\infty\!ds\int_{-y}^y\!dv\,
\frac{s}{(s^2-v^2)^{3/2}}
P\!\left(\frac{2y^2-s^2-v^2}{s^2-v^2}\right).
\]

At fixed `v`, let `u=(s²−v²)^(−1/2)` and then `x=u sqrt(y²−v²)`. The transformed angle is `xi=2x²−1`, with `0<x<1`. Thus

\[
M(y)=y\left[\int_{-y}^y\frac{dv}{\sqrt{y^2-v^2}}\right]
\left[\int_0^1 P(2x^2-1)dx\right].
\]

The two factors are `pi` and

\[
\int_0^1(-12x^2+48x^4-40x^6)dx=-4+48/5-40/7=-4/35.
\]

This proves the identity. Scaling `e=yq` identifies `K=integral q^(−1/2)F(q)dq=−4pi/35` without analytic continuation or extrapolation of the lower branch.

## Operational implication and limits

For `f(y)=nu(y)−1` assume `integral y|f(y)|dy<infinity`. The absolute kernel bound is `integral e^(−1/2)|w_e(y)|de=y integral q^(−1/2)|F(q)|dq`, so the response-level Fubini exchange is justified. With the parent's convention

\[
Q_2(e)=-\frac{9a_0}{4r_M}\int f(y)w_e(y)dy,
\quad C=\int yf(y)dy,
\]

one obtains

\[
\boxed{\int_0^\infty e^{-1/2}Q_2(e)de=\frac{9\pi a_0}{35r_M}C.}
\]

This is an exact functional determination of `C` from an ideal entire continuum. It does not select `C=32pi`, provide such observational data, or establish inference from a finite/noisy external-field range. Relating `C` to a relativistic vacuum coefficient still requires a separate dictionary. A constant `f` lies outside the finite absolute-moment class; the script's zero constant-kernel Mellin benchmark is only a convergent weight identity, not a counterexample in the stated class.

## Bounded corroboration

The frozen independent script uses exact SymPy identities and separately desingularized 45-digit mpmath quadratures on both genuine branches. Eight-term series are used only for `q<.001` or `q>1000`; this is numerical corroboration, not interval-certified quadrature or a substitute for the proof. The main run passes all ten implemented checks. Its lower and upper contributions are approximately `+0.18297629249` and `−0.54201545290`, totaling `−0.35903916041026208=−4pi/35`. The mutation omitting `q>1` fails both intended whole-domain numerical moments; both runner manifests validate with output/input hash checks. Standard runner manifests preserve bounds, stdout/stderr, source hashes and outcomes in `independent_mellin/main/` and `independent_mellin/control/`.
