# BI1 RESULT: FAIL at B0 / FAIL at B0 on all carriers (criteria 91e81dcd76; A1 f661cc7517; A2 521a16260c; correction below)

## Correction (post-result, disclosed): A2's conditional PASS is WITHDRAWN

**What was wrong.** A2's "Yukawa-smoothed" reading estimated the reaction force as (dL/df)(df/dXi)(dXi/drho) x l^2 / (2 R_W^2) / R_W.
That dilutes it by the window twice. The orchestrator's checked identity (dL/df = g_b g_chi / (4 pi G), so a_extra = g_b g_chi |df/dr|
/ (4 pi G rho_chi)) has no such dilution. The conditional PASS rested on the diluted reading.

**Recomputed** (`bi1_a2b.py`) with an actual Helmholtz-smoothed Xi = Psi_kin profile (spherical Yukawa convolution around SS1 halos;
field dispersion 60 km/s outside the halo, stated), at R_W x 0.5 / 1 / 2:

| system | canonical, R_W x 1 | alt, R_W x 1 |
|---|---|---|
| group (M_b 5e12) at 102 / 400 kpc | 6.0e-13 / 8.2e-14 m/s^2 = 0.0064 / 0.00088 a0 = **0.016 / 0.0047 of the law's g** | **0.0084 / 0.0023 of g** |
| group at R_W x 0.5 | 0.040-0.052 of g | |
| group at R_W x 2 | 3e-4 to 1e-3 of g | |
| L* (100 / 250 / 1000 kpc) | <= 6e-7 of g | |

**Line 1e-3 of g: FAIL at the group on both footings.**
- The Psi_kin-only Xi gives f of only 0.02-0.08 in the group, against the specification's intended 0.30-0.55. Adding the
  Psi_coll term raises f, and with it the force, so the FAIL is robust.
- The orchestrator's own figures for a 2e13 group (0.009-0.105 a0 at 102-400 kpc) are larger still.
- The force is borderline against a0, not a wall, but it is 2-50x over the frozen 1e-3-of-g line.

**The open defect (orchestrator, concurred).** One Xi formula must be large on the linear web, small around galaxies out to 3 Mpc,
and large in groups. The source set the web value by hand through (H / H0)^3 / (1 + Psi_coll^2). This is the record's non-monotone-key
wall (HX1) again.

**Label: FAIL at B0 on all carriers, both footings.**
- (i): a fifth force.
- (ii): momentum non-conservation.
- (iii)-generic: the switch force is 0.3-21 % of g.
- (iii)-explicit: ghost-free with local fields, but the reaction at groups is 0.2-1.6 % of g (line 0.1 %). The (1 + f^2) G
  baryon coupling (2G at recombination) and the missing A . grad f term in the claimed Phi_chi equation are recorded.
- No usual gates run.

---

# A2 text as first written (its conditional PASS is withdrawn above)

## A2 update: carrier (iii) as explicitly specified (added after the earlier results; disclosed in AMENDMENT_A2.md). Script `bi1_a2.py`.

**(1) Field equations (sympy, 1D reduction of the stated L).**
- The Phi equation matches the claim.
- **The Phi_chi equation does not.** The Euler-Lagrange equation is lap Phi_chi = 4 pi G (rho_chi + f rho_b) + (grad Phi - f grad Phi_chi - grad Phi_Q) . grad f.
  The claim drops the last term, which vanishes only where grad f = 0.
- **Couplings at constant f** (Fourier): Phi is sourced by (1 + f^2) rho_b + f rho_chi; Phi_chi by rho_chi + f rho_b. The cross
  coupling is symmetric (Newton's third law kept), but **the baryon-baryon coupling is (1 + f^2) G** wherever f is not 0.
  - At recombination (H / H0)^3 is huge, so Xi is huge and f -> 1 (with Psi_coll -> 0): the baryons' self-gravity is 2G, and the
    component sources the baryons' potential at full weight.
  - That is a direct change to the primary CMB's baryon driving. It is not the "standard cold" early universe claimed, and it must
    be graded at the CMB gate.
- **Ghost:** the gradient energy is a sum of squares; the Hessian determinant is 1/(16 pi^2 G^2) > 0 for every f. No ghost.

**(2) Helmholtz fields with an action (mu_0).**
- Psi's equation: mu_0 (R_W^2 Psi'' - Psi + c_1 rho_chi) + (dL_g/df) F'(Psi) = 0.
- Horn A (Helmholtz-dominated, large mu_0): the coupling mu_0 c_1 Psi rho_chi gives a Yukawa self-force on the component of at
  least a_extra.
- Horn B (small mu_0): Psi stops being the specified Helmholtz field, or momentum is violated by a_extra.
- **No mu_0 escapes "force >= a_extra".** The source's "inescapable trade-off" is right in form. Whether it is fatal depends on how
  large a_extra is.

**(3) Numbers** (record halos: SS1 primary halo; R_W = v_stiff / (2 H0); Xi from Psi_kin only, the channel through which the
reaction lands on the component):

| system | Xi_local | a_extra unsmoothed | a_extra Yukawa-smoothed | smoothed / law's g | source's claim |
|---|---|---|---|---|---|
| L* at 250 kpc (canonical) | 4e-4 | 3.0e-19 | 2.4e-21 | 6e-10 | 4.6e-12 |
| group (M_b 5e12) at 400 kpc (canonical) | 3.1 | 1.3e-13 (about 6e-3 of g) | 2.7e-15 | 1.2e-4 | 2.6e-9 |

Alt is similar: 2.0e-19 / 1.6e-13 unsmoothed; 1.1e-4 of g smoothed at the group.

- **The source's numbers do not follow from its own formula** with the record's halos: they are 10^4-10^7 too large.
- Its "21 a0" uses a0 = 1.2e-10. In the record's footings 2.6e-9 m/s^2 is 27.8 / 23.0 a0, and 4.6e-12 is 0.049 / 0.041 a0.
- Near isolated galaxies Xi is tiny and f proportional to Xi^2, so the reaction vanishes by design.
- At the group boundary the smoothed reading is under the 1e-3 line. The unsmoothed upper bound (about 6e-3) is over it.

**B0 status.**
- Carrier (iii)-explicit uses local Helmholtz fields (so conservation can be carried), is ghost-free, and its Psi_kin reaction is
  <= 1e-3 of the law's g in the smoothed (faithful) reading at the evaluated points: **PASS, CONDITIONAL**.
- **Conditions, stated:**
  - the Psi_coll channel is NOT EVALUATED (rho_b,crit is defined for M_b,min 1e9 and then 1e8 in the same answer; the reaction
    through Psi_coll lands on the baryons);
  - the unsmoothed bound at groups exceeds the line;
  - only two radii were evaluated.

**Per the frozen rule the usual gates (KiDS, SPARC, groups, X-COP, Bullet, web, CMB) must be frozen in a further amendment before
any of their numbers. They are NOT RUN here.** The first one to run is the CMB primary under the (1 + f^2) G baryon coupling with
f -> 1 at recombination: expected to be decisive.

**Reported, not graded:** the source's web unscreened 12.5 % (sigma8 +6.5 %) is unchecked here. Its kill test (small spirals 1.8-2.4
Mpc from rich clusters, Xi about 6.5) is recorded as its prediction.

---

# Earlier label: FAIL at B0 / FAIL at B0 on carriers (i), (ii), (iii)-generic (A1)

## A1 update: carrier (iii), bimetric (added after the first result; disclosed in AMENDMENT_A1.md)

**Setup (sympy).** K^-1 = [[1, f], [f, 1]] gives lap Phi = 4 pi G (rho_b + f rho_chi) and lap Phi_chi = 4 pi G (rho_chi + f rho_b).
Self-gravity stays standard; the cross weight is symmetric, so Newton's third law holds.

**(a) Ghost and conservation.**
- The eigenvalues of K are 1/(1 - f) and 1/(1 + f): **ghost-free iff |f| < 1**. f -> 1 is the single-metric limit.
- With f = f(Xi(x)), the field stress has d_j T^ij = -(dL/df) d_i f, with dL/df = g_Phi g_Phi_chi / (4 pi G) at f = 0.
- That is conserved only if Xi is a dynamical local field carrying it. The unswitched bimetric class (constant f; AX1's grading)
  has no such term: the switch adds a new scalar coupled at gravitational strength.
- The record's Xi, a Yukawa-smoothed dispersion functional, is not a field.

**(b) Size of the switch force.** a_switch = |grad Phi| |grad Phi_chi| |grad f| / (4 pi G rho_chi) for an L* galaxy (SS1 primary
halo; R_W 1.5 Mpc):

| r (Mpc) | 0.1 | 0.3 | 1 | 3 |
|---|---|---|---|---|
| a_switch (m/s^2) | 7.4e-14 | 7.2e-13 | 8.3e-15 | 9.0e-16 |
| / law g (canonical) | 0.0069 | **0.21** | 0.008 | 0.0026 |

Alt: 0.0063 / 0.19 / 0.0073 / 0.0024. It exceeds the 1e-3 line at every radius: **B0(iii) FAIL**. The force is largest where the
component leaves its halo for the mean-density field (rho_chi drops while both gradients are still large).

**(c)** No carrier passes B0, so the usual gates do not run.

**Label: FAIL at B0 on all three carriers, both footings.**
- (i): a fifth force of 1e5-1e6 x g.
- (ii): broken momentum conservation (0.63 Mpc self-displacement) and a Bianchi violation of 5-47 % of g.
- (iii): ghost-free, but conserved only with a new local Xi field, and that field's force on the component is 0.3-21 % of the
  law's g.

Files: `AMENDMENT_A1.md`, `bi1_a1.py` -> `bi1_a1.json` / `.out`.

---

# Original result (carriers (i) and (ii))

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
