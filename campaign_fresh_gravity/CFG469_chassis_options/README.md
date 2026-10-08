# CFG469: three ways out of CFG467's alpha_c tension, tested

Criteria frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit fd00569e9, committed alone before any script.
Theory plus offline numerics; no downloads. Every source lane is read-only here.

| run | output files | checks | exit code |
|---|---|---|---|
| main | `cfg469_chassis_options.out`, `cfg469_results.json` | 30/30 pass | 0 |
| MUTATE (`CFG469_MUTATE=1`) | `cfg469_chassis_options_MUTATE.out`, `cfg469_results_MUTATE.json` | 30/32; A1c and the B4 band fail, as required; both flips confirmed | 1, as required |
| first main run (kept) | `cfg469_chassis_options_run1.out` | 28/29; K3 failed on a string-truncation bug (disclosures) | 1 |

    python3 campaign_fresh_gravity/CFG469_chassis_options/cfg469_chassis_options.py
    CFG469_MUTATE=1 python3 campaign_fresh_gravity/CFG469_chassis_options/cfg469_chassis_options.py

The main run takes about 2.5 minutes, the MUTATE run about 1.3 minutes. `cfg469_uv_bh.py` holds the option-B
derivation and the local (Frobenius / Newton-polygon / WKB) analysis.

## The options table

| option | what it adds | constants | verdict (frozen rule) | the deciding result |
|---|---|---|---|---|
| **A** lenient black holes + hierarchy | the owner adopts reading W: black holes regular outside the universal horizon (UH), with CFG319's weak, integrable defect on it | 0 on the sliver alpha_c in [9.624e-14, alpha_rs(c_2)], c_2 >= 0.038 (3 of 9 c_2); +1 UV scale M_* <= 9.87e8 GeV for the full window [9.624e-14, 3.2e-9] | **WORKS-CONDITIONAL** | the defect is causally disconnected (even for infinite-speed signals), carries no free data, is integrable and weak (Tipler and Krolak), and leaves the first-law terms finite. Condition: the owner adopts reading W |
| **B** UV constant M_* | the lowest-order Horava-type higher-derivative term, one coefficient set by M_* | +1 (M_*) | **FAILS** at G12 of CFG467 (strict black-hole regularity) | in both tested operators the moving black hole stays over-determined by exactly one: 7 conditions for 6 constants at every point tested. The UH exponent s+ = 0.618 is untouched |
| **C** retire the chassis | nothing; candidate B becomes a recipe | 15 declared inputs: 2 fitted, 2 data, 1 declared function, 9 declared rules or constants, 1 nuisance | **WORKS-CONDITIONAL** | no current candidate-B pass uses a chassis-only ingredient. Condition: 16 relativistic gates become untested (not passed), and the khronon-based settling leads lose their carrier |

**Recommendation.**
- **Option A is the only option that keeps a relativistic theory consistent with all twelve gates.** It costs one
  explicit criterion choice: accepting a weak, hidden UH defect. For the full window it also costs CFG320's hierarchy.
  - On the record that choice was a bare label. CFG469 shows it is physically coherent. The defect cannot signal out,
    has no free data, is integrable even in the quadratic curvature invariants, and does not obstruct the black-hole
    first law at this order.
  - It remains a real curvature singularity at finite area. Under the Ramos-Barausse / Franchini-Herrero-Valea-Barausse
    criterion it is still a KILL. The choice is the owner's.
- **Option B should not be adopted to fix black holes.** The UV constant buys nothing for G12.
  - The reason is structural. Horava terms are spatial derivatives on the leaves. At the UH the leaf is the r = r_UH
    surface, so the singular radial direction there is the khronon's time direction, where spatial terms cannot act
    (h^rr = Y^2 -> 0).
  - M_* is still what A's hierarchy names for G11, and B shows that this UV sector leaves option C intact.
- **Option C is the fallback.** It keeps every current candidate-B result. But it does not resolve the tension, it
  removes the place where it lives.
  - Sixteen relativistic gates go from passed or conditional to untested.
  - Four settling-mechanism leads lose their only zero-constant carrier, the khronon lapse: CFG373, CFG381, CFG462 and
    CFG483 (the last is the 10-08 khronon-boundary settling class).
- **Next computation for A:** the metric-coupled (not test-khronon) moving black hole inside the window, and collapse
  formation of the UH. Both are inherited from CFG319 as open conditions.

## Option A in detail

### A1: causal disconnection, including the instantaneous mode (pass)
- **A1a.** On the khronon background, lim x H'(r_UH + x) = -1/(y1 W0) = -9/(2 sqrt6), from both sides.
  - So the khronon time T -> +infinity at the UH at every finite advanced time.
  - No exterior leaf (finite T) contains a point on or inside the UH.
- **A1b.** tau = -exp(-kappa_U T), with kappa_U = y1 W0 = 2 sqrt6/9, extends analytically across the UH. It is a global
  time function: H' + 1/(kappa_U x) has no pole, d tau/dr != 0, and the normal is timelike, g^{mn} d tau d tau =
  e(r_UH)(d_r tau)^2 = -(1/3)(d_r tau)^2.
  - The UH is the level set tau = 0. The exterior has tau < 0 and the interior tau > 0.
  - Every signal of any speed, including an elliptic constraint solved on a leaf, moves forward in tau or along a leaf.
- **A1c, fastest-signal reach.** From 18 start points on or inside the UH, signals were followed along the leaf
  (infinite speed) and along characteristics with c = 1, 444, 7.9e5 and 1e12, in both leaf directions.
  - No signal gets past r = 1.5 = r_UH. Start points on the UH stay on it, since the UH is itself a leaf.
  - Control K5: from exterior start points the same code reaches r = 1e4.
- **A1d.** The option-C perturbation of tau goes as x^(1+s+) with 1 + s+ = 1.6180 to 1.6182, so tau stays C^1 with a
  non-vanishing gradient at O(v).
  - Control: the C' option (s-) gives 1 + s- = -0.618. That option destroys the foliation, and it is flagged.
- **A1e.** Option C has 4 constants for 4 conditions (computed count, K2), so the s+ amplitude is an output. No free data
  lives on the defect.
  - The committed exterior difference between the C and C' rules at 6M (3e-13 down to 5e-21) is a static, rule-level
    difference, not a signal.
- **ARG (not computed).** For a black hole formed by collapse, the exterior leaves are complete slices through the
  collapsing matter that never meet the UH. The leaf-elliptic problem on them then has no inner boundary at all.

### A2: finiteness (pass under reading W; fails under reading S by definition)
- The exterior is regular (CFG319, all five window points).
- At the UH the stress and the Ricci curvature diverge as x^(s+ - 1) = x^-0.382. That is integrable.
- The quadratic invariants at O(v^2) go as x^-0.764, also integrable. This needs s+ > 1/2; the margin is 0.118 in s+.
- Along radial free fall (dr/dtau = -1.155 at r_UH, so the crossing is transversal), the Tipler and Krolak integrals
  are finite. Their change between cut-offs 1e-15 and 1e-30 is 8.7e-10. Control K6: the s- mode's integral changes by
  2e48.
- The metric is C^{1, 0.618}. Its Christoffel symbols are Hoelder, so geodesics crossing the UH are unique.
- The defect is therefore a weak, C^1-extendible singularity. It is not a strong one.
- **ARG (reading only).** At O(v) the Killing-energy flux integrates cos(theta) to zero. At O(v^2) it is fixed by
  conservation and vanishes at infinity. The O(v^2) fields were not computed.

### A3: UH thermodynamics (pass at the order computed)
- For L = -lambda K^2 + alpha a.a, the momentum dL/d(grad_m u_n) = -2 lambda K g^{mn} + 2 alpha u^m a^n (sympy). It
  contains no derivatives of u.
- So the Noether charge and the symplectic current involve only u, K and a. Their option-C perturbations vanish at the
  UH: the exponents are 1.618 for dK and 0.618 for da and du.
- kappa_UH is unperturbed at O(v), and the O(v) first law is trivial, since delta A_UH = delta M = 0 for l = 1.
- Whether the UH carries a temperature (Berglund-Bhattacharyya-Mattingly 2012/13 and later disputes) is literature
  recalled from memory. It is PROVISIONAL, not read and not scored.

### A4: the joint window (pass)

| reading | constants | alpha_c window |
|---|---|---|
| A4-0: reading W, no hierarchy | 0 | [9.624e-14, alpha_rs(c_2)], non-empty only at c_2 = 0.0383 / 0.0506 / 0.0667: [9.624e-14, 9.93e-14 / 1.08e-13 / 1.18e-13] |
| A4-H: reading W + Pospelov-Shang hierarchy | +1 (M_* <= 9.87e8 GeV and <= Lambda_sc) | [9.624e-14, 3.2e-9] at all 9 c_2 (CFG467's I_len; the edges are tested ranges) |

- alpha_rs is where Lambda_sc = Lambda_HL_max. It reproduces CFG467's G11 edge exactly (K9).
- **A4-UV.** Option C survives both tested UV operators. With the UV term, its lenient count stays determined (6
  conditions for 6 constants), and the new UV modes at the UH are excluded.

## Option B in detail

**The operators** (frozen; test-khronon limit as in CFG319; +1 constant each):
- O_A = + alpha_c eps (D_m a^m)^2, Horava's A-type acceleration term;
- O_K = - c_2 eps h^{mn} d_m K d_n K;
- eps = 1/(M_* r_g)^2.

The leaf-curvature (B-type) terms have no quadratic piece in this limit (K4b): the leaf metric is delta + O(eps^2).

**B1 dispersion** (derived with sympy on Minkowski; both equal the closed forms):
- O_A gives omega^2 = c_S^2 k^2/(1 + eps k^2). The phase speed falls to zero (z = 0).
- O_K gives omega^2 = c_S^2 k^2 (1 + eps k^2), with z = 2.
- Both are healthy with the frozen signs. The opposite signs give a ghost (O_A) or a gradient instability (O_K).

**B2 derivation.** The O(v) Lagrangian was rebuilt with jets.
- At eps = 0 it reproduces CFG319's committed S22, dK_ops and daa_ops exactly (K1).
- The UV leading coefficients are:
  - S33(O_K) = -8 eps lambda Y^8/(3(W^2 - Y^2 + 1)^2);
  - S33(O_A) = 8 eps alpha W^2 Y^6/(3(W^2 - Y^2 + 1)^2).
- Neither vanishes at the spin-0 horizon, so r_S stops being a singular point. Its logarithm condition disappears.

**Local solutions and the count.** Each arm has six local solutions at each end; at r_S there are none.

| | O_K (z = 2) | O_A (z = 0) |
|---|---|---|
| UH, IR modes | {-1, 0, s+, s-} exactly as CFG319 (-1, 0 regular; s+ weak; s- strong) | the same four, shifted by O(eps) (0.617994 at eps = 1e-4; unchanged at physical eps) |
| UH, UV modes | an oscillating pair x^(1 + i Im beta) exp(+-i b/x), with b ~ W0 sqrt(alpha/lambda)/(y1^2 sqrt eps). Strong: d(a.a) ~ x^-1 | two Frobenius roots ~ -1/2 +- 1/(y1 sqrt eps) (e.g. +-7.8e28 for 10 Msun at the band top). The positive one is regular, the negative one strong |
| infinity | r^3 excluded, r normalised, 1 and r^-2 allowed; e^(+r/sqrt eps) excluded, e^(-r/sqrt eps) allowed | r^3 excluded, r normalised; an oscillating pair r^-4 exp(+-i b r^3/3), both excluded (F'' does not decay, F''' grows as r^2) |
| r_S | regular point (no condition) | regular point (no condition) |
| strict count | 3 + 4 = 7 conditions vs 6 constants: **over-determined by 1** | 4 + 3 = 7 vs 6: **over-determined by 1** |
| lenient count (option C) | 3 + 3 = 6 vs 6: determined | 4 + 2 = 6 vs 6: determined |

- **Every one of the 34 analyses gives the same counts.** That covers:
  - the stealth background at eps = 1e-4 and 1e-20;
  - each of the five window points with its own CFG319 background, at M_* at the band top for a 10 Msun hole (eps
    1.8e-58) and for M87* (4.3e-76), and at the reading lower edge 1e-12 GeV for 10 Msun (1.8e-16).
- The control K2 runs the same code on the IR operator. It reproduces CFG319: 4 constants against 5 conditions, and
  option C determined.

**Why it fails, in one line.**
- The UV term adds two constants and removes the r_S condition. But it adds two new conditions: two at the UH for O_K,
  or one at the UH and one extra at infinity for O_A.
- The deficit of one is unchanged, and s+ = 0.618 is untouched.
- The identity behind this: h^rr = g^rr + u^r u^r = Y^2 on the background (residual 0). Every leaf-projected radial
  derivative of a stationary perturbation carries Y^2 ~ y1^2 x^2 near the UH. So spatial UV terms enter at Euler order
  or weaker there, and they cannot reach the IR exponents beyond O(eps).
- This rules out the record's suggestion (CFG319 "Horava UV terms: argument") for these two operators. It is also the
  missing-ingredient line of failure-ledger row 9.

**B4 the band.**
- min(Lambda_HL_max, Lambda_sc) runs from 8.48e8 to 9.87e8 GeV over CFG320's 81 points.
- No lower bound is on the record. The reading lower edge 1e-12 GeV is recalled from sub-mm tests and PROVISIONAL.
- So the band is non-empty, but B fails before the band matters.
- MUTATE M_* = 1e12 GeV lies outside it at 0 of 81 points.

## Option C in detail

**Candidate B without the chassis: declared inputs.** Every row's quoted source string was found in the cited
committed file (K7a, 15/15).

| input | status | source |
|---|---|---|
| kappa = 1/2 | FITTED | closure_map/GATES.md 3.11 |
| rho_DE(t) in a0(t) = kappa c sqrt(G rho_DE(t)) | DATA | WORKING_MODEL_SETTLED_PHANTOM |
| nu_mono (nu_RAR to y* = 2.3374, log splice delta = 0.05) | DECLARED FUNCTION (+ shape constant delta) | CFG5_common.py |
| bound-only switch | DECLARED RULE | GATES 3.02 |
| KiDS density edge x_e = 0.4 | DECLARED CONSTANT | GATES 3.09 |
| growth edge r_M/ln(1/(1 - f_b)) = 5.85 r_M with the turnaround catchment | DECLARED RULE (zero-knob given kappa, f_b) | STANDING 10-08 |
| f_b | DATA | STANDING 10-08 |
| Omega_c h^2 = 0.12 | FITTED (as in LCDM) | GATES 3.01 |
| cold fluid relaxes toward the phantom target at rate Gamma (bookkeeping) | DECLARED RULE | WORKING_MODEL |
| ownership (the Sun carries no phantom; globulars class E) | DECLARED RULE | GATES 4.01 |
| lensing = GR lensing of the effective dark density | DECLARED RULE | GATES 4.03 |
| background cosmology GR + CDM at z >~ 10 | DECLARED RULE | GATES 3.01 |
| baryon field includes gas pressure | DECLARED MODELLING RULE | WORKING_MODEL |
| stellar M/L | NUISANCE (per data set) | GATES 1.01 |
| G = measured G (no alpha_c/2 correction) | DECLARED | RECIPE_GATE_AUDIT G2 |

**Gates that become untested (16).**
- Twelve status-board tiles:
  - gravity waves at light speed;
  - high-frequency well-posedness;
  - full nonlinear well-posedness;
  - the lapse condition;
  - binary pulsars;
  - strong coupling;
  - Solar System PPN + Cassini Q2. B keeps GATES 4.01 through ownership, but alpha1, alpha2 and gamma become untested;
  - matter conservation G9;
  - structural order G0;
  - the zero-field FAIL, which becomes moot, not passed;
  - black holes;
  - radiative stability G12.
- Four more rows: lensing = dynamics as a derivation, measured G derived, the DOF / ghost count, and the Cauchy problem.

**Dependency audit.**
- None of the 14 current candidate-B rows uses a chassis-only ingredient (the khronon, alpha_c, c_2, the heat filter,
  the leaf average or the C-H term).
- Control K7b: injecting one fake dependency turns the verdict to FAILS.
- **Lost as mechanisms (they are not passes):**
  - CFG373, the khronon-lapse carrier;
  - CFG381, the khronon sink;
  - CFG462, the lapse settling edge;
  - CFG483, the khronon-boundary settling class;
  - the khronon-class a0-rho_Lambda tie.

## MUTATE
- **(A)** The instantaneous mode is put on the hypersurfaces v - r = const, which cross the UH. A signal from the UH
  then reaches r = 1.0004e4, A1c fails, and A reads FAILS.
- **(B)** M_* = 1e12 GeV lies inside the band at 0 of 81 points. B4 fails, and B reads FAILS, now also at G11.
- Both flips are confirmed, and rc = 1.

## Controls

| control | result |
|---|---|
| K1 | CFG319's S22, dK_ops, daa_ops reproduced exactly at eps = 0; both UV arms reduce to the IR form |
| K2 | IR count 4 vs 5 (Delta +1), option C determined |
| K3 | stealth UH exponents = {-1, 0, (sqrt5-1)/2, -(sqrt5+1)/2}; the five W5 points reproduce CFG319's rootsU to <= 5e-12 |
| K4a/K4b | dispersions equal the closed forms; leaf metric delta + O(eps^2) |
| K5 | the reach code takes exterior leaves to r = 1e4 |
| K6 | the s- Krolak integral diverges |
| K7a/K7b | provenance 15/15; fake-dependency injection gives FAILS |
| K8 | a0 enters no computation; both footing labels give identical windows and band |
| K9 | alpha_rs equals CFG467's G11 edge; the sliver is non-empty at exactly 3 c_2 |
| K10 (added, not in the frozen list) | in all 35 analyses the number of local solutions equals the order of the equation, at the UH and at infinity |

## Disclosures
- **Not blind.** All source lanes were read before freezing. The expected outcome for B (spatial UV terms cannot act at
  the UH) was written into the criteria as a heuristic before any computation, and the rule does not depend on it.
- **First main run kept** (`cfg469_chassis_options_run1.out`). K3 failed there because the stealth exponents were
  compared against my in-code 1e-30 tolerance from 12-digit strings (deviation 1.05e-13).
  - The frozen per-point 1e-8 comparison passed in that run.
  - The fix stores the exponents at 40 digits. No physics changed: the verdicts and counts are identical.
  - Bugs fixed before any complete run:
    - a `lambda` keyword clash when re-parsing sympy strings;
    - `factor_list` on a rational expression;
    - Laurent windows that started inside cancelled leading zeros at infinity. These were fixed by deciding leading
      orders component by component, with a window-length guard.
- **Added after the freeze** (reporting only, no rule change): K10, the h^rr = Y^2 identity line, and the
  data-driven wording of A's condition.
- **Interpretation of one frozen phrase.** A4-UV says "the healthy UV operator". Both arms turned out healthy and both
  keep option C, so the reading does not matter.
- **Option C is a curated audit.** The ingredient lists of the 14 B rows and the 16 untested gates are this lane's
  reading of the board, GATES.md and STANDING. They are not a computation.
- **Literature is PROVISIONAL:** Ramos-Barausse 2019, Franchini-Herrero-Valea-Barausse 2021, Kovachik-Sibiryakov,
  Berglund-Bhattacharyya-Mattingly, Pospelov-Shang, and the sub-mm reading. None was fetched here.

## What this lane cannot say
- **Test-khronon limit only**, as in CFG319: no metric response, O(v), l = 1, a stationary eternal black hole.
- **Option B covers two operators only.** Horava's full z = 3 sector and the B-type terms enter only through the metric
  coupling, which is not computed.
  - The h^rr = Y^2 mechanism suggests the result is general for purely spatial terms. That is an argument, not a proof.
- **Option A's singularity is real**, pointwise. Accepting it is a criterion choice, not a mechanism.
- **This is one axis of one chassis.** It is not "the theory works", and not "theory closed".
- kappa = 1/2 is FITTED. No dark-matter particle is added, and the cold fluid's mass is still required. Candidate B has
  no action, so nothing here is a test of B.
