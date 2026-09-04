# HPI-Delta exterior-orbit numerical audit (2026)

## Result

**PASS (bounded numerical validation), not theory closure and not a novelty
claim.**  Conditional on the isolated spherical weak-static equation

\[
\mu(g/a_0)g={G M_b(<r)\over r^2},\qquad \mu(y)=1-e^{-y},
\]

the near-circular epicyclic/apsidal law is

\[
{\kappa^2\over\Omega^2}
= {e^y-1+3y\over e^y-1+y},\qquad
\Delta\varpi
=2\pi\left[\sqrt{{e^y-1+y\over e^y-1+3y}}-1\right]
\]

on the **exterior constant-enclosed-mass branch**, where
\(y=g/a_0=\Omega^2r/a_0\).  Equivalently,

\[
{T_r\over T_\phi}={\Omega\over\kappa}
=\sqrt{{e^y-1+y\over e^y-1+3y}}.
\]

The sign convention is angular advance between successive pericenters minus
\(2\pi\); negative values are retrograde.

## Derivation and the extended-mass correction

For a central force, linearizing
\(\ddot r=\ell^2/r^3-g(r)\) around a circular orbit gives

\[
\kappa^2=g'(r)+{3g(r)\over r},\qquad \Omega^2={g(r)\over r}.
\]

Let

\[
L={d\ln\mu\over d\ln g}={y\over e^y-1},\qquad
m={d\ln M_b(<r)\over d\ln r}.
\]

Differentiating the same spherical flux law yields

\[
(1+L){d\ln g\over d\ln r}=m-2,
\]

and therefore the more general local spherical formula

\[
{\kappa^2\over\Omega^2}
= {1+m+3L\over1+L}
= {(1+m)(e^y-1)+3y\over e^y-1+y}.
\]

Thus the short exterior formula is not valid unchanged inside an extended
baryonic mass distribution.  It also does not cover nonspherical sources or
an external-field effect.

## Independent nonlinear check

The script uses units \(GM=a_0=1\), solves the implicit force with Brent's
method at every force evaluation, integrates the nonlinear central-force
orbit, and measures successive pericenter times and angles.  The analytic
epicycle formula is not used to generate the measured frequency.

| \(y\) | predicted \(\kappa/\Omega\) | measured | relative error | measured \(\Delta\varpi\) (deg) |
|---:|---:|---:|---:|---:|
| 0.01 | 1.4133286673 | 1.4133286685 | 8.34e-10 | -105.282178150 |
| 0.1 | 1.4052747142 | 1.4052747153 | 8.36e-10 | -103.822331627 |
| 1 | 1.3174820235 | 1.3174820246 | 8.07e-10 | -86.751490132 |
| 5 | 1.0322844243 | 1.0322844265 | 2.09e-9 | -11.258906195 |
| 10 | 1.0004537109 | 1.0004537111 | 1.92e-10 | -0.163261935 |

At \(y=1\), reducing the radial displacement from \(10^{-2}\) to \(10^{-3}\)
to \(10^{-4}\) reduces the relative frequency discrepancy from
\(8.21\times10^{-6}\) to \(8.08\times10^{-8}\) to
\(8.07\times10^{-10}\), consistent with the expected quadratic
near-circular correction.  DOP853 and RK45 agree to \(6.51\times10^{-11}\)
fractionally at \(y=1,\epsilon=10^{-3}\).

A live mutation that discards the constitutive slope and falsely predicts
\(\kappa/\Omega=1\) has relative error \(0.4053\) at \(y=0.1\), while the
derived law has error \(8.36\times10^{-10}\).  The mutation is rejected.

The exact limits are

\[
y\to\infty:\quad \Delta\varpi\to0,
\qquad
y\to0^+:\quad \Delta\varpi\to
2\pi\left({1\over\sqrt2}-1\right)
=-105.4415587728^\circ.
\]

## Scope and non-claims

- This validates a consequence of the reduced spherical weak-static branch;
  it does not independently prove that the parent relativistic action closes.
- The five-point floating-point experiment is not a proof over all \(y>0\).
  The separate SymPy residual check establishes the displayed algebraic
  identity, conditional on the spherical flux and central-force equations.
- The exact \(y=0\) endpoint is excluded.  Only the one-sided limit is taken.
- No finite-eccentricity theorem, PPN result, stability result, or novelty
  claim follows from this computation.
- The central-force epicycle identity is standard.  The specific closed form
  above comes from substituting the exponential constitutive law.

## Reproduction

```bash
python3 hpi_delta_orbit_numeric_2026.py
python3 -m unittest -v test_hpi_delta_orbit_numeric_2026.py
python3 -m py_compile hpi_delta_orbit_numeric_2026.py test_hpi_delta_orbit_numeric_2026.py
```

The run is deterministic and uses no random numbers.  See
`computation_manifest.json` for the finite computation contract and
`hpi_delta_orbit_numeric_2026.out` for a recorded run.
