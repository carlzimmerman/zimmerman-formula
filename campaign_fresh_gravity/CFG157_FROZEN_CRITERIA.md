# CFG157 -- independent re-derivation of CFG121's G1 / B1 headline (Door 3, dipolar dark matter): FROZEN CRITERIA

Written 2026-09-29, PHASE 1, before any physics script, number or plot of this lane exists. Nothing was run. Standing rules:
kappa = 1/2 is FITTED; a scoped no-go is a valid result; nothing here says the data favour the framework or that the theory
is closed; a disagreement with CFG121 is a valid result and is kept; failed controls and wrong expectations are kept, never
repaired. Any amendment is an appended, dated AMENDMENT section only.

## 0. What is read, what is not (declaration)

Read for this file: campaign_fresh_gravity/CFG121_FROZEN_CRITERIA.md; campaign_fresh_gravity/CFG121_door3_dipolar_dm/README.md;
campaign_fresh_gravity/CFG44_fluid_target/README.md, the docstring of B1_target_and_hydrostatics.py (the target definition) and
the one-line docstring of the exponential-sphere function in Bcommon.py (definition only, no code copied);
campaign_fresh_gravity/closure_map/TEN_DOORS_GATES_2026-09-29.md.
NOT opened, and not to be opened before my own main and MUTATE runs are saved: every script, .out and .json file of
CFG121_door3_dipolar_dm/ (including cfg121_common.py), and CFG44's code. The CFG121 README numbers below are TARGETS I READ
BEFORE deriving anything. They are not blind predictions; the hand estimates in section 4 were made after reading them, so they
test my understanding of the mechanism, not my ability to predict blind. This must be said in the phase-2 report.

## 1. What is re-derived (the headline)

CFG121 T1.2 + T1.5 (G1, the extended-baryon test of the single-law polarisation) and the B1 medium budget.

Model as frozen in CFG121 section 2/4 (V_B geometry; the same for the pure phantom): baryons with enclosed mass m(r) = M_b(<r),
g_b = G m / r^2, polarisation Pi = chi(g_b) g_b with 4 pi G chi = sqrt(1 + a0/g_b) - 1 (the P2 kernel, derived from the point-mass
target), bound mass M_pol(<r) = 4 pi r^2 Pi = m (nu - 1), rho_pol = M_pol' / (4 pi r^2), g_model = G (m + M_pol) / r^2, and
    C_model(r) = rho_pol r^3 g_model,     C_tgt(r) = (a0 / 4 pi) M_b(<r)     (the CFG44 exact target),
    deviation(x) = C_model / C_tgt - 1 on x = r / r_M in [0.1, 30], r_M = sqrt(G M_b / a0), 121 log-spaced points (and a 2001-point
    robustness grid); gate quantity = max_x |deviation|; pass line for the DOOR is 0.10 (CFG121's), which is not my test.
Baryons: 3-D exponential sphere rho_b = rho_0 exp(-r/h), rho_0 = M_b/(8 pi h^3), M_b(<r) = M_b [1 - (1 + s + s^2/2) e^{-s}],
s = r/h (CFG44 Bcommon docstring). Masses 1e9, 1e10, 1e11, 1e12 Msun; scale-length rule h(M) = 2 + (log10 M - 9) kpc
(CFG121 disclosure, taken from CFG50's four points); a0 = 9.3603e-11 m/s^2 canonical and 1.1312e-10 second footing;
G = 6.6743e-11, Msun = 1.98841e30 kg, kpc = 3.0856775814913673e19 m (CFG121's stated G, Msun).
Target ODE for the reference mass M_c (used only in B1): (m + M_c) dM_c/dr = (a0/G) r m, M_c(0) = 0 (CFG44 (T)).

Pinned README numbers (targets read, not predicted):
- T1.2 max |C_model/C_tgt - 1| = 1.31 / 1.02 / 0.43 / 0.063 at 1e9 / 1e10 / 1e11 / 1e12 (canonical a0; only 1e12 passes 0.10).
- T1.5 (committed nu_mono kernel) = 1.46 / 1.40 / 1.19 / 0.62.
- B1: F_req = 0.41-0.97 (pass line 0.10) and Q* = 9.68, where F_req(x) = M_c(<r) / (4 pi eps_c Q r^3 rho_tgt(r)), eps_c = Q = 1,
  rho_tgt r^3 g_tot = (a0/4 pi) m, and Q* = the Q that makes max_x F_req <= 0.10 at eps_c = 1.
CFG121 states the second footing (1.1312e-10) gives "slightly different numbers" without printing them here; I pin none for it.

## 2. Shared and NOT independent

Shared (taken as given, so agreement does not test them): the exponential-sphere definition and the h(M) rule; a0 (both values),
G, Msun; the CFG44 target definition and the framing that C_tgt = (a0/4 pi) M_b(<r) is the object to reproduce; CFG121's
definition of C_model (rho_pol from Pi = chi g_b, g_model including the bound mass); the x range/grid convention; the
identification of "T1.5" with the committed nu_mono kernel. Not independent: I have read the README results, and the analytic
route in section 3 is my own derivation but was finished after reading them. Independent: all code, the ODE integration, the
enclosed-mass and derivative routes, the kernels' implementation, the controls. Literature statements (Blanchet et al.) are
NOT used. What agreement would NOT establish: that dipolar dark matter is or is not viable (CFG121's other gates G1c-G5 are not
re-derived here), nor that P2 is the right kernel.

## 3. Hand derivation (mine, to be verified numerically, not assumed)

With y = g_b/a0, nu = sqrt(1 + 1/y), M_pol = m (nu - 1), g_b' = (G m'/r^2) - 2 g_b/r, one gets exactly
    C_model / C_tgt = 1 + (dln m / dln r) * B(y),     B(y) = y + 1/2 - sqrt(y (y + 1))   (0 < B < 1/2; B -> 1/2 as y -> 0, ~ 1/(8y) at large y).
Consequences to verify: (i) point mass: dln m/dln r = 0, ratio identically 1 (T1.1 identity); (ii) the deviation is >= 0 everywhere
(rho_pol >= 0, no sign problem), is largest at the centre where y is small and dln m/dln r -> 3, tends to 1.5 as r -> 0
(ratio -> 2.5), and decreases with r, so the gate maximum sits at the grid edge x = 0.1 for every mass; (iii) for the target
ODE at small r inside the core (deep, w >> m): with m = m0 r^3: M_c^2 = (2 a0 m0 / 5 G) r^5, so F_req = G M_c^2 /(a0 r^2 m) -> 2/5 as r -> 0, and for a point mass
F_req = y + 1 - sqrt(y^2 + y) (0.5 at large y, 1 at small y), so max_x F_req ~ 0.968 at x = 30 and Q* = 10 max F_req = 9.68.
The script must compute C_model NUMERICALLY (finite differences of M_pol and, separately, a sympy-lambdified analytic
derivative, and a third route by direct differentiation of rho_pol from the field of the exact rho_b) and compare each with the
closed form above; the closed form is a cross-check, never the reported number.

## 4. My ESTIMATES (hand, made after reading the targets; probability = my subjective chance the README number reproduces)

Evaluating the closed form of section 3 at x = 0.1 (by hand, series for the exponential enclosed mass):
| mass | my hand value of max dev (at x = 0.1) | README | P(reproduces within the pass line of section 5) |
| 1e9  | 1.31  | 1.31  | 90% |
| 1e10 | 1.02  | 1.02  | 90% |
| 1e11 | 0.43  | 0.43  | 90% |
| 1e12 | 0.063 | 0.063 | 90% |
(hand digits: 1.310, 1.016, 0.434, 0.063). These agree with the README to the digits I could carry, which makes an
independent-formula agreement likely, but I could have mis-derived g_b' or the definition of g_model, so I keep 10% for a
definitional disagreement (the largest risk is CFG121 defining g_model or the grid differently from what its README implies).
- Joint probability that all four reproduce: 80%. That the maximum is at x = 0.1 (grid edge) for all four masses: 90%.
- B1: max F_req = 0.968 (x = 30) and Q* = 9.68 (= 10 x max F_req): 85% that Q* reproduces within 2%. Extended profiles change
  the x = 30 value by a tiny offset (the CFG44 constant D, ~0.1-0.3%); min F_req of the README (0.41): my deep-core limit is 2/5
  but the value on the gate grid depends on the range convention ([0.1, 30] vs [0.3, 30]) and on sub-leading terms of order
  sqrt(y); I expect 0.36-0.45 and give 45% that it reproduces within 3%.
- T1.5 (nu_mono): the README figures are described as "max dev" while CFG44 quotes a point-mass charge function R(1) = 1.46
  (R - 1 = 0.46); the first entry 1.46 coinciding with R(1) may be a labelling accident. I will build nu_mono only from the
  README-level recipe of CFG5/CFG4 (read the README text, not code, at the start of phase 2, and state which). 40% that all four
  reproduce within 2%; if the recipe is not recoverable from text, T1.5 is reported NOT RE-DERIVED and does not count against
  CFG121.
- Second footing: I expect the four deviations to change by a few percent (y at fixed x scales like a0^(-3/2) inside the core,
  so the deviation rises slightly), ordering unchanged, the 1e12 point still passing 0.10 (85%).

## 5. Exact pass lines (agreement with CFG121)

A number "reproduces" if |mine - README| <= max(2% of README, half a unit of its last printed digit) AFTER all integrity checks pass:
T1.2 at each mass (canonical a0): 1.31 (+-0.026), 1.02 (+-0.020), 0.43 (+-0.0086), 0.063 (+-0.0013). Verdicts (1e9-1e11 FAIL, 1e12 PASS
at 0.10) must match exactly. B1: Q* within 2% of 9.68 (9.48-9.87); max F_req within 2% of 0.97; min F_req within 3% of 0.41 (both
range conventions printed; the pass uses whichever the README's number is closer to, and both are reported). T1.5: each of the four
within 2% of 1.46 / 1.40 / 1.19 / 0.62 (conditional on the recipe being recoverable, see section 4). Headline verdict of my lane:
REPRODUCES if all T1.2 numbers and Q* pass and the section 3 identities (i)-(iii) hold numerically to 1e-6 / stated tolerance;
PARTIAL if T1.2 passes and B1 or T1.5 does not; DISAGREES if any T1.2 number misses by more than the tolerance and the miss survives
the tolerance checks below. A disagreement is a valid, kept result and is reported with the size and the suspected definitional
difference, NOT repaired by tuning my definitions to match.

## 6. Integrity checks (a failure aborts, exit 2, and no verdict is valid)

(a) Point mass: max |ratio - 1| <= 1e-9 (analytic), <= 1e-6 (finite differences). (b) M_b(<r) closed form equals the numerical
integral of rho_b to 1e-8 and M_b(<inf) = M_b. (c) Three derivative routes for rho_pol agree to 1e-5 relative where |ratio - 1| is
larger than 1e-3. (d) Closed form 1 + (dln m/dln r) B(y) agrees with the numerical ratio to 1e-6. (e) Target ODE: point-mass case
reproduces (M + M_c)^2 = M^2 (1 + x^2) to 1e-8; extended profile converged to 1e-8 under tolerance halving and start radius
r0 -> r0/10 (using the analytic small-r series as the start); outside the baryons the first integral (M + M_c)^2 - (M + M_c,e)^2 =
(a0 M / G)(r^2 - r_e^2) holds to 1e-6. (f) Grid convergence: 121 -> 2001 points changes max dev by < 0.5%. (g) Constants sensitivity:
G, Msun of CFG121 versus G = 4.30091727e-6 kpc (km/s)^2/Msun changes results < 1e-3 relative (reported).

## 7. MUTATE controls (each must flip a load-bearing cell; exit 1 when it bites, exit 0 when it does not, and a non-bite is kept)

- MUTATE=sign: chi -> -chi (bound charge sign flipped: M_pol = -m (nu - 1), g_model = G m (2 - nu)/r^2). Point-mass ratio becomes
  1 - 2/nu, so the T1.1 identity must FAIL with max |ratio - 1| >= 1.5 (analytic 2/nu at x = 0.1 is ~2), and every T1.2 verdict must be FAIL,
  in particular the 1e12 cell flips PASS -> FAIL. Bites iff point-mass max dev > 0.10 and the 1e12 deviation > 0.10.
- MUTATE=kernel: P2 replaced by the "simple" nu = 1/2 + sqrt(1/4 + 1/y). For the point mass ratio = 1 + 1/(2 sqrt(1/4 + 1/y)) (hand):
  identity must FAIL (max dev >= 0.5 at x = 0.1) and the extended-profile numbers must move by more than 10% relative at least at
  one mass. Bites iff point-mass max dev > 0.10 and at least one T1.2 number moves > 10% relative to the main run.
- MUTATE=target: the CFG44 target replaced by the constant-charge closure C = a0 M_b,tot / (4 pi) (enclosed mass replaced by total
  mass; CFG44's own B1 control idea, reimplemented). At the point mass there is no bite by construction (as in CFG44; reported); for
  the exponential spheres the ratio at x = 0.1 is ~ R m(<r)/M so |dev| ~ 0.9-1.0 at all four masses and the 1e12 cell must flip
  PASS -> FAIL. Bites iff 1e12 deviation > 0.10 with the point-mass identity still passing.
- MUTATE=pm_target (B1 script): in F_req replace the extended-profile target ODE by the point-mass closed form
  M_c = M(sqrt(1 + x^2) - 1) while keeping the extended baryons; then min F_req must rise to >= 0.5 (from ~0.4) and the
  ODE-integrity check (e) must FAIL. Bites iff min F_req changes by > 10% relative to the main run.
Controls that must reproduce CFG44's committed values without being copied: point-mass M_c to 1e-8 (check e).

## 8. What would count as disagreement, and how it is reported

Disagreement = at least one T1.2 number outside its section 5 tolerance, or Q* outside 2%, with all section 6 checks passed. It is
reported as such with (a) my numbers next to the README's, (b) the x at which the maximum sits, (c) the closed-form value, (d) a list
of definitional differences that could explain it (g_model with or without the bound mass, scale-length convention s = r/h versus a
disc-type projection, log-grid endpoints, the target's start condition), each tested by a labelled post-hoc variant that does not
replace the frozen main result. If mine agree, that is agreement on a Newtonian identity plus its analytic deviation formula,
nothing more; CFG121's verdict "scoped no-go" rests on gates this lane does not re-derive.

## 9. Scripts (phase 2; after the orchestrator commits this file)

- cfg157_common.py: constants, exponential sphere (closed form + numerical integral), kernels (P2, simple, nu_mono only if
  recoverable), target ODE with analytic start, path handling, integrity checks. No import from any CFG121 file.
- cfg157_g1.py: T1.1, T1.2 (both footings, 121- and 2001-point grids, three derivative routes, closed-form cross-check), T1.5.
  Writes cfg157_g1.out / cfg157_g1_results.json; MUTATE=sign|kernel|target write cfg157_g1_MUTATE_<mode>.out / _results.json.
- cfg157_b1.py: F_req(x), min/max on both ranges, Q*; MUTATE=pm_target writes cfg157_b1_MUTATE_pm_target.*.
- Exit codes: main 0 when all integrity checks pass (verdicts REPRODUCES / PARTIAL / DISAGREES are results, not exit codes); MUTATE 1
  when the named control bites as declared, 0 when it does not (kept and disclosed); 2 = an integrity check failed (no verdict valid).
- Path handling: REPO = Path(os.environ["ZF_REPO"]) if set, else the nearest ancestor of __file__ containing
  campaign_fresh_gravity/; outputs go next to the script; no script may print an absolute home path (print <repo>-relative paths or the
  literal "<repo>"); sys.dont_write_bytecode = True. Both a0 footings are printed in every output.
- Phase 2 order: (1) run main and all four MUTATEs and save them; (2) only then open CFG121's outputs (and scripts) and write the
  comparison table; (3) score every section 4 estimate as held/failed, kept either way; (4) report the README line-by-line.

Programme rules restated: kappa = 1/2 FITTED; Z == kappa; a scoped no-go is a valid result; nothing here says the theory is closed
or that data favour it; a pass of the point-mass identity is a positive control, not evidence; one lane's agreement is not a new
result about the framework.
