# Exact-exponential QUMOND Cassini certificate

## Scope

This directory certifies one deliberately narrow statement: the standard QUMOND
external-field quadrupole produced by the physical law

\[
\mu(y)=1-e^{-y},\qquad y=g/a_0,
\]

is above the adopted Cassini bound for the constants recorded in `MANIFEST.json`.
It is **QUMOND, not AQUAL**, and it is not a certificate for a relativistic action,
modified inertia, or every possible external-field prescription.

## Exact inverse and integral

The QUMOND argument is explicitly named
\(x=g_N/a_0\).  The code solves

\[
x=y(1-e^{-y}),\qquad \nu_{\exp}(x)=y/x,
\]

by root finding.  It does not use the inequivalent shortcut
\(1/[1-e^{-\sqrt{x}}]\).  The true external acceleration
\(\eta=g_{\rm ext}/a_0\) is converted before integration through
\(e_N=\eta\mu(\eta)\).

The implemented dimensionless QUMOND quadrupole is

\[
q=\frac32\left|\int_0^\infty\!dv\int_{-1}^{1}\!d\xi\,
[\nu(\sqrt{e_N^2+v^4+2e_Nv^2\xi})-1]
\{e_N(3\xi-5\xi^3)+v^2(1-3\xi^2)\}\right|.
\]

Two numerically independent forms are compared:

1. nested adaptive SciPy quadrature, with every warning promoted to an error;
2. fixed-order tensor-product Gauss--Legendre quadrature, radially split at and
   around the cancellation shell \(v=\sqrt{e_N}\).

The fixed rule is scanned through orders 32, 64, 128, and 256.  Both rules are
scanned from radial endpoint 6 to 10.  For \(V=6\), the omitted tail is bounded by

\[
|q_{v>V}|\le 12e^{e_N}\int_V^\infty(e_N+v^2)e^{-v^2}\,dv
=8.698093\times10^{-14}.
\]

The mutations \(\nu=1\) and \(\eta=0\) independently return exactly zero
quadrupole, so the result is not a hard-coded constant.

## Reproduce

From the repository root:

```bash
PYTHONWARNINGS=error python3 hunt_2026/exact_mu_cassini_2026/test_exact_mu_qumond_cassini.py
PYTHONWARNINGS=error python3 hunt_2026/exact_mu_cassini_2026/exact_mu_qumond_cassini.py
```

Both commands must exit 0.  The second command's stdout is checked into
`exact_mu_qumond_cassini.out`.  Its zero exit means the *numerical exclusion
calculation* passed its audit; it does not mean the theory passed Cassini.

## Result and limitation

For the canonical footing \(a_0=9.3619\times10^{-11}\,\mathrm{m\,s^{-2}}\),
the adaptive value is \(q=0.165855042414111\), giving

\[
Q_2=1.956185874272\times10^{-26}\ {\rm s}^{-2},
\]

or 3.761895912 times the adopted \(5.2\times10^{-27}\,{\rm s}^{-2}\) two-sigma
ceiling.  Thus the exact-exponential kernel is excluded **within this QUMOND
calculation and these inputs**.  This result must not be relabeled as a direct
AQUAL calculation or as a no-go theorem for all relativistic MOND actions.

The alternate repository footing
\(a_0=1.1279\times10^{-10}\,\mathrm{m\,s^{-2}}\) is recomputed rather than
rescaled. It gives \(q=0.165430921606774\) and
\(Q_2=2.580227657819\times10^{-26}\,\mathrm{s^{-2}}\), or 4.961976265 times
the same ceiling. Both footings are therefore adverse within this narrow
standard-QUMOND calculation.
