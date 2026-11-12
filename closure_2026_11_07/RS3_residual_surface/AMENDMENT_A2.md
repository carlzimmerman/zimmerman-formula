# RS3 AMENDMENT A2 (post-freeze, after a smoke test; committed before the graded run)

Criteria 8158e4645f, A1 5123eda762. Disclosure: a smoke test of the fitting code on the canonical footing, four pairs
((g_N, sigma), (g_N, Sigma_b), (rho_b, rho_b/rho_DE), (g_N, x_e)), showed that the free 2D isotonic family of section 4
(I) fits ANY values on an antichain: with mixed orientation (increasing in one variable, decreasing in the other) two
positively correlated variables leave few or no comparable rows, so the QP has few or no constraints and chi^2 -> 0
((rho_b, rho_b/rho_DE) and (g_N, Sigma_b) reached chi^2 = 3e-26 with ZERO order constraints; (g_N, sigma) reached
chi^2/N 0.22 with 222 free values). That is a true property of monotone functions of two variables, not a code bug,
and it makes family (I) unable to fail: the shuffled-label MUTATE could not bite, so the frozen rules would return NO
VERDICT for a reason unrelated to the physics. The brief's cap "<= 6 free numbers" is read here as applying to every
fit family. Smoke-test numbers seen (canonical only): quadratic (g_N, sigma) chi^2/N 2.34, worst Coma UDGs z +6.33;
(g_N, Sigma_b) 3.33, SPARC z -10.2; (rho_b, rho_b/rho_DE) 2.91, UDGs +6.08; (g_N, x_e) 0.74, UDGs +2.37 (NO VERDICT on
X-COP, groups). No other pair, footing, MUTATE or LOO number was computed.

Changes:
1. Family (I) is replaced by (G) GRID6: a monotone surface with 6 free numbers, the values at a 2 x 3 (or 3 x 2) knot
   grid with bilinear interpolation; knots at min / max of the first variable and min / median / max of the second
   over the fitted rows (both assignments tried); grid values constrained monotone in the orientation (bilinear
   interpolation of monotone knot values is monotone in each variable). Duplicate knots are merged. Gating families:
   GRID6 and the 6-number quadratic (P), each with 4 orientations. Free isotonic (I) is still run and REPORTED, never
   gating.
2. Exactness of (P)'s constraint: the gradient of the quadratic is linear in (u, v), so the sign constraints "at every
   row" are imposed at the rows on the convex hull of the fitted (u, v), which is equivalent. A primal SLSQP fallback
   is used when the dual NNLS does not converge.
3. KA4's planted pair (g_N, Sigma_b) is identically degenerate (g_N = pi G Sigma_b for enclosed quantities), as are
   (rho_b, rho_b/rho_DE). KA4 / KA4n plant instead on (g_N, sigma): y = 0.5 + 0.4 u - 0.3 v, u = log g_N, v = log
   sigma, standardized. Degenerate pairs are run and flagged as one-variable fits.
Everything else (rows, variables, line, MUTATE, LOO, labels) is unchanged.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
