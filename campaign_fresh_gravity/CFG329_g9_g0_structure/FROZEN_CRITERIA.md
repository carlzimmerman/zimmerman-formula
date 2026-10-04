# CFG329 FROZEN CRITERIA: recipe gates G9 (matter conservation) and G0 (structural order) on the chassis

Frozen before any computation. Chassis = the filtered C-H/K khronon completion (L340 + FP2/FP5 core):
C-H (ACTION.md:95-106: R - 2Lambda, 2|DU - a|^2, 2 alpha^2 q(|D W_b|^2/alpha^2), heat pair L(dW/dz - Delta_h W),
lambda_0(W_0 - U)) + alpha_c a^2 - c_2 (K - <K>_Sigma)^2, beta = 0, nu_mono kernel, heat-filter scale xi.
Matter: S_m[g, psi] as written in ACTION.md (point masses + Maxwell, no U/tau/W/L coupling). kappa = 1/2 is FITTED and
plays no role here.

## Definitions
- **Scalar-density test (Noether II).** For a Lagrangian density 𝓛 and an arbitrary vector field xi^mu, residual
  R_xi = delta_xi 𝓛 - d_mu(xi^mu 𝓛), with delta_xi g = Lie derivative, delta_xi(scalar) = xi.d(scalar). R_xi = 0
  identically <=> the generalized Bianchi identity 2 nabla_mu E^mu_nu = sum_fields E_phi d_nu phi holds off shell.
  Evaluated in a plane-symmetric reduced sector (metric -A dt^2 + 2B dt dx + C dx^2 + D(dy^2+dz^2), all fields of
  (t, x)), xi = (xi^t(t,x), xi^x(t,x)), with exact symbolic derivatives and numerical evaluation at >= 3 random points
  with concrete smooth fields (mpmath, 40 digits). "Zero" = |R| < 1e-25 x (scale of the individual terms).
- **Heat filter in the test.** At each z the heat pair is a local spacetime scalar Lagrangian in the scalars W_z,
  (dW/dz)_z, L_z; one z-slice with W, Wz, L independent represents it (spacetime diffeos act at fixed z).
- **Leaf average in the test.** -c_2 (K - F(tau))^2 with F an arbitrary function of the clock (polynomial, symbolic
  coefficients); varying F leaf by leaf gives F = <K>_Sigma (N-weighted). The sqrt(h)-weighted average is also a
  covariant functional of (g, tau) on closed leaves; the verdict does not depend on the choice.
- **Extra term.** Any non-zero R_xi; its coefficient is the extra term in nabla_mu T^mu_nu on the other fields' shell.
- **Weak-field order (recipe G0).** Phi -> eps Phi (all potentials, U, W; rho -> eps rho); order of every term.
- **Time order.** Highest d_t power of each field in each field equation; in unitary gauge (tau = t) both from the
  nonlinear reduced Lagrangian and from the FP2-derived quadratic block (det M(omega, k) degree in omega).

## Decision rules
**G9**
- PASS: (a) the matter action depends on g and matter fields only; (b) R_xi = 0 for the full chassis density
  (all terms incl. heat slice + leaf-average proxy); (c) the matter identity nabla_mu T^mu_nu + E_psi d_nu psi = 0
  holds off shell; (d) linear check: the clock (Stueckelberg pi) equation equals a combination of the metric equations
  plus d_t rho_s + j_s, so nabla T = 0 is implied on shell. Then nabla_mu T^mu_nu = 0 follows exactly.
- CONDITIONAL: (a)-(d) hold for closed leaves but a term needed on the record's backgrounds (isolated R^3 leaves, IR
  subtraction, frozen filter or frozen <K>) gives a non-zero extra term, bounded below 1e-3 of the matter force on
  solar-system, galaxy and cosmology backgrounds.
- FAIL: R_xi != 0 for the action as written, or an extra term >= 1e-3 on any of the three backgrounds.
**G0**
- PASS: (i) the weak-field ordering needs no cancellation between terms of different eps order; (ii) unitary-gauge
  Lagrangian has no second time derivatives and no time derivatives of N, N^i, U, W, L, lambda_0 (manifestly
  second order); (iii) det M(omega, k) of the derived scalar block has omega-degree 2 (one scalar mode, no
  Ostrogradsky pair) with the filter (C -> e^{-xi^2 k^2} C) and leaf average included; (iv) the momentum constraint is
  preserved (spatial Noether identity, R_xi = 0 for leaf-preserving xi) and the second-class lapse/U/W/L/lambda_0
  equations are elliptic leaf equations solvable on the record's backgrounds.
- CONDITIONAL: (i)-(iii) hold but (iv) holds only where the leaf operator is invertible, or depends on non-local terms
  not proven nonlinearly. A higher time order in a frame tilted against the foliation (the instantaneous mode) is
  reported and is not by itself a FAIL.
- FAIL: any unitary-gauge equation above second order in time, omega-degree > 2, or a required cross-order cancellation.

## Controls (all must behave as stated, else the lane is INCONCLUSIVE)
1. GR: contracted Bianchi nabla_mu G^mu_nu = 0 at random points of the reduced sector; FRW + dust: nabla T = 0 <=>
   rho a^3 = const.
2. Plain khronometric (no C-H, no filter, no leaf average; alpha_c a^2 - c_2 K^2): R_xi = 0 (known result); its clock
   equation is the Noether combination of the metric equations (BPS 2011).
3. Power check: a non-covariant term (c (d_t U)^2 in coordinate t) gives R_xi != 0.
4. MUTATE (env CFG329_MUTATE=1, separate outputs *_MUTATE.*): matter Lagrangian multiplied by e^{beta U} (explicit
   non-minimal coupling to the chassis scalar). G9 must flag it: matter identity residual = -(dL_m/dU) d_nu U != 0,
   G9 verdict not PASS, exit code 1.
Bounds use record numbers: a0 = 9.36e-11 / 1.13e-10 m s^-2, H0 = 67.36 km/s/Mpc, xi floor 0.031-0.049 pc,
c_2 in [7.29e-3, 0.0667], alpha_c in [9.6e-14, 3.2e-9]. At most 4 processes.
