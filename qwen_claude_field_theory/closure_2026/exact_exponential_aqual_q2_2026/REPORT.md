# Exact-exponential AQUAL Solar-System quadrupole audit

## Result

The repository did **not** previously calculate the Solar-System quadrupole of the
target law by solving its nonlinear AQUAL equation.  The executable calculations for
the exponential kernel used the exact **QUMOND** quadrupole integral, after either
using the empirical RAR function or inverting the spherical AQUAL relation.  That is a
useful control, but it is not the AQUAL boundary-value problem.

This directory now solves

\[
 \nabla\!\cdot\!\left[\left(1-e^{-|\nabla\phi|/a_0}\right)
 \nabla\phi\right]=4\pi GM\,\delta^3(\mathbf r),
 \qquad \nabla\phi\longrightarrow-\mathbf g_{\rm ext},
\]

directly on an axisymmetric finite-volume grid.  In units \(GM=a_0=1\), write
\(u=\phi+\eta z\), where \(\eta=g_{\rm ext}/a_0\).  The numerical boundaries are
the physical condition \(\phi(r_{\min})=-1/r_{\min}\), equivalently
\(u(r_{\min},\theta)=-1/r_{\min}+\eta r_{\min}\cos\theta\), and
\(u(r_{\max})=0\), with
\(r_{\min}=10^{-6}\) and \(r_{\max}=10^4\).  The central quadrupole is extracted from

\[
 u+\frac1r=c_2r^2P_2(\cos\theta)+\cdots,
 \qquad |q_{zz}|=2|c_2|,
 \qquad q_2^{\rm BN}=3|c_2|=\frac32|q_{zz}|.
\]

For the frozen repository parameters

\[
 a_0=9.3619\times10^{-11}\ {\rm m\,s^{-2}},\qquad
 g_{\rm ext}=2.32\times10^{-10}\ {\rm m\,s^{-2}},
\]

the mesh-extrapolated result is

\[
 |q_{zz}|=0.17748\pm0.00255_{\rm num},\qquad
 |Q_2|=(2.093\pm0.030_{\rm num})\times10^{-26}\ {\rm s^{-2}}.
\]

The positive two-sigma ceiling from the stated 2026 Cassini result,
\(Q_2=(1.6\pm1.8)\times10^{-27}\ {\rm s^{-2}}\), is
\(5.2\times10^{-27}\ {\rm s^{-2}}\).  The direct AQUAL prediction is therefore
**4.025 times that ceiling**.  The executable classification is not a label inserted
by hand: it takes the minimum of \(Q_2-\delta Q_{2,\rm num}\) over the central and
\(g_{\rm ext}\pm1\sigma\) runs.  That robust lower endpoint is still 3.818 times the
ceiling.  Moving \(g_{\rm ext}\) through its quoted one-sigma
range \((2.32\pm0.16)\times10^{-10}\ {\rm m\,s^{-2}}\), while holding \(a_0\)
fixed, gives

\[
 |Q_2|=(2.041\text{--}2.123)\times10^{-26}\ {\rm s^{-2}},
\]

so this sensitivity does not change the verdict.

## Independent validation

Blanchet and Novak numerically solved the nonlinear AQUAL equation for exactly
\(\mu_{\exp}(y)=1-e^{-y}\).  At \(a_0=1.2\times10^{-10}\) and
\(g_{\rm ext}=1.9\times10^{-10}\ {\rm m\,s^{-2}}\), their Table 1 gives
\(q_2=0.26\) and \(Q_2=3.0\times10^{-26}\ {\rm s^{-2}}\)
([arXiv:1010.1349, Eq. 34c, Eq. 37a, and Table 1](https://arxiv.org/abs/1010.1349)).
The present three-mesh extrapolation gives

\[
 q_2^{\rm BN}=0.259773,
\]

only \(-0.087\%\) from that published two-significant-figure anchor.  Separately,
the zero-external-field numerical solution matches the exact spherical first integral
\(x(1-e^{-x})=r^{-2}\) to a maximum relative field error of \(1.95\times10^{-3}\)
on the tested interior annulus.

The physical inner boundary is also stable against its numerical placement.  Moving
\(r_{\min}\) from \(10^{-5}\) to \(10^{-7}r_M\), while matching the logarithmic
radial spacing to leading order, changes the raw \(|q_{zz}|\) values by a fractional
span of only \(3.92\times10^{-4}\).  This is far below the continuum-extrapolation
budget used above.

| grid | anchor \(|q_{zz}|\) | frozen \(|q_{zz}|\) |
|---:|---:|---:|
| 192 x 48 | 0.184709 | 0.187688 |
| 288 x 72 | 0.178302 | 0.182021 |
| 384 x 96 | 0.176066 | 0.180030 |
| \(h^2\) extrapolation | 0.173182 | 0.177480 |

The conservative numerical error is the full distance between the extrapolated value
and the finest raw mesh, not the much smaller regression residual.

## The category error this closes

There are three different functions/calculations in play:

1. The target AQUAL law is \(\mu(x)=1-e^{-x}\).
2. Its spherical inverse partner is defined implicitly by
   \(x(1-e^{-x})=y_N\) and \(\nu_{\mu\exp}(y_N)=x/y_N\).
3. The empirical RAR shortcut is
   \(\nu_{\rm RAR}(y_N)=[1-e^{-\sqrt{y_N}}]^{-1}\).

They are not interchangeable.  At \(y_N=1\), this script derives

\[
 \nu_{\mu\exp}=1.349976,\qquad \nu_{\rm RAR}=1.581977.
\]

Even using the correct spherical inverse does not make the QUMOND integral an AQUAL
calculation.  Desmond, Hees, and Famaey explicitly note that the QUMOND integral is
exact only for QUMOND and that AQUAL requires a nonlinear Poisson solve
([arXiv:2401.04796, Sec. 3.3](https://arxiv.org/abs/2401.04796)).  For the same
spherical target and frozen parameters, this audit finds

\[
 |Q_2|_{\rm QUMOND}=1.956\times10^{-26}\ {\rm s^{-2}},\qquad
 \frac{|Q_2|_{\rm AQUAL}}{|Q_2|_{\rm QUMOND}}=1.0701.
\]

Thus the previous QUMOND proxy underestimated the exact-AQUAL failure by about 7%,
rather than hiding a rescue.

The observational comparison uses the updated result
\(Q_2=(1.6\pm1.8)\times10^{-27}\ {\rm s^{-2}}\) reported by Park et al.
([arXiv:2602.17884](https://arxiv.org/abs/2602.17884)).

## Classification and limits

**DEAD at this gate:** any candidate whose actual Solar-System weak-field branch is
the unscreened, exact-exponential AQUAL equation above, with the standard Galactic
external-field boundary condition and the frozen \(a_0\), fails the stated Cassini
quadrupole ceiling.

This is not a global no-go for every relativistic MOND theory.  A theory could change
the Solar-System field equation, screen the external field, use modified inertia, or
alter the coupling between the weak potential and planetary motion.  Each such move
would be a new action-level branch and must be rederived.  The calculation also does
not establish a new formula in the literature: the exact-AQUAL quadrupole and one
exponential-kernel anchor were already published in 2011.  The new result here is the
reproducible repository-local calculation at the frozen parameters and the correction
of the AQUAL/QUMOND/RAR category mix-up.

Numerical limitations are explicit: a point source is represented by an inner
Newtonian boundary, the far external-field condition is imposed at finite radius,
and the uncertainty quoted above is a discretisation budget only.  It does not include
uncertainty in \(a_0\), the Galactic field model, or the Solar mass.

## Reproduction

```bash
cd qwen_claude_field_theory/closure_2026/exact_exponential_aqual_q2_2026
python3 -m unittest -v test_exact_exponential_aqual_q2_2026.py
python3 exact_exponential_aqual_q2_2026.py
```

The second command rewrites `exact_exponential_aqual_q2_2026.json` with all mesh
values, nonlinear residuals, parameter inputs, controls, and dimensional results.
