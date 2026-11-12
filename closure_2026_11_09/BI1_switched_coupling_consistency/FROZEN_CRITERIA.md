# BI1 (switched coupling of the cold component, the outside source's variant R): FROZEN CRITERIA, committed alone before any script or number

TEST lane, quarantined; registered RUNNING by the orchestrator (owner "Yes, check it"). Adopts nothing. kappa = 1/2 FITTED; not
theory closed. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10), never pooled. Symbolic first (sympy), then numbers.

## Variant R, as relayed

- A cold component in standard cold halos (mass conserved, standard seeds and clustering).
- Its contribution to the metric felt by baryons and photons is multiplied by f_clus(Xi).
- Xi is a non-local variable: the Yukawa-smoothed velocity dispersion over R_W of 1.5-2 Mpc, compared with v_stiff, times a
  collapsed-fraction factor.
- f -> 0 around isolated galaxies (where the law's phantom acts), f -> 1 on the linear web, 0.30-0.55 in groups and clusters.

## Gate B0: covariant consistency (decides the label before anything else)

**Carrier (i): f in the component's matter action, S = -integral f(Xi) m c dtau.**
- sympy derives the Euler-Lagrange equations of a point particle with mass f(x) m in a weak static metric
  (Phi, ds^2 = -(1 + 2 Phi / c^2) c^2 dt^2 + dx^2) to O(v^2 / c^2).
- It reports the extra force term (expected -c^2 grad ln f, with its direction relative to low f) and its size for f varying by
  O(1) over R_W = 1.5 Mpc, against the law's g_N at 0.1-1 Mpc for an L* galaxy (M_b 8e10).
- It states what Xi's stress tensor must supply for nabla_mu T^{mu nu}_total = 0: a term balancing rho c^2 grad ln f.
- **B0(i) FAIL** if the extra force exceeds 1e-3 of g_N anywhere at 0.1-3 Mpc and Xi is not a field whose stress tensor carries
  it. A non-local smoothing functional is not a field.
- MUTATE M1: f constant gives an extra force of exactly 0.

**Carrier (ii): f only in the component's active gravitational mass (passive mass unchanged).**
- sympy, Newtonian pair (galaxy M_g, component clump m_c at distance d): the net force on the pair and the centre-of-mass
  self-acceleration a_cm = G M_g m_c (1 - f) / ((M_g + m_c) d^2).
- Field form: the Einstein / Poisson equation with the source rho_b + f rho_c requires nabla_mu (f T_c^{mu nu}) = 0, i.e.
  T_c^{mu nu} d_mu f = 0.
- **Static pressureless dust escapes:** T^{0 nu} d_0 f = 0 when d_t f = 0, and T^{ij} = 0.
- **The terms that do not vanish:**
  - the halo dispersion, T^{ij} = rho sigma^2 delta^{ij}, gives rho sigma^2 d_j f;
  - the time term rho c^2 d_t f as Xi evolves with collapse.
  - Each is evaluated as an anomalous force density, compared with rho g, at 0.1-1 Mpc for an L* galaxy (sigma 150 km/s,
    d_t f about 1 / t_collapse of 2 Gyr, grad f about 1 / R_W).
- Numbers: a_cm for a full-share clump (5.41 M_b) and for a dipole asymmetry epsilon = 0.1 of the share at 0.1, 0.3, 1 Mpc, in
  m/s^2, with the Hubble-time displacement.
- **B0(ii) FAIL** if any non-vanishing violation term is >= 1e-3 of rho g at 0.1-1 Mpc, or if a_cm over 10 Gyr displaces a galaxy
  from its component by more than 0.1 Mpc (the record's DB1 / Bullet offset scale) for epsilon = 0.1.
- MUTATE M2: f = 1 gives zero violation and a_cm = 0.

**Label.**
- If both carriers FAIL B0: FAIL at B0, with the numbers.
- If either PASSES: the usual gates (KiDS, SPARC, groups, X-COP, Bullet, web) under that carrier, frozen in an amendment before
  any of their numbers.

## Reported beside (no grading)

- **HX1:** the record's dispersion-keyed phantom boost (NO LADDER: ellipticals at sigma 170-260 need B 3-4, groups 1.1-1.5,
  clusters at 1000 km/s about 3-4). The lane states whether Xi, a smoothed sigma against v_stiff, faces the same non-monotone need.
- **I5 (NA1):** the disformal bulk-motion selector, dead by reduction: every local scalar reduces to {gamma, X, p / rho}. The lane
  states whether Xi escapes by non-locality, and what non-locality costs (B0).

## Hand estimates

- **(i):** the extra acceleration c^2 |grad ln f| is about c^2 / R_W = 9e16 / 4.6e22, about 2e-6 m/s^2, against g_N of about
  1e-12 at 1 Mpc: 10^6 x gravity, pointing toward low f, i.e. into galaxies. FAIL.
- **(ii):**
  - a_cm for a full-share clump at 0.1 Mpc is about 1e-12 m/s^2, and over 10 Gyr that displaces Mpc-scale.
  - The dispersion term sigma^2 / R_W is about 5e-13 m/s^2, comparable to g at 0.5 Mpc.
  - The time term rho c^2 d_t f is an active-mass non-conservation of order the whole component mass.
  - FAIL.
- **Expected: FAIL at B0 on both carriers.**

## Operational

- Files: bi1.py (sympy + numbers), bi1.json / .out, RESULT.md.
- Small outputs; explicit-path commits via a sparse temporary worktree.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
