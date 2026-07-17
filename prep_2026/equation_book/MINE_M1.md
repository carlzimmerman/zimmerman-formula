# EQUATION BOOK — LANE M1 (seams S1 algebraic, S3 welds, S5 EFE, S8 estimators)

**Date:** 2026-07-16. **Framework judged on its own terms:** modified-INERTIA, horizon-derived
`a0 = cH_Lambda/Z`, `Z = sqrt(32pi/3)`, its own `nu(y) = sqrt(1+1/y)` → `g_obs = sqrt(g_bar^2 + g_bar a0)`.
**Both footings carried everywhere:** canonical `9.36e-11` (rho_DE/cH_Lambda), alternate `1.13e-10` (rho_total/cH0).
**Every equation below is backed by a committed, runnable, exit-0 script in this directory.**
No proof language; exact-vs-approx flagged per equation; novelty checked by literature search
(honest caveat: search absence is evidence, not proof, of novelty).

Scripts (all exit 0, outputs in `*.out`):
`eqbook_S1_algebraic.py` (17 checks) · `eqbook_S3_welds.py` (9) · `eqbook_S5_efe.py` (11) ·
`eqbook_S8_estimators.py` (10) · `eqbook_quickfire_sparc.py` (real SPARC, read-only).

Rubric per candidate: **N**ovelty / **T**estability / **D**erivedness / **U**tility, each 0–3. Total /12.

---

## THE TOP FIVE

### 1. E-S1.7+E-S1.5+E-S1.6 — THE RAR LANDMARK TRIPLET (pure numbers) — score 12/12
From the law alone, the log-log RAR slope is exactly
```
sigma(y) = (2y+1) / (2(y+1)),        y = g_bar/a0
```
which yields three parameter-free landmarks **specific to this nu**:
- **Curvature maximum at y = 1 exactly** (g_bar = a0), where the slope is **exactly 3/4**
  and the log-log curvature is **exactly 1/8**; the anchor point is (a0, sqrt(2) a0).
- **Reciprocity symmetry:** curvature `C(y) = y/(2(y+1)^2)` satisfies `C(1/y) = C(y)` —
  the RAR curvature profile is an exactly even function of `ln(g_bar/a0)`.
- **Slope sum rule:** `sigma(y) + sigma(1/y) = 3/2` for **all** y.

Discriminating power (computed, not asserted): McGaugh's nu peaks at y=3.46 with (0.829, 0.103);
the MOND "simple" nu at y=2.00 with (0.789, 0.096); both break the sum rule and the symmetry.
The symmetry/sum-rule tests are **Upsilon-rescale-immune in shape** (a global M/L shift slides
the profile along the x-axis but cannot create or destroy the symmetry); the landmark *location*
then reads off a0. [EXACT from the law. Novelty search: no hit on any RAR
inflection/curvature-landmark or slope-sum-rule statement.]
**Quick-fire (SPARC, binned medians):** at Upsilon_disk=0.50 the sum reads ~1.40; at the
framework's own committed ML footing Upsilon_disk=0.70 it reads **1.496/1.481 (x=2/x=3) at the
canonical footing — the exact 1.500 to ~1%**. Both ways shown; the 0.50 shortfall is an
M/L-convention artifact (consistent with banked RAR non-diagnosticity). EIV control mocks bound
pipeline bias at ~+0.06. Verdict: encouraging, not yet a measurement (needs hierarchical errors).

### 2. E-S8.1 — THE PAIR ESTIMATOR (distance-free AND inclination-free a0) — score 11/12
Because the law is **quadratic** (linear in a0), the ratio of the law at two radii solves for a0
in closed form. With pure observables `R12 = (v_los,1/v_los,2)^4 (theta_2/theta_1)^2`:
```
a0/Upsilon = (s1^2 − R12 s2^2) / (R12 s2 − s1)        [disk-dominated, s_j = photometric shape]
a0        = (g1^2 − R12 g2^2) / (R12 g2 − g1)          [gas-dominated: D, i, Upsilon* ALL cancel]
```
Distance and inclination cancel **identically** (d/dD = d/d sin i = 0, sympy-verified; g_bar is a
surface density × G, hence D-free). The same elimination for McGaugh's nu is transcendental —
sympy finds no closed form — so this estimator **exists because of, and only because of, the
framework's quadratic law**. [EXACT given the law; real-data systematics = asymmetric drift,
warps, non-circular motions.]
**Derived conditioning fact (honest):** in the deep-deep limit R → g1/g2 and the denominator → 0
(parallel constraints); the estimator is well-conditioned only for pairs **straddling y=1**. So the
fully-Upsilon-free gas-dominated variant is ill-conditioned in practice (SPARC: 2 usable pairs);
the usable variant takes straddling pairs at fiducial Upsilon (D, i still cancel exactly).
**Quick-fire:** 10,196 straddling SPARC pairs → median `1.5e-10` (16–84%: 0.7–3.3e-10) —
brackets both footings; heavy-tailed single-pair noise, median-only statistic. The 20% fake
distance error shifts the estimator by <1e-12 relative — **exact D-cancellation confirmed
numerically on real data**. [Novelty search: no two-point ratio a0 estimator found.]

### 3. E-S5.1/2/3 — THE EFE CUBIC AND THE ATTENUATED a0-LINE — score 11/12
From the framework's own worldline EFE kernel (`theta0 = sqrt(2)` DC weight, BASELINE_ACTION.md),
with `x = g_obs/a0`, `b = g_bar/a0`, `e = sqrt(2) g_ext/a0`:
```
x^3 + e x^2 − b(b+1) x − b^2 e = 0                      (the EFE cubic; e=0 → the a0-line)
g_obs^2 − g_bar^2 = a0 g_bar · g_obs/(g_obs + sqrt2 g_ext)   (the attenuated a0-line)
```
The a0-line generalizes to an external field by an **exact attenuation factor** — an environmental
a0-line whose measured slope is `a0_eff = a0 · <g_obs/(g_obs+sqrt2 g_ext)>`. Corollaries (all
sympy-verified):
- **Half-quench law:** the MOND excess is halved exactly when `sqrt(2) g_ext = g_obs`.
- **EFE susceptibility:** `d g_obs/d(sqrt2 g_ext)|_0 = −1/(2(1+g_bar/a0))` → deep-limit −1/2
  (directly confrontable with Chae-type EFE amplitude fits).
- Unique positive root in closed (trig-Cardano) form, verified against the unsquared balance.
- External-dominated limit recovers **Milgrom's known** quasi-Newton `G_eff = G/mu(e)` form
  (credited; that piece is NOT novel) with the framework's own mu and sqrt2-weighted argument.
[EXACT given theta0=sqrt2 — postulate-dependent on the framework's DC kernel; scalar/aligned
composition per the framework's own usage; direction-blind, consistent with the pure-MI
zero-directional-asymmetry memory. Novelty search: "difficult to derive analytic expressions"
is the literature's own summary of the EFE — no closed cubic found.]

### 4. E-S3.3+E-S8.5 — THE DISTANCE-LADDER-FREE HUBBLE CHAIN — score 10/12
The premise inverts to `Lambda = 3 Z^2 a0^2/c^4` and welds to (flat FRW, definitions only):
```
H0 sqrt(Omega_Lambda) = Z a0 / c            (the triangle weld)
H0^2 = (Z a0/c)^2 + (8 pi G/3) rho_m0       (the Pythagorean weld)
```
Chained with E-S8.1 (a0 with **no distances**): rotation-curve shapes + CMB physical density
`omega_m` → an H0 with **no distance ladder anywhere in the chain**. Numbers: canonical footing +
Planck omega_m=0.1430 → **H0 = 67.4 km/s/Mpc**; alternate footing → 77.2 (spread shown, fork
honest). The weld also maps the Hubble tension onto an a0 tension: Planck→9.36e-11,
SH0ES→1.014e-10 (8.3%) — a few-percent galactic a0 **arbitrates the Hubble tension** inside this
framework. [EXACT given the premise; the a0~cH0 COINCIDENCE is Milgrom's (1983/1999) — credited;
the framework adds the definite coefficient 1/Z and footing, and the estimator chain is what's new.
NOT a derivation of a0 (kappa-closure memory: value postulated).]

### 5. E-S1.2+E-S1.3 — THE ZERO-FIT BARYON-MASS PREDICTOR + VELOCITY a0-LINE — score 9/12
Exact inversion `g_bar = (sqrt(a0^2+4g_obs^2) − a0)/2` gives a per-radius, zero-free-parameter
baryonic-mass prediction from kinematics alone:
```
M_bar(<r) = (r^2 / 2G) ( sqrt(a0^2 + 4 v^4/r^2) − a0 )
v_obs^4(r) − v_bar^4(r) = a0 G M_bar(r)      (the velocity a0-line, EXACT at every radius)
v^4 = G M a0 + (G M/r)^2                      (exact finite-radius BTFR, point mass)
```
The exact BTFR correction is the Newtonian term `(GM/r)^2` — the BTFR "curvature" at high mass is
predicted, not fitted. [Law EXACT; spherical-equivalent M interpretation approximate for disks
(geometry factor ~1.1–1.3) — flagged.]
**Quick-fire (10 extended Q=1 SPARC galaxies, outermost point):** median `M_pred/M_phot` = 1.15
canonical / 0.97 alternate (16–84%: ~0.8–2.3). Order-unity zero-fit agreement; the tail
(NGC2841 2.9) is the classic distance/M-L-sensitive case. Not diagnostic between footings.

---

## FULL CANDIDATE LEDGER (rest, ranked)

| # | Eq | Statement | Exact? | Novelty check | Score |
|---|----|-----------|--------|--------------|-------|
| 6 | E-S8.4 | Three-radius consistency polygon: `(s1²−R12 s2²)(R23 s3−s2) = (s2²−R23 s3²)(R12 s2−s1)` — pure-observable identity testing the LAW with no a0, Upsilon, D, i | EXACT | no hit | 9 |
| 7 | E-S8.2 | Per-radius kinematic distance `D = v_los²/(sin²i·theta·sqrt(g_bar(g_bar+a0)))`; constancy across radii = new per-galaxy test (BTFR-distance's per-radius generalization) | EXACT | BTFR distances known (McGaugh); per-radius closed form not found | 8 |
| 8 | E-S3.6 | CPL bump closed form (declining footing): `z_pk = −(1+w0)/(1+w0+wa)`, amplitude `[(wa/(1+w0+wa))^{3(1+w0+wa)} e^{3(1+w0)}]^{1/2}`; DESI-class → z_pk=0.41, +6.3% bump; RISING footing: monotonic, NO bump — the bump is a footing discriminator | EXACT given CPL | no hit | 8 |
| 9 | E-S5.4 | EFE susceptibility `chi = −1/(2(1+y))` (see #3) | EXACT given theta0 | no hit | 8 |
| 10 | E-S8.3 | Inclination estimator `sin²i = v_los²/(D·theta·sqrt(g_bar(g_bar+a0)))` — inverts the law for the nuisance; useful for face-on gas-rich galaxies | EXACT | fitted-inclination practice known; closed form not found | 7 |
| 11 | E-S1.4 | Slope law `sigma(y)=(2y+1)/(2(y+1))` (parent of #1) | EXACT | no hit | 7 |
| 12 | E-S3.4 | Hubble→a0 tension map `a0(H0) = cH0 sqrt(OmL)/Z` (part of #4) | EXACT | coincidence = Milgrom, credited | 6 |
| 13 | E-S3.5 | `tau_mem = 2Z/(H0 sqrt(OmL))` = 13.99/H0 = 203 Gyr canonical — memory time in pure cosmological observables | EXACT | framework-internal | 5 |
| 14 | E-S5.6 | External-dominated `G_eff/G = (1+sqrt(1+4e²))/(2e) = 1/mu_fw(e)` | EXACT series | **Milgrom's known G_eff=G/mu form — credited, NOT claimed novel** | 4 |
| 15 | E-S1.8 | Anchor `g_obs(a0) = sqrt2 a0` (member of #1) | EXACT | no hit | 4 |
| 16 | E-S3.1 | `Lambda = 3Z²a0²/c⁴` (premise inversion, a0-line E2 restated) | EXACT | framework-published | 3 |

Structural note (verified in eqbook_S8_estimators.py, check 10): every closed-form estimator above
exists **because the framework law is quadratic in g_obs and linear in a0**. For McGaugh's
exponential nu the identical eliminations are transcendental (sympy: no closed form). The a0-line
and all its siblings here are a **family signature of this specific nu** — that is the vein.
Also structurally distinct from Verlinde's emergent-gravity relation, which is additive
(`g_obs − g_bar ∝ sqrt(g_bar a0)`), not quadratic-in-quadrature.

## HONESTY RAILS APPLIED
- No numerology: every equation derives from the law / the framework's own stated kernels; no digit hunts.
- Both footings on every number; the alternate footing's H0=77.2 shown, not hidden.
- Exact-vs-approx flagged per equation (the EFE trio is postulate-dependent on theta0=sqrt2; the
  M_bar predictor's sphericity caveat flagged; CPL forms are exact-given-CPL).
- Deficit-shaped readings verified before relaying (memory rule 2): the FIRE 2 Upsilon fork was
  run both ways (0.50 → 1.40; framework's own 0.70 → 1.48–1.50); EIV control mocks run; verdict
  stated as non-diagnostic-at-this-crudeness, neither caved nor overclaimed.
- FIRE 3's gas-dominated ill-conditioning is reported as a derived property, with the failed
  (2-pair, negative-median) variant shown rather than filtered away.
- Novelty: searched Milgrom/McGaugh/Famaey/Lelli literature (4 targeted searches). The
  Milgrom–Sanders nu-families do not contain (1+1/y)^{1/2}; no hits on the landmark triplet,
  pair estimator, EFE cubic, or velocity a0-line. E-S5.6's G_eff form and the a0~cH0 coincidence
  are Milgrom's — credited. Caveat: the MOND literature is large; search absence is strong but
  not conclusive.
- Frozen repo touched READ-ONLY (SPARC data); all outputs live here.

## FORWARD (data pick suggestions, not claims)
1. The **landmark triplet** on a hierarchical SPARC/WALLABY RAR fit (slope-field, not binned
   medians) — the (1, 3/4, 1/8) triple vs McGaugh's (3.46, 0.83, 0.10) is a clean nu discriminator.
2. The **pair estimator** on Cepheid/TRGB-anchored galaxies: since D cancels, the residual spread
   directly calibrates the non-circular-motion systematic — then gas-rich straddling pairs give
   the distance-free a0 feeding the Hubble chain (#4).
3. The **attenuated a0-line** on Chae-style samples: slope vs |g_ext| with the exact
   `g_obs/(g_obs+sqrt2 g_ext)` factor — one-parameter, falsifiable, and its deep-limit
   susceptibility −1/2 is a sharp number.
