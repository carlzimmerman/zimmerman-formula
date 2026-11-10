# QG1: quantum health of action (A) as an effective field theory (gate T2 of TOE0), 2026-11-10

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2,
Lstar 21.7 pc, mu_K* 8.890e6 Mpc^-1) and alt (1.1312e-10 m/s^2, 22.9 pc, 8.889e6 Mpc^-1), never pooled. The cold
component is cold dark energy (the clock's charge), never a particle. Not a LCDM lane. No download; literature named
below is PROVISIONAL (from memory, primary sources named, not fetched). Committed alone, before any script or number.
kappa = 1/2 FITTED; not theory closed.

Gate: T2 of `toe_2026_11_10/TOE0_gate_battery/FROZEN_CRITERIA.md` (8a99cb7c34). Action: (A) of
`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md` section 0, field equations E1-E4 there (certified):

    S = Int sqrt(-g) { [R - 2 Lambda + 2 mu_K^2 (Q-1)^2]/(4K) + P^m A_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m } + S_m
    W(p) = (a0^2/K)[-p/a0 - ln(1 - p/a0)],  F = [max(Pi,0)]^2/2,  Pi = D_m P^m,  gamma_L = K Lstar^2/2,  K = 4 pi G/c^2.

Parameters: a0 and Lstar per footing; Lambda from a0 by rule 4 (rho_DE = 4 a0^2/(c^2 G)); mu_K in two readings, 0 (form
B's standing clock, SCS1's primary) and mu_K* (the CMB-required value, SCS1 / KD1); the cold charge today
rho_c0 = I0/(2K) with KD1's I0 = 4.037e-8 Mpc^-2 (SCS1's constant), baryons rho_c/5.41, radiation from T_CMB = 2.7255 K
with N_eff = 3.046.

## 1. Step R: what the record already holds (quoted, not re-graded)

- **DOF and constraint algebra.** STANDING's fix-forward note (2026-10-23) and `reviews/v3_constraint_algebra_2026_10_23/`:
  for v3 (beta = eta = 0, P auxiliary, BS K(Q)) the Dirac chain stops at the secondaries, "(26 - 12 - 8)/2 = 3 DOF
  (2 tensor + the khronon scalar)", on Minkowski (mu_K 0 and > 0), FRW with BS dust and sheared backgrounds; "det A < 0
  everywhere except on the locus {mu_K = 0, x = 0, and k = 0 or gamma_L rho_P = -1}". Its own scope: "It does not test
  the sign or health of the reduced scalar Hamiltonian ..., the vector and tensor sectors, ... or the strong-coupling
  scale." It also reports near-degeneracy of the lapse operator at high background-P (the P3 loop factor <= 1.3e-3 is
  quoted there, not re-examined). The DSF-21 5-DOF count is withdrawn and does not apply to (A).
- **Causality.** AC18: tau-ordering PASS; light-cone causality FAIL on both footings (an instantaneous, tau-ordered,
  gauge-invariant influence through the leaf-elliptic Xi, about 1e-67 m/s for a ton moved at 1 m/s), needing nonzero
  charge AND MOND anisotropy. AZ39: NO VERDICT on the full branch; the uncharged GR branch is causal.
- **Linear dispersion, FRW.** AC2 (a different action, one canonical scalar as the clock): scalar-only FRW quadratic block
  healthy, (omega/H)^2 = E x^2 (1 + ell^2 x^2)/[E + (1 + E ell^2) x^2]; "A small positive sound speed does not establish
  weak coupling". It names strong coupling as not checked. AC2 is not (A); only its P-integration (the lapse-gradient
  term M_Pl^2 cY(k) k^2 alpha^2, cY = 1/(1 + Lstar^2 k^2/2)) carries over, because (A) has the same P.A - W - gamma_L F.
- **Classical stability, static clock.** SCS1: STABLE / STABLE around a point mass at mu_K = 0 (gravity coupled), with
  omega^2 = K G [(1 - K m) k^2 - mu^2 Qbar^2]/(mu^2 Qbar^2 + K m k^2), G = Qbar n_d + D.P, m = khat.J''.khat; at mu_K*
  JEANS-ONLY (growth at the local free-fall rate, bounded in k); "the clock resists being bent with a stiffness equal to
  its own charge density". SCS2: isolated discs STABLE / STABLE (D.P > 0 everywhere); external field NO VERDICT. Both are
  Newtonian-order, quasi-static metric, shift and momentum constraint dropped by 1PN counting.
- **STANDING two-loop a0 results (lines 486-523).** They are computed on the retired modified-inertia kernel
  K(Box_u/a0^2): a worldline-nonlocal action with a passive 0-dof frame and exact geodesy, a Herglotz measure and its sum
  rule. What transfers to (A): only the exact shift symmetry of the clock (tau -> tau + c; (A) contains tau only through
  d tau), which forbids a generated potential for tau to all orders. What does not: the multiplicative (sum-rule) leg,
  the tadpole leg (K(0) = 0) and the graviton k_perp leg, because each rests on the kernel K(Box_u) and on a frame with
  zero degrees of freedom, while (A)'s clock carries one degree of freedom and a0 enters through W(K|P|), not through a
  kernel of Box_u. So no record result bounds a0's renormalization in (A).

## 2. Method (frozen)

**M-A. Exact relativistic check on Minkowski (unitary gauge, sympy).** Scalar sector N = 1 + alpha, N_i = d_i B,
h_ij = (1 + 2 zeta) delta_ij in the general khronometric form
(M^2/2) N sqrt(h) [(1 - beta) K_ij K^ij - (1 + lambda) K^2 + R3 + alpha_a a_i a^i] + M^2 mu^2 alpha^2, M^2 = 1/(2K).
(A) is this form with beta = lambda = 0 (no term of (A) outside R depends on K_ij or on the shift; Q = 1/N, A_i = d_i ln N
and Pi = h^{-1/2} d_i (h^{1/2} P^i) in unitary gauge) and alpha_a(k) = 2 cY(k) after P is integrated out.

**M-B. Newtonian-order Stueckelberg reduction (the record's weak-field system, AC18 criterion B).** tau = t + sigma,
Xi = phi - sigma_dot + |grad sigma|^2/2 (= -(Q - 1) at this order), A = grad Xi, and

    L = -(1/2K) |grad phi|^2 - rho_b phi + P.grad Xi - W(K|P|) - (gamma_L/2) [(div P)_+]^2 + (mu^2/2K) Xi^2 .

Frozen coefficients (WKB) on each background; metric quasi-static (modes have omega/k << c); phi = psi. P is auxiliary
(no time derivative); it is integrated out mode by mode: M(k) = (H_P + gamma_L k k^T)^{-1}, H_P the Hessian of W(K|P|)
at Pbar, m(k) = khat.M(k).khat. With a = m k^2 + mu^2/K and b = k^2/K, eliminating phi gives

    L_2 = (1/2) Z sigma_dot^2 - (1/2) G k^2 sigma^2,  Z = a b/(b - a),  omega^2 = G k^2/Z,  G = n_d + D.Pbar .

The unmixed kinetic coefficient is Z_0 = a (before phi is eliminated). Approximations stated, not removed: 1PN terms of
the covariant Pi = div P - P.A (QX17 section 3, relative size <= U), background corrections of order gamma_L Pi_bar
(<= 1e-10), Hubble friction except in T2-Jeans below, graviton vertices (scale M_Pl).

## 3. Backgrounds (T2's list; L as T2 gives it)

| id | background | Abar, Pbar | G (charge) | Pi_bar | mu_K reading graded | L |
|---|---|---|---|---|---|---|
| MINK | Minkowski | 0, 0 | 0 | 0 | both (identical: G = 0) | 1 mm |
| FRW1100 | FRW z = 1100, local patch | 0, 0 | rho_c(z) c^2 | 0 (switch) | mu_K* | 10 Mpc comoving |
| FRW1 | FRW z = 1 | 0, 0 | rho_c(z) c^2 | 0 (switch) | mu_K* | 10 Mpc comoving |
| PM-2 / PM0 / PM2 | point mass 6e10 Msun on the law, x_N = g_N/a0 = 1e-2 / 1 / 1e2 | g from law S; K|Pbar| = a0 u/(1+u), u = g/a0 | phantom density | = G | 0 | 1 kpc |
| SUN | Sun at 1 AU (x about 6e7) | g_N + g*; screened K|Pbar| = g* = GM/Lstar^2 (QX17C hedgehog) | M/(2 pi Lstar^2 r) | = G | 0 | 1 AU |

The other mu_K reading on each row is computed and reported, not graded (the record has no single mu_K: FB1 / SCS1).
Reported, not graded: null points (point-mass profile down to x_N = 1e-8, and a generic null with field a0 s/l,
l = 10 kpc, G = a0/(K l)), with the size of the region where (ii) fails; an Earth-surface laboratory (Sun's and Earth's
hedgehogs, Abar = 9.8 m/s^2, L = 1 mm).

## 4. Graded criteria (T2's; tightened where marked, never loosened)

**(i) No ghost, no gradient instability.** On each row and footing: (a) every eigenvalue of H_P + gamma_L k k^T is > 0
(P auxiliary with positive algebraic cost); (b) the tensor mode has a positive kinetic term and the non-GR correction to
its omega^2 is below 1e-6 of k^2 at k = 1/L; (c) Z_0(k) > 0 at every k of the band and at k = 1e3, 1e6 x the band top
(no ghost); (d) no gradient instability: no k at or above the band top with omega^2 < 0 and |omega^2| increasing with k;
(e) a growth bounded in k is Jeans-type. On FRW rows it passes only if slower than H: the linear growth rate
f = dlnD/dlna of the cold component in the expanding background (its own Jeans term; baryons smooth for z > 1100,
comoving with it below) is < 1 at the row's z. On static rows a bounded growth is reported with its rate (T2 names only
ghosts and gradient instabilities).

**(ii) Strong coupling, Lambda_s L >= 10.** Lambda_s is defined by the vacuum-fluctuation ratio: at wavenumber k the
khronon's vacuum variance per ln k is s^2 = k^3/(4 pi^2 |Z| omega_eff), omega_eff = |omega(k)| (static rows) or
max(|omega|, H) (FRW rows); the linear fields follow (|dXi_1| = b omega_eff s/|b - a|, |dP| = |M khat| k |dXi_1|,
|dPi| = m k^2 |dXi_1|); |L_2| = (1/2)(|Z| omega_eff^2 + |G| k^2) s^2. Vertices (each field by its amplitude, each
derivative by k or omega_eff):
- V_tilt = m k^4 |dXi_1| s^2/2 (dP.grad(|grad sigma|^2/2), the clock's tilt);
- V_law3 = |f'''(0)| |dP|^3/6 and V_law4 = |f''''(0)| |dP|^4/24, f(t) = W(K|Pbar + t dPhat|) (at Pbar = 0 the
  non-analytic K^2 |dP|^3/(3 a0) and K^3 |dP|^4/(4 a0^2));
- V_dust3 = (mu^2/K) |dXi_1| k^2 s^2/2 and V_dust4 = mu^2 k^4 s^4/(8K);
- the switch: R_sw = (gamma_L k^2 m0/2) c_cross, m0 = khat.H_P^{-1}.khat, c_cross = 1 if Pi_bar = 0 (every fluctuation
  crosses the C^1 switch) else min(1, |dPi|/Pi_bar).
R(k) = max(V/|L_2|, R_sw), maximised over khat parallel, perpendicular and at 45 degrees to Pbar (or Abar).
k_x = the smallest k >= k_IR on a log grid (20 per decade, up to 1e40/L) with R >= 1; Lambda_s = k_x/sqrt(2 pi) (so
that a relativistic (d phi)^3/Lambda^2 or (d phi)^4/Lambda^4 operator returns Lambda exactly, KA6). If R(k_IR) >= 1, or
omega_eff = 0 on the band, Lambda_s = 0. k_IR: 1/r (PM, SUN), H/c physical (FRW), 1e-3/L (MINK).
PASS iff Lambda_s L >= 10 (T2's number).

**(iii) One loop.** Cutoff Lambda_c = min(Lambda_s, M_Pl) (T2's).
- Matter loops: structural statement checked by inspection of (A) (S_m has no tau, P, lambda): they generate only
  diffeomorphism-invariant functionals of g (Lambda, R, curvature squared), no A-term. Their effect on the law comes only
  through the Planck mass: if M^2 -> M^2 (1 + eps), the law becomes mu_eff(u) = 1 - 1/((1 + eps)(1 + u)), so
  Delta mu(x) = eps/((1 + eps)(1 + x)) (sympy identity, Lean).
- eps = N_eff Lambda_c^2/(16 pi^2 M^2) + eps_SM, N_eff = 121 (118 SM degrees of freedom + 2 graviton + 1 khronon, each
  with the conservative 1/(16 pi^2)); eps_SM = sum n_i m_i^2 ln(M^2/m_i^2)/(16 pi^2 M^2) over t (12), H (1), W (6),
  Z (3) (dimensional regularization, scheme-independent log).
- Khronon loop: one-loop zero-point energy E_0 = (1/2) Int_{k < Lambda_c} d^3k/(2 pi)^3 |omega(k)| (angle-averaged),
  as a function of the law's Pbar(x) at the row's fixed G, gamma_L, mu; Delta J'(g) = -dE_0/dg, Delta mu_khr(x) =
  K |dE_0/dg|/g.
- **Tightened:** |Delta mu(x)| <= 0.1 mu(x) (T2 has 0.1 absolute; 0.1 mu(x) <= 0.1 everywhere, so this is tighter) for
  every x in [0.01, 100] (x = g/a0, the law's argument), and |Delta a0/a0| = |Delta mu(0.01)|/mu(0.01) <= 0.10.
- PASS iff both hold. Where (ii) gives Lambda_s = 0 the loop expansion does not exist: (iii) NOT EVALUABLE, row FAIL on (ii).

**Row label:** PASS iff (i), (ii) and (iii) all pass; FAIL if any fails; OPEN if any is NOT EVALUABLE for a reason other
than a failed (ii). **T2 label:** PASS iff every graded row passes on both footings; FAIL if any graded row fails with every
known answer passing and every MUTATE twin biting; OPEN otherwise.

**T4 report (placed in T4, not part of T2's label).** Matter loops shift the vacuum energy by
sum_i (-1)^F n_i m_i^4/(64 pi^2) (one log, dimensional regularization) over the massive SM species, and by
N_eff Lambda_c^4/(16 pi^2) with T2's cutoff; a0 in W is not shifted by matter (structural). BREAKS if
|Delta rho_vac|/rho_DE >= 1 in either reading (the relation Lambda = 32 pi a0^2/c^4 then needs the cosmological-constant
tuning), HOLDS otherwise. Also reported: the matter cutoff at which eps reaches 1e-3 (where matter loops would move
mu(0.01) by 10 %).

## 5. Known answers (all must pass before any graded line is read)

- **KA1** GR graviton on Minkowski: second-order sqrt(-g) R for a TT wave h_xy = h_yx = h(t, z) gives
  (1/2)(h_t^2 - h_z^2) up to total derivatives (Fierz-Pauli; sympy, residual 0): omega^2 = k^2, positive kinetic term.
- **KA2** Blas-Pujolas-Sibiryakov khronon speed from M-A with general (beta, lambda, alpha_a):
  c_s^2 = (beta + lambda)(2 - alpha_a)/[alpha_a (1 - beta)(2 + beta + 3 lambda)] (sympy, residual 0) (BPS, JHEP 04 (2011)
  018; Jacobson-Mattingly spin-0 speed with c_13 = beta, c_2 = lambda, c_14 = alpha_a; PROVISIONAL).
- **KA3** Legendre check: max_P [P.A - W(K|P|)] = (a0^2/K)[u - ln(1 + u)] at 5 values of u (1e-30), and K J''(0) = 1
  (alpha_a = 2 at A = 0).
- **KA4** SCS1's closed form omega^2 = K G[(1 - K m)k^2 - mu^2]/(mu^2 + K m k^2) (Qbar = 1) from M-B (sympy, residual 0).
- **KA5** Pure dust (P sector off): omega^2 = (K n_d/mu^2)(k^2 - mu^2), Jeans rate sqrt(4 pi G rho) as k -> 0 (SCS1 KA2).
- **KA6** Strong coupling of a |grad phi|^3/a0 Lagrangian around a background gradient: for L = (2/3) M^2 g^3/a0
  (deep-MOND AQUAL), canonical expansion around gbar = x a0 gives Lambda_3^2 = 12 M a0 x^{3/2}; the frozen ratio method,
  run on L_2 = (1/2) Z (d phi)^2, L_3 = c_3 (d phi)^3 with these Z, c_3, returns Lambda_s = Lambda_3 to 1e-6 at
  x = 1e-2, 1, 1e2 (both footings).
- **KA7** Zero-point integrator: omega = c_s k gives c_s Lambda^4/(16 pi^2), omega = const gives omega Lambda^3/(12 pi^2),
  to 1e-8.
- **KA8** Growth ODE: Einstein-de Sitter f = 1 to 1e-8; flat matter + Lambda with Omega_m = 0.3, f(z = 0) within 1 % of
  Omega_m^0.55.

## 6. MUTATE twins (each must bite: the named criterion must change from PASS to FAIL)

- **M1** dust sign flipped (mu^2 -> -mu^2 in Z_0 and the dust vertices, background held): (i) on FRW1 (both footings).
- **M2** W sign flipped (H_P -> -H_P, background held): (i) on PM0 (both footings).
- **M3** tilt term dropped (G -> 0, background held): (ii) on PM0 (both footings).
- **M4** deep-MOND tuning broken by hand (eps += 1e-2): (iii) on PM0 (both footings).

## 7. Outputs

`qg1.py` (sympy + mpmath at 30 digits, single thread) writes `qg1.out` and `qg1.json`; `QG1_MUTATE=M1..M4` writes
`qg1_MUTATE_<arm>.out/.json`. Optional Lean file `QG1.lean` (identities that carry a verdict) with a false twin
`QG1_MUTATE.lean` that must fail. `RESULT.md` opens with T2's label per background and footing in one sentence.

## 8. Hand expectation (mine, before any script; recorded to be checked, not trusted)

The lead's: P auxiliary; alpha_eff about 2; khronon dust-like with c_s -> 0; gamma_L gives omega^2 ~ Lstar^2 k^4; no ghost;
low Lambda_s around Minkowski and null points; matter loops cannot make A-terms; mu's shape radiatively stable; the
a0-Lambda relation not. Mine differs in two places: (1) on Minkowski omega^2 = 0 exactly at every k (G = 0 and
beta = lambda = 0), not a k^4 branch, so Lambda_s = 0 there and T2 FAILS on MINK, both footings; with charge, gamma_L
gives omega^2 = G gamma_L k^2 (k^2, not k^4); (2) the charged rows (FRW, point mass, Sun) pass (ii) by many decades.
T4: BREAKS (electron alone about 1e31 rho_DE).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
