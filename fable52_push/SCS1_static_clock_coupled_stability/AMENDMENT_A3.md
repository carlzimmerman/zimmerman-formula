# SCS1 AMENDMENT A3 (post hoc; committed alone, before the final route-2 run)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.** Route 2 keeps an eigenpair only if the clock perturbation carries part of its eigenvector:
|zeta|/|v| > 1e-4, where zeta = chi - phi is proportional to pi. Before this amendment the bound was 1e-8. The amendment A2
tolerance stays. Nothing else changes: no line, grid, known answer, MUTATE arm or label rule.

**Why.** In the substitution pi = (chi - phi)/(i omega), the pencil (C, -A) has a family of modes with zeta = 0, one per
interior node. For these modes lambda is 0/0: C vanishes on them because C acts on zeta only. They are not clock modes, and
their eigenvalues are rounding.

**What was seen first (post hoc).** Under A2, one row (canonical, log M_b 9.4, l = 0, N = 800) still had an eigenvalue of
-3.1e-20 kpc^-2. Its eigenvector has |zeta|/|v| = 2.3e-8, just above the old bound. In that solve and in two others
(log M_b 10.9, l = 2, N = 800; log M_b 10.45, l = 1, N = 400) the two families are five decades apart:
- The physical family has exactly one mode per interior node (796, 796 and 396), every one with |zeta|/|v| >= 2.1e-3.
- The null family has |zeta|/|v| <= 2.3e-8.
- Every physical eigenvalue is positive and inside the local WKB band.

The partial runs before A2 and A3 are kept: scs1_radial_run1_partial.out and scs1_radial_run2_partial.out.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
