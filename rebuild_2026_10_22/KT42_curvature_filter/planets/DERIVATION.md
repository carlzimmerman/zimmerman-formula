# Supplementary planetary radial screen for the fixed KT42 law

Pre-result, 2026-11-04. This is a new observable for the already fixed
curvature-only filter, not a change to its law, baryons, Cassini threshold
or Milky Way cuts. Test a={.0001,.001,.1,.3}kpc, p=9/8 and ell=3kpc at
Mars and Saturn, with both original acceleration footings. Keep the exact
KT39/KT42 Solar GM and uniform external gradient; do not silently replace
them with AZ11's ephemeris GM or its converted external-field convention.

The supplementary cuts are the actual AZ11/AZ12 definitions:

- AZ11 point-radius diagnostic: sigma_g=dg_tight*max(EPM,INPOP)/min(EPM,INPOP)
  from `RQ3_acceptance_v2/tolerances.json`; accept abs(delta g)/sigma_g<=2.
- AZ12 monopole secular-rate diagnostic: compare with max(EPM,INPOP) in
  mas/year, again abs(rate)/sigma<=2. Eccentricities are Mars .093 and
  Saturn .054, from the existing AZ12 source.

These are archived supplementary-precession summaries, not a new extraction
of raw tracking data or a joint likelihood. Full orbital multipoles, fitted
initial conditions and covariance remain absent. A failed convergence/control
gate means no numerical verdict, rather than a physical exclusion.

## Exact monopole including the full adjoint

Use rM/a0 units and retain the notation of `../solar/DERIVATION.md`. Let
the baryonic radial gradient be u=r^(-2), H_a=h_r nn+h_t(I-nn), and

\[
C=R(z)-1+xR'(z),\quad D=p\lambda^2s^{p-1}xR'(z),
\quad d_0(r)=\int_{-1}^1D(r,\mu)d\mu.
\]

The exact mean radial A acceleration is

\[
g_A(R)=\frac12\int_{-1}^1 C(R,\mu)[R^{-2}+\eta\mu]d\mu.
\]

The source has not been assumed spherical: averaging commutes with the
isotropic linear outer Gaussian filter and extracts its l=0 sector. Define
b_r=d_0 h_r/2 and b_t=d_0 h_t/2. Before the outer filter the B force in
that sector is -[b_r'+2(b_r-b_t)/r]. Filtering the vector gives an l=1
Gaussian angular kernel. Integrating b_r' by parts yields

\[
g_B(R)=\frac{\mathcal C}{2}\int_0^\infty d_0(r)
 e^{-(R^2+r^2)/(2\alpha^2)}
 \left\{h_r\left[-\frac{r^4}{\alpha^2}i_1(z)
  +\frac{r^3R}{\alpha^2}i_1'(z)\right]
       +2r^2h_t i_1(z)\right\}d\log r,
\]
\[
\mathcal C=\frac{4\pi}{(2\pi\alpha^2)^{3/2}},\qquad
z=Rr/\alpha^2,\quad
i_1(z)=\frac{z\cosh z-\sinh z}{z^2}
=\sum_{k\ge0}\frac{2(k+1)z^{2k+1}}{(2k+3)!}.
\]

There is no finite-difference derivative of B and no missing outer filter.
For the largest tested R/alpha, the Gaussian-weighted integration domain
has abs(z)<.02. Eight series terms are more than sufficient; compare six
versus eight and record the actual largest z. The origin surface vanishes
because point-source B=O(r^2) for fixed alpha>0; infinity is Gaussian damped.

An independent exact representation follows from enclosed source. Put
W_R(y)=integral_{|x|<R} Gaussian_alpha(x-y) d^3x. Then

\[
g_B(R)=-\frac1{2R^2}\int_0^\infty r^3d_0(r)
       [h_r W_R''(r)+2h_t W_R'(r)/r]d\log r.
\]

The W derivatives can be evaluated by integrating the Gaussian Hessian
over the small observation ball directly. With epsilon=R/alpha, u=r/alpha,

\[
\begin{split}
W_R''&=\frac{R^3}{\sqrt{2\pi}\alpha^5}
\int_0^1v^2dv\int_{-1}^1d\xi\,
e^{-(u^2+\epsilon^2v^2-2u\epsilon v\xi)/2}
[(u-\epsilon v\xi)^2-1],\\
W_R'/r&=\frac{R^3}{\sqrt{2\pi}\alpha^5}
\int_0^1v^2dv\int_{-1}^1d\xi\,
e^{-(u^2+\epsilon^2v^2-2u\epsilon v\xi)/2}
[\epsilon^2v^2(1-\xi^2)/2-1].
\end{split}
\]

This avoids subtracting nearly equal error functions. In the R/alpha->0
limit both representations give

\[
g_B(R)=-\frac{R}{3\sqrt{2\pi}\alpha^5}
\int r^3d_0 e^{-r^2/(2\alpha^2)}
[h_r(r^2/\alpha^2-1)-2h_t]d\log r+O(R^3).
\]

The total supplementary radial anomaly is a0*(g_A+g_B), not A alone.

## High-field mechanism and orbit convention

At fixed positive a, H_a is finite near the Sun while raw u diverges.
Thus x dominates s^p eventually. The simple response has C~x^(-1/2),
giving g_A->1 and the dimensional inward anomaly ->a0. The returned B
force is smooth and odd, so its monopole is O(R) at the origin. It cannot
cancel a constant inward anomaly in that limit. Actual planetary radii
still require the full finite-radius calculation; the limiting argument
alone does not grade a planet.

For inward positive anomaly A(r), use AZ12's exact first-order monopole
precession average over eccentric anomaly E:

\[
\langle\dot\omega\rangle=
\frac{\sqrt{1-e^2}}{n a e}
\int_0^{2\pi}A(a[1-e\cos E])(\cos E-e)\frac{dE}{2\pi},
\quad n=\sqrt{GM/a^3}.
\]

Here the physical orbital semimajor axis a is distinct from the filter
width, denoted alpha in the dimensionless formulas. The code uses explicit
names to avoid that ambiguity. Use the original planet radii in AU and
365.25 days/year. Constant, harmonic and inverse-square radial-force
oracles and the Newtonian zero are retained from AZ12's checks.

Predeclared numerical controls: radial grid2000->4000, source angular
80->160, orbital quadrature64->128, Gaussian tail domain16->24 filter
widths, Gaussian-ball quadrature4->8, and six/eight i1 series terms. Require
changes in radial/periodic diagnostic Z below1e-5, and independent B
representations to agree within1e-8 in acceleration/a0 (also report their
relative discrepancy). The finite endpoint tail values and linear-B
approximation discrepancy are reported, not silently substituted for the
exact calculation. The source remains the inherited exterior point Sun.
