# BI1 RESULT: FAIL at B0 / FAIL at B0 (criteria 91e81dcd76)

Variant R: the cold component's coupling to the metric felt by baryons and photons is switched by f_clus(Xi). TEST lane,
quarantined. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Both carriers fail covariant consistency, so no later gate
runs, as frozen.

## (i) f in the component's matter action, S = -integral f(Xi) m c dtau

**sympy, the Euler-Lagrange equation of L = -f(x) m c^2 sqrt(1 + 2 Phi / c^2 - v^2 / c^2):**

  a = -c^2 (f' / f) - Phi' + (f' / f)(v^2 - 2 Phi) + O(1/c^2)

- The extra force is **-c^2 grad ln f**. It points toward low f, so **into the galaxies** where f -> 0.
- MUTATE M1 (f constant): a = -Phi'. The extra force vanishes, as it should.

**Size.** With f varying by O(1) over R_W = 1.5 Mpc, c^2 |grad ln f| = **1.9e-6 m/s^2**. That is 1.8e5 / 5.6e5 / 1.9e6 / 5.7e6
times the law's g at 0.1 / 0.3 / 1 / 3 Mpc around an L* galaxy (canonical; alt 1.6e5-5.2e6). Line 1e-3: **FAIL by 8-9 orders of
magnitude.**

**Conservation.**
- nabla_mu T_chi^{mu nu} = -rho c^2 d^nu f, so total conservation needs a field Xi with nabla_mu T_Xi^{mu nu} = +rho c^2 d^nu f.
- That is a mediator coupled at the strength of the component's rest energy, i.e. a fifth force of order c^2 / R_W.
- A Yukawa-smoothed dispersion functional has no local stress tensor at all.

## (ii) f only in the component's active gravitational mass

**sympy pair.** The net force on a galaxy + component pair is G M_g m_c (f - 1) / d^2. It is zero only for f = 1 (MUTATE M2), and
the centre-of-mass self-acceleration is a_cm = G M_g m_c (f - 1) / ((M_g + m_c) d^2).

With f = 0 around an isolated L*:

| reading | a_cm at 0.1 / 0.3 / 1 Mpc (m/s^2) | 10 Gyr displacement |
|---|---|---|
| full-share clump (5.41 M_b) | 9.4e-13 / 1.0e-13 / 9.4e-15 | |
| 10 % dipole asymmetry | 3.9e-13 / 4.4e-14 / 3.9e-15 | **0.63** / 0.07 / 0.01 Mpc |

**Line: 0.1 Mpc at epsilon 0.1. FAIL**, by 6x at 0.1 Mpc. The galaxy self-propels away from its own lopsided halo.

**Field form.** With the source rho_b + f rho_c, the Bianchi identity needs T_c^{mu nu} d_mu f = 0. sympy with
T = diag(rho c^2, rho sigma^2 x 3) gives (rho c^2 d_0 f, rho sigma^2 grad f).
- **Static pressureless dust escapes** (sigma^2 = 0, d_t f = 0: all four components vanish).
- **The dispersion term** sigma^2 |grad f| = 4.9e-13 m/s^2 (sigma 150 km/s, R_W 1.5 Mpc). That is 0.05 / 0.14 / 0.47 of the law's
  g at 0.1 / 0.3 / 1 Mpc (alt 0.04 / 0.13 / 0.43): **FAIL** (line 1e-3).
- **The time term** d_t f is about 1 / (2 Gyr) = 7.3 H0. The component's active mass changes by order itself per collapse time
  (about 2e11 Msun / Gyr for an L* share), which the Bianchi identity forbids without a compensating field carrying rho c^2.

## Beside the record's dead keys (reported)

- **HX1 (dispersion-keyed boost, NO LADDER).** Xi is a smoothed sigma against v_stiff. HX1 found that the needed boost is not one
  function of sigma: ellipticals at 170-260 km/s need B 3-4, groups at 470 need 1.1-1.5, clusters at 1000 need 3-4. A
  sigma-keyed f_clus (0 in galaxies, 0.30-0.55 in groups and clusters) faces the same non-monotone need on the component side.
  The smoothing over R_W changes which sigma is used, not the ladder.
- **I5 (NA1, disformal bulk-motion selector, dead by reduction).** Every local scalar reduces to {gamma, X, p / rho}. Xi escapes
  that reduction only by being non-local. Non-locality is exactly what B0 shows has no stress tensor: the escape from I5 is the
  failure here.

## Reading

Switching the component's gravitational coupling by an environment variable fails covariance both ways it can be carried.
- In the action, it is a fifth force of order c^2 / R_W, a million times gravity, pushing the component into galaxies.
- In the active mass only, it breaks momentum conservation: halos self-propel galaxies by about 0.6 Mpc in 10 Gyr at a 10 %
  asymmetry, and a dispersion-supported halo violates the Bianchi identity at 5-50 % of the law's g.
- Only static cold dust escapes, which a virialised halo is not.

**What a repair would need:** a dynamical Xi field with its own local action, coupled at the component's rest-energy scale, whose
force is screened to 1e-6 of c^2 / R_W inside 3 Mpc of every galaxy. That is a new screened fifth force, not a coupling switch.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Script: `bi1.py` (sympy + numbers).
- Outputs: `bi1.json` / `bi1.out`.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
