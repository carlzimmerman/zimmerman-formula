# CFG312 — FROZEN CRITERIA: CFG294's lapse-kernel condition W <= 0 for realistic data

Frozen 2026-10-03, before any CFG312 script was written or run. Nothing below may be edited after the commit that adds
this file. Corrections go in a dated section appended at the end.

Disclosure before freezing: the perfect-fluid form of W in §2 (C2) and the static-patch potential in §2 (C6) were
worked out by hand while reading CFG294. They are stated here as predictions that the script must reproduce
symbolically. If the script's symbolic result differs, the script's result stands and the difference is reported.

## 1. What is being closed (committed, not chosen here)

- **Source.** CFG294 (`campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/`, commit e92012b82), README
  S4c(Lag) and condition C4.
  - In formulation F2a with velocities fixed, on Bianchi-I flat-leaf backgrounds, the lapse second variation is
    h_F2a(k) ∝ (alpha_c − 1/2)|k|^2_gamma + W.
  - W = −2 Lambda − 16 pi G V − 8 pi G rho_rest (2 − 3u^2)/(1 − u^2)^{3/2}, with the homogeneous background lapse
    equation used to rewrite it.
  - CFG294 checked W < 0 only for FLRW + Lambda + comoving dust.
- **The chassis action** (ACTION.md of g03_covariant_action_2026, plus L340's two khronon terms):
  - R − 2 Lambda with Lambda >= 0 a fixed constant;
  - the C-H clock/heat fields;
  - point masses and a Maxwell field as the explicit matter;
  - "minimally coupled standard matter may replace this example".
- **Parameters.** alpha_c in the L340 P1 window, so 0 < alpha_c < 1/2 and the F2a coefficient (alpha_c − 1/2) < 0. The
  18 record (alpha_c, c_2) points are read from CFG294's committed results JSON. kappa = 1/2 is FITTED and plays no
  role.

## 2. Claims to prove (each a check() row)

- **C1 — Re-derivation.** An in-lane minisuperspace Lagrangian is built without importing CFG294's code. It has:
  - Bianchi-I flat leaves with three independent scale factors;
  - the chassis gravity terms (K.K − lambda K^2 with lambda = 1 + c_2, alpha_c |DN|^2/N, −2 Lambda N);
  - the F2a gauge term −1/2 N |D ln N|^2;
  - dust moving with coordinate speed v;
  - a homogeneous scalar.

  Its velocity-fixed lapse Hessian must reproduce CFG294's W exactly once the background equation is used. It must
  also reproduce the k^2 coefficients alpha − 1/2 (F2a) and alpha (physical).

  The script must state what V and rho_rest are:
  - **V** is the potential of an optional minimally coupled scalar. It is not a term of the chassis action, so the
    chassis-native value is V = 0.
  - **rho_rest** = mu/sqrt(gamma), the rest mass per unit proper leaf volume. That is Gamma rho_0, where rho_0 is the
    fluid-frame density and Gamma = (1 − u^2)^{-1/2}.
  - **u** is the speed relative to the khronon frame, in units of c.
- **C2 — Perfect fluid (pressure).** Matter is extended to a barotropic perfect fluid through the fixed-flux
  (Brown-type) action −N sqrt(gamma) rho(n). Velocities fixed means the densitised flux J^mu is fixed.

  Prediction (rho, p = fluid-frame energy density and pressure; c_s^2 = dp/drho):

      W = −2 Lambda − 16 pi G V − 8 pi G B/(1 − u^2)^2,
      B = 2 rho − 3 rho u^2 + p u^2 − 2 p u^4 + (rho + p) c_s^2 u^4.

  The dust limit (p = c_s = 0) must reproduce C1. At u = 0 the matter term is −16 pi G rho and the pressure drops out.
- **C3 — Theorems on the matter term** (sympy, symbolic, for all admissible values):
  - **(a) Dust.** For rho > 0: B <= 0 iff u^2 >= 2/3 (B = 0 iff u^2 = 2/3), and B > 0 iff u^2 < 2/3.
  - **(b) Universal fluid bound.** If rho >= 0, −rho <= p <= rho (dominant energy condition) and 0 <= c_s^2 <= 1, then
    u^2 <= 1/2 implies B >= 2 rho (1 − u^2)^2. Hence the matter term −8 pi G B/(1 − u^2)^2 is <= −16 pi G rho: non-positive, and
    negative when rho > 0.
  - **(c) Exact thresholds** for linear equations of state p = w rho, c_s^2 = w:
    - dust: u^2 = 2/3;
    - radiation (w = 1/3): u^2 = sqrt(45) − 6 ≈ 0.7082;
    - stiff (w = 1): none, since B > 0 for all u < 1;
    - w = −1: none, since B = 2 rho (1 − u^2)^2.
- **C4 — The sign condition for W.**
  - **Exact.** W <= 0 iff 2 Lambda + 16 pi G V + 8 pi G Σ_i B_i/(1 − u_i^2)^2 >= 0 (components additive).
  - **Sufficient.** Lambda + 8 pi G V >= 0 (i.e. V >= −Lambda/(8 pi G)), every component below its threshold
    (B_i >= 0), and rho_i >= 0.
  - **Strict.** W < 0 if in addition Lambda + 8 pi G V > 0, or some component has rho_i > 0 with B_i > 0.
  - **Chassis-native** (V = 0, Lambda > 0): W < 0 for all matter below threshold.
  - Lean certifies the polynomial core (C3a, C3b, C4) if it compiles quickly. Lean never certifies analysis.
- **C5 — The scope of W.** W is derived on homogeneous (Bianchi-I, flat-leaf) backgrounds with the C-H sector absent,
  exactly as in CFG294. Applying it pointwise to a bound system is an indicator, not a theorem. That is stated, not
  hidden.
- **C6 — Static inhomogeneous patch (a scoped extension).** On a flat leaf with a static lapse N(x), matter at rest and
  a homogeneous expansion term, the velocity-fixed second variation has:
  - k^2 coefficient (alpha − 1/2)/N;
  - zero-order potential (2/N)[(K.K − lambda K^2) + (alpha − 1/2) Delta ln N], in CFG294's normalisation W_loc =
    (K.K − lambda K^2) + (alpha − 1/2) Delta ln N.

  W_loc is not CFG294's W. In vacuum it is positive where |D ln N|^2 exceeds the cosmological term. Two sufficient
  conditions for an invertible operator are to be proved or checked:
  - **(i) Hardy.** −Delta − |D ln N|^2 >= 0 if |x| |D ln N| <= 1/2 about a single centre, i.e. G M(r)/(r c^2) <= 1/2
    in the weak field.
  - **(ii) Localised positive region.** If W <= W_+ on a ball of radius R and W <= −w0 <= 0 outside, then
    the operator (1/2 − alpha)(−Delta) − W is positive when (W_+ + w0) R^2 <= (1/2 − alpha)/4. This is Hardy's inequality
    restricted to the ball.

  These are sufficient conditions. Numerical s-wave zero-energy node counts are a cross-check, not a proof.

## 3. Backgrounds to check (numbers)

Committed constants are taken from `a0kit/a0kit.py`: C, G, MPC, MSUN, LAMBDA_PLANCK, and H0 = 67.36 with
Omega_Lambda = 0.6847 (the Planck-alone chain named there). Astrophysical densities, pressures and speeds are standard
order-of-magnitude reference values, typed in and labelled "reference value, not fetched". No downloads.

1. **FLRW today** (Lambda + matter), comoving.
2. **Radiation era** (z = 1e4 and z = 1e9), comoving radiation + matter; plus radiation with a peculiar velocity.
3. **Solar System:** the solar interior (mean density); the interplanetary medium (solar wind ~400 km/s plus the Sun's
   ~370 km/s relative to the CMB, taken as the khronon-frame proxy); planets.
4. **Milky Way-like galaxy at the solar radius:** stars, gas and the cold component (the mass that is still required;
   no particle assumed). Speeds are rotation (~230 km/s) plus the galaxy's motion (~600 km/s).
5. **A cluster:** the hot intracluster medium (p/rho c^2 ~ kT/(mu m_p c^2)) and galaxies at ~1500 km/s.
6. **A neutron star:** the central density, relativistic pressure (p/rho up to ~0.3–0.5) and c_s^2 <= 1; u from a
   kick (~1000 km/s) plus the surface spin of the fastest millisecond pulsar (~0.18 c). It is evaluated with the fluid
   form C2, which shows whether pressure enters.
7. **Ultra-relativistic flows:** AGN jets (Gamma ~ 10) and GRB jets (Gamma ~ 300). These are expected to exceed the
   threshold; C6(ii) is applied to their size.
8. **The static-patch potential C6** for the Sun and a neutron star (Hardy compactness) and for the vacuum near the
   Earth's orbit.

Speeds: the maximum allowed |u| (dust sqrt(2/3) c, radiation, universal sqrt(1/2) c) is compared with real peculiar
velocities (<= 1e3 km/s).

## 4. Controls (each can fail)

- **(i) FLRW + Lambda + comoving dust** at all 18 record c_2: W = −(2 Lambda + 16 pi G rho) < 0. This reproduces
  CFG294.
- **(ii) Vacuum** (Lambda = rho = V = 0, Kasner): W = 0 exactly, the relabelling mode.
- **(iii) MUTATE** (`MUTATE=1`, separate outputs `*_MUTATE.out` / `*_results_MUTATE.json`):
  - dust at u^2 = 0.70 > 2/3 with Lambda = V = 0;
  - radiation at u^2 = 0.75;
  - V = −1.5 Lambda/(8 pi G) with no matter.

  Each must give W > 0 and be flagged. The MUTATE run must therefore fail its W <= 0 checks (rc = 1).
- **(iv)** The C6 node-count test must find a bound state when the lapse profile is made super-compact (G M/(R c^2) >>
  1/2, unphysical). This shows that the test can fail.

## 5. Decision rule

- **PASS (for C4, scoped)** if all of the following hold:
  - C1–C4 are proven symbolically;
  - controls (i)–(iv) behave;
  - every homogeneous-class background (1–2) and every pointwise indicator for 3–6 gives W < 0;
  - the speeds of 3–6 are below the universal bound;
  - C6 shows the static patches satisfy the Hardy sufficient condition.
- **PASS-WITH-EXCEPTIONS** if the above holds except on an exactly stated sub-class (e.g. ultra-relativistic flows,
  V < −Lambda/(8 pi G)). The sub-class is reported with whether C6(ii) rescues it.
- **FAIL** if a realistic, non-ultra-relativistic background gives W > 0, or C1/C2 cannot be reproduced.

The verdict is about CFG294's condition C4 only. It does not upgrade CFG294's overall CONDITIONAL verdict (A1–A5 stay
assumed), and it never makes an unconditional well-posedness claim. Excluded and disclosed: the C-H (MOND) sector's
zero-order contribution to the lapse potential, and strong-field interiors where the flat-leaf derivation does not
apply.

## 6. Deliverables

- `cfg312_lapse_condition_W.py`: check() rows and a final "N/M checks pass" line;
- `.out` and `_results.json` files, plus their MUTATE counterparts;
- `cfg312_lapse_condition_W.lean` with its `.out`, if the Lean core is done;
- README.md.
