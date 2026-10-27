# Granting the isolated-law baseline does not remove the conditional tracer test

The exact theorem in VIRIAL_DERIVATION.md assumes all tracer support is
Newtonian gravity from the radial mass measure. Here is an explicitly different
force reading. Suppose the tracer acceleration is

`g(r)=g0(r)+G M_extra(<r)/r^2`,

where `g0` is specified independently of the extra nonnegative finite mass.
The whole-tracer projected virial identity is linear in acceleration. Define

`S0_i=(4 pi/(3 L_i)) integral nu_i(r) g0(r) r^3 dr`.

Then `S_i-S0_i` obeys the same mass-measure kernel as in the original theorem.
For positive residual moments, the sharp two-tracer bound applies verbatim to
`y_i=3 a_i (S_i-S0_i)/G`. A negative residual cannot be supplied by positive
extra Newtonian mass. If either residual is zero, positivity of each kernel
requires zero extra mass, hence both residuals must be zero. This is an algebraic extension under the stated additive
force assumption. A backreaction changing `g0`, a force acting differently on
the two tracers or an extra non-Newtonian acceleration requires another model.

The conditional comparison computed here uses the Tolstoy population scales
and widths from source_extraction.json with the same caveats as the original
theorem. It grants the full isolated-law acceleration of the stars:

```
Mstar(<r)=Mstar [f_MR F(r/a_MR)+(1-f_MR) F(r/a_MP)],
F(x)=x^3/(1+x^2)^(3/2), f_MR=.63,
gstar=G Mstar(<r)/r^2,
g0=gstar nu(gstar/a0).
```

Here .63/.37 are **assumed stellar-mass weights**. Linking them to the observed
selected tracer number fraction requires population luminosity-function and
completeness/selection conversions; equal present stellar M/L alone does not
establish that link. These mass weights are not measured by that table.
`Mstar` still uses the old Sextans Upsilon_V=2 and catalogue
luminosity. Four explicitly tested baselines use a0 canonical/alt and the
rational/exponential nu kernels already present in local research. The nu
function acts on **stellar** Newtonian acceleration in this test. Applying it
also to extra mass is a different hypothesis and is not excluded here.

For a Plummer tracer set `r=a_i x` to evaluate

`S0_i=a_i integral_0^infinity x^3 (1+x^2)^(-5/2) g0(a_i x) dx`.

The checker uses both `x=t/(1-t)` on (0,1) and a compact three-dimensional
radial-integral expression on (0,infinity), then applies the independently
audited algebraic mass floor to the residuals. Tracer fractions, baseline,
geometry and the selected observed moments remain conditional inputs.

This is a deliberately generous stock stress test: the isolated-law baseline
is **not charged to the inventory at all**, and the extra mass is allowed all
`5.364/f_ret * Mstar`, with f_ret=.1, rather than just the remaining-free stock.
This concession does not construct a finite-stock realization of the baseline
(its asymptotic isolated-law halo itself has infinite mass). It is a relaxation
of the budget **at this fixed baseline**: if even this larger allowance fails,
charging baseline mass to the same stock cannot rescue that specified additive
model. The sharp JOINT residual bound need not be monotone when the baseline
profile changes. It is not automatically a bound for all capped/modified
baselines. Neither the stock
ratio nor retention is an independent measured cosmological catchment here.

A separate **one-tracer** bound does extend to lower baselines: if
`g_actual_baseline(r)<=g0(r)` pointwise, its outer-tracer residual is at least
`S_MP-S0_MP`, and thus extra mass is at least
`3 a_MP (S_MP-S0_MP)/G`. The checked outer residual bound alone exceeds the
same cold-stock allowance in all four declared baseline cases. This statement
requires the actual pointwise force ordering, the same stellar profile and
the same conditional full-tracer moments; it is not a theorem about arbitrary
backreaction or the original field action.

The surviving astrophysical obligation is unchanged: derive matched tracer
weights/geometry/selection and the actual force decomposition or forward fit
the selected velocities. These arithmetic results do not replace that work.
