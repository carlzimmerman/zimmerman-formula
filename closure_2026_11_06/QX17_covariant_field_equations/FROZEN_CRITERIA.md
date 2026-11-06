# QX17_covariant_field_equations: FROZEN CRITERIA (committed alone, before any script)

**Owner 11-06:** "i need all the field equations today". The record (EQUATIONS_IN_ORDER.md, V3_FULL_PICTURE §2,
PAPER68 §3) has only the static and weak-field limits. This lane writes the **full covariant Euler-Lagrange set** of the
adopted (scoped) v3s action and checks every equation against a direct variation. Adopts nothing. kappa = 1/2 FITTED.
Not theory closed. Lane id checked free (`ls closure_2026_11_06 | grep QX17`, `git log --all | grep QX17`: empty).

## Action (operative Legendre form, V3W/H4; c = 1, K = 4 pi G)

    S = Int sqrt(-g) { [R - 2 Lambda + 2 mu_K^2 (Q-1)^2]/(4K) + P^mu A_mu - W(K|P|) - gamma_L F(Pi) + lambda n^mu P_mu } + S_m

Q = sqrt(-g^{mn} d_m tau d_n tau), n_m = -d_m tau/Q, h = g + n n, A_m = -h_m^n d_n ln Q, Pi = D.P,
F(Pi) = [max(Pi,0)]^2/2, lambda a multiplier for n.P = 0. Note: PAPER68's printed form (J(Y) plus an independent P with
only (D.P)^2) leaves P decoupled; the Legendre form is the one every lane solved. At gamma_L = 0 eliminating P returns
-J(Y)/(2K) with J = J_x (check K0).

## Checks (all must pass; PASS = relative residual <= 1e-10 at every test point)

- **K0** Legendre: max_P [P.A - W(K|P|)] = (a0^2/K)[u - ln(1+u)], u = |A|/a0, stationary K|P| = a0 u/(1+u). sympy exact.
- **K1** P equation, **K2** khronon (tau) equation, **K3** metric equation (non-GR stress tensor): the closed forms in
  RESULT.md vs. Euler-Lagrange derivatives of the Lagrangian density taken by sympy on jet variables, evaluated on random
  polynomial fields in 2+1 dimensions (1+1 is degenerate: h_mn = P_m P_n/|P|^2 there) with n.P = 0 imposed by
  P = h.V, on the Pi > 0 branch (Pi < 0: gamma_L terms vanish identically, F in C^1). At least 3 random configurations.
- **K4** FRW: from the covariant forms, P = 0 gives Q-bar = 1 + const/a^3 and rho, w equal to C4 K7's
  (rho = I0(1 + w0/a^3)/(8 pi G a^3), w = w0/(w0 + a^3)).
- **K5** Static weak field: T_mn n^m n^n of the P sector = Pi + gamma_L F(Pi) - so leading order rho_tau = D.P, matching
  the record's Poisson source.
- **MUTATE**: flip the sign of the Pi_+ d ln Q term in the metric equation and of the lambda term in the tau equation;
  K1-K3 must then FAIL on the mutated pieces.

Labels: CERTIFIED (all pass), FAIL (any closed form disagrees; the sympy-variation form is then reported instead).
