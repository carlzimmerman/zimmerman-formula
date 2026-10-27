# Admission refinements and first-run failure

This addendum preserves the immutable pre-run DERIVATION.md rather than
overwriting it. It is part of the v2 execution input.

## Hadronic power counting

Equations (5)-(7),(9) of DERIVATION.md order the perturbative OPERATOR
coefficients. They do not constitute a complete NLO HADRONIC endpoint.
The trace anomaly gives H_g=O(1/g_s^2). Therefore an unknown next gluon
threshold delta g_s=O(u g_s^5), equivalently an O(u g_s^4) canonical
G^2 coefficient, contributes O(u g_s^2) to M. That is the same hadronic
order as the known mixed quark coefficient C_F(-3L+17/4).

A uniformly complete hadronic result at that order needs the next gluon
threshold, consistently evolved scalar operators, anomalous dimensions,
threshold flavor changes and matrix elements. The current result fixes
new operator coefficients. It supplies no numerical bound on the omitted
proton or finite-s tail. A fixed-scale matching statement does not license
changing the fixed-parameter differentiation path while varying mu with s.

## Reproducible symbolic-library branch problem

The original run_v1 failed at the OPTIONAL log-density filter-moment check.
Its direct SymPy 1.14.0 evaluation of the upper integral on (1,infinity)
added a spurious imaginary branch term, even though the displayed real
integrand is positive and integrable. All earlier source-translation checks
had passed before this assertion. The failed run and exact inputs remain.

Use the elementary real substitution x=1/y for this upper integral:

    int_1^infinity log(x)/[x(1+x)] dx
      =int_0^1 -log(y)/(1+y) dy.

Both halves then have the same positive real integrand. The corrected v2
script checks the Jacobian identity explicitly before integrating over
the finite interval. This resolves an integration-branch defect without
changing the source coefficients or the finite gluon matching proof.

## Self-review scope

The math-proofreading self-review covers this package's new derivation,
source transcriptions and addendum. PDF equation numbers and the distinction
between gamma_m=-dlogm/dlogmu and the inherited negative convention were
checked. No mathematical-token edit was made to the frozen derivation.
