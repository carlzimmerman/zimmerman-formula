# CFG312: CFG294's lapse-kernel condition W <= 0 for realistic data

**Verdict (frozen rule): PASS-WITH-EXCEPTIONS (scoped).** The verdict covers CFG294's condition C4 only. CFG294's
overall verdict stays CONDITIONAL, because A1–A5 are still assumed. This is not an unconditional well-posedness claim.

The criteria were frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit 030106e11. Results: 16/16 checks pass
(13/13 load-bearing). The MUTATE run fails as required (15/16, rc = 1). Lean: 7 theorems, standard axioms only; the
Lean MUTATE file does not compile.

## Bottom line

- **The homogeneous class.** On the class where CFG294 derived W (Bianchi-I flat leaves, C-H sector absent), the
  condition W <= 0 holds for all realistic matter. With the chassis's own content (V = 0, Lambda > 0) it holds strictly:
  W < 0. The sufficient conditions are:
  - rho >= 0, rho + p >= 0 (null/weak energy condition) and c_s^2 >= 0;
  - |u| below a threshold that depends on the matter, against real peculiar velocities of at most 1e3 km/s:
    - 0.7071 c for any such fluid;
    - 0.8165 c for dust;
    - 0.8416 c for radiation.
- **Static bound systems.** On these (Solar System, galaxy, cluster, neutron star) CFG294's pointwise W is the wrong
  test.
  - The correct local lapse potential is W_loc = (K.K − lambda K^2) + (alpha_c − 1/2) Delta ln N. It is positive in
    vacuum wherever g > 2.3e-9 m/s^2.
  - Hardy's inequality covers every isolated weak-field body with G M(r)/(r c^2) <= 1/2.
- **The exact sub-class where it fails.**
  - Ultra-relativistic outflows (AGN and GRB jets). W is positive pointwise there. Hardy's inequality about the engine
    still covers AGN jets and typical or bright GRBs. It does not cover the most extreme GRBs, roughly
    L_iso Gamma^2 > 3.4e51 W.
  - An added scalar with V < −Lambda/(8 pi G). This is not a chassis field.

## 1. Re-derivation, and what V, rho_rest and u are (C1)

An in-lane minisuperspace Lagrangian was built without importing CFG294's code. It has:

- anisotropic Bianchi-I flat leaves;
- the terms K.K − lambda K^2 with lambda = 1 + c_2, alpha_c |DN|^2/N and −2 Lambda N;
- the F2a gauge term −1/2 N |D ln N|^2;
- dust moving at coordinate speed v;
- a homogeneous scalar.

Its velocity-fixed lapse Hessian reproduces CFG294's committed W exactly, together with the k^2 coefficients
alpha − 1/2 (F2a) and alpha (physical). Before the background equation is used, the Hessian is

    W_raw = (K.K − lambda K^2) + 8 pi G phidot^2/N^2 + 8 pi G rho_rest u^2/(1 − u^2)^{3/2}.

Using the homogeneous background lapse equation turns it into
W = −2 Lambda − 16 pi G V − 8 pi G rho_rest (2 − 3u^2)/(1 − u^2)^{3/2}. The scalar's kinetic energy cancels.

| Symbol | Meaning |
|---|---|
| **V** | The potential of an optional, minimally coupled scalar: CFG294's probe. It is **not a term of the chassis action**. ACTION.md's action block has R − 2 Lambda, the C-H fields, point masses and Maxwell, and states "Lambda>=0 is a fixed cosmological constant". Chassis-native V = 0. |
| **rho_rest** | mu/sqrt(gamma), the rest mass per proper leaf volume. This is Gamma rho_0 (rho_0 = fluid-frame density). |
| **u** | The speed relative to the khronon frame, in units of c. |

## 2. Pressure: the perfect fluid (C2)

The fluid uses a fixed-flux action, −N sqrt(gamma) rho(n), with J^mu fixed (velocities fixed). Symbolically:

    W = −2 Lambda − 16 pi G V − 8 pi G B/(1 − u^2)^2,
    B = 2 rho − 3 rho u^2 + p u^2 − 2 p u^4 + (rho + p) c_s^2 u^4      (rho, p fluid-frame; c_s^2 = dp/drho).

- The background equation is sourced by the khronon-frame energy density, (rho + p u^2)/(1 − u^2).
- The dust limit reproduces C1.
- **At u = 0 the pressure drops out exactly**, leaving W = −2 Lambda − 16 pi G rho. A star at rest in the khronon frame
  needs no pressure term in the condition. Pressure enters only through moving matter, at O(p u^2).

## 3. Theorems (C3, C4; sympy, with the polynomial core also in Lean)

- **Dust (C3a).** For rho > 0 the matter term is negative iff u^2 < 2/3. It is zero at 2/3 and positive above.
- **Universal identity (C3b).**

      B = 2 rho (1 − u^2)^2 + (rho + p) u^2 (1 − (2 − c_s^2) u^2).

  So rho >= 0, rho + p >= 0, c_s^2 >= 0 and u^2 <= 1/(2 − c_s^2) together give a matter term <= −16 pi G rho. The
  bound u^2 <= 1/2 works for every fluid. Only the null energy condition and c_s^2 >= 0 are needed.
- **Exact thresholds (C3c)** for p = w rho with c_s^2 = w:

  | Matter | Threshold u^2 | Threshold u |
  |---|---|---|
  | Dust | 2/3 | 0.8165 c |
  | Radiation | 3 sqrt5 − 6 = 0.7082 | 0.8416 c |
  | Stiff (w = 1) | none: B = 2 rho (1 − u^2) | — |
  | w = −1 | none: B = 2 rho (1 − u^2)^2 | — |

- **C4.** W <= 0 iff 2(Lambda + 8 pi G V) + 8 pi G Σ_i B_i/(1 − u_i^2)^2 >= 0.
  - Sufficient: V >= −Lambda/(8 pi G), with every component below its threshold and rho_i >= 0.
  - Strict: W < 0 if, in addition, Lambda + 8 pi G V > 0, or some rho_i > 0 is strictly below its threshold.
  - Chassis-native (V = 0, Lambda > 0): W < 0 strictly, including vacuum + Lambda.
- **Lean.** `cfg312_lapse_condition_W.lean` contains dust_pos, dust_neg, fluid_identity, fluid_bound, radiation_pos,
  W_nonpos and W_neg. All use [propext, Classical.choice, Quot.sound] only. Lean certifies these inequalities and
  nothing analytic.

## 4. Backgrounds (W in m^-2; chassis-native V = 0)

Constants come from `a0kit/a0kit.py`: Lambda = 1.089e-52 m^-2, H0 = 67.36, Omega_L = 0.6847. Astrophysical densities,
pressures and speeds are reference values, typed in and not fetched. Rows marked [indicator] apply the homogeneous
formula pointwise; see §5.

| Background | W (m^-2) |
|---|---|
| FLRW today, comoving (also with 1000 km/s peculiar speed) | −3.18e-52 (1.46 × (−2 Lambda)) |
| Radiation era, z = 1e4 | −3.9e-40 |
| Radiation era, z = 1e9 (u = 1e-4) | −2.9e-20 |
| Radiation at u = 0.80 c (below its threshold) | −2.3e-40 |
| Sun, mean density / centre (with pressure) [indicator] | −5.3e-23 / −5.6e-21 |
| Earth [indicator] | −2.1e-22 |
| Solar wind at 1 AU [indicator] | −3.1e-46 |
| Milky Way at R_sun (stars + gas + cold component, u = 1000 km/s) [indicator] | −2.4e-46 |
| Cluster core (hot ICM + galaxies/cold component, u = 2500 km/s) [indicator] | −4.5e-48 |
| Neutron-star centre, p = 0.4 rho c^2, c_s^2 = 0.6, kick 1000 km/s [indicator] | −3.73e-8 |
| Same at u = 0.18 c (fastest ms-pulsar surface spin) [indicator] | −3.82e-8 |
| Maximal stiffness p = rho c^2 at u = 0.18 c [indicator] | −3.86e-8 |
| Added scalar with V = −0.5 Lambda c^4/(8 pi G), no matter | −1.09e-52 |

All 15 rows have W < 0. In the neutron star, pressure at u = 0.18 c makes the matter term slightly *more* negative
(−3.82e-8 against −3.79e-8 without pressure).

**Speeds.** The limits are 0.7071 c (any fluid), 0.8165 c (dust) and 0.8416 c (radiation). Real peculiar velocities are
at most 1e3 km/s, i.e. 3.3e-3 c, a margin of ×212 against the universal bound. The fastest non-jet bulk motion is 0.18 c.

## 5. Static bound systems: the right local test (C6)

**The potential.** On a flat leaf with a static N(x), the velocity-fixed second variation was derived symbolically in
3-D:

- gradient coefficient (alpha − 1/2)/N;
- potential W_loc = (K.K − lambda K^2) + (alpha − 1/2) Delta ln N.

There is no −16 pi G rho here. In the static case CFG294's background-equation rewrite does not apply. In vacuum,
Delta ln N ≈ −|D ln N|^2, so W_loc ≈ −(9 lambda − 3) H^2/c^2 + (1/2)(g/c^2)^2. That is positive wherever
g > 2.3e-9 m/s^2; at 1 AU it is +2.2e-39 m^-2. So "W <= 0 pointwise" fails throughout the Solar-System vacuum, and is
the wrong criterion there.

**Hardy.** Hardy's inequality is Int |grad f|^2 >= (1/4) Int f^2/|x − x0|^2. It gives the following:

- Where Delta N >= 0, the operator (1/2 − alpha)(−Delta + Delta ln N) + (9 lambda − 3) H^2 is positive if
  |x − x0| |D ln N| <= 1/2. In the weak field that is G M(r)/(r c^2) <= 1/2.
- The cosmological −Lambda in Delta N/N costs at most (1/2) Lambda, against (9 lambda − 3) H^2 >= 2 Lambda.

Values of max r|D ln N|:

| Body | max r\|D ln N\| | How obtained |
|---|---|---|
| Sun | 2.1e-6 | s-wave node count: no bound state |
| Weak-field neutron-star model | 0.192 | s-wave node count: no bound state |
| Milky Way-like galaxy | 5.9e-7 | analytic, v^2/c^2 |
| Cluster | 2.2e-5 | analytic, 2 sigma^2/c^2 |

The node-count control (iv) works: a super-compact bump, max r|D ln N| = 4.4, binds one state.

**Not proved here:**

- multi-body leaves (a localisation argument is needed, although every r|D ln N| here is <= 0.2);
- the C-H sector's zero-order lapse potential;
- strong-field interiors, where the flat-leaf derivation does not apply.

## 6. The exception: ultra-relativistic flows

In a steady outflow W r^2 does not depend on r. Hardy about the engine requires W r^2 <= (1/2 − alpha)/4 = 0.125.

| Jet | W r^2 (cold / hot) | Covered |
|---|---|---|
| M87 kpc jet (1e37 W, Gamma = 10) | 5e-14 / 4e-14 | yes |
| Powerful blazar (1e40 W, Gamma = 50) | 1.4e-9 / 9e-10 | yes |
| Typical GRB (1e45 W, Gamma = 300) | 5.0e-3 / 3.3e-3 | yes |
| Bright GRB (1e46 W, Gamma = 300) | 0.050 / 0.033 | yes |
| Extreme GRB (1e47 W, Gamma = 1000) | 5.5 / 3.7 | **no** |

W is positive in every jet tested. Hardy covers L_iso up to about 3.8e46 W at Gamma = 300 and 3.4e45 W at
Gamma = 1000, i.e. L_iso Gamma^2 up to about 3.4e51 W, which is of order c^5/(16 G). Beyond that, invertibility of the
F2a lapse operator is **not proved**. Hardy is sufficient, not necessary. A jet is also far outside the homogeneous
class in which W was derived.

## Controls

| Control | Outcome |
|---|---|
| (i) FLRW + Lambda + comoving dust at all 18 record c_2 | W = −(2 Lambda + 16 pi G rho) from both the raw Hessian and the formula. Reproduces CFG294. PASS |
| (ii) Vacuum | W = 0 exactly (the relabelling mode). PASS |
| (iii) MUTATE (`*_MUTATE.out`, `*_results_MUTATE.json`) | Dust at u^2 = 0.70 gives +2.1e-26; radiation at u^2 = 0.75 gives +3.7e-26; V = −1.5 Lambda c^4/(8 pi G) gives +1.09e-52. All three are flagged and B1 fails (rc = 1). Lean MUTATE (threshold 3/4; fluid bound without the null energy condition) does not compile. |
| (iv) Super-compact bump in the node count | binds 1 state. PASS |

## Scope and disclosures

- The verdict concerns CFG294's C4 only. A1–A5 remain assumed, so CFG294 stays CONDITIONAL.
- The background rows for bound systems are indicators. §5 gives the proper static treatment, and it is a sufficient
  condition only.
- The perfect-fluid form and the static potential were hand-derived before freezing. They were stated as predictions,
  and the script reproduces both.
- kappa = 1/2 is FITTED and plays no role. Nothing here bears on data.

## Files

| File | Contents |
|---|---|
| `cfg312_lapse_condition_W.py` | the lane script (C1–C6, backgrounds, jets, controls, verdict) |
| `cfg312_lapse_condition_W.out`, `cfg312_lapse_condition_W_results.json` | the normal run (16/16) |
| `cfg312_lapse_condition_W_MUTATE.out`, `cfg312_lapse_condition_W_results_MUTATE.json` | the MUTATE run (15/16, rc = 1) |
| `cfg312_lapse_condition_W.lean`, `cfg312_lapse_condition_W_lean.out` | the Lean core (7 theorems) |
| `cfg312_lapse_condition_W_MUTATE.lean`, `cfg312_lapse_condition_W_MUTATE_lean.out` | must not compile |

Run from the repository root (each run takes about 5 s):

    python3 campaign_fresh_gravity/CFG312_lapse_condition_W/cfg312_lapse_condition_W.py
    MUTATE=1 python3 campaign_fresh_gravity/CFG312_lapse_condition_W/cfg312_lapse_condition_W.py
    (cd fable_independent_2026/lean_2026 && lake env lean ../../campaign_fresh_gravity/CFG312_lapse_condition_W/cfg312_lapse_condition_W.lean)
