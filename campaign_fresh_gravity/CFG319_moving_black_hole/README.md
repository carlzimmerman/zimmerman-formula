# CFG319: the slowly moving black hole (gate G11's named condition) for the filtered C-H/K chassis

Criteria frozen first: `FROZEN_CRITERIA.md` (commit 5c8f4d640).

Scripts:
- `cfg319_moving_bh.py`: main; it derives the equations in sympy, runs the points in parallel, does the controls and
  the verdict.
- `cfg319_lib.py`: truncated power series, Frobenius tools, local-Taylor marching.

| run | output files | checks | exit code |
|---|---|---|---|
| main | `cfg319_moving_bh.out`, `cfg319_moving_bh_results.json` | 9/9 pass | 0 |
| MUTATE (`CFG319_MUTATE=1`: the s+ mode at the universal horizon declared admissible) | `cfg319_moving_bh_MUTATE.out`, `cfg319_moving_bh_results_MUTATE.json` | 5/6 (the MUTATE row fails, as designed) | 1, as required |

Run from anywhere:

    python3 campaign_fresh_gravity/CFG319_moving_black_hole/cfg319_moving_bh.py
    CFG319_MUTATE=1 python3 campaign_fresh_gravity/CFG319_moving_black_hole/cfg319_moving_bh.py

- Main run: about 10 minutes of symbolic work, then 12 point runs plus two controls in parallel (14 processes). Wall
  time is about 30 minutes on 14 cores.
- MUTATE runs the five window points only.

## Verdict: CONDITIONAL (frozen rule, section 5)

**There is no fully regular slowly moving black hole at any of the five window points.** This confirms Ramos & Barausse
2019 inside the window, as a computation and not only an extrapolation.

What does exist is the solution that is regular at the spin-0 horizon ("option C"):
- It is regular everywhere outside the universal horizon (UH), including the spin-0 horizon and the Killing horizon
  r = 2M.
- Its only singular content sits **on the UH itself**, which is the causal boundary for signals of any speed.
- The singularity is **weak**:
  - K and a.a stay bounded.
  - Only their gradients diverge, as x^(-0.382) with x = r - r_UH. That divergence is integrable.
  - Coupled to the metric, it is an integrable curvature singularity whose amplitude is proportional to alpha_c v.
- The exterior is regular, and the dipole bound passes by at least 3.7e5.

**Owner flag.** Under RB2019 / FHB2021's criterion (regular everywhere except r = 0), this reads **KILL** for the
chassis, which needs alpha_c > 0. This lane does not make that call.

**What remains (the named conditions):**
1. Accepting a weak, integrable curvature singularity on the universal horizon. It is hidden from every signal,
   but it is a singularity at finite area. This is a strong-cosmic-censorship-type question.
2. The full metric coupling. This lane works in the test-khronon limit, and an RB-type coupled computation inside the
   window is the next step.
3. The UV and collapse-formation arguments listed under "Physical character". They are arguments, not computations.

## The system and the count

**Setup.**
- Scope: the khronon on fixed Schwarzschild (ingoing EF, M = 1); this is the test-khronon limit.
- Action: L = sqrt(-g)[-lambda K^2 - beta K_mn K^mn + alpha a.a], with beta = 0 in the window.
- Static background: T = v + H(r), Y = -u.chi, W = sqrt(Y^2 - e).
  - It is regular at the spin-0 horizon r_S, where alpha W^2 = (lambda + beta) Y^2.
  - The asymptotic K-mode is excluded at infinity.
  - It is found by two-sided matching; the residual is <= 5e-23.
  - (r_S - r_UH) c_S -> 0.6124, and the khronon charge C -> 3 sqrt3/4 (= 1.29904) as alpha -> 0.

**O(v) perturbation.**
- T -> T + v F(r) cos(theta), with F -> -r: the khronon moves at -v at infinity.
- The angle-integrated quadratic Lagrangian is L2 = sum S_ij F^(i) F^(j), derived covariantly in sympy, with beta.
  - S22 = (2/3) r^2 Y^4 (alpha W^2 - (lambda + beta) Y^2).
- This gives a 4th-order ODE for F, integrated as a 4x4 Hamiltonian (Ostrogradsky) system.

**Count.** Four constants against five conditions.

| where | local solutions (exponents) | conditions |
|---|---|---|
| infinity | r^3, r, 1, r^-2 | no r^3 (1); coefficient of r = -1 (1, inhomogeneous) |
| spin-0 horizon r_S | {0, 1, 1, 2}: one logarithm, F ~ x ln x, so dK ~ 1/x | no logarithm (1) |
| universal horizon r_UH | {-1, 0, s+, s-}, with s(s+1)(2 y1^2 s^2 + 2 y1^2 s - (W0^2+1)^2) = 0 | s+ and s- excluded (2) |

- **The system is over-determined by one for every alpha > 0.**
  - The UH exponents depend only on W0 and y1, the background at the UH. The leading UH coefficients are pure
    alpha-terms.
  - As alpha -> 0, s+ -> (sqrt5 - 1)/2 = 0.618034 and s- -> -(sqrt5 + 1)/2. The window values are 0.61803-0.61820.
- **At alpha = 0 exactly the count changes.**
  - The spin-0 horizon merges with the UH. The exponents become {sqrt2-1, sqrt2-2, -1-sqrt2, -2-sqrt2}.
  - The operator factorises through dK = 0, and the stealth (maximal-slicing) solution exists (control C1).
  - This is RB2019's regular alpha = beta = 0 line.

**UH mode classification**, computed in-lane at every point:

| UH mode | foliation e^(-kappa T) | dK | grad dK | d(a.a) | grad d(a.a) | class |
|---|---|---|---|---|---|---|
| s- = -1.618 | singular | x^-0.618 | x^-1.618 | x^-1.618 | x^-2.618 | strongly singular |
| -1 (displacement of the UH) | smooth | bounded | bounded | bounded | bounded | regular |
| 0 | smooth | x^1 | bounded | x^1 | bounded | regular |
| s+ = +0.618 | C^1 only | x^1.618 | x^0.618 | x^0.618 | x^-0.382 | weakly singular (integrable) |

## Singular or regular in the window, and why

**The two one-parameter-removed options at the W5 points** (F normalised to -r, M = 1):
- "Ratio" is the singular amplitude relative to the regular one at r - r_UH = dS.
- C: regular at r_S, s- removed.
- C': regular at r_S, s+ removed.

| point | alpha_c | c_2 | c_S (test) | r_S - r_UH (M) | s+ | c_s+ (C) | ratio (C) | c_s- (C') | ratio (C') |
|---|---|---|---|---|---|---|---|---|---|
| alpha max, c_2 min | 3.2e-9 | 7.29e-3 | 1509 | 4.06e-4 | 0.61820 | -5.976 | 2.217 | 1.69e-8 | 1.019 |
| alpha max, c_2 max | 3.2e-9 | 0.0667 | 4564 | 1.34e-4 | 0.61809 | -7.483 | 2.218 | 1.78e-9 | 1.023 |
| centre | 1.75e-11 | 0.0220 | 3.54e4 | 1.73e-5 | 0.61804 | -11.36 | 2.218 | 2.76e-11 | 1.024 |
| alpha min, c_2 min | 9.62e-14 | 7.29e-3 | 2.75e5 | 2.23e-6 | 0.618035 | -17.25 | 2.219 | 4.29e-13 | 1.024 |
| alpha min, c_2 max | 9.62e-14 | 0.0667 | 8.32e5 | 7.36e-7 | 0.618034 | -21.61 | 2.219 | 4.53e-14 | 1.024 |

- **Why no option is regular.** Both options keep an order-one bad component at the boundary-layer scale: a ratio of
  2.2 in C and 1.0 in C'.
- **Stability.**
  - Under N 30 -> 40, rho 0.25 -> 0.15, x0 dS/4 -> dS/6 and R0 1e6 -> 1e8, c_s+ and c_s- change by 1.7e-12 (C5).
  - The symplectic product is conserved to <= 5e-16 (C6).
- **The amplitude follows matched asymptotics.**
  - Outside the boundary layer, option C is the alpha = 0 stealth solution, which goes as x^(sqrt2 - 1) at the UH.
  - Inside the layer that becomes x^(s+). So c_s+ ~ dS^((sqrt2 - 1) - (sqrt5 - 1)/2) = dS^-0.204. The window gives
    3.61 over a factor 552 in dS, against 3.62 predicted.
  - The ratio is a universal 2.218.
  - The singular content of the khronon therefore does not vanish as alpha -> 0. What vanishes is its physical effect
    (below), because a.a enters the action with alpha.

**alpha ladder at c_2 = 0.05** (reading):

| alpha | s+ | c_s+ (C) | ratio (C) | c_s- (C') | r^2 dK at 6M |
|---|---|---|---|---|---|
| 1e-3 | 0.6498 | -2.30 | 2.46 | 9.9e-4 | -1.27e-3 |
| 1e-4 | 0.6286 | -2.66 | 2.26 | 9.0e-5 | -1.26e-4 |
| 1e-5 | 0.6214 | -3.26 | 2.22 | 8.5e-6 | -1.26e-5 |
| 1e-6 | 0.6191 | -4.07 | 2.21 | 8.2e-7 | -1.26e-6 |
| 1e-7 | 0.6184 | -5.13 | 2.22 | 7.9e-8 | -1.26e-7 |

## Physical character (option C)

**Where it is.**
- On the UH, r_UH = 1.5000 M, inside the Killing horizon r = 2M.
- It is also inside the spin-0 horizon, which lies 0.612 M/c_S further out: 4.1e-4 M to 7.4e-7 M across the window.

**Hidden?**
- The UH is the causal boundary for signals of any finite speed, including Horava's UV modes. So the singularity is
  hidden from every propagating field. That is rigorous for the stationary background.
- It can reach the exterior only through the boundary condition of the leaf-elliptic (instantaneous) part of the
  khronon equation. Its exterior imprint is the difference between options C and C' at r = 6M:
  - 3.0e-13 relative at (alpha max, c_2 min);
  - 1.3e-14 at (alpha max, c_2 max);
  - 4e-17 at the centre;
  - 1.2e-19 and 5.3e-21 at the alpha-min corners.

**What diverges.**
- K and a.a are bounded; their linear perturbations go to zero as x^1.618 and x^0.618.
- Their radial gradients diverge as x^-0.382. That is integrable over proper volume.
- So the alpha-part of the khronon stress-energy diverges integrably, ~ alpha v c_s+ x^-0.382. With the metric
  coupled, that sources an integrable Ricci divergence on the UH.
- It is not a coordinate artefact: these are scalars of the physical foliation, and the foliation function e^(-kappa T)
  is C^1 but not C^2 there.
- In MUTATE and in every main run, the marched solution itself shows |grad d(a.a)| growing by x2.48 per decade toward
  the UH. That is 10^0.382, as expected.

**Amplitude scaling.**
- Linear in v (linear theory).
- In the khronon, the singular part is a fixed ratio (2.22) of the regular part at the layer scale.
- In curvature, the amplitude is proportional to alpha_c v.

**Where it matters, for a 10 Msun hole at v = 1e-3** (reading):
- Linear khronon perturbation theory fails, with the gradient perturbation reaching the background's, only within
  6e-4 m (alpha max) to 1.8 cm (alpha min) of the UH.
- The curvature sourced by the singular stress reaches the background curvature only within 3e-25 m (alpha max) and
  8e-36 to 1.4e-35 m (alpha min).
- The alpha-min value is at the Planck length, 1.6e-35 m.

**Exterior observables.**
- The exterior is regular.
- The khronon's dipole content is r^2 dK|_6M = -0.063 alpha_c/c_2 (= -0.063/c_S^2), which is zero for the stealth
  solution.
- Dipole scoring with |s_BH| <= 10 x |proxy|:
  - 2.8e-7 at most, against s_crit >= 0.10;
  - margins from 3.7e5 (alpha max, c_2 min) up to 7.5e12 (alpha min, c_2 max).
- Shadow, ringdown and ISCO are untouched at this order: the metric is the CFG318 one, and the O(v) khronon has no
  metric back-reaction in this limit.

**Chassis ingredients.**
- **Heat filter / MOND sector:** irrelevant here, by a rigorous bound. CFG318 found suppression of exp(-552) at M87*
  and more for smaller holes, and the MOND force is bounded by 9.9e-14 of g at the photon sphere.
- **Horava UV terms:** argument. The higher-spatial-derivative terms change the dispersion at k ~ M*. They act where
  the IR gradients diverge, i.e. on the UH, and plausibly regularise the x^-0.382 gradient there. Not computed.
- **Formation by collapse:** argument.
  - Spherical collapse forms a regular UH at alpha = beta = 0 (FHB2021) and in Einstein-aether (Bhattacharjee et al.
    2018).
  - A collapse-formed, moving BH would plausibly select the finite-energy option. C has an integrable stress; C'
    (x^-1.618, dK ~ x^-0.618) does not.
  - No dynamical computation was done.

## Sensitivity and dipole margins

- s_BH is not computed. The test-khronon limit has no metric response.
- The scored proxy is the khronon's exterior dipole content, which scales as 1/c_S^2: -1.26 alpha at c_2 = 0.05, and
  -2.8e-8 at the most exposed window corner.
- With the frozen allowance (x10), the dipole passes at every W5 point, by 3.7e5 to 7.5e12.
- An O(1) BH sensitivity would be needed to bite. Here the khronon's exterior response is ~ 0.06/c_S^2.

## Controls

| control | result |
|---|---|
| C1, alpha = 0 | the stealth dK = 0 solution exists: UH exponent sqrt2 - 1 (dev 5e-32); F/r -> 0.6697 constant (ratio 4000 vs 1000 = 1.00038), so it normalises to -r; it solves the alpha = 0 4th-order system to 3e-22 |
| C2, RB2019 point (0.02, 0.01, 0.1) with beta | no fully regular solution (ratios 3.17 for C, 0.16 for C'); the r_S-regular option is singular at the UH, matching RB2019's "curvature singularities at the universal horizon"; qualitative only (test-khronon limit) |
| C3, injection | toy (D phi)^2/2: exponents at r = 2 {0, 0, 1, 1}; phi = r - 1 recovered, phi(6) = 5 to 1e-16 |
| C4, Frobenius | leading-coefficient zero orders 1 (r_S) and 4 (UH) confirmed (dropped <= 7e-31); UH exponents equal the closed form to 2e-16 (beta = 0 runs; the beta run matches too, 3e-17); r_S exponents {0, 1, 1, 2} to 2e-8 (the double root splits at sqrt(eps)); static r_S exponent 0 |
| C5, numerics (reading under the frozen fallback) | amplitudes change by 1.7e-12 under the N / rho / x0 / R0 refinement |
| C6, Hamiltonian | symplectic products conserved to <= 5.3e-16 (all runs) |
| C7, background | matching <= 5e-23; inward march vs UH series <= 2e-24; r_m match of the O(v) marches <= 5e-23 |
| C8, beta = 0 reduction | covariant S_ij at beta = 0 equal the beta-free derivation exactly; static K, K.K and a.a match the reduced forms to 5e-31 |
| MUTATE (s+ declared admissible) | the bookkeeping labels all five points fully regular, and the printed verdict reads PASS. The independent check on the marched option-C solution finds grad d(a.a) diverging (x2.48 per decade) at all five. The contradiction is flagged and rc = 1, as required |
## Disclosures

- **Literature is PROVISIONAL.** It was read through a summarising fetch tool (arXiv abstracts, ar5iv HTML, the arXiv
  export API). No PDF was fetched. RB2019's equations and Frobenius data were not read, so the C2 reproduction is
  qualitative.
- **Not blind.** The FROZEN_CRITERIA list the pre-freeze scratch work: the count, the exponents, and an alpha ladder at
  lambda = 0.05.
  - Those ladder amplitudes (-2.3 to -3.2) came from code that still had a resonance-detection bug, found after the
    freeze (next item).
  - The committed ladder is the corrected one. The frozen rule does not use those numbers.
- **Bugs found and fixed during development.** No run with any of them is kept.
  1. Pre-freeze: a wrong spin-0-horizon background series (wrong at 3e-6); a null-space extraction that took the wrong
     singular vectors.
  2. Post-freeze: Frobenius resonance detection used an absolute threshold. That flagged spurious resonances, setting
     non-zero coefficients to zero, and gave amplitudes unstable at the 10% level. It is now relative to the
     polynomial's magnitude.
     - A first relative version used the term values themselves. That fails when the resonant root is 0 (both sides
       vanish) and made the UH mode matrix singular; this was caught by four failed runs.
     - After the fix, a scratch re-run at alpha = 1e-5 with N 30 -> 40, rho 0.25 -> 0.15, x0 dS/4 -> dS/6 and 40
       digits gave identical amplitudes to 10 digits.
  3. Post-freeze: the background two-sided Newton.
     - The first version clipped its steps, and the thick-layer RB point stopped at residual 5e-4.
     - Backtracking was added. A second version kept backtracking at the precision floor (hours per point), so it now
       stops when no further decrease is possible.
  4. Post-freeze, symbolic: the operators dK and d(a.a) are derived directly, with the static khronon written through
     Y(r); for that khronon -g^{mn} dT0 dT0 = 1/Y^2 exactly. They agree with the slower generic derivation at random
     points.
  5. Post-freeze: the Frobenius normal form first detected the order of the leading coefficient's zero automatically.
     That failed deep in the window. The known orders (1 at r_S, 4 at the UH) are now passed in and verified
     (C4: the dropped terms are <= 7e-31).
  6. Post-freeze, efficiency only: the radius-of-convergence estimate was scale-dependent. Deep in the window,
     S22 ~ Y^4 ~ 1e-24 made the steps ~1000x too small, and the deep points took hours. It is now scale-free; the
     error control is unchanged.
  7. Post-freeze, precision: in the first complete run, C6 failed. The symplectic product drifted by 1.1e-9 at the
     alpha-min corners with 30 digits, while the amplitudes and the ratio 2.218 were already stable.
     - Points with c_S > 1e4 now run at 40 digits. C6 then holds to 5e-16.
     - The frozen text says "30+ digits"; no threshold was changed.
- **Run history.** Several complete runs were aborted or discarded because of items 2-7. The committed outputs come from
  the final script, re-run end to end for both the main and the MUTATE run.
- **Departures from the frozen text.**
  - C4's UH closed form is the beta = 0 one, and the beta = 0.01 RB run is exempt from that comparison. In fact it
    matches there too (dev ~ 6e-17): at the UH the leading coefficients are pure alpha-terms.
  - C5 is reported as a reading, under the frozen fallback ("if not, the amplitudes are readings").
  - The dipole uses a proxy (section 6 of the criteria). That is an argument, not a computation of s_BH.
  - The C2 RB point starts its background search from a coarse scan in d, because its boundary layer is thick
    (c_S = 2.35). The window points start from d = 0.61.
- **Runtime.** About 10 minutes of symbolic work, then 12 point runs in parallel, each 9-21 minutes. Total wall time
  is about 30 minutes on 14 cores.

## What this lane cannot say

- It works in the **test-khronon limit**: the metric is fixed Schwarzschild.
  - The metric response is O(alpha) outside the boundary layer and O(lambda) mixing inside it (the 2 + 3 lambda in
    the full c_S).
  - At the UH itself the leading coefficients are alpha-terms only, so the UH exponents depend on the metric only
    through W0 and y1. That is why the structure is expected to survive, but it is an argument.
  - A full RB-type coupled computation inside the window is the next step.
- It covers O(v), beta = 0 in the window, a stationary eternal BH, and l = 1 only.
- It does not compute the BH sensitivity, the formation by collapse, or the effect of Horava's UV terms.
- It is one condition of one gate on one chassis. It is not "the theory works". kappa = 1/2 remains FITTED, and the
  cold mass is still required.
